"""In-memory ownership state for temporary voice rooms."""

# Python modules
from typing import Dict, Optional

# Mapping of temporary voice channel id to its owner's user id.
ROOM_OWNERS: Dict[int, int] = {}


def get_room_owner_id(channel_id: int) -> Optional[int]:
    """Return the owner id for a temporary room, or ``None`` if unknown."""
    return ROOM_OWNERS.get(channel_id)


def set_room_owner(channel_id: int, owner_id: int) -> None:
    """Register the owner of a temporary room."""
    ROOM_OWNERS[channel_id] = owner_id


def remove_room_owner(channel_id: int) -> None:
    """Forget the owner registration for a temporary room."""
    ROOM_OWNERS.pop(channel_id, None)
