#
# spec file for package srv
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		srv
%define version 	0.27.1
%define release 	1%{?dist}%{?rescue_rel}

%define _srvdir         %{_var}/service

Summary:	Tool to manage runsv-controlled services
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System Environment/Base
URL:		http://annvix.org/viewvc/tools/srv/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel

Requires:	runit >= 1.5.0

%description
A tool to manage runsv-controlled services.


%prep
%setup -q


%build
diet gcc -Os -pipe nothing.c -o nothing


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{/sbin,%{_bindir},%{_sbindir},%{_mandir}/man8,%{_datadir}/srv}
install -m 0700 srv %{buildroot}%{_sbindir}
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8
install -m 0755 nothing %{buildroot}%{_bindir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/srv
%{_bindir}/nothing
%{_mandir}/man8/srv.8*


%changelog
* Sat Apr 18 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.27.1
- first build for CentOS/RHEL 5
- fix URL

* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.27.1
- 0.27.1

* Mon Nov 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.27
- 0.27

* Tue Jul 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.26.2
- 0.26.2: fixes bug #47

* Sat Jan 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.26.1
- 0.26.1
  - don't exit if a service is available but stopped on --restart

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.26
- 0.26
  - adds --reload (restart via HUP) and changes --restart to do a full
    stop then start
  - -h is no longer for --help, but for --reload

* Tue Aug 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.25
- 0.25
  - use /sbin/sv rather than runsv* programs since runit no longer
    provides them via default
  - requires runit 1.5.0 or higher

* Wed Feb 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24
- 0.24
  - explicitly use /bin/bash
  - fix wrong fuzz application of sean's patch for rebuilding cdb files
  - add support to manipulate envdir settings (-e/--env) (spt)

* Tue Feb 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.23
- 0.23
  - create cdb file on add if it doesn't exist and to rebuild the cdb file
    if --peers command is given (spt)
  - remove the down file before adding service and also creates the file
    when looping is encountered.  This will protect against the service
    looping when reboot (spt)

* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.22
- 0.22
  - drop the packaged rpm spec file
  - make --restart send a HUP rather than stop/start (spt)
  - make --restart forceable (send KILL) (spt)
  - added a sysnotice facility that only logs to syslog but not the console
  - fixed status messages so you can see what is happening before you see
    the dots indicating it is doing something
  - refactor the code somewhat for readability
  - don't log the output of --info to syslog
  - add serror and sfatal facilities that are exactly the same as error and
    fatal but do not log to syslog; modified a lot of error strings to use
    the new facilities
  - put error messages below usage() so the last thing seen is the error
    message

* Sun Jan 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.21
- 0.21: properly manage the down file to save state across reboots

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.20
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-3avx
- don't display rpm package info if the run file doesn't belong to an rpm
- some --info tidying

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-2avx
- cosmetics and change the timeouts from 15s to 10s

* Mon Oct 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.20-1avx
- 0.20

* Fri Aug 26 2005 Sean P. Thomas <spt-at-build.annvix.org> 0.10-1avx
- 0.10

* Mon Aug 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9-5avx
- remove the srv-start and srv-stop scripts; they should never be used
- srv should be mode 0700 not 0755
- use dietlibc to compile nothing

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9-4avx
- bootstrap build

* Wed Oct 06 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-3avx
- add %%{_datadir}/srv/exceptions so we can have more services for
  process killing exceptions than just sshd; so far we have both
  sshd and mysqld here

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-2avx
- add godown() function for a service to shut itself down if certain
  requirements (usually configuration-related) are not met

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9-1avx
- 0.9
- overhaul srv to work with runit (runsv) rather than daemontools (supervise);
  this can use more work but this should be a sufficient transition for now

* Thu Aug 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.7-2avx
- make srv *not* kill "rogue" sshd processes as that makes remote
  upgrades of sshd impossible

* Tue Jul 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.7-1avx
- remove srv-addinit and %%post scriptlet to add it to inittab; it's now
  done in initscripts
- add logging support to srv (logs to daemon.info)
- add external functions for run scripts to use (logging and to check
  for dependencies)
- add a final "super kill" for processes that fork and supervise can't
  kill (ie. smbd)

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.6-2avx
- fix really bad and stupid typeo in srv-stop
- give some feedback on starting and stopping supervise

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.6-1avx
- numerous fixes; there was some bad bash going on (this solves
  the problem with every service taking 15s to shutdown, they should
  be instant now)
- it is prefered to run svscan from init so that it can be restarted
  should something happen, so the initscript is gone
- don't remove the build directory by default
- move most of the files in %%{_bindir} to %%{_sbindir} because only
  root can really do anything with services

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.5-2avx
- Annvix build

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 0.5-1sls
- 0.5:
  - nice overall status summary
  - fixed the handling of services that don't come with a log service

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.4-2sls
- fix from Oden to handle restarts better

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.4-1sls
- 0.4
- include Bruce's supervise-scripts (3.3)

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 0.3-2sls
- include nothing

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 0.3-1sls
- 0.3

* Tue Jan 13 2004 Vincent Danen <vdanen@opensls.org> 0.2-1sls
- 0.2

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- PreReq: rpm-helper
- add %%post and %%preun service stuff

* Fri Jan 02 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
