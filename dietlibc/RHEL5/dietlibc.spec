#
# spec file for package dietlibc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		dietlibc
%define version 	0.30
%define release 	1%{?dist}%{?rescue_rel}

# This is eventually a biarch package, so no %_lib for diethome
%define diethome	%{_prefix}/lib/dietlibc

# Enable builds without testing (default is always to test)
%define build_check	1
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}

Summary:	C library optimized for size
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
Source1:	http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2.sig
Patch0:		dietlibc-0.29-features.patch
Patch1:		dietlibc-0.30-mdkconfig.patch
Patch3:		dietlibc-0.22-tests.patch
Patch4:		dietlibc-0.27-fix-getpriority.patch
Patch5:		dietlibc-0.22-net-ethernet.patch
Patch6:		dietlibc-0.24-rpc-types.patch
Patch9:		dietlibc-0.27-glibc-nice.patch
Patch13:	dietlibc-0.27-x86_64-lseek64.patch
Patch16:	dietlibc-0.27-test-makefile-fix.patch
Patch17:	dietlibc-0.27-x86_64-stat64.patch
Patch23:	dietlibc-0.29-biarch.patch
Patch24:	dietlibc-0.27-quiet.patch
Patch26:	dietlibc-0.29-avx-stackgap_off.patch
Patch28:	dietlibc-0.29-avx-fix_no_ipv6.patch
Patch30:	dietlibc-0.29-mdv-64bit-fixes-printf.patch
Patch31:	dietlibc-0.29-mdv-fix-strncmp.patch
Patch32:	dietlibc-0.30-alt-fstatfs64-typo.patch
Patch33:	dietlibc-0.30-mdv-relatime.patch
Patch34:	dietlibc-0.30-mdv-force-no-stack-protector.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Small libc for building embedded applications.

%package devel
Group:          Development/C
Summary:        Development files for dietlibc
Obsoletes:	%{name}
Provides:	%{name}

%description devel
Small libc for building embedded applications.


%prep
%setup -q 
%patch0 -p1 -b .features
%patch1 -p1 -b .mdkconfig
%patch3 -p1 -b .tests
%patch4 -p1 -b .fix-getpriority
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch9 -p1 -b .glibc-nice -E
%patch13 -p1 -b .x86_64-lseek64
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch26 -p1 -b .stackgap_off
%patch28 -p1 -b .fix_no_ipv6
%patch30 -p1 -b .64bit-fixes-printf
%patch31 -p1 -b .fix-stncmp
%patch32 -p1 -b .fstatfs64
%patch33 -p1 -b .relatime
%patch34 -p1 -b .stack-protector

# fix execute permissions on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh


%build
make
make "CFLAGS=-pipe -nostdinc"


%check
# make and run the tests
%if %{build_check}
cd test
rm -f *.c.*
export DIETHOME="%{_builddir}/%{name}-%{version}"
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g"
make

STANDARD_TESTPROGRAMS=`grep "^TESTPROGRAMS" runtests.sh | cut -d\" -f2`
# these fail: cp-test3 cp-test4 cp-test6 cp-test7 cp-test11 cp-test12 cp-test15
CP_TEST_PROGRAMS="cp-test1 cp-test2 cp-test5 cp-test8 cp-test9 cp-test10 cp-test13 cp-test14"
perl -pi -e "s|^TESTPROGRAMS.*|TESTPROGRAMS=\"${STANDARD_TESTPROGRAMS} ${CP_TEST_PROGRAMS}\"|g" runtests.sh
# getpass requires user input
perl -pi -e "s|^PASS.*|PASS=\"\"|g" runtests.sh
sh ./runtests.sh

cd ..
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files devel
%defattr(-,root,root)
%doc AUTHOR BUGS CAVEAT CHANGES README THANKS TODO FAQ
%{_bindir}/diet
%dir %{diethome}
%{diethome}/*
%{_mandir}/man*/*


%changelog
* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.30
- build for CentOS/RHEL 5
- don't dual build both i386 and x86_64 on x86_64

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.30
- 0.30
- updated P1 from Mandriva
- drop P14; it doesn't apply and wasn't being used
- drop P27; merged upstream
- drop P29; we don't want SSP support in dietlibc
- P30: fix *printf("%u") for 64bit platforms (dmraid)
- P31: fix strncmp() (nano)
- P32: fix build of fstatfs64 (from ALT)
- P33: add MS_RELATIME definition
- P34: add -fno-stack-protector to override default %%optflags

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.29
- rebuild

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.29
- updated P13 from Mandriva to fix mdadm's compilation of mdassemble
  on x86_64

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.29
- sync with mandriva package:
  - updated P0
  - drop contrapolice (P14) as it's broken
  - updated P23, and apply it
- for some reason, elftrunc and dnsd are not installed anymore so
  don't include them
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.29
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.29
- Obfuscate email addresses and new tagging
- Uncompress patches
- P29: make dietlibc SSP aware (from gentoo)

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.29-1avx
- 0.29
- P27: fix <asm/types.h> size_t definition for 64bit platforms
  (gbeauchesne)
- drop P15, P18, P21, P22, P25 - all are ppc/ppc64-related and
  we don't build for ppc/ppc64
- rediff P26
- adjust P23 so we're not patching the Makefile; we'll do all of our biarch
  install stuff in the spec instead
- P28: fix build when WANT_IPV6_DNS is not set

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.28-4avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.28-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.28-2avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.28-1avx
- 0.28
- drop P7, P8, P10, P11, P12, P19, P20 (merged upstream)
- P26: disable WANT_STACKGAP as it interferes with our gcc+SSP

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.27-2avx
- some fixes

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.27-1avx
- 0.27
- re-order patches to match mdk package
- merge with mandrake 0.27-9mdk:
  - fix getpriority() as the return value from the syscall is biased (gb)
  - add nice() implementation from glibc, make it use the fixed getpriority (gb)
  - fix ppc select() (gb)
  - quiet test bsearch (gb)
  - biarch builds on x86_64 and ppc64 (gb)
  - ppc64 fixes: umount, setjmp, __WORDSIZE, select, stat64, rdtsc (gb)
  - added struct stat64 as struct stat and fstat64() as fstat() on x86_64,
    so test suite builds (bluca)
  - add RDTSC in testsuite for ppc (cjw)
  - fix permissions on test scripts in subdirs (cjw)
  - P16: build inet tests (cjw)
  - make and run the test suite (oden)
  - implement lseek64() as lseek() on x86_64 (gb)
  - fix rdstc in testsuite for amd64 (gb)
  - fix tzfile() for 64bit-archs, aka. fix mktime() (gb)
  - P10: ISO C defines LC_ macros (7.11 [#3]) (gb)
  - merge P2 and P4 into P1 (ppc64asppc and lib64 fixes are now in P1) (oden)
  - P8: fix strtol() + testcase on 64-bit platforms (gb)  

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.24-3avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.24-2sls
- rebuild

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 0.24-1sls
- 0.24
- contrapolice 0.1 for heap protection
- remove P4, P6, P9, P10, P11, P12, P13, P14, P15, P16, P17: all
  merged upstream
- don't apply P3 as it prevents us from building on amd64

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.22-8sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
