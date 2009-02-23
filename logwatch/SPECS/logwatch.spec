Summary: A log file analysis program
Name: logwatch
Version: 7.3
Release: 6%{dist}
License: MIT
Group: Applications/System
URL: http://www.logwatch.org/
Source: ftp://ftp.kaybee.org/pub/linux/logwatch-%{version}.tar.gz
Patch2: logwatch-7.2.1-nosegfault.patch
Patch3: logwatch-7.2.1-up2date.patch
Patch4: logwatch-7.3-samba.patch
Patch5: logwatch-7.3-temp_dir.patch
Patch6: logwatch-7.3-secure.patch
Patch7: logwatch-7.3-audit.patch
Patch8: logwatch-7.3-sshd.patch
Patch9: logwatch-7.3-iptables.patch
Patch10: logwatch-7.3-amavis.patch
Patch11: logwatch-7.3-man.patch
Patch12: logwatch-7.3-postfix.patch
Patch13: logwatch-7.3-oldfiles.patch

Requires: textutils sh-utils grep mailx
BuildRoot: %{_tmppath}/logwatch-build
BuildArchitectures: noarch

%description
Logwatch is a customizable, pluggable log-monitoring system.  It will go
through your logs for a given period of time and make a report in the areas
that you wish with the detail that you wish.  Easy to use - works right out
of the package on many systems.

%prep
%setup -q
%patch2 -p1 
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%install

rm -rf %{buildroot}

install -m 0755 -d %{buildroot}%{_var}/cache/logwatch
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/scripts
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf/logfiles
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/logfiles
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/html
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/dist.conf/logfiles
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/dist.conf/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/scripts/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/scripts/shared
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/lib

for i in scripts/logfiles/*; do
    if [ $(ls $i | wc -l) -ne 0 ]; then
	install -m 0755 -d %{buildroot}%{_datadir}/logwatch/$i
	install -m 0755 $i/* %{buildroot}%{_datadir}/logwatch/$i
    fi
done

install -m 0755 scripts/logwatch.pl %{buildroot}%{_datadir}/logwatch/scripts/logwatch.pl
install -m 0755 scripts/services/* %{buildroot}%{_datadir}/logwatch/scripts/services
install -m 0755 scripts/shared/* %{buildroot}%{_datadir}/logwatch/scripts/shared

install -m 0644 conf/logwatch.conf %{buildroot}%{_datadir}/logwatch/default.conf/logwatch.conf
install -m 0644 conf/logfiles/* %{buildroot}%{_datadir}/logwatch/default.conf/logfiles
install -m 0644 conf/services/* %{buildroot}%{_datadir}/logwatch/default.conf/services
install -m 0644 conf/html/* %{buildroot}%{_datadir}/logwatch/default.conf/html

install -m 0644 lib/Logwatch.pm %{buildroot}%{_datadir}/logwatch/lib/Logwatch.pm

install -m 0755 -d %{buildroot}%{_mandir}/man8
install -m 0644 logwatch.8 %{buildroot}%{_mandir}/man8

rm -f  %{buildroot}%{_sysconfdir}/cron.daily/logwatch \
   %{buildroot}%{_sbindir}/logwatch \
   %{buildroot}%{_datadir}/logwatch/scripts/services/zz-fortune* \
  %{buildroot}%{_datadir}/logwatch/conf/services/zz-fortune* \
 %{buildroot}%{_datadir}/logwatch/conf/logfiles/fortune*
touch %{buildroot}%{_datadir}/logwatch/scripts/services/zz-fortune
chmod 755 %{buildroot}%{_datadir}/logwatch/scripts/services/zz-fortune

install -m 0755 -d %{buildroot}%{_sysconfdir}/cron.daily
ln -s %{_datadir}/logwatch/scripts/logwatch.pl %{buildroot}%{_sysconfdir}/cron.daily/0logwatch
install -m 0755 -d %{buildroot}%{_sbindir}
ln -s %{_datadir}/logwatch/scripts/logwatch.pl %{buildroot}%{_sbindir}/logwatch

echo "###### REGULAR EXPRESSIONS IN THIS FILE WILL BE TRIMMED FROM REPORT OUTPUT #####" > %{buildroot}%{_sysconfdir}/logwatch/conf/ignore.conf
echo "# Local configuration options go here (defaults are in %{_datadir}/logwatch/default.conf/logwatch.conf)" > %{buildroot}%{_sysconfdir}/logwatch/conf/logwatch.conf
echo "# Configuration overrides for specific logfiles/services may be placed here." > %{buildroot}%{_sysconfdir}/logwatch/conf/override.conf



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README HOWTO-Customize-LogWatch 
%dir %{_var}/cache/logwatch
%dir %{_sysconfdir}/logwatch
%dir %{_sysconfdir}/logwatch/conf
%dir %{_sysconfdir}/logwatch/scripts
%dir %{_sysconfdir}/logwatch/conf/logfiles
%dir %{_sysconfdir}/logwatch/conf/services
%dir %{_datadir}/logwatch
%dir %{_datadir}/logwatch/default.conf
%dir %{_datadir}/logwatch/default.conf/services
%dir %{_datadir}/logwatch/default.conf/logfiles
%dir %{_datadir}/logwatch/default.conf/html
%dir %{_datadir}/logwatch/dist.conf
%dir %{_datadir}/logwatch/dist.conf/services
%dir %{_datadir}/logwatch/dist.conf/logfiles
%dir %{_datadir}/logwatch/scripts
%dir %{_datadir}/logwatch/scripts/logfiles
%dir %{_datadir}/logwatch/scripts/services
%dir %{_datadir}/logwatch/scripts/shared
%dir %{_datadir}/logwatch/scripts/logfiles/*
%dir %{_datadir}/logwatch/lib
%{_datadir}/logwatch/scripts/logwatch.pl
%config(noreplace) %{_sysconfdir}/logwatch/conf/*.conf
#%config(noreplace) %{_sysconfdir}/logwatch/conf/services/*
#%config(noreplace) %{_sysconfdir}/logwatch/conf/logfiles/*
%{_sbindir}/logwatch
%{_datadir}/logwatch/scripts/shared/*
%{_datadir}/logwatch/scripts/services/*
%{_datadir}/logwatch/scripts/logfiles/*/*
%{_datadir}/logwatch/lib/Logwatch.pm
%{_datadir}/logwatch/default.conf/*.conf
%{_datadir}/logwatch/default.conf/services/*.conf
%{_datadir}/logwatch/default.conf/logfiles/*.conf
%{_datadir}/logwatch/default.conf/html/*.html
%{_sysconfdir}/cron.daily/0logwatch
%doc %{_mandir}/man8/logwatch.8*

%doc License project/CHANGES project/TODO

%changelog
* Thu Jan  3 2008 Ivana Varekova <varekova@redhat.com> 7.3-6
- Resolves: #307281
  logwatch HTML output
- Resolves: #249792
  option --usage deleted from the man page
- Resolves: #296001
  Logwatch is unable to handle e.g. postfix 2.3 mail logs
- Resolves: #230974
  add no-oldfiles-log option

* Tue Aug 29 2006 Ivana Varekova <varekova@redhat.com> 7.3-5
- fix amavis problem #204432 

* Mon Aug 14 2006 Marcela Maslanova <mmaslano@redhat.com> 7.3-4
- add audit patch for SElinux (#200116)
- add patch for sshd (#200105)
- add patch from bugzilla, made by Allen Kistler (#200147)

* Fri Jun 23 2006 Ivana Varekova <varekova@redhat.com> 7.3-3
- added secure-service patch

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> 7.3-2
- added tests to file creation and access, clean up 
resulting files when logwatch fails (upstream change) 
(#190498)

* Mon Mar 27 2006 Ivana Varekova <varekova@redhat.com> 7.3-1
- update to 7.3
- added samba, up2date

* Fri Mar 17 2006 Ivana Varekova <varekova@redhat.com> 7.2.1-1
- update to 7.2.1
- update nosegfault, pam_unix, http patches
- added sshd, smart, named, audit, secure and mountd services
  patches

* Mon Feb 20 2006 Ivana Varekova <varekova@redhat.com> 7.1-8
- fix http exploit problem #181802

* Fri Jan 20 2006 Ivana Varekova <varekova@redhat.com> 7.1-7
- extended pam_unix patch (fix sshd service)

* Wed Jan 18 2006 Ivana Varekova <varekova@redhat.com> 7.1-6
- removed nounicode patch
- added patch to fix pam_unix logs parsing (#178058)

* Fri Dec 23 2005 Ivana Varekova <varekova@redhat.com> 7.1-5
- fix http exploits problem (bug 176324 - comment 2)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 7.1-4
- updated /etc/.../logwatch.conf file (bug 175233)

* Tue Nov 29 2005 Ivana Varekova <varekova@redhat.com> 7.1-3
- add secure service patch
- add iptables patch created by Allen Kistler (bug 174954) 
- add audit service patch

* Wed Nov 24 2005 Ivana Varekova <varekova@redhat.com> 7.1-2
- add named script patch (bug 171631)
- change autdated description

* Wed Nov 23 2005 Ivana Varekova <varekova@redhat.com> 7.1-1
- update to 7.1
- added sshd and samba patches

* Wed Nov  2 2005 Ivana Varekova <varekova@redhat.com> 7.0-2
- fix zz-disk_space problem (bug 172230) 
  used michal@harddata.com patch
- fix a few inconsistencies with new directory structure
- changed previous zz-disk_space 
- add secure sript patch allow case insensitivity for GID, UID)

* Thu Oct 13 2005 Ivana Varekova <varekova@redhat.com> 7.0-1
- update to 7.0 (new directory structure)
- add smartd and zz-disk_space patch

* Mon Oct  3 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-7
- add audit script patch recognized other unmatched logs
- add cron script patch 
- change sshd script patch

* Fri Sep 30 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-6
- add audit script patch to recognize number of unmatched entries

* Mon Sep 26 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-5
- change secure script patch
- add sshd script patch (sshd part should not display 0.0.0.0 
   in "Failed to bind" column)
- add one unmatch line to named script

* Mon Sep 19 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-4
- fixed secure script (part of bug 141116, added a few 
  unknown logs)
- bug 168469 - fixed up2date script 

* Mon Jul 25 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-3
- bug 162689 - add noreplace option

* Wed Jun 29 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-2
- fix bug 161973 - The logwatch yum service doesn't properly 
show removed entries
- used patch created by Dean Earley (patch5)

* Thu Jun 23 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-1
- update to 6.1.2-1

* Thu May 19 2005 Jiri Ryska <jryska@redhat.com> 6.0.1-2
- fixed temp dir creation #155795

* Thu Apr 15 2005 Jiri Ryska <jryska@redhat.com> 6.0.1-1
- update to 6.0.1

* Tue Nov 09 2004 Jiri Ryska <jryska@redhat.com>
- Patch for #134288, #138285

* Wed Jul 14 2004 Elliot Lee <sopwith@redhat.com> 5.2.2-1
- Update to 5.2.2
- Patch for #126558, #101744

* Wed Jul 07 2004 Elliot Lee <sopwith@redhat.com> 5.1-6
- Extra patch from #80496

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Joe Orton <jorton@redhat.com> 5.1-4
- stop logging access_log entries with 2xx response codes

* Wed Mar 17 2004 Elliot Lee <sopwith@redhat.com> 5.1-3
- Fix the perl(Logwatch) problem the correct way, as per #118507

* Mon Mar 15 2004 Elliot Lee <sopwith@redhat.com> 5.1-2
- Add provides perl(Logwatch)

* Fri Mar 12 2004 Elliot Lee <sopwith@redhat.com> 5.1-1
- Update (#113802)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 05 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-4
- Fix #103720

* Wed Aug 13 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-3
- Fix a reported bug about MsgsSent/BytesTransferred stats not
  counting locally-originated traffic.

* Wed Jul 10 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-2
- Fix #81144 (nounicode), #85551 and part of #97421 (nosegfault), #87483 (funkyhn)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Elliot Lee <sopwith@redhat.com> 4.3.1-1
- Update to new upstream version

* Tue Dec 10 2002 Elliot Lee <sopwith@redhat.com> 4.0.3-3
- Apply patch from #77173

* Wed Oct 16 2002 Elliot Lee <sopwith@redhat.com> 4.0.3-2
- Update to new upstream version

* Thu Aug 08 2002 Elliot Lee <sopwith@redhat.com> 2.6-8
- Apply patch from #68804, #68806

* Mon Jul 15 2002 Elliot Lee <sopwith@redhat.com> 2.6-7
- Fix #68869 (the other half of the expandrepeats job)

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 2.6-6
- Remove expandrepeats (#67606)
- Patch6 (ftpd-messages.patch) from #68243

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.6-5
- logwatch-2.6-applydate-65655.patch to fix xferlog date parsing
- logwatch-2.6-xinetd_match-65856.patch to match more xinetd lines properly
- logwatch-2.6-confparse-65937.patch to properly parse lines with multiple 
  = chars in them

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Elliot Lee <sopwith@redhat.com> 2.6-2
- Fix #62787 (logwatch-2.6-newline-62787.patch) and #63279 (logwatch-2.6-applystddate-63279.patch)

* Sun Mar 31 2002 Elliot Lee <sopwith@redhat.com> 2.6-1
- Don't trust homebaked tempdir creation - always use mktemp.

* Thu Mar 28 2002 Elliot Lee <sopwith@redhat.com> 2.5-4
- Fix the /tmp race for real
- Merge changes from both spec files.

* Thu Mar 28 2002 Kirk Bauer <kirk@kaybee.org> 2.5-2
- Updated new changes from Red Hat's rawhide packaging

* Tue Sep 04 2001 Elliot Lee <sopwith@redhat.com> 2.1.1-3
- Fix #53077

* Thu Aug 09 2001 Elliot Lee <sopwith@redhat.com> 2.1.1-2
- Fix warning in services/init (#51305) and don't include fortune module 
(#51093).

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- updated to 2.1.1
- adapted changes from Kirk Bauer's spec file into this one

* Sat Aug 5 2000 Tim Powers <timp@redhat.com>
- fix bug #15478, spelling error in the description

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man page location to be FHS compliant
- use predefined RPM macros whenever possible

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Mon Jul 19 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Thu Apr 15 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated source

* Wed Nov 18 1998 Kirk Bauer <kirk@kaybee.org>
- Modified to comply with RHCN standards

* Fri Oct 2 1998 Michael Maher <mike@redhat.com>
- built package

* Sun Feb 23 1998 Kirk Bauer <kirk@kaybee.org>
- Minor changes and addition of man-page

* Sun Feb 22 1998 Kirk Bauer <kirk@kaybee.org>
- initial release
