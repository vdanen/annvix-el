#
# spec file for package rsec
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		rsec
%define version		0.72.4
%define release		1%{?dist}%{?rescue_rel}

Summary:	Security Reporting tool for Annvix
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2
Group:		System/Base
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/tools/rsec/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}

Requires:	bash
Requires:	coreutils
Requires:	perl
Requires:	diffutils
Requires:	shadow-utils
Requires:	gawk
Requires:	mailx
Requires:	setup >= 2.2.0-21mdk
Requires:	iproute
Requires:	rkhunter >= 1.3.0
Conflicts:	passwd < 0.67
Conflicts:	msec

%description
The Annvix Security Reporting tool (rsec) is largely based on the
Mandriva Linux msec program.  rsec produces the same reports as msec, but
does not manage permission issues or system configuration changes.  It is
nothing more than a reporting tool to advise you of changes to your system
and potential problem areas.  Any changes or fixes are entirely up to the
user to correct.


%prep
%setup -q


%build
make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/{security,logrotate.d,cron.daily,cron.hourly}
mkdir -p %{buildroot}{%{_datadir}/rsec,%{_bindir},/var/log/security,%{_mandir}/man8}

install -m 0640 cron-sh/{security,diff}_check.sh %{buildroot}%{_datadir}/rsec
install -m 0750 cron-sh/{promisc_check,security,pkgcheck,apt_cleancache}.sh %{buildroot}%{_datadir}/rsec
install -m 0750 src/promisc_check/promisc_check src/rsec_find/rsec_find %{buildroot}%{_bindir}
install -m 0644 rsec.logrotate %{buildroot}/etc/logrotate.d/rsec
install -m 0644 *.8 %{buildroot}%{_mandir}/man8/
install -m 0640 rsec.conf %{buildroot}%{_sysconfdir}/security
install -m 0750 rsec.crondaily %{buildroot}%{_sysconfdir}/cron.daily/rsec
install -m 0750 rsec.cronhourly %{buildroot}%{_sysconfdir}/cron.hourly/rsec
pushd %{buildroot}%{_sysconfdir}/cron.daily
    ln -s ../..%{_datadir}/rsec/pkgcheck.sh pkgcheck
    ln -s ../..%{_datadir}/rsec/apt_cleancache.sh apt_cleancache
popd

touch %{buildroot}/var/log/security.log


%post
touch /var/log/security.log && chmod 0640 /var/log/security.log


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog
%{_bindir}/promisc_check
%{_bindir}/rsec_find
%dir %_datadir/rsec
%{_datadir}/rsec/*
%{_mandir}/man8/rsec.8*
%dir %attr(0750,root,root) /var/log/security
%config(noreplace) %{_sysconfdir}/security/rsec.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rsec
%config(noreplace) %{_sysconfdir}/cron.daily/rsec
%config(noreplace) %{_sysconfdir}/cron.hourly/rsec
%{_sysconfdir}/cron.daily/pkgcheck
%{_sysconfdir}/cron.daily/apt_cleancache
%ghost %attr(0640,root,root) /var/log/security.log


%changelog
* Fri Jul 2 2010 Vincent Danen <vdanen-at-build.annvix.org> 0.72.4
- 0.72.4

* Sat Jun 5 2010 Vincent Danen <vdanen-at-build.annvix.org> 0.72.3
- 0.72.3

* Wed Dec 30 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.72.2
- 0.72.2

* Wed Aug 19 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.72.1
- 0.72.1

* Mon Aug 3 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.72
- 0.72

* Wed Apr 29 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- 0.71

* Sun Apr 19 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.70.3
- 0.70.3

* Sat Apr 18 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.70.2
- change dependency on iproute2 to iproute
- change dependency on perl-base to perl

* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.70.2
- 0.70.2
- first build for CentOS/RHEL 5

* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.69.1
- 0.69.1

* Sun Dec 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.69
- 0.69
- require rkhunter
- update the URL and license

* Sat Dec 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- 0.68
- fix the %%install

* Sat Feb 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.67
- 0.67

* Sat Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.66
- fix URL

* Wed Jul 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.66
- 0.66:
  - fix call to logger

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.65
- 0.65:
  - security_check.sh: don't check /etc/shadow if it doesn't exist
  - rsec.conf: turn off CHECK_SHADOW by default since we use tcb instead
  - urpmicheck.sh: also check update/check apt if it's available
- fix URL
- add -doc subpackage

* Mon Mar 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.63
-0.63:
  - change reporting of unowned user/group files since we don't chown
    them anymore
  - document the EXCLUDEDIR option and include it in the default rsec.conf
    with a default entry of "/var/lib/rsbac"
  - set EXCLUDE_REGEXP to exclude /override and /var/tmp/php_sessions by
    default

* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.62
- 0.62:
  - don't change ownership of unowned files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.61
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.61-2avx
- update the docs/configs to explain EXCLUDE_REGEXP better

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.61-1avx
- 0.61
  - don't check sysfs, usbfs, or hfs filesystems
  - fix user or homedir with spaces
  - new option to rsec.conf: EXCLUDE_REGEXP; used to exclude directories from
    the various reports
  - use getent rather than /etc/passwd for lookups (due to LDAP/NIS users)
  - allow % in filenames
  - removed xfs from remote filesystems
  - updated manpage and moved it from .3 to .8

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.60-1avx
- 0.60: uses rkhunter rather than chkrootkit

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-2avx
- rebuild

* Sun Feb 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-1avx
- 0.51: new option to exclude certain directories from the world-writeable file check

* Wed Jul 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.50-4avx
- Requires: mailx (for /bin/mail)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.50-3avx
- Requires: packages, not files
- Annvix build

* Fri Apr 23 2004 Vincent Danen <vdanen@opensls.org> 0.50-2sls
- make urpmicheck.sh a bit more robust

* Wed Mar 10 2004 Vincent Danen <vdanen@opensls.org> 0.50-1sls
- first OpenSLS package based on msec-0.42-1mdk

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
