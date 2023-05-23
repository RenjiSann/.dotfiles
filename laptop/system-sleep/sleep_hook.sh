#! /bin/sh


function before_sleep() {
    # Unmount the wifi driver before going to sleep
    modprobe -r rtw88_8822ce rtw88_8822c rtw88_pci rtw88_core
}

function after_sleep() {
    modprobe rtw88_8822ce
}



case $1 in
    pre)
        before_sleep ;;
    post)
        after_sleep ;;
esac

exit 0
