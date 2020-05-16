"""Slack User Sensor."""

import logging

from homeassistant.const import CONF_TOKEN, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from slack import WebClient
from slack.errors import SlackApiError

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Slack User Sensor based on config_entry."""

    _LOGGER.debug("debug huo hui")
    _LOGGER.error("error hui hui")

    token = entry.data.get(CONF_TOKEN)
    name = entry.data.get(CONF_NAME)

    client = WebClient(
        token=token, run_async=True, session=async_get_clientsession(hass)
    )

    try:
        await client.auth_test()
    except SlackApiError:
        _LOGGER.error("Error setting up Slack Control Entry %s", name)
        return False

    async_add_entities([SlackUser(client, token, name)], True)


class SlackUser(Entity):
    """ Slack User."""

    def __init__(self, client, token, name):
        """Initialize the sensor."""

        self._client = client
        self._name = name
        self._token = token
        self._available = False

        self._title = None
        self._real_name = None
        self._display_name = None
        self._status_text = None
        self._status_emoji = None
        self._entity_picture = None

    async def async_update(self):
        """Retrieve latest state."""

        try:
            user_profile = await self._client.users_profile_get()
            self._available = True

            profile = user_profile.get("profile")
            self._title = profile.get("title")
            self._real_name = profile.get("real_name")
            self._display_name = profile.get("display_name")
            self._status_text = profile.get("status_text")
            self._status_emoji = profile.get("status_emoji")
            self._entity_picture = profile.get("image_original")

        except SlackApiError:
            _LOGGER.error("Error updating Slack User %s", self._name)
            self._available = False
            return

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._token

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
        return self._status_text

    @property
    def title(self):
        """Return Title."""
        return self._title

    @property
    def real_name(self):
        """Return Real name."""
        return self._real_name

    @property
    def display_name(self):
        """Return Display name."""
        return self._display_name

    @property
    def status_text(self):
        """Return Status text."""
        return self._status_text

    @property
    def status_emoji(self):
        """Return Status emoji."""
        return self._status_emoji

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
        }

        return {k: v for k, v in attrs.items() if v is not None}
