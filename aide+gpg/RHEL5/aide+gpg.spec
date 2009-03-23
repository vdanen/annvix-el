#
# spec file for package aide+gpg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		aide+gpg
%define version		1.0.1
%define release         1%{?dist}%{?rescue_rel}

Summary:	GPG support for AIDE
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/System
URL:		http://annvix.org/Tools/AIDE_gpg
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Requires:	aide
Requires:	gnupg

%description
AIDE (Advanced Intrusion Detection Environment) is a free alternative
to Tripwire.  This package provides a GPG-enabled frontend to AIDE.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/cron.daily
make PREFIX=%{buildroot} install

ln -sf ../..%{_sbindir}/aidecheck %{buildroot}%{_sysconfdir}/cron.daily/aide


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0700,root,root) %{_sbindir}/aidecheck
%attr(0700,root,root) %{_sbindir}/aideinit
%attr(0700,root,root) %{_sbindir}/aideupdate
%{_mandir}/man8/aide*
%attr(0700,root,root) %{_sysconfdir}/cron.daily/aide

%changelog
* Sun Mar 22 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.0.1
- 1.0.1
- first Annvix package (broken out from old Annvix aide package to just
  provide the aide+gpg stuff)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
