"""Helpers for querying and modifying temporary voice rooms."""

# Python modules
from typing import List, Optional

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.state import get_room_owner_id


def is_room_owner(channel: discord.VoiceChannel, user_id: int) -> bool:
    """Return ``True`` when ``user_id`` owns the given temporary room."""
    return get_room_owner_id(channel.id) == user_id


async def get_owned_room(
    interaction: discord.Interaction,
) -> Optional[discord.VoiceChannel]:
    """Return the caller's owned voice room, or reply with an error and return ``None``."""
    voice_state = getattr(interaction.user, "voice", None)
    channel = voice_state.channel if voice_state else None

    if channel is None:
        await interaction.response.send_message(
            texts.NOT_IN_VOICE,
            ephemeral=True,
        )
        return None

    if not is_room_owner(channel, interaction.user.id):
        await interaction.response.send_message(
            texts.NOT_ROOM_OWNER,
            ephemeral=True,
        )
        return None

    return channel


def get_room_members(
    room: discord.VoiceChannel,
    owner_id: Optional[int] = None,
) -> List[discord.Member]:
    """Return human members of the room, excluding bots and the owner."""
    resolved_owner_id = owner_id if owner_id is not None else get_room_owner_id(room.id)

    return [
        member
        for member in room.members
        if not member.bot and member.id != resolved_owner_id
    ]


def is_member_muted(room: discord.VoiceChannel, member: discord.Member) -> bool:
    """Return ``True`` when ``member`` cannot speak in the given room."""
    return room.overwrites_for(member).speak is False


async def set_member_muted(
    room: discord.VoiceChannel,
    member: discord.Member,
    muted: bool,
    reason: Optional[str] = None,
) -> None:
    """Allow or deny speaking for ``member`` in this room only."""
    overwrite = room.overwrites_for(member)
    overwrite.speak = False if muted else None

    await room.set_permissions(member, overwrite=overwrite, reason=reason)


def is_room_private(room: discord.VoiceChannel) -> bool:
    """Return ``True`` when the default role cannot view or connect to the room."""
    overwrite = room.overwrites_for(room.guild.default_role)
    return overwrite.connect is False or overwrite.view_channel is False


async def set_room_privacy(room: discord.VoiceChannel, private: bool) -> None:
    """Open or close the room for the default role."""
    everyone = room.guild.default_role
    overwrite = room.overwrites_for(everyone)
    overwrite.view_channel = not private
    overwrite.connect = not private

    await room.set_permissions(everyone, overwrite=overwrite)
