"""Slack User Component."""

DOMAIN = "slack_user"
COMPONENT_TYPES = ["sensor"]


async def async_setup(hass, config):
    """Set up the Slack User Component."""
    return True


async def async_setup_entry(hass, entry):
    """Set up Slack User Entry."""
    await hass.config_entries.async_forward_entry_setups(entry, COMPONENT_TYPES)

    return True
