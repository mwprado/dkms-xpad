%global debug_package %{nil}
%global dkms_name xpad

Name:       dkms-%{dkms_name}
Version:    4.1
Release:    2%{?dist}
Summary:    X-Box gamepad driver (SteamOS variant)
License:    GPLv2+
URL:        http://store.steampowered.com/steamos/
BuildArch:  noarch

# Source file:
# https://github.com/ValveSoftware/steamos_kernel/blob/brewmaster-4.1/drivers/input/joystick/xpad.c

Source0:    https://raw.githubusercontent.com/ValveSoftware/steamos_kernel/8e9ecc9caee1ae1d18c2cc4572729ef355091b6e/drivers/input/joystick/xpad.c
Source1:    Makefile
Source2:    dkms.conf

Provides:   %{dkms_name}-kmod = %{version}
Requires:   dkms

%description
X-Box gamepad driver with specific patches made by Valve for SteamOS.

%prep
%setup -q -T -c -n %{name}-%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} .

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 4.1-2
- Update to latest commits.

* Sat Nov 14 2015 Simone Caronni <negativo17@gmail.com> - 4.1-1
- Update to version from 4.1 branch (SteamOS 2.x).

* Thu Jul 16 2015 Simone Caronni <negativo17@gmail.com> - 0.2-2
- Update to latest commits.

* Wed Jul 08 2015 Simone Caronni <negativo17@gmail.com> - 0.2-1
- Rebase to brewmaster 3.18 kernel.
- Drop integrated patches.

* Sat May 23 2015 Simone Caronni <negativo17@gmail.com> - 0.1-3
- Apply patche from tjormola tree which includes extra fixes:
  https://github.com/tjormola/steamos_kernel/commits/xpad_fixes_from_linus_tree/drivers/input/joystick/xpad.c

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 0.1-2
- Use directly SteamOS kernel source, remove patches:
  https://github.com/ValveSoftware/steamos_kernel/commits/alchemist-3.10/drivers/input/joystick/xpad.c

* Thu May 29 2014 Simone Caronni <negativo17@gmail.com> - 0.1-1
- First build, with Valve patches.
