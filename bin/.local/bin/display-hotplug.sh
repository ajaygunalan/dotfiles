#!/bin/bash
# Listen for Mutter's MonitorsChanged D-Bus signal, then apply correct config
# This runs AFTER Mutter finishes its (buggy) reconfiguration

apply_config() {
    sleep 0.5  # Brief pause for Mutter to finish
    
    if xrandr 2>/dev/null | grep -q "HDMI-1-0 connected"; then
        # Samsung connected: native 3440x1440@100Hz, laptop off
        xrandr --output eDP-2 --off \
               --output HDMI-1-0 --mode 3440x1440 --rate 100 --primary
    else
        # Samsung disconnected: laptop native
        xrandr --output HDMI-1-0 --off \
               --output eDP-2 --mode 2560x1600 --rate 240 --primary --transform none --scale 1x1
    fi
}

dbus-monitor --session "type='signal',interface='org.gnome.Mutter.DisplayConfig',member='MonitorsChanged'" 2>/dev/null |
while read -r line; do
    if echo "$line" | grep -q "MonitorsChanged"; then
        # Kill any previous pending apply (debounce rapid events)
        kill %% 2>/dev/null
        apply_config &
    fi
done
