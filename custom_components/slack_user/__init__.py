"""Slack User Component."""

DOMAIN = "slack_user"
COMPONENT_TYPES = ["sensor"]


async def async_setup(hass, config):
    """Set up the Slack User Component."""
    return True


async def async_setup_entry(hass, entry):
    """Set up Slack User Entry."""
    for component in COMPONENT_TYPES:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True
