"""Application configuration and static constants."""

# Python modules
import os
from typing import Optional

# Third-party modules
from dotenv import load_dotenv

# Load environment variables before reading them.
load_dotenv()

TOKEN: Optional[str] = os.getenv("TOKEN")

# Discord channel and category identifiers.
CREATE_CHANNEL_ID: int = 1567149900972560465
CATEGORY_ID: int = 1567149899454087211
PANEL_CHANNEL_ID: int = 1567150052902699218

# Marker stored in the panel embed footer to locate it after restarts.
PANEL_MARKER: str = "mount-bot-control-panel"

# Upper bound for the room member limit.
MAX_USER_LIMIT: int = 99

# Default amount of messages removed by the clear command.
DEFAULT_CLEAR_AMOUNT: int = 10
MAX_CLEAR_AMOUNT: int = 100
