# Slack User Sensor

[![HACS][hacs-shield]][hacs-link]
[![GitHub Release][releases-shield]][releases-link]
[![Project Maintenance][maintenance-shield]][maintenance-link]
[![License][license-shield]][license-link]

## Description

This is a custom integration for [Home Assistant](https://www.home-assistant.io/). It provides a sensor for a slack user
by a given token.

## Installation

`ha-slack-user` is available through [HACS](https://hacs.xyz/).
Or, install manually by downloading the `custom_components/slack_user` folder from this repo and placing it in your `config/custom_components/` folder.

## Setup

`ha-slack-user` is set up with Config Flow. After installing the integration, go to Configuration -> Integrations, click
the + button at the bottom right, and search for "Slack User".

The component requires a Slack Member ID (User ID), and API Token.

### Tokens

If you are using the deprecated [Legacy Tokens](https://api.slack.com/legacy/custom-integrations/legacy-tokens), this should work out of the box.

If you are using a token from a Slack App, it'll need to have access to the following scopes:

- `users.profile:read` - to get general profile information - title, profile, status, etc
- `users.profile:write` - to set user status
- `users:read` - to get presence information
- `dnd:read` - to get DND information

## Sensor data

After setting up a Slack User sensor, you'll have a `sensor.name` (with the name you specified during config) with the following attributes:

```
title: string
real_name: string
display_name: string
status_text: string
status_emoji: string
entity_picture: string

# Presence Info
presence: "online" or "away"
online: boolean
auto_away: boolean
manual_away: boolean
connection_count: number
last_activity: timestamp

# DND Info
dnd_enabled: boolean
next_dnd_start_ts: timestamp
next_dnd_end_ts: timestamp
snooze_enabled: boolean
```

Here's an example:

![Example sensor](https://raw.githubusercontent.com/GeorgeSG/ha-slack-user/master/examples/sensor.png)

## Services

### `slack_user.set_status`

Sets the user's slack status.

| Field        | Value                  | Necessity  | Description                                                                                                                                 |
| ------------ | ---------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| entity_id    | `sensor.slack_user`    | _Required_ | Name(s) of the sensor entities                                                                                                              |
| status_text  | `Commuting`            | _Optional_ | New status. Pass empty string (`""`) to clear. Don't pass anything to keep current status.                                                  |
| status_emoji | `:car:`                | _Optional_ | New status emoji. Pass empty string (`""`) to clear. Don't pass anything to keep current emoji. Will throw an error if emoji doesn't exist. |
| expiration   | `2021-06-12 15:00:001` | _Optional_ | Expiration date. Must be in format `yyyy-mm-dd hh:mm:ss`                                                                                    |

### `slack_user.clear_status`

Clears the user's slack status.

| Field     | Value               | Necessity  | Description                    |
| --------- | ------------------- | ---------- | ------------------------------ |
| entity_id | `sensor.slack_user` | _Required_ | Name(s) of the sensor entities |

## Meta

**Georgi Gardev**

- [gar.dev](https://gar.dev)
- [![GitHub][github-icon]][github-link] [GeorgeSG][github-link]
- [![Twitter][twitter-icon]][twitter-link] [@georgesg92][twitter-link]

[hacs-shield]: https://img.shields.io/badge/HACS-Default-green.svg
[hacs-link]: https://github.com/custom-components/hacs
[releases-shield]: https://img.shields.io/github/release/GeorgeSG/ha-slack-user.svg
[releases-link]: https://github.com/GeorgeSG/ha-slack-user/releases
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg
[maintenance-link]: https://github.com/GeorgeSG/ha-slack-user
[license-shield]: https://img.shields.io/github/license/GeorgeSG/ha-slack-user?color=brightgreen
[license-link]: https://github.com/GeorgeSG/ha-slack-user/blob/master/LICENSE
[github-icon]: http://i.imgur.com/9I6NRUm.png
[github-link]: https://github.com/GeorgeSG/
[twitter-icon]: http://i.imgur.com/wWzX9uB.png
[twitter-link]: https://twitter.com/georgesg92
