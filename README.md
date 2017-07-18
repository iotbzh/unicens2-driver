---------------------------------------------------------------
   The easy way to install and maintain MOST kernel modules
---------------------------------------------------------------

  Dynamic Kernel Module Support (DKMS) allows you to install a kernel driver module,
  outside of kernel source tree. Its automatically recompile and reinstall the modules
  when kernel is updated.

  Module source tree is 100% indentical to the one publish with source source.
  https://github.com/torvalds/linux/tree/master/drivers/staging/most but
  use dkms.conf as main config entry file.
  
  Author   : Fulup Ar Foll (fulup-at-iot.bzh)
  Date     : Feb-2017
  Licence  : What ever you want until you fix problems by yourself 
  Reference: http://xmodulo.com/build-kernel-module-dkms-linux.html

1)  Make sure running kernel matches kernel-headers version
-------------------------------------------------------------
  apt-get update, zypper update, yum update, ...
  (!) Must have the right version of Kernel header installed check with 'ls -l /lib/modules/`uname -r`/build/Makefile'
  (!) If needed reboot after update to get running kernel version in sync with install kernel headers

2) Installing DKMS on your distro
----------------------------------
  Debian/Ubuntu: apt-get install dkms          # (#) at lest on latest LTS should work out of the box
  OpenSuse     : zypper install dkms.rpm       # (!) dkms.rpm is avaliable from http://packman.links2linux.de/package/dkms
  Fedora       : yum install kernel-devel dkms # (!) default dkms point onto kernel-debug-devel which is not a good idea
  Sources      : https://github.com/dell/dkms
  (+) DMKS depends on kernel-devel but does not require kernel-sources.
  (+) If you have kernel-header missing error, return to step(1)

3) Install Most Kernel Modules
-------------------------------
  export VERSION=1.5.0
  sudo mkdir /var/tmp/dkms
  sudo cp -R . /usr/src/mld-$VERSION
  sudo dkms add     -m mld -v $VERSION
  sudo dkms build   -m mld -v $VERSION --verbose
  sudo dkms install -m mld -v $VERSION
  sudo modprobe hdm_usb   # (!) See SeLinux note

  # SeLinux note:
    # For SeLinux protected system (Fedora, CentOs, ...) You need to allow modprobe to load kernel modules
    # Otherwise modprobe fail with "permission deny". You should find SeLinux autorization commands in "journald 'f" 
    # With Fedora-25 the two following commands should do the job
    ausearch -c 'modprobe' --raw | audit2allow -M my-modprobe
    semodule -i my-modprobe.pp
 
4) Manage installed Modules
--------------------------
  sudo dkms status                                       # list all dkms installed modules
  sudo dkms status -m mld -v $VERSION                    # status of MOST kernel driver only
  sudo dkms uninstall status -m mld -v $VERSION          # remove MOST kernel module
  sudo dkms remove  -m mld -v $VERSION --verbose --all   # clean build directory 
