#!/bin/sh

icon=""

case $(gsettings get org.gnome.desktop.interface color-scheme) in
    *dark*) icon="";;
    *light*) icon="";;
esac

printf "%s" "$icon"

