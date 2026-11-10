"""Discord client definition for the Mount voice bot."""

# Python modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Local modules
from bot import panel
from bot.commands import register_commands
from bot.events import register_events
from bot.ui.control_view import VoiceControlView

logger = logging.getLogger(__name__)


class MountBot(commands.Bot):
    """Bot that creates temporary voice rooms and manages their control panel."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.voice_states = True
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

        register_events(self)
        register_commands(self)

    async def setup_hook(self) -> None:
        """Register persistent views and publish the control panel."""
        # Register persistent buttons so old panel buttons keep working.
        self.add_view(VoiceControlView())

        try:
            await panel.create_or_update_panel(self)
        except Exception as error:
            logger.exception("Could not create control panel: %s", error)
