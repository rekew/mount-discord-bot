"""Member selection UI for muting members inside a temporary voice room."""

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

        await set_member_muted(
            room,
            member,
            muted=not was_muted,
            reason=reason_template.format(owner=interaction.user),
        )

        message = (
            texts.UNMUTE_SUCCESS if was_muted else texts.MUTE_SUCCESS
        ).format(name=member.display_name)

        await interaction.response.send_message(message, ephemeral=True)


class MuteView(discord.ui.View):
    """Short-lived view containing the member selection menu."""

    def __init__(self, room: discord.VoiceChannel) -> None:
        super().__init__(timeout=60)
        self.add_item(MuteSelect(room))
