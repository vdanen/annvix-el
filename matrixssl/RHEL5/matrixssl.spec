#
# spec file for package matrixssl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	name		matrixssl
%define	version		1.8.2
%define	release		1%{?dist}%{?rescue_rel}

%define diethome	%{_prefix}/lib/dietlibc

Summary:	MatrixSSL is an embedded SSL implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.matrixssl.org/
Source0:	%{name}-1-8-2-open.tar.bz2
Patch0:		matrixssl-1.8-shared_and_static.diff
Patch1:		matrixssl-1.8.1-debian.diff

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.27-2avx

%description
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 


%package devel
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	dietlibc-devel >= 0.20

%description devel
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

This package contains the static libraries and headers for both
glibc and dietlibc.


%prep
%setup -q -n %{name}-1-8-2
%patch0 -p0
%patch1 -p1

# prepare for dietlibc
mkdir -p dietlibc
cp -rp src dietlibc/
cp matrixSsl.h matrixCommon.h dietlibc/


%build
# first make the standard glibc stuff...
make -C src DFLAGS="%{optflags} -fPIC"

COMP="diet gcc"

# now make the dietlibc static library
make -C dietlibc/src CC="$COMP -Os" \
    LDFLAGS="-nostdlib" \
    static


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{diethome}/{lib-${MYARCH},include}
install -d %{buildroot}%{_libdir}

# install the glibc version
install -m 0755 src/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -m 0644 src/lib%{name}.a %{buildroot}%{_libdir}/
install -m 0644 matrixSsl.h %{buildroot}%{_includedir}/
install -m 0644 matrixCommon.h %{buildroot}%{_includedir}/
install -m 0644 src/matrixConfig.h %{buildroot}%{_includedir}/
perl -pi -e 's|src/matrixConfig.h|matrixConfig.h|g' %{buildroot}%{_includedir}/matrixCommon.h

# install the dietlibc version
install -m 0644 dietlibc/src/lib%{name}.a %{buildroot}%{diethome}/lib-${MYARCH}/
install -m 0644 dietlibc/matrixSsl.h %{buildroot}%{diethome}/include/
install -m 0644 dietlibc/matrixCommon.h %{buildroot}%{diethome}/include/
install -m 0644 dietlibc/src/matrixConfig.h %{buildroot}%{diethome}/include/
perl -pi -e 's|src/matrixConfig.h|matrixConfig.h|g' %{buildroot}%{diethome}/include/matrixCommon.h

# cleanup the examples directory
rm -f examples/*.sln
rm -f examples/*.vcproj
rm -f examples/*.pem
rm -f examples/*.p12


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc examples
%{_includedir}/*
%{diethome}/include/*
%{_libdir}/*.so
%{_libdir}/*.a
%{diethome}/lib-*/*.a


%changelog
* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.8.2
- first build for CentOS/RHEL 5

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.8.2
- implement devel naming policy
- implement library provides policy

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.2
- 1.8.2
- updated P1

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8
- 1.8
- rediff P0, P1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.1-1avx
- 1.7.1
- drop all pdf docs
- rediff P0 (oden)
- rediff P1 (fixes x86_64 build) (oden)
- include matrixConfig.h and fix the #include location in matrixCommon.h

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-5avx
- rebuild

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-4avx
- rebuild against new dietlibc

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-3avx
- revert lib64 "fixes"
- rebuild against new dietlibc and use %%diethome with MYARCH

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-2avx
- lib64 fixes (oden)

* Wed Oct 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2-1avx
- 1.2.2

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2-1avx
- Annvix build; needed for ipsvd

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
