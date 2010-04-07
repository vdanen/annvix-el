#
# spec file for package runit
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	name		runit
%define	version		2.1.1
%define	release		2%{?dist}%{?rescue_rel}

%define aver		0.20

%define _runitddir      %{_sysconfdir}/runit.d
%define _srvdir         %{_var}/service

%define logger_uid      67
%define logger_gid      67

%define use_init        1
%define use_upstart     0

Summary:	A UN*X init scheme with service supervision
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
URL:		http://smarden.org/runit/
Source0:	http://smarden.org/runit/%{name}-%{version}.tar.gz
# available from http://annvix.org/cg-bin/viewcvs.cgi/tools/runit/
Source1:	annvix-runit-%{aver}.tar.bz2
Source2:        upstart-runsvdir.conf
Patch0:		runit-1.3.1-avx-localtime.patch
Patch1:		runit-1.6.0-avx-svlogd_perms.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.28

Requires:	SysVinit >= 2.85-7avx
Requires:	initscripts
Requires:	srv
Requires:	mingetty
Requires:	execline
Requires:	ipsvd
Requires:	psmisc
Requires:       /sbin/nologin
%if %{use_upstart}
Requires:       upstart
%endif

%description
runit is a daemontools-like replacement for SysV-init and other
init schemes.  It currently runs on GNU/Linux, OpenBSD, FreeBSD,
and can easily be adapted to other Unix operating systems.  runit
implements a simple three-stage concept.  Stage 1 performs the
system's one-time initialization tasks.  Stage 2 starts the
system's uptime services (via the runsvdir program).  Stage 3
handles the tasks necessary to shutdown and halt or reboot. 


%prep
%setup -q -n admin -a 1
pushd %{name}-%{version}
%patch0 -p1 -b .localtime
%patch1 -p1 -b .svlogd_perms
popd


%build
COMP="diet gcc"
pushd %{name}-%{version}/src
    echo "$COMP -Os -pipe" > conf-cc
    echo "$COMP -Os -static -s" > conf-ld
    make
    # we really need to keep svwait*
    make svwaitup
    make svwaitdown
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/{service,sbin,%{_mandir}/man8}

pushd %{name}-%{version}
    for i in `cat package/commands` svwaitup svwaitdown; do
	install -m 0755 src/$i %{buildroot}/sbin/
    done
popd

pushd annvix-runit-%{aver}
    make DESTDIR=%{buildroot} install
popd

install -m 0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/

%if %{use_upstart}
mkdir -p %{buildroot}%{_sysconfdir}/event.d
install %{SOURCE2} %{buildroot}%{_sysconfdir}/event.d/runsvdir.conf
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
# create logger user
/usr/sbin/useradd -c "runit logger" -u %{logger_uid} \
        -s /sbin/nologin -r -d /var/log/supervise logger 2> /dev/null || :

# in order for runit to properly handle our reboot/halt signals, we need to
# make a copy of runit, but the inode must remain identical so we do this by
# making a hard link of runit; we check for and delete the old file before
# making a new link so we can delete if we need to, but runit stage 1 should
# always delete this file when a system starts and it's found (thanks Gerrit
# for the help on this one!)
if [ -f /sbin/runit ]; then
    pushd /sbin >/dev/null 2>&1
        [ -f /sbin/runit.old ] && rm -f /sbin/runit.old
        ln /sbin/runit /sbin/runit.old
    popd >/dev/null 2>&1
fi


%post
%if %{use_init}
if [ $1 == "1" ]; then
    # new install requires changes to inittab
    if [ "$(grep -q runit /etc/inittab; echo $?)" == "1" ]; then
        echo "SV:123456:respawn:/etc/runit/2" >>/etc/inittab
        /sbin/init q
    fi
fi
%endif
%if %{use_upstart}
if [ $1 == "1" ]; then
    /sbin/start runsvdir
fi
%endif


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/package/THANKS
%doc %{name}-%{version}/doc/*.html
%doc %{name}-%{version}/etc/2
%doc %{name}-%{version}/etc/debian
%dir %attr(0750,root,wheel) %{_runitddir}
%attr(0700,root,root) /sbin/runit
%attr(0700,root,root) /sbin/runit-init
%attr(0755,root,root) /sbin/runsv
%attr(0755,root,root) /sbin/runsvdir
%attr(0755,root,root) /sbin/runsvchdir
%attr(0755,root,root) /sbin/sv
%attr(0755,root,root) /sbin/svlogd
%attr(0755,root,root) /sbin/svwaitup
%attr(0755,root,root) /sbin/svwaitdown
%attr(0755,root,root) /sbin/chpst
%attr(0755,root,root) /sbin/utmpset
%attr(0700,root,root) /sbin/rc
%attr(0700,root,root) /sbin/rc-update
%attr(0700,root,root) /sbin/convert-envdir
%attr(0644,root,root) %{_mandir}/man8/*.8*
%if %{use_upstart}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/event.d/runsvdir.conf
%endif
%attr(0700,root,root) %dir %{_sysconfdir}/runit
%attr(0700,root,root) %{_sysconfdir}/runit/1
%attr(0700,root,root) %{_sysconfdir}/runit/2
%attr(0700,root,root) %{_sysconfdir}/runit/3
%attr(0700,root,root) %{_sysconfdir}/runit/ctrlaltdel
%attr(0750,root,root) %dir %{_sysconfdir}/sysconfig/env/clock
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/clock/UTC
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/clock/ZONE
%attr(0750,root,root) %dir %{_sysconfdir}/sysconfig/env/network
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/network/GATEWAY
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/network/HOSTNAME
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/network/NETWORKING
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/usb/USB
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/usb/MOUSE
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/usb/KEYBOARD
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/usb/PRINTER
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/usb/STORAGE
%dir %attr(0750,root,root) %{_srvdir}
%dir %attr(0750,root,root) /service
%{_srvdir}/*
%dir %attr(0750,root,root) %{_sysconfdir}/sysconfig/env/runit
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/runit/STAGE_3_TIMEOUT
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/runit/GETTY_TIMEOUT
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/env/runit/CTRLALTDEL_TIMEOUT
%attr(0750,root,root) %{_runitddir}/rc.functions.sh
%attr(0750,root,root) %config(noreplace) %{_runitddir}/rc.local
%attr(0750,root,root) %config(noreplace) %{_runitddir}/rc.local-stop
%attr(0750,root,root) %{_runitddir}/consmap.sh
%attr(0750,root,root) %{_runitddir}/netfs
%attr(0750,root,root) %{_runitddir}/network
%attr(0750,root,root) %{_runitddir}/usb
%dir %attr(0750,root,root) %{_sysconfdir}/runlevels/default
%dir %attr(0750,root,root) %{_sysconfdir}/runlevels/default/service
%dir %attr(0750,root,root) %{_sysconfdir}/runlevels/single
%dir %attr(0750,root,root) %{_sysconfdir}/runlevels/single/service


%changelog
* Wed Apr 7 2010 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- use group wheel, not admin (group admin does not exist, wheel is the
  closest to it)

* Wed Apr 7 2010 Vincent Danen <vdanen-at-build.annvix.org> 2.1.1
- 2.1.1
- create logger user (static uid/gid: 67)
- requires /sbin/nologin
- handle modifications to inittab (%%use_init) or adding upstart config file
  (%%use_upstart), so that it will work with existing SysVinit or upstart

* Sun Apr 19 2009 Vincent Danen <vdanen-at-build.annvix.org> 2.0.0
- 2.0.0

* Sun Apr 19 2009 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0
- overhaul to install initscripts in /etc/runit.d/ and the annvix-runit
  install comes from itself, not the spec
- package contains all runscripts now
- install /sbin/runit-init again so can co-exist with SysVinit
- annvix-runit 0.20

* Fri Mar 07 2008 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0
- fix perms on initscripts (bug #64)

* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0
- annvix-runit 0.18

* Wed Dec 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0
- annvix-runit 0.17

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.8.0
- runit 1.8.0
- annvix-runit 0.16

* Sat Mar 31 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- annvix-runit 0.15

* Sun Jan 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- annvix-runit 0.14

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- annvix-runit 0.13
- fix requires

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- annvix-runit 0.12

* Tue Jan 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- annvix-runit 0.11

* Sat Nov 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.2
- 1.7.2
- reinclude svwaitup and svwaitdown; these are essential to our run
  scripts that deal with dependencies

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.1
- fix the usb initscript

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.1
- 1.7.1
- annvix-runit 0.10

* Mon Oct 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- add the %%_{post,preun}_service macros for network and netfs

* Sat Oct 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- fix the usb initscript

* Sat Oct 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- rc: don't disable modprobe loading by default as it breaks shorewall

* Fri Oct 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- we also need to populate the default runlevel a bit

* Fri Oct 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- rc: if runlevel doesn't exist, set it to default
- move /service upon removal of chkconfig (the installer does things right,
  but upgrades need to be handled)

* Fri Oct 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- fix the perms of consmap.sh (should be 0755 not 0700)

* Fri Oct 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- we need more than just an obsoletes so add a trigger to get rid of
  some chkconfig-related files that interfere with our proper operation

* Tue Oct 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- add an obsoletes on chkconfig; we can't provide it tho

* Tue Oct 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- don't include /service (it's now a symlink from to the appropriate
  service directory for the runlevel)
- include the service directories for each default runlevel
- on fresh installs setup mingetty services in both the default and
  single runlevels
- annvix-runit 0.9 (full support for runlevel-based service directories)
- drop P2; stage 3 now silences sv's output for us so we don't need it

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- update P2 as per some of Sean's suggestions for the quiet mode

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- annvix-runit 0.8 (minor fixes)

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- annvix-runit 0.7 (lots of changes)

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- we now have our own initscripts here rather than in the initscripts package
- set NETWORKING=yes by default
- add rc.local here
- add the USB config files here

* Thu Oct 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- updated tarball to get some stage{1,3} fixes and an /sbin/rc fix
  to not mount filesystems marked auto

* Tue Oct 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.0
- 1.7.0
- fix source url
- put rc.functions.sh in the right place

* Sun Oct 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.0
- with the new srv, we can drop runsvctrl, runsvstat, svwaitdown, and
  svwaitup
- include the new rc script and friends
- Requires: psmisc (rc needs fuser)
- P1: make the log perms 0640 and 0740 rather than 0644 and 0744
- P2: add a -q switch to sv (quiet mode)

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.0
- 1.6.0
- S2-S4: include the manpages for runsvctrl, runsvstatus, svwaitdown,
  and svwaitup as they're no longer included -- this means we really
  need to update srv to work with newer runit
- add -doc subpackage
- rebuild with gcc4

* Thu Mar 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.1
- 1.4.1
- runsvctrl, runsvstat, svwaitdown, and svwaitup are no longer built per
  default but we still need them for srv, so force a build/install

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- need to ln /sbin/runit, not /sbin/init for the reboot to work
- annvix-runit 0.5:
  - remove /sbin/runit.old in stage 1 if we find it

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- revert the copy; it made no difference (either with cp or ln)

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- annvix-runit 0.4:
  - set /etc/sysconfig/env/tcpsvd/HOSTNAME on boot
- try to fix our lack of reboot on upgrade issue

* Tue Jan 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3
- 1.3.3

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- re-enable dietlibc build on x86_64; have to specify the explicit
  arch'd compiler to use for it to work properly

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc doesn't like us on x86_64

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-6avx
- don't use srv to bring up the mingetty services (in case we're in install mode)

* Sat Oct 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-5avx
- fix the ctrl-alt-del scripts so it reboots rather than halts

* Mon Sep 05 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.3.1-4avx
- added ipsvd as a dependency now we are utilizing it more for services.

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-3avx
- stage 1, 2, 3, and ctrlaltdel scripts are in execlineb format (re: spt)
- run scripts are now considered config files and are not replaceable
- env/runit/TIMEOUT is a config file too
- update P0 to note in svlogd.8 that we are logging in local time and
  not UTC
- add CTRLALTDEL_TIMEOUT to control timeout for ctrlaltdel (duh) and
  GETTY_TIMEOUT to control the timeout for getties

* Mon Aug 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-2avx
- added /etc/sysconfig/env/runit/TIMEOUT to control the delay for
  shutdowns (default is 180 seconds)
- P0: log in local time rather than UTC

* Mon Aug 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1-1avx
- 1.3.1

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.0-2avx
- fix perms on run scripts

* Wed Aug 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.0-1avx
- 1.3.0
- Requires: execline
- new tarball from cvs (tools/runit) for runit scripts
- change run script ownership to root:admin and mode 0740
- make runit and init mode 0700

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-8avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-7avx
- note the time we're waiting for service shutdowns (re: Sean Thomas)
- fix changelog entries

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-6avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-5avx
- instead of waiting 350secs for all services to stop, we wait
  180secs; this is because logged in ssh users will cause this
  timeout as sshd will not die with any children running.  3
  minutes is more than reasonable

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-4avx
- build against new dietlibc

* Tue Jan 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-3avx
- build without dietlibc
- remove BuildRequires: dietlibc; add BuildRequires: glibc-static-devel

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-2avx
- rebuild against fixed dietlibc

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1-1avx
- 1.2.1
- don't set -march=pentium anymore

* Wed Oct 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.5-1avx
- 1.0.5

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-6avx
- own /service since daemontools will soon be removed

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-5avx
- don't ever restart the gettys
- Requires: mingetty

* Sat Sep 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-4avx
- dammit... works good if you install from remote, but kicks you off your vc
  if you're local, so don't automatically add tty1; the installer will take
  care of this for new installs

* Sat Sep 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-3avx
- somewhat ugly means of getting the getty's up and running for the
  reboot, but necessary as %%_post_srv only checks to restart a service
  and doesn't set one up or make it ready to start

* Sat Sep 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-2avx
- Conflicts: SysVinit <= 2.85-6avx (7avx moves init to init.srv)
- Requires SysVinit >= 2.86-7avx, initscripts, srv

* Sat Sep 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4-1avx
- first Annvix build
- S1: runit scripts

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
