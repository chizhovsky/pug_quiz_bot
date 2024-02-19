from aiogram.types.reaction_type_emoji import ReactionTypeEmoji


async def set_reaction(bot, chat_id, message_id, emoji):
    reaction = ReactionTypeEmoji(type="emoji", emoji=emoji)
    await bot.set_message_reaction(chat_id, message_id, reaction=[reaction])
