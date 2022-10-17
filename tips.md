## For removing the beep sound when operation not permitted:

Edit the file `/etc/inputrc`

Add `set bell-style none`

## For deleting it in all applications

`$ xset b off`


## For wireless card to work after suspend

Modify /etc/NetworkManager/conf.d/default-wifi-powersave.conf with:
```text
[connection]
wifi.powersave = 2
```

Enable power management
`sudo iwconfig wlp1s0 power on`

## additional yay packages

xidlehook

### libinput-gestures (advanced touchpad gestures)
NEED PKGS: libinput, libinput-gestures, wmctrl
In order to work, the user must be in the `input` group.

## For HONOR brightness working
NEED PKGS: acpilight
In order to work, the user must be in the `video` group.

