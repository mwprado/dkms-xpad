%global date 20210303
%global debug_package %{nil}
%global dkms_name xpad

Name:       kmod-%{dkms_name}-dkms
Version:    5.15.26
Release:    1%{?dist}
Summary:    X-Box gamepad driver
License:    GPLv2+
URL:        http://www.kernel.org/
BuildArch:  x86_64

# Source file:

Source0:    https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/drivers/input/joystick/xpad.c?h=v%{Version}#/xpad.c
Source1:    Makefile
Source2:    dkms.conf

Provides:   %{dkms_name} = %{version}
Requires:   dkms

%description
X-Box gamepad driver from latest upstream kernel. It is built to depend upon the
specific ABI provided by a range of releases of the same variant of the Linux
kernel and not on any one specific build.

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
* Thu Feb 17 2022 Moacyr Prado <mwprado@yahoo.com> - 5.15.24
- Update to latest stable 5.15.24 kernel version (commit a0ebea480bb319a3ad408c99db91262dbc696b76).

* Thu Feb 17 2022 Moacyr Prado <mwprado@yahoo.com> - 4.18
- Update to latest 4.18 snapshot kernel version.

* Thu Sep 21 2017 Simone Caronni <negativo17@gmail.com> - 4.14-1.20170915gitbbc8608
- Update to latest snapshot.

* Sat Apr 15 2017 Simone Caronni <negativo17@gmail.com> - 4.11-1.20170410git5376366
- Update to latest snapshot from the official kernel repository.

* Tue Feb 21 2017 Simone Caronni <negativo17@gmail.com> - 4.1-4
- Update to latest commits.

* Mon Sep 12 2016 Simone Caronni <negativo17@gmail.com> - 4.1-3
- Update to latest commits.

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
