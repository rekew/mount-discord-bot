"""Entrypoint for the Mount voice bot."""

# Python modules
import logging

# Local modules
from bot.client import MountBot
from bot.config import TOKEN
from bot.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Validate configuration, then start the Discord bot."""
    configure_logging()

    if not TOKEN:
        raise RuntimeError(
            "TOKEN is missing. Set it in the environment or in the .env file."
        )

    bot = MountBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
