"""Slack User Config Flow."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_ID, CONF_TOKEN, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from slack import WebClient
from slack.errors import SlackApiError

from . import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): str,
        vol.Required(CONF_TOKEN): str,
        vol.Required(CONF_NAME): str,
    }
)


@config_entries.HANDLERS.register(DOMAIN)
class FlowHandler(config_entries.ConfigFlow):
    """Handle a config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """User initiated config flow."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

        user_id = user_input[CONF_ID]
        token = user_input[CONF_TOKEN]
        name = user_input[CONF_NAME]

        await self.async_set_unique_id(user_id)
        self._abort_if_unique_id_configured()

        client = WebClient(
            token=token, run_async=True, session=async_get_clientsession(self.hass)
        )

        errors = {}

        try:
            await client.users_getPresence(user=user_id)
        except SlackApiError as ex:
            if ex.response is None:
                errors["base"] = "generic_error"
            if ex.response.get("error") == "user_not_found":
                errors["base"] = "user_not_found"
            elif ex.response.get("error") == "invalid_auth":
                errors["base"] = "invalid_auth"
            else:
                errors["base"] = "generic_error"

            return self.async_show_form(
                step_id="user", data_schema=DATA_SCHEMA, errors=errors
            )

        return self.async_create_entry(
            title=name, data={CONF_ID: user_id, CONF_TOKEN: token, CONF_NAME: name},
        )
