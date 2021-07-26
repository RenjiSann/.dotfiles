## For removing the beep sound when operation not permitted:

Edit the file `/etc/inputrc`

Add `set bell-style none`

## For deleting it in all applications

`$ xset b off`


## For HONOR Backlight working

install `acpilight` package to provide better implementation of xbacklight
then chmod 666 on /sys/class/backlight/amdgpu_bl0/brightness.
