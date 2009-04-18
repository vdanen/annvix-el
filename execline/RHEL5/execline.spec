#
# spec file for package execline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name 		execline
%define version		1.07
%define release		1%{?dist}%{?rescue_rel}

%define _bindir		/bin

Summary:	A light non-interactive scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System Environment/Shells
URL:		http://www.skarnet.org/software/execline/
Source0:	http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28
BuildRequires:  skalibs-devel >= 0.40

%description
execline is a very light, non-interactive scripting language, which is 
similar to a shell. Simple shell scripts can be easily rewritten in the 
execline language, improving performance and memory usage. execline was 
designed for use in embedded systems, but works on most Unix flavors.


%prep
%setup -q -n admin


%build
COMP="diet gcc"

pushd %{name}-%{version}
    echo "$COMP -O2 -W -Wall -fomit-frame-pointer -pipe" > conf-compile/conf-cc
    echo "$COMP -Os -static -s" > conf-compile/conf-ld
    echo "strip" >conf-compile/conf-stripbins

    echo "linux-:%{_target_cpu}-:" > src/sys/systype

    echo "%{_includedir}/skalibs" > conf-compile/import
    echo "%{_libdir}/skalibs" >> conf-compile/import

    package/compile
    perl -pi -e 's|\/command|\/bin|g' etc/execline-{startup,shell}
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sysconfdir},/bin}

pushd %{name}-%{version}
    for i in `cat package/command.exported` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done
    install -m 0755 etc/* %{buildroot}%{_sysconfdir}/
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*
%config(noreplace) %{_sysconfdir}/execline-shell
%config(noreplace) %{_sysconfdir}/execline-startup


%changelog
* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- first build for CentOS/RHEL 5

* Mon Nov 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- 1.07
- explicitly set 'strip' as conf-compile/conf-stripbins
- put in the /etc files

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Tue Aug 23 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.06-1avx
- initial Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
