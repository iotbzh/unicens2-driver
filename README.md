# unicens2-driver

## The easy way to install and maintain MOST kernel modules

Dynamic Kernel Module Support (DKMS) allows you to install a kernel driver module,
outside of kernel source tree.  
Its automatically recompile and reinstall the modules when kernel is updated.

Module source tree is 100% indentical to the one publish with source source.
<https://github.com/torvalds/linux/tree/master/drivers/staging/most>  
But use dkms.conf as main config entry file.

```bash
Author   : Fulup Ar Foll (fulup-at-iot.bzh)
Date     : Feb-2017
Licence  : What ever you want until you fix problems by yourself
Reference: http://xmodulo.com/build-kernel-module-dkms-linux.html
```

### step1: Installing kernel devel on your distro

Debian/Ubuntu:

```bash
sudo apt-get update
sudo apt-get install linux-headers-generic
```

OpenSuse :

```bash
sudo zypper ref
sudo zypper update kernel-default
sudo zypper install kernel-default-devel
```

Fedora :

```bash
sudo yum update kernel-core
# default dkms point onto kernel-debug-devel which is not a good idea
sudo yum install kernel-devel
```

### step2: Make sure running kernel matches kernel-headers version

Must have the right version of Kernel header installed check with

```bash
ls -l /lib/modules/`uname -r`/build/Makefile
```

If needed reboot after update to get running kernel version in sync with install kernel headers

### step3: Installing DKMS on your distro

Debian/Ubuntu:

```bash
# at lest on latest LTS should work out of the box
sudo apt-get install dkms
```

OpenSuse :
dkms is avaliable on openSUSE_Tumbleweed
For DISTRO={openSUSE_Leap_42.2, openSUSE_Leap_42.3} you can use repository

```bash
export DISTRO="openSUSE_Leap_42.2"
#Or
export DISTRO="openSUSE_Leap_42.3"
sudo zypper ar http://download.opensuse.org/repositories/isv:/LinuxAutomotive:/app-Framework/${DISTRO}/isv:LinuxAutomotive:app-Framework.repo
sudo zypper ref
```

Install dkms:

```bash
sudo zypper install dkms
```

For older DISTRO version dkms is also avaliable from <http://packman.links2linux.de/package/dkms>

Fedora :

```bash
sudo yum install dkms
```

Sources : <https://github.com/dell/dkms>

* DMKS depends on kernel-devel but does not require kernel-sources.
* If you have kernel-header missing error, return to step(2)

### step4: Install Most Kernel Modules

```bash
export VERSION=1.5.0
git clone https://github.com/iotbzh/unicens2-driver.git
cd unicens2-driver
sudo cp -R mld-$VERSION /usr/src
sudo dkms add     -m mld -v $VERSION
sudo dkms build   -m mld -v $VERSION --verbose
sudo dkms install -m mld -v $VERSION
# (!) See SeLinux note
sudo modprobe hdm_usb
```

#### SeLinux note

For SeLinux protected system (Fedora, CentOs, ...) You need to allow modprobe to load kernel modules
Otherwise modprobe fail with "permission deny".  
You should find SeLinux autorization commands in

```bash
journalctl -f
```

With Fedora-25 the two following commands should do the job

```bash
ausearch -c 'modprobe' --raw | audit2allow -M my-modprobe
semodule -i my-modprobe.pp
```

### step5: Manage installed Modules

```bash
sudo dkms status                                       # list all dkms installed modules
sudo dkms status -m mld -v $VERSION                    # status of MOST kernel driver only
sudo dkms uninstall status -m mld -v $VERSION          # remove MOST kernel module
sudo dkms remove  -m mld -v $VERSION --verbose --all   # clean build directory
```

### Archive project

```bash
VERSION=1.5.0
GIT_TAG=master
PKG_NAME=unicens2-driver
git archive --format=tar.gz --prefix=agl-${PKG_NAME}-${VERSION}/ ${GIT_TAG} -o agl-${PKG_NAME}_${VERSION}.orig.tar.gz
```