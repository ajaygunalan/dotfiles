#!/usr/bin/env python3
"""Top-bar indicator that launches Flameshot (Flatpak) on click.

Independent of Flameshot's own tray daemon (which dies on Wayland/Flatpak).
This is its own long-lived process: it just spawns `flameshot gui` on demand.
"""
import subprocess
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import Gtk, AyatanaAppIndicator3 as appindicator

FLAMESHOT = ["flatpak", "run", "org.flameshot.Flameshot"]


def screenshot(_=None):
    subprocess.Popen(FLAMESHOT + ["gui"])


def launcher(_=None):
    subprocess.Popen(FLAMESHOT + ["launcher"])


def quit_app(_=None):
    Gtk.main_quit()


def build_menu():
    menu = Gtk.Menu()

    item_shot = Gtk.MenuItem(label="Take Screenshot")
    item_shot.connect("activate", screenshot)
    menu.append(item_shot)

    item_launcher = Gtk.MenuItem(label="Open Launcher")
    item_launcher.connect("activate", launcher)
    menu.append(item_launcher)

    menu.append(Gtk.SeparatorMenuItem())

    item_quit = Gtk.MenuItem(label="Quit Indicator")
    item_quit.connect("activate", quit_app)
    menu.append(item_quit)

    menu.show_all()
    return menu


def main():
    ind = appindicator.Indicator.new(
        "flameshot-indicator",
        "org.flameshot.Flameshot",  # Flameshot's own icon (Flatpak-exported)
        appindicator.IndicatorCategory.APPLICATION_STATUS,
    )
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    ind.set_title("Flameshot")
    menu = build_menu()
    ind.set_menu(menu)
    # Double-clicking the icon takes a screenshot directly (no menu).
    ind.set_secondary_activate_target(menu.get_children()[0])
    Gtk.main()


if __name__ == "__main__":
    main()
