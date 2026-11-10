"""Text commands and their error handlers."""

# Python modules
import logging

# Third-party modules
from discord.ext import commands

# Local modules
from bot import texts
from bot.config import DEFAULT_CLEAR_AMOUNT, MAX_CLEAR_AMOUNT

logger = logging.getLogger(__name__)


def register_commands(bot: commands.Bot) -> None:
    """Attach text commands and error handlers to the bot."""

    @bot.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(
        ctx: commands.Context,
        amount: int = DEFAULT_CLEAR_AMOUNT,
    ) -> None:
        """Delete a number of recent messages from the current channel."""
        if amount < 1 or amount > MAX_CLEAR_AMOUNT:
            logger.warning("Invalid clear amount: %s", amount)
            await ctx.send(texts.CLEAR_INVALID_AMOUNT)
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        message = await ctx.send(
            texts.CLEAR_SUCCESS.format(amount=len(deleted) - 1),
        )
        await message.delete(delay=3)

    @clear.error
    async def clear_error(
        ctx: commands.Context,
        error: Exception,
    ) -> None:
        """Report permission and argument errors raised by the clear command."""
        logger.error("[CLEAR ERROR] %s: %s", type(error).__name__, error)

        if isinstance(error, commands.MissingPermissions):
            await ctx.send(texts.CLEAR_MISSING_PERMISSIONS)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(texts.CLEAR_BAD_ARGUMENT)
        else:
            raise error
