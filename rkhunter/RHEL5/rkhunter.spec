#
# spec file for package rkhunter
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		rkhunter
%define version		1.3.6
%define release		1%{?dist}%{?rescue_rel}

Summary:	Rootkit scans for rootkits, backdoors and local exploits
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Configuration
URL:		http://www.rootkit.nl/projects/rootkit_hunter.html
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		rkhunter-1.3.6-avx-conf.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildArch:	noarch

Requires:	curl
Requires:	e2fsprogs
Requires:	binutils

%description
Rootkit scanner is scanning tool to ensure you for about 99.9%% you're
clean of nasty tools. This tool scans for rootkits, backdoors and local
exploits by running tests like:
	- MD5 hash compare
	- Look for default files used by rootkits
	- Wrong file permissions for binaries
	- Look for suspected strings in LKM and KLD modules
	- Look for hidden files
	- Optional scan within plaintext and binary files


%prep
%setup -q
%patch0 -p0 -b .avx-conf

chmod a+r files/{README,CHANGELOG}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sbindir},%{_var}/lib/%{name}/{db/i18n,scripts,tmp},%{_sysconfdir},%{_mandir}/man8}

install -m 0750 files/rkhunter %{buildroot}%{_sbindir}/
install -m 0640 files/rkhunter.conf %{buildroot}%{_sysconfdir}
echo "INSTALLDIR=%{_var}" >> %{buildroot}%{_sysconfdir}/rkhunter.conf
echo "SCRIPTDIR=%{_var}/lib/%{name}/scripts" >> %{buildroot}%{_sysconfdir}/rkhunter.conf
install -m 0640 files/*.dat %{buildroot}%{_var}/lib/%{name}/db
install -m 644 files/i18n/* %{buildroot}%{_var}/lib/%{name}/db/i18n
install -m 0750 files/*.{pl,sh} %{buildroot}%{_var}/lib/%{name}/scripts
install -m 0644 files/rkhunter.8 %{buildroot}%{_mandir}/man8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README 
%config(noreplace) %{_sysconfdir}/rkhunter.conf
%{_sbindir}/*
%dir %{_var}/lib/%{name}
%dir %{_var}/lib/%{name}/db
%dir %{_var}/lib/%{name}/scripts
%dir %attr(0700,root,root) %{_var}/lib/%{name}/tmp
%{_var}/lib/%{name}/db/*
%{_var}/lib/%{name}/scripts/*
%{_mandir}/man8/*


%changelog
* Wed Dec 30 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6
- 1.3.6

* Sat Apr 18 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.3.4
- 1.3.4
- first build for CentOS/RHEL 5
- update avx-conf patch to remove Annvix entries and add CentOS 5.2/5.3 entries
- require curl instead of webfetch (nothing provides webfetch in RHEL5)

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.0
- 1.2.9
- rediff P0 and add support for 2.0-CURRENT, dropping 1.x
- drop P1; curl support added upstream

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.8
- 1.2.8
- update the config to support 2.0
- make the install a bit better
- relocate everything to /var/lib rather than have half in /lib and the
  other half in /var/lib

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- fix group

* Wed Feb 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- re-order patches and break out the config stuff vs. the curl stuff
  and update the config to support 1.2-RELEASE

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7-2avx
- update P0 to make 1.1-RELEASE supported rather than 1.1-CURRENT

* Thu Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7-1avx
- build for Annvix to replace chkrootkit
- P0: add support for curl and Annvix

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
