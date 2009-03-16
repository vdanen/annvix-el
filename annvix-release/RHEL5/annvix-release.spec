#
# spec file for package annvix-release
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

Summary:	Annvix release file and package configuration
Name:		annvix-release
Version:	1.0
Release:	2%{?dist}
License:	GPL
Group:		System Environment/Base
URL:		http://annvix.org/

Packager:	Vincent Danen <vdanen@annvix.org>
Vendor:		Annvix [http://annvix.org/]

Source0:	RPM-GPG-KEY-annvix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Annvix release file for yum.

%prep
%if "%{dist}" == ".el5.avx"
version="EL5"
%endif

%{__cat} <<EOF >annvix.yum
# Annvix CentOS/RHEL third-party repository [http://annvix.org/]
[annvix]
name = CentOS/RHEL-$version - Annvix
baseurl = http://repo.annvix.org/media/$version/\$basearch
enabled = 1
protect = 0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-annvix
gpgcheck = 1
EOF


%build


%install
rm -rf %{buildroot}
install -Dp -m0644 %{_sourcedir}/RPM-GPG-KEY-annvix %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-annvix
install -Dp -m0644 annvix.yum %{buildroot}%{_sysconfdir}/yum.repos.d/annvix.repo


%clean
rm -rf %{buildroot}
rm -f annvix.yum


%post
rpm -q gpg-pubkey-65d5605c-49988ded &>/dev/null || rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-annvix || :


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/yum.repos.d/annvix.repo
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-annvix


%changelog
* Mon Mar 16 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.1-2
- clean up the created yum repository file

* Tue Feb 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.1-1
- first Annvix build

# vim:set et ts=8 sw=8 list listchars=tab\:>-,trail\:.:
