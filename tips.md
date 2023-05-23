## For removing the beep sound when operation not permitted:

Edit the file `/etc/inputrc`

Add `set bell-style none`

## For deleting it in all applications

`$ xset b off`

## additional yay packages

xidlehook

### libinput-gestures (advanced touchpad gestures)
NEED PKGS: libinput, libinput-gestures, wmctrl
In order to work, the user must be in the `input` group.

## For HONOR brightness working
NEED PKGS: acpilight
In order to work, the user must be in the `video` group.

