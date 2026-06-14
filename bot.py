import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReactionTypeEmoji

import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher()


def get_mention(message: Message) -> str:
    user = message.from_user

    if not user:
        return "человек без имени"

    if user.username:
        return f"@{user.username}"

    return user.full_name


def get_random_nickname() -> str:
    return random.choice(config.NICKNAMES)


def render_phrase(template: str, message: Message) -> str:
    return template.format(
        mention=get_mention(message),
        nickname=get_random_nickname(),
    )


def is_target(message: Message) -> bool:
    return (
        message.from_user is not None
        and message.from_user.id == config.TARGET_USER_ID
    )


def is_long_message(message: Message) -> bool:
    text = message.text or message.caption or ""
    return len(text) >= config.LONG_MESSAGE_LENGTH


def find_target_trigger_reply(message: Message) -> str | None:
    text = (message.text or message.caption or "").lower()

    for trigger, replies in config.TARGET_TRIGGER_REPLIES.items():
        if trigger.lower() in text:
            phrase = random.choice(replies)
            return render_phrase(phrase, message)

    return None


async def try_set_reaction(message: Message) -> None:
    if random.random() > config.REACTION_CHANCE:
        return

    try:
        reaction = ReactionTypeEmoji(emoji=random.choice(config.REACTIONS))
        await message.react([reaction])
    except Exception:
        pass


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Я Был Кузнец. Я здесь, чтобы наблюдать, осуждать и иногда унижать логику."
    )


@dp.message(Command("stats"))
async def stats_handler(message: Message):
    wrong_opinions = random.randint(300, 999)
    useful_messages = random.randint(0, 4)
    reality_match = random.randint(1, 18)
    confidence = random.randint(91, 100)
    cringe_index = random.randint(7, 10)

    lines = [
        line.format(
            wrong_opinions=wrong_opinions,
            useful_messages=useful_messages,
            reality_match=reality_match,
            confidence=confidence,
            cringe_index=cringe_index,
        )
        for line in config.STATS_LINES
    ]

    await message.answer(
        "Статистика наблюдаемого объекта:\n\n" + "\n".join(lines)
    )


@dp.message(Command("whoami"))
async def whoami_handler(message: Message):
    if not message.from_user:
        return

    await message.answer(
        f"Твой Telegram ID: `{message.from_user.id}`",
        parse_mode="Markdown"
    )


@dp.message()
async def message_handler(message: Message):
    if not message.from_user:
        return

    if message.from_user.is_bot:
        return

    text = message.text or message.caption or ""
    lower_text = text.lower()

    await try_set_reaction(message)

    robot_triggers = [
        "робот",
        "я робот",
        "will smith",
        "уилл смит",
        "я, робот",
        "i robot",
    ]

    if any(trigger in lower_text for trigger in robot_triggers):
        if random.random() < config.ROBOT_REFERENCE_CHANCE:
            await message.reply(random.choice(config.ROBOT_REFERENCES))
            return

    if is_target(message):
        trigger_reply = find_target_trigger_reply(message)

        if trigger_reply and random.random() < config.TARGET_TRIGGER_REPLY_CHANCE:
            await message.reply(trigger_reply)
            return

        if is_long_message(message) and random.random() < config.LONG_MESSAGE_CHANCE:
            phrase = random.choice(config.LONG_MESSAGE_TROLLS)
            await message.reply(render_phrase(phrase, message))
            return

        if random.random() < config.TROLL_TARGET_CHANCE:
            phrase = random.choice(config.TROLL_PHRASES)
            await message.reply(render_phrase(phrase, message))
            return

    if random.random() < config.CUSTOM_REPLY_CHANCE:
        await message.reply(random.choice(config.CUSTOM_RANDOM_REPLIES))
        return

    if random.random() < config.RANDOM_REPLY_CHANCE:
        await message.reply(random.choice(config.RANDOM_REPLIES))
        return


async def main():
    print("Был Кузнец запущен.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())