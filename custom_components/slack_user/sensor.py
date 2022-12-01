"""Slack User Sensor."""

import datetime
import logging
import voluptuous as vol
from homeassistant.const import CONF_ID, CONF_TOKEN, CONF_NAME
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from slack import WebClient
from slack.errors import SlackApiError

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_ATTR_ENTITY_ID = "entity_id"

SERVICE_SET_STATUS = "set_status"
SERVICE_ATTR_STATUS_TEXT = "status_text"
SERVICE_ATTR_STATUS_EMOJI = "status_emoji"
SERVICE_ATTR_EXPIRATION = "expiration"
SERVICE_SET_STATUS_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ATTR_ENTITY_ID): cv.entity_ids,
        vol.Optional(SERVICE_ATTR_STATUS_TEXT): cv.string,
        vol.Optional(SERVICE_ATTR_STATUS_EMOJI): cv.string,
        vol.Optional(SERVICE_ATTR_EXPIRATION): vol.Or("", cv.datetime)
    }
)

SERVICE_CLEAR_STATUS = "clear_status"
SERVICE_CLEAR_STATUS_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ATTR_ENTITY_ID): cv.entity_ids,
    }
)

SERVICE_SET_PRESENCE = "set_presence"
SERVICE_ATTR_PRESENCE = "presence"
SERVICE_SET_PRESENCE_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ATTR_ENTITY_ID): cv.entity_ids,
        vol.Required(SERVICE_ATTR_PRESENCE): vol.In(['away', 'auto'])
    }
)

SERVICE_SET_DND = "set_dnd"
SERVICE_ATTR_NUM_MINUTES = "num_minutes"
SERVICE_SET_DND_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ATTR_ENTITY_ID): cv.entity_ids,
        vol.Required(SERVICE_ATTR_NUM_MINUTES): cv.positive_int
    }
)

SERVICE_END_DND = "end_dnd"
SERVICE_END_DND_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ATTR_ENTITY_ID): cv.entity_ids,
    }
)


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

    slack_user = SlackUser(client, user_id, token, name)
    async_add_entities([slack_user], True)

    # Setup services
    platform = entity_platform.async_get_current_platform()

    async def async_service_handler(service_call):
        """Handle dispatched services."""
        assert platform is not None
        entities = await platform.async_extract_from_service(service_call)

        if not entities:
            return

        if service_call.service == SERVICE_SET_STATUS:
            status_text = service_call.data.get(SERVICE_ATTR_STATUS_TEXT)
            status_emoji = service_call.data.get(SERVICE_ATTR_STATUS_EMOJI)
            expiration = service_call.data.get(SERVICE_ATTR_EXPIRATION)
            [await entity.async_set_status(status_text, status_emoji, expiration) for entity in entities]

        elif service_call.service == SERVICE_CLEAR_STATUS:
            [await entity.async_clear_status() for entity in entities]

        elif service_call.service == SERVICE_SET_PRESENCE:
            presence = service_call.data.get(SERVICE_ATTR_PRESENCE)
            [await entity.async_set_presence(presence) for entity in entities]

        elif service_call.service == SERVICE_SET_DND:
            num_minutes = service_call.data.get(SERVICE_ATTR_NUM_MINUTES)
            [await entity.async_set_dnd(num_minutes) for entity in entities]

        elif service_call.service == SERVICE_END_DND:
            [await entity.async_end_dnd() for entity in entities]


    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_STATUS,
        async_service_handler,
        SERVICE_SET_STATUS_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CLEAR_STATUS,
        async_service_handler,
        SERVICE_CLEAR_STATUS_SCHEMA,
    )


    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_PRESENCE,
        async_service_handler,
        SERVICE_SET_PRESENCE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_DND,
        async_service_handler,
        SERVICE_SET_DND_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_END_DND,
        async_service_handler,
        SERVICE_END_DND_SCHEMA,
    )


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
        self._status_expiration_ts = None
        self._status_emoji = None
        self._status_emoji_display_info = None
        self._entity_picture = None

        # Huddle info
        self._huddle_state = None
        self.huddle_state_expiration_ts = None

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
            self._status_expiration_ts = profile.get("status_expiration")
            self._status_emoji = profile.get("status_emoji")
            self._entity_picture = profile.get("image_original")
            self._huddle_state = profile.get("huddle_state");
            self._huddle_state_expiration_ts = profile.get("huddle_state_expiration_ts")

            if len(profile.get("status_emoji_display_info")) > 0:
                self._status_emoji_display_info = profile.get("status_emoji_display_info")[0]

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
            "status_expiration_ts": self._status_expiration_ts,
            "status_emoji": self._status_emoji,
            "status_emoji_display_info": self._status_emoji_display_info,
            "entity_picture": self._entity_picture,
            "huddle_state": self._huddle_state,
            "huddle_state_expiration_ts": self._huddle_state_expiration_ts,
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

    async def async_set_status(self, status_text = None, status_emoji = None, expiration = None):
        new_text = self._status_text if status_text == None else status_text
        new_emoji = self._status_emoji if status_emoji == None else status_emoji

        if expiration == "" or expiration == None:
            expiration_ts = expiration
        else:
            expiration_ts = int(datetime.datetime.timestamp(expiration))

        self._client.users_profile_set(
            profile = {
                "status_text": new_text,
                "status_emoji": new_emoji,
                "status_expiration": expiration_ts
            }
        )

        await self.async_update()

    async def async_clear_status(self):
       await self.async_set_status("", "", "")

    async def async_set_presence(self, presence):
        self._client.users_setPresence(presence = presence)
        await self.async_update()

    async def async_set_dnd(self, num_minutes):
        self._client.dnd_setSnooze(num_minutes = num_minutes)
        await self.async_update()

    async def async_end_dnd(self):
        self._client.dnd_endDnd()
        await self.async_update()
