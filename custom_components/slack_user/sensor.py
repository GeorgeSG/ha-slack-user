"""Slack User Sensor."""

import logging

from homeassistant.const import CONF_ID, CONF_TOKEN, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from slack import WebClient
from slack.errors import SlackApiError

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Slack User Sensor based on config_entry."""

    user_id = entry.data.get(CONF_ID)
    token = entry.data.get(CONF_TOKEN)
    name = entry.data.get(CONF_NAME)

    client = WebClient(
        token=token, run_async=True, session=async_get_clientsession(hass)
    )

    try:
        await client.auth_test()
    except SlackApiError:
        _LOGGER.error("Error setting up Slack User Entry %s", name)
        return False

    async_add_entities([SlackUser(client, user_id, token, name)], True)


class SlackUser(Entity):
    """ Slack User."""

    def __init__(self, client, user_id, token, name):
        """Initialize the sensor."""

        self._client = client
        self._user_id = user_id
        self._name = name
        self._token = token

        self._available = False

        # profile info
        self._title = None
        self._real_name = None
        self._display_name = None
        self._status_text = None
        self._status_emoji = None
        self._entity_picture = None

        # Presence Info
        self._presence = None
        self._online = None
        self._auto_away = None
        self._manual_away = None
        self._connection_count = None
        self._last_activity = None

        # DND Info
        self._dnd_enabled = None
        self._next_dnd_start_ts = None
        self._next_dnd_end_ts = None
        self._snooze_enabled = None

    async def async_update(self):
        """Retrieve latest state."""

        try:
            user_profile = await self._client.users_profile_get(user=self._user_id)
            self._available = True

            profile = user_profile.get("profile")
            self._title = profile.get("title")
            self._real_name = profile.get("real_name")
            self._display_name = profile.get("display_name")
            self._status_text = profile.get("status_text")
            self._status_emoji = profile.get("status_emoji")
            self._entity_picture = profile.get("image_original")

            dnd_info = await self._client.dnd_info(user=self._user_id)
            self._dnd_enabled = dnd_info.get("dnd_enabled")
            self._next_dnd_start_ts = dnd_info.get("next_dnd_start_ts")
            self._next_dnd_end_ts = dnd_info.get("next_dnd_end_ts")
            self._snooze_enabled = dnd_info.get("snooze_enabled")

            presence_info = await self._client.users_getPresence(user=self._user_id)
            self._presence = presence_info.get("presence")
            self._online = presence_info.get("online")
            self._auto_away = presence_info.get("auto_away")
            self._manual_away = presence_info.get("manual_away")
            self._connection_count = presence_info.get("connection_count")
            self._last_activity = presence_info.get("last_activity")

        except SlackApiError:
            _LOGGER.error("Error updating Slack User %s", self._name)
            self._available = False
            return

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._user_id

    @property
    def available(self):
        """Return True when state is known."""
        return self._available

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._presence

    @property
    def entity_picture(self):
        """Return Entity Picture."""
        return self._entity_picture

    @property
    def state_attributes(self):
        """Return entity attributes."""

        attrs = {
            "title": self._title,
            "real_name": self._real_name,
            "display_name": self._display_name,
            "status_text": self._status_text,
            "status_emoji": self._status_emoji,
            "entity_picture": self._entity_picture,
            "presence": self._presence,
            "online": self._online,
            "auto_away": self._auto_away,
            "manual_away": self._manual_away,
            "connection_count": self._connection_count,
            "last_activity": self._last_activity,
            "dnd_enabled": self._dnd_enabled,
            "next_dnd_start_ts": self._next_dnd_start_ts,
            "next_dnd_end_ts": self._next_dnd_end_ts,
            "snooze_enabled": self._snooze_enabled,
        }

        return {k: v for k, v in attrs.items() if v is not None}
