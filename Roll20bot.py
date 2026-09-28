import asyncio
import logging
import os
import random
import re

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Add it to your .env file.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DICE_RE = re.compile(
    r"^(?:(?P<count>\d+)?[kKdD])(?P<sides>\d+)(?:(?P<sign>[+-])(?P<mod>\d+))?$"
)


def parse_dice(expr: str):
    m = DICE_RE.fullmatch(expr.strip())
    if not m:
        return None
    count = int(m.group("count")) if m.group("count") else 1
    sides = int(m.group("sides"))
    mod = int(m.group("mod") or 0)
    if m.group("sign") == "-":
        mod = -mod
    return count, sides, mod


def roll_dice(count, sides, mod):
    rolls = [random.randint(1, sides) for _ in range(count)]
    return rolls, sum(rolls) + mod


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    name = message.from_user.first_name if message.from_user else "friend"
    await message.answer(
        f"Привет, {name}!\n\n"
        "Здесь ты можешь кинуть кубы для своей игры.\n"
        "Используй: /roll 3k4+2 или /roll d20"
    )


@dp.message(Command("roll"))
async def cmd_roll(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Формат: /roll XkN+M, например /roll 3k4+2 или /roll d20")
        return

    parsed = parse_dice(args[1])
    if not parsed:
        await message.answer("Не могу разобрать. Пример: /roll 3k4+2")
        return

    count, sides, mod = parsed

    if not (1 <= count <= 100):
        await message.answer("Слишком много костей. Кол-во костей: 1-100")
        return
    if not (2 <= sides <= 1000):
        await message.answer("Не подходит количество граней. Граней: 2-1000")
        return

    rolls, total = roll_dice(count, sides, mod)
    mod_str = f"+{mod}" if mod > 0 else (str(mod) if mod < 0 else "")
    await message.answer(
        f"🎲 {count}k{sides}{mod_str}\n"
        f"Броски: {rolls}\n"
        f"Итого: {total}"
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
