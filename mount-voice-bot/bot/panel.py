"""Creation and publishing of the persistent control panel."""

# Python modules
import logging

# Third-party modules
import discord

# Local modules
from bot import texts
from bot.config import PANEL_CHANNEL_ID, PANEL_MARKER
from bot.ui.control_view import VoiceControlView

logger = logging.getLogger(__name__)


def create_panel_embed() -> discord.Embed:
    """Build the embed shown in the control panel channel."""
    embed = discord.Embed(
        title=texts.PANEL_TITLE,
        description=texts.PANEL_DESCRIPTION,
        color=discord.Color.blurple(),
    )
    embed.set_footer(text=PANEL_MARKER)
    return embed


async def create_or_update_panel(bot: discord.Client) -> None:
    """Publish the control panel, reusing an existing message when present."""
    channel = await bot.fetch_channel(PANEL_CHANNEL_ID)

    if not isinstance(channel, discord.TextChannel):
        logger.error("PANEL_CHANNEL_ID is not a text channel.")
        return

    if bot.user is None:
        logger.error("Bot user is unavailable; cannot publish the control panel.")
        return

    embed = create_panel_embed()
    view = VoiceControlView()

    async for message in channel.history(limit=100):
        if message.author.id != bot.user.id:
            continue

        if not message.embeds:
            continue

        if message.embeds[0].footer.text == PANEL_MARKER:
            await message.edit(embed=embed, view=view)
            logger.info("Control panel updated.")
            return

    await channel.send(embed=embed, view=view)
    logger.info("Control panel sent.")
