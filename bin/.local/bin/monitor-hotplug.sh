#!/bin/bash
# Auto-switch between external ultrawide and laptop display
# Triggered by udev on HDMI hotplug

export DISPLAY=:1
export XAUTHORITY=/run/user/1000/gdm/Xauthority
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"

# Give the connection a moment to stabilize
sleep 2

# Get the current serial number from GNOME's display config
SERIAL=$(gdbus call --session \
  --dest org.gnome.Mutter.DisplayConfig \
  --object-path /org/gnome/Mutter/DisplayConfig \
  --method org.gnome.Mutter.DisplayConfig.GetCurrentState 2>/dev/null \
  | grep -oP '^\(uint32 \K[0-9]+')

if [ -z "$SERIAL" ]; then
    exit 1
fi

# Check if external monitor is connected
if xrandr | grep -q "HDMI-1-0 connected"; then
    # External connected: ultrawide at 3440x1440@100Hz, laptop off
    gdbus call --session \
      --dest org.gnome.Mutter.DisplayConfig \
      --object-path /org/gnome/Mutter/DisplayConfig \
      --method org.gnome.Mutter.DisplayConfig.ApplyMonitorsConfig \
      "$SERIAL" 2 \
      "[(0, 0, 1.0, 0, true, [('HDMI-1-0', '3440x1440@100.000', {})])]" \
      "{}"
else
    # External disconnected: laptop at 2560x1600@240Hz with 2x scaling
    gdbus call --session \
      --dest org.gnome.Mutter.DisplayConfig \
      --object-path /org/gnome/Mutter/DisplayConfig \
      --method org.gnome.Mutter.DisplayConfig.ApplyMonitorsConfig \
      "$SERIAL" 2 \
      "[(0, 0, 2.0, 0, true, [('eDP-2', '2560x1600@240.000', {})])]" \
      "{}"
fi
