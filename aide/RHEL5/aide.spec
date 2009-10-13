%{?_with_static: %define nostatic %nil }
%{!?_with_static: %define nostatic --disable-static }

# segfaults
%{!?_with_curl: %{!?_without_curl: %define _without_curl --without-curl}}

Summary: Intrusion detection environment
Name: aide
Version: 0.13.1
Release: 12.1%{?dist}
URL: http://sourceforge.net/projects/aide
License: GPLv2+
Group: Applications/System
Source0: http://download.sourceforge.net/aide/aide-%{version}.tar.gz
Source1: aide.conf
Source2: README.quickstart
Patch1: aide-0.13.1-contextsize.patch
Patch2: aide-0.12-dedosify.patch
Patch3: aide-0.13.1-manuals.patch
Patch4: aide-0.13.1-prelink2.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: mktemp 
BuildRequires: prelink autoconf automake elfutils-libelf-devel
Buildrequires: mhash-devel
Buildrequires: zlib-devel libgcrypt-devel
Buildrequires: flex bison
Buildrequires: libattr-devel libacl-devel libselinux-devel
Buildrequires: audit-libs-devel >= 1.2.8-2
%if "%{?_with_curl}x" != "x"
Buildrequires: curl-devel
%endif
#Buildrequires: postgresql-devel libgcrypt-devel
#(needs --with-psql and -lgcrypt in src/Makefile.in)

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.


%prep
%setup -q
%patch1 -p1 -b .contextsize
%patch2 -p1 -b .dedosify
%patch3 -p1 -b .manpages
%patch4 -p1 -b .prelink
autoreconf

%build
find . -name '*.dedosify' -exec rm -f {} \;
%configure --with-config_file=%{_sysconfdir}/aide.conf \
           --with-zlib \
           --disable-static \
           --with-mhash \
           %{?_with_curl} %{?_without_curl} \
           --with-selinux --with-posix-acl --with-audit \
           --with-xattr \
           --with-prelink

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/aide
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p -m0700 $RPM_BUILD_ROOT%{_localstatedir}/lib/aide
install -p %{SOURCE2} README.quickstart


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/manual.html contrib/
%doc README.quickstart
%attr(0700,root,root) %{_sbindir}/aide
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf
%dir %attr(0700,root,root) %{_localstatedir}/lib/aide
%dir %attr(0700,root,root) %{_localstatedir}/log/aide


%changelog
* Tue Oct 13 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.13.1-12.1.el5.avx
- rebuild with proper mhash-devel/libmhash from rpmforge

* Tue Oct 13 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.13.1-12.el5.avx
- build Fedora source for EL5, should help with prelink issues
- remove .dedosify suffixed files

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.13.1-12
- rebuilt with new audit

* Wed Aug 19 2009 Steve Grubb <sgrubb@redhat.com> 0.13.1-11
- rebuild for new audit-libs
- Correct regex for root's dot files (#509370)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-9
- Make aide smarter about prelinked files (Peter Vrabec)
- Add /lib64 to default config

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-6
- enable xattr support and update config file

* Fri Sep 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13.1-5
- fix selcon patch to apply without fuzz

* Fri Feb 15 2008 Steve Conklin <sconklin@redhat.com>
- rebuild for gcc4.3

* Tue Aug 21 2007 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 22 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-2
- Apply Steve Conklin's patch to increase displayed portion of
  selinux context.

* Sun Dec 17 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-1
- Update to 0.13.1 release.

* Sun Dec 10 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13-1
- Update to 0.13 release.
- Include default aide.conf from RHEL5 as doc example file.

* Sun Oct 29 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-3.20061027cvs
- CAUTION! This changes the database format and results in a report of
  false inconsistencies until an old database file is updated.
- Check out CVS 20061027 which now contains Red Hat's
  acl/xattr/selinux/audit patches.
- Patches merged upstream.
- Update manual page substitutions.

* Mon Oct 23 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-2
- Add "memory leaks and performance updates" patch as posted
  to aide-devel by Steve Grubb.

* Sat Oct 07 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-1
- Update to 0.12 release.
- now offers --disable-static, so -no-static patch is obsolete
- fill last element of getopt struct array with zeroes

* Mon Oct 02 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-3
- rebuilt

* Mon Sep 11 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-2
- rebuilt

* Sun Feb 19 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-1
- Update to 0.11 release.
- useless-includes patch merged upstream.
- old Russian man pages not available anymore.
- disable static linking.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 28 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.1
- Update to 0.10 release.
- memleaks patch merged upstream.
- rootpath patch merged upstream.
- fstat patch not needed anymore.
- Updated URL.

* Thu Nov 13 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.2.cvs20031104
- Added buildreq m4 to work around incomplete deps of bison package.

* Tue Nov 04 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.1.cvs20031104
- Only tar.gz available upstream.
- byacc not needed when bison -y is available.
- Installed Russian manual pages.
- Updated with changes from CVS (2003-11-04).
- getopt patch merged upstream.
- bison-1.35 patch incorporated upstream.

* Tue Sep 09 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.2.20030902
- Added fixes for further memleaks.

* Sun Sep 07 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.1.20030902
- Initial package version.

