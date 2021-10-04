## For removing the beep sound when operation not permitted:

Edit the file `/etc/inputrc`

Add `set bell-style none`

## For deleting it in all applications

`$ xset b off`


## For HONOR Backlight working

install `acpilight` package to provide better implementation of xbacklight
then chmod 666 on /sys/class/backlight/amdgpu_bl0/brightness.

## For wireless card to work after suspend

Modify /etc/NetworkManager/conf.d/default-wifi-powersave.conf with:
```text
[connection]
wifi.powersave = 2
```

Enable power management
`sudo iwconfig wlp1s0 power on`

## additional yay packages

i3lockmore
ncmatrix for bling
vtop for monitoring
xidlehook (better than xautolock)
bash-completion
