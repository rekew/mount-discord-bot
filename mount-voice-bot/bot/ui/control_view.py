"""Persistent control panel view for temporary voice rooms."""

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.rooms import get_kickable_members, get_owned_room, is_room_private, set_room_privacy
from bot.ui.kick import KickView
from bot.ui.modals import LimitModal, RenameModal


class VoiceControlView(discord.ui.View):
    """Persistent buttons that let a room owner manage their voice room."""

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        emoji=texts.EMOJI_RENAME,
        style=discord.ButtonStyle.secondary,
        custom_id="mount_rename",
        row=0,
    )
    async def rename(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Open the rename modal for the caller's room."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await interaction.response.send_modal(RenameModal())

    @discord.ui.button(
        emoji=texts.EMOJI_KICK,
        style=discord.ButtonStyle.secondary,
        custom_id="mount_kick",
        row=0,
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Show the member selection menu for denying access."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        if not get_kickable_members(channel):
            await interaction.response.send_message(
                texts.KICK_NO_MEMBERS,
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            texts.KICK_PROMPT,
            view=KickView(channel),
            ephemeral=True,
        )

    @discord.ui.button(
        emoji=texts.EMOJI_LIMIT,
        style=discord.ButtonStyle.secondary,
        custom_id="mount_limit",
        row=1,
    )
    async def limit(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Open the member limit modal for the caller's room."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await interaction.response.send_modal(LimitModal())

    @discord.ui.button(
        emoji=texts.EMOJI_PRIVACY,
        style=discord.ButtonStyle.secondary,
        custom_id="mount_privacy",
        row=1,
    )
    async def privacy(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Toggle the room visibility for the default role."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        was_private = is_room_private(channel)
        await set_room_privacy(channel, private=not was_private)

        message = texts.PRIVACY_OPENED if was_private else texts.PRIVACY_CLOSED

        await interaction.response.send_message(message, ephemeral=True)
