"""Discord event listeners and temporary room lifecycle."""

# Python modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Local modules
from bot import texts
from bot.config import CATEGORY_ID, CREATE_CHANNEL_ID
from bot.state import get_room_owner_id, remove_room_owner, set_room_owner

logger = logging.getLogger(__name__)


async def _create_room(member: discord.Member) -> None:
    """Create a temporary voice room for the member and move them into it."""
    category = member.guild.get_channel(CATEGORY_ID)

    if category is None:
        logger.error("Voice category not found.")
        return

    try:
        room = await member.guild.create_voice_channel(
            name=texts.ROOM_NAME_TEMPLATE.format(name=member.display_name),
            category=category,
            reason=texts.ROOM_CREATE_REASON,
        )

        set_room_owner(room.id, member.id)
        await member.move_to(room)

        logger.info("Created room for %s", member.display_name)

    except discord.Forbidden:
        logger.error("Bot lacks permission to create rooms or move members.")
    except discord.HTTPException as error:
        logger.error("Could not create room: %s", error)


async def _delete_room_if_empty(channel: discord.VoiceChannel) -> None:
    """Delete a tracked temporary room once no members remain in it."""
    if get_room_owner_id(channel.id) is None:
        return

    if channel.members:
        return

    try:
        await channel.delete(reason=texts.ROOM_DELETE_REASON)
        remove_room_owner(channel.id)
        logger.info("Deleted empty room: %s", channel.name)
    except discord.HTTPException as error:
        logger.error("Could not delete room: %s", error)


def register_events(bot: commands.Bot) -> None:
    """Attach voice-state and message listeners to the bot."""

    async def on_voice_state_update(
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        """Create a room when joining the create channel and clean up empty rooms."""
        if after.channel is not None and after.channel.id == CREATE_CHANNEL_ID:
            await _create_room(member)

        if before.channel is not None:
            await _delete_room_if_empty(before.channel)

    async def on_message(message: discord.Message) -> None:
        """Log incoming messages and let the command framework process them."""
        if message.author.bot:
            return

        logger.debug("[MESSAGE RECEIVED] %s: %s", message.author, message.content)
        await bot.process_commands(message)

    bot.add_listener(on_voice_state_update, "on_voice_state_update")
    bot.add_listener(on_message, "on_message")
