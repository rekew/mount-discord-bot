"""Member selection UI for denying access to a temporary voice room."""

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.rooms import get_room_members, is_room_owner
from bot.state import get_room_owner_id


class KickSelect(discord.ui.Select):
    """Select menu listing members that may be removed from the room."""

    def __init__(self, room: discord.VoiceChannel) -> None:
        self.room_id: int = room.id

        owner_id = get_room_owner_id(room.id)
        members = get_room_members(room, owner_id)

        options = [
            discord.SelectOption(
                label=member.display_name[:100],
                value=str(member.id),
            )
            for member in members
        ]

        super().__init__(
            placeholder=texts.KICK_SELECT_PLACEHOLDER,
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Deny the selected member access and disconnect them from the room."""
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

        overwrite = room.overwrites_for(member)
        overwrite.connect = False

        await room.set_permissions(
            member,
            overwrite=overwrite,
            reason=texts.KICK_REASON_TEMPLATE.format(owner=interaction.user),
        )

        await member.move_to(None, reason=texts.KICK_DISCONNECT_REASON)

        await interaction.response.send_message(
            texts.KICK_SUCCESS.format(name=member.display_name),
            ephemeral=True,
        )


class KickView(discord.ui.View):
    """Short-lived view containing the member selection menu."""

    def __init__(self, room: discord.VoiceChannel) -> None:
        super().__init__(timeout=60)
        self.add_item(KickSelect(room))
