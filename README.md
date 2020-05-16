# Slack User Sensor

[![HACS][hacs-shield]][hacs-link]
[![Downloads][downloads-shield]][downloads-link]
[![GitHub Release][releases-shield]][releases-link]
[![CI][ci-shield]][ci-link]
[![Project Maintenance][maintenance-shield]][maintenance-link]
[![License][license-shield]][license-link]

## Description

This is a custom integration for [Home Assistant](https://www.home-assistant.io/). It provides a sensor for a slack user
by a given token.

## Installation

Install through [HACS](https://hacs.xyz/):

1. Go to HACS -> Settings.
1. Enter "https://github.com/GeorgeSG/ha-slack-user/" for _ADD CUSTOM REPOSITORY_ and choose "Integration" for _Category_.
1. Click Save.

Or, install manually by downloading the `custom_components/slack_user` folder from this repo and placing it in your `config/custom_components/` folder.

## Usage

The Slack User component is setup with a Config Flow. After installing it, go to Configuration -> Integartions, click
the + button at the bottom right, and search for "Slack User".

After setting up a Slack User sensor, you'll have a `sensor.sensor_name` with the following attributes:

```
title: "User Title"
real_name: "User Real Name"
display_name: "Display Name"
status_text: "Status text"
status_emoji: "Status emoji"
entity_picture: "Slack avatar"
```

## Meta

**Georgi Gardev**

- [gar.dev](https://gar.dev)
- [![GitHub][github-icon]][github-link] [GeorgeSG][github-link]
- [![Twitter][twitter-icon]][twitter-link] [@georgesg92][twitter-link]

[hacs-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs-link]: https://github.com/custom-components/hacs
[downloads-shield]: https://img.shields.io/github/downloads/GeorgeSG/ha-slack-user/latest/total?color=brightgreen&logo=github
[downloads-link]: https://github.com/GeorgeSG/ha-slack-user/releases
[releases-shield]: https://img.shields.io/github/release/GeorgeSG/ha-slack-user.svg
[releases-link]: https://github.com/GeorgeSG/ha-slack-user/releases
[ci-shield]: https://img.shields.io/github/workflow/status/GeorgeSG/ha-slack-user/CI?label=CI&logo=github&
[ci-link]: https://github.com/GeorgeSG/ha-slack-user/actions?query=workflow%3ACI
[maintenance-shield]: https://img.shields.io/maintenance/yes/2020.svg
[maintenance-link]: https://github.com/GeorgeSG/ha-slack-user
[license-shield]: https://img.shields.io/github/license/GeorgeSG/ha-slack-user?color=brightgreen
[license-link]: https://github.com/GeorgeSG/ha-slack-user/blob/master/LICENSE
[github-icon]: http://i.imgur.com/9I6NRUm.png
[github-link]: https://github.com/GeorgeSG/
[twitter-icon]: http://i.imgur.com/wWzX9uB.png
[twitter-link]: https://twitter.com/georgesg92
