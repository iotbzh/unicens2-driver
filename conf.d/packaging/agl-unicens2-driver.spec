#
# agl-unicens2-driver.spec
# agl-unicens2-driver KMP spec file
#

Name:          agl-unicens2-driver
%if 0%{?fedora} || 0%{?fedora_version} || 0%{?centos}
BuildRequires: kernel-devel kernel-rpm-macros elfutils-libelf-devel
%else
BuildRequires: %kernel_module_package_buildreqs
%endif

BuildRequires: udev
Requires:      udev
Requires:      %{name}-kmp-default
License:       GPL-2.0
Group:         System/Kernel
Url:           https://github.com/iotbzh/unicens2-driver
Summary:       Sample Kernel Module Package
Version:       1.6.0
Release:       0
Source0:       %{name}_%{version}.orig.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-build


%kernel_module_package

%if 0%{?fedora} || 0%{?fedora_version}
%define _kernel_ver %(rpm -q --qf '%%{VERSION}-%%{RELEASE}' `rpm -q kernel-devel | /usr/lib/rpm/redhat/rpmsort -r | head -n 1` | head -n 1)
%define _kernel_src /usr/src/kernels/%{_kernel_ver}.%{_target_cpu}
%else
%define _kernel_src %{kernel_source default}
%endif

%description
This is a unicens2-driver Kernel Module Package.

%prep
%setup
set -- *
mkdir source
mv mld-%{version}/* source/
mkdir obj

%build
rm -rf obj/default
cp -r source obj/default

make -C %{_kernel_src} modules M=$PWD/obj/default \
  C_INCLUDE_PATH=$PWD/obj/default/mostcore:$PWD/obj/default/aim-network \
  CONFIG_MOSTCORE=m CONFIG_MOSTCONF=m\
  CONFIG_AIM_CDEV=m\
  CONFIG_AIM_NETWORK=m\
  CONFIG_AIM_SOUND=m\
  CONFIG_HDM_USB=m\
  CONFIG_AIM_V4L2=m\
  CONFIG_HDM_DIM2=m\
  CONFIG_HDM_I2C=m

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=updates

make -C %{_kernel_src} modules_install M=$PWD/obj/default

mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
cp source/config-scripts/45-mostnet.conf %{buildroot}%{_sysconfdir}/modprobe.d/
cp source/config-scripts/45-mostnet.rules %{buildroot}%{_prefix}/lib/udev/rules.d

%post
udevadm control --reload-rules && udevadm trigger || echo %{name} udevadm command failed;

%postun
udevadm control --reload-rules && udevadm trigger || echo %{name} udevadm command failed;

%files
%defattr(-,root,root)
%config %{_sysconfdir}/modprobe.d/45-mostnet.conf
%{_prefix}/lib/udev/rules.d/45-mostnet.rules

%changelog
