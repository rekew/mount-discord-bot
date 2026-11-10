"""Member selection UI for muting members inside a temporary voice room."""

# Python modules
import logging

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.rooms import (
    get_room_members,
    is_member_muted,
    is_room_owner,
    set_member_muted,
)
from bot.state import get_room_owner_id


logger = logging.getLogger(__name__)
MUTE_RECONNECT_CHANNEL_ID = 1569776643952746587


async def _reconnect_member_in_room(
    room: discord.VoiceChannel,
    member: discord.Member,
) -> bool:
    """Move the member through another accessible voice channel and back."""
    bot_member = room.guild.me
    if bot_member is None:
        return False

    staging_channel = room.guild.get_channel(MUTE_RECONNECT_CHANNEL_ID)
    if not isinstance(staging_channel, discord.VoiceChannel):
        logger.error(
            "Mute reconnect channel %s is missing or is not a voice channel",
            MUTE_RECONNECT_CHANNEL_ID,
        )
        return False
    if staging_channel.id == room.id:
        logger.error("Mute reconnect channel cannot be the managed room %s", room.id)
        return False
    bot_channel_permissions = staging_channel.permissions_for(bot_member)
    if not bot_channel_permissions.view_channel or not bot_member.guild_permissions.move_members:
        logger.error(
            "Bot lacks permission to move member %s through mute reconnect channel %s "
            "(view_channel=%s, move_members=%s)",
            member.id,
            staging_channel.id,
            bot_channel_permissions.view_channel,
            bot_member.guild_permissions.move_members,
        )
        return False

    await member.move_to(staging_channel, reason="Обновление голосовых прав комнаты")
    try:
        await member.move_to(room, reason="Применение запрета говорить в комнате")
    except (discord.Forbidden, discord.HTTPException):
        logger.exception(
            "Could not return member %s to room %s after staging move",
            member.id,
            room.id,
        )
        try:
            await member.move_to(
                room,
                reason="Повторная попытка вернуть участника в комнату",
            )
        except (discord.Forbidden, discord.HTTPException):
            logger.exception(
                "Could not restore member %s to room %s",
                member.id,
                room.id,
            )
        raise
    return True


class MuteSelect(discord.ui.Select):
    """Select menu listing members that may be muted inside the room."""

    def __init__(self, room: discord.VoiceChannel) -> None:
        self.room_id: int = room.id

        owner_id = get_room_owner_id(room.id)
        members = get_room_members(room, owner_id)

        options = [
            discord.SelectOption(
                label=member.display_name[:100],
                value=str(member.id),
                description=(
                    texts.MUTE_STATUS_MUTED
                    if is_member_muted(room, member)
                    else texts.MUTE_STATUS_ACTIVE
                ),
            )
            for member in members
        ]

        super().__init__(
            placeholder=texts.MUTE_SELECT_PLACEHOLDER,
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Toggle the room-local mute for the selected member."""
        guild = interaction.guild

        if guild is None:
            return

        room = guild.get_channel(self.room_id)

        if not isinstance(room, discord.VoiceChannel):
            await interaction.response.send_message(
                texts.ROOM_NOT_FOUND,
                ephemeral=True,
            )
            return

        if not is_room_owner(room, interaction.user.id):
            await interaction.response.send_message(
                texts.NOT_ROOM_OWNER,
                ephemeral=True,
            )
            return

        member = guild.get_member(int(self.values[0]))

        if member is None or member.voice is None or member.voice.channel is None:
            await interaction.response.send_message(
                texts.MEMBER_LEFT_VOICE,
                ephemeral=True,
            )
            return

        if member.voice.channel.id != room.id:
            await interaction.response.send_message(
                texts.MEMBER_LEFT_ROOM,
                ephemeral=True,
            )
            return

        was_muted = is_member_muted(room, member)
        reason_template = (
            texts.UNMUTE_REASON_TEMPLATE if was_muted else texts.MUTE_REASON_TEMPLATE
        )

        muted = not was_muted
        try:
            await set_member_muted(
                room,
                member,
                muted=muted,
                reason=reason_template.format(owner=interaction.user),
            )
        except discord.Forbidden:
            logger.exception(
                "Permission denied while changing mute for member %s in room %s",
                member.id,
                room.id,
            )
            await interaction.response.send_message(
                "❌ Не удалось изменить права участника. Проверьте, что у бота есть Manage Channels.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            logger.exception(
                "Discord API error while changing mute for member %s in room %s",
                member.id,
                room.id,
            )
            await interaction.response.send_message(
                "❌ Discord не смог применить изменение. Попробуйте ещё раз.",
                ephemeral=True,
            )
            return

        try:
            reconnected = await _reconnect_member_in_room(room, member)
        except discord.Forbidden:
            logger.exception(
                "Permission denied while reconnecting member %s in room %s",
                member.id,
                room.id,
            )
            await interaction.response.send_message(
                "✅ Права участника изменены, но бот не смог переместить его. Проверьте право Move Members и верните участника в комнату, если он остался в другом канале.",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            logger.exception(
                "Discord API error while reconnecting member %s in room %s",
                member.id,
                room.id,
            )
            await interaction.response.send_message(
                "✅ Права участника изменены, но Discord не смог переместить его. Проверьте, что участник находится в исходной комнате.",
                ephemeral=True,
            )
            return

        if not reconnected:
            logger.warning(
                "Permission change applied, but reconnect could not be completed for member %s in room %s",
                member.id,
                room.id,
            )
            await interaction.response.send_message(
                "✅ Права участника изменены, но подключение не обновлено. Проверьте staging voice-канал и наличие у бота права Move Members.",
                ephemeral=True,
            )
            return

        message = (
            texts.UNMUTE_SUCCESS if was_muted else texts.MUTE_SUCCESS
        ).format(name=member.display_name)

        await interaction.response.send_message(message, ephemeral=True)


class MuteView(discord.ui.View):
    """Short-lived view containing the member selection menu."""

    def __init__(self, room: discord.VoiceChannel) -> None:
        super().__init__(timeout=60)
        self.add_item(MuteSelect(room))
