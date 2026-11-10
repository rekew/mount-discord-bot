"""Modals used to edit temporary voice room settings."""

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.config import MAX_USER_LIMIT
from bot.rooms import get_owned_room


class RenameModal(discord.ui.Modal, title=texts.RENAME_MODAL_TITLE):
    """Modal that renames the caller's voice room."""

    new_name: discord.ui.TextInput = discord.ui.TextInput(
        label=texts.RENAME_INPUT_LABEL,
        placeholder=texts.RENAME_INPUT_PLACEHOLDER,
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """Apply the new room name and confirm the change."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        await channel.edit(name=str(self.new_name.value))

        await interaction.response.send_message(
            texts.RENAME_SUCCESS.format(name=self.new_name.value),
            ephemeral=True,
        )


class LimitModal(discord.ui.Modal, title=texts.LIMIT_MODAL_TITLE):
    """Modal that updates the caller's room member limit."""

    limit: discord.ui.TextInput = discord.ui.TextInput(
        label=texts.LIMIT_INPUT_LABEL,
        placeholder=texts.LIMIT_INPUT_PLACEHOLDER,
        max_length=2,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """Validate the requested limit and apply it to the room."""
        channel = await get_owned_room(interaction)
        if channel is None:
            return

        try:
            limit = int(str(self.limit.value))

            if limit < 0 or limit > MAX_USER_LIMIT:
                raise ValueError
        except ValueError:
            await interaction.response.send_message(
                texts.LIMIT_INVALID,
                ephemeral=True,
            )
            return

        await channel.edit(user_limit=limit)

        message = (
            texts.LIMIT_DISABLED
            if limit == 0
            else texts.LIMIT_SET.format(limit=limit)
        )

        await interaction.response.send_message(message, ephemeral=True)
