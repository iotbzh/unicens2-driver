#
# spec file for package agl-unicens2-driver
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           agl-unicens2-driver
Version:        1.5.0
Release:        1
License:        GPL-2.0
Summary:        Unicens2-driver
Url:            https://github.com/iotbzh/unicens2-driver
Group:          AGL
Source:         %{name}_%{version}.orig.tar.gz

BuildRequires:  dkms
BuildRequires:  udev, audit
Requires:       %{name}-devel

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
agl-unicens2-driver

%package devel
Summary:        Unicens2-driver-devel
Group:          Development/AGL
Requires:       udev, audit
Requires:       dkms
%if 0%{?fedora}
Requires:       kernel-devel
%else
Requires:       kernel-default-devel
%endif
Provides:       pkgconfig(%{name}) = %{version}

%description devel
%{name}-devel

%global debug_package %{nil}

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/%{_usrsrc}
cp -R mld-%{version} %{buildroot}/%{_usrsrc}

%post devel
dkms add     -m mld -v %{version} || echo "dkms add     -m mld -v %{version} Failed"
dkms build   -m mld -v %{version} --verbose || echo "dkms build   -m mld -v %{version} Failed"
dkms install -m mld -v %{version} || echo "dkms install -m mld -v %{version} Failed"
modprobe hdm_usb || echo "modprobe hdm_usb Failed"

%if 0%{?fedora}
ausearch -c 'modprobe' --raw | audit2allow -M my-modprobe
semodule -i my-modprobe.pp
%endif

%postun devel
if [ -d /lib/modules/$(uname -r) ]; then 
# remove MOST kernel module
  dkms uninstall status -m mld -v %{version}
# clean build directory
  dkms remove  -m mld -v %{version} --verbose --all
fi

%files devel
%defattr(-,root,root)
%dir %{_usrsrc}/mld-%{version}
%{_usrsrc}/mld-%{version}/*

%changelog
