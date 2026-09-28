import asyncio
import logging
import random
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F



BOT_TOKEN="8852218366:AAH_IWmq728JvOuS0RHBwfh6mDXtPId08VA"

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

DICE_RE = re.compile(r'^(\d*)[kKdD](\d+)(?:([+-])(\d+))?$')

#парсинг команды
def parse_dice(s: str):
    m = DICE_RE.match(s.strip())
    if not m:
        return None
    count = int(m.group(1)) if m.group(1) else 1
    sides = int(m.group(2))
    sign = m.group(3)
    mod = int(m.group(4)) if m.group(4) else 0
    if sign == '-':
        mod = -mod
    return count, sides, mod

#логика броска
def roll_dice(count, sides, mod):
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + mod
    return rolls, total

#хэндлеры

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        f"Здесь ты можешь кинуть кубы для своей игры.\n"
        f"Чтобы бросить кубы, воспользуйся командой /roll"
    )

@dp.message(Command("roll"))
async def cmd_roll(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Формат: /roll XkN+M, например /roll 3k4+2 или /roll d20")
        return
    
    parsed = parse_dice(args[1])
    if not parsed:
        await message.answer("Не могу разобрать. Пример: /roll 3k4+2")
        return
    
    count, sides, mod = parsed
    # валидация
    if not (1 <= count <= 100) or not (2 <= sides <= 1000):
        await message.answer("Слишком много. Кол-во костей: 1-100, граней: 2-1000")
        return
    
    rolls, total = roll_dice(count, sides, mod)
    mod_str = f"+{mod}" if mod > 0 else (f"{mod}" if mod < 0 else "")
    await message.answer(
        f"🎲 {count}k{sides}{mod_str}\n"
        f"Броски: {rolls}\n"
        f"Итого: {total}"
    )

@dp.message(Command("roll", ignore_case=True))
@dp.message(Command("roll"), ~F.from_user.is_bot)

#точка входа

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
