#
# spec file for package skalibs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name 		skalibs
%define version		0.46
%define release		1%{?dist}%{?rescue_rel}

Summary:	The skarnet.org development library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Development/Other
URL:		http://www.skarnet.org/software/skalibs/
Source0:	http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
skalibs is a package centralizing the public-domain C
development files used for building other skarnet.org software.


%package devel
Group:          Development/C
Summary:        Development files for skalibs
Obsoletes:      %{name}
Provides:       %{name}

%description devel
skalibs is a package centralizing the public-domain C
development files used for building other skarnet.org software.

skalibs can also be used as a sound basic start for C
development.  There are a lot of general-purpose libraries out
there; but if your main goal is to produce small and secure C
code, you will like skalibs.

skalibs contains exclusively public-domain code.  So you can
redistribute it as you want, and it does not prevent you from
distributing any of your executables.


%prep
%setup -q -n prog


%build
pushd %{name}-%{version}
    package/compile
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/%{name}
install -d %{buildroot}%{_includedir}/%{name}

pushd %{name}-%{version}
    for i in `cat package/include` ;  do
        install -m 0755 include/$i %{buildroot}%{_includedir}/%{name}/
    done

    for i in `cat package/library` ;  do
        install -m 0755 library/$i %{buildroot}%{_libdir}/%{name}/
    done
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files devel
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
%dir %{_includedir}/%{name}
%dir %{_libdir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/*.a


%changelog
* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.46
- first build for CentOS/RHEL 5

* Mon Nov 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.46
- 0.46

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.45
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.45
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.45
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Aug 23 2005 Sean P. Thomas <spt-at-build.annvix.org> 0.45-1avx
- initial Annvix build (needed by execline)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
