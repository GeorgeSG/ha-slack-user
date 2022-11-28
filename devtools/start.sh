docker run --rm -p8124:8123 -v $(pwd)/devtools/homeassistant:/config -v $(pwd)/custom_components:/config/custom_components homeassistant/home-assistant:latest
