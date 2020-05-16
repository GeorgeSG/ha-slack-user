"""Slack User Component."""

import asyncio
import voluptuous as vol
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.config_entries import ConfigEntry

from slack import WebClient
from slack.errors import SlackApiError

DOMAIN = "slack_user"
COMPONENT_TYPES = ["sensor"]


async def async_setup(hass, config):
    """Set up the Slack User Component."""
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up Slack User Entry."""
    for component in COMPONENT_TYPES:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True
