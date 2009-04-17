#
# spec file for package ipsvd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	name		ipsvd
%define	version		0.13.0
%define	release         1%{?dist}%{?rescue_rel}	

Summary:	Internet protocol service daemons
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Servers
URL:		http://smarden.org/ipsvd/
Source0:	http://smarden.org/ipsvd/%{name}-%{version}.tar.gz
Patch0:		ipsvd-0.13.0-avx-system_matrixssl.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.27-2avx
BuildRequires:	matrixssl-devel >= 1.2.2-3avx

Requires(pre):	setup

%description
ipsvd is a set of internet protocol service daemons for Unix. It 
currently includes a TCP/IP service daemon, and a UDP/IP service 
daemon. 

An internet protocol service (ipsv) daemon waits for incoming 
connections on a local socket; for new connections, it conditionally 
runs an arbitrary program with standard input reading from the 
socket, and standard output writing to the socket (if connected), 
to handle the connection. Standard error is used for logging. 

ipsv daemons can be told to read and follow pre-defined instructions 
on how to handle incoming connections; based on the client's IP 
address or hostname, they can run different programs, set a different 
environment, deny a connection, or set a per host concurrency limit. 

On Linux the network connection optionally can be encrypted using 
SSLv3. 

Normally the ipsv daemons are run by a supervisor process, such as 
runsv from the runit package, or supervise from the daemontools 
package. 

ipsvd can be used to run services normally run by inetd, xinetd, or 
tcpserver. 


%prep
%setup -q -n net
pushd %{name}-%{version}
%patch0 -p2
popd


%build
COMP="diet gcc"

pushd %{name}-%{version}/src
    MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
    perl -pi -e "s|{ARCH}|${MYARCH}|g" Makefile
    echo "$COMP -Os -pipe -nostdinc" > conf-cc
    echo "$COMP -Os -static -s -nostdinc" > conf-ld
    make
    make sslsvd
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/sbin/
install -d %{buildroot}%{_mandir}/man{5,7,8}

pushd %{name}-%{version}
    for i in ipsvd-cdb sslio tcpsvd udpsvd sslsvd; do
	install -m 0755 src/$i %{buildroot}/sbin/
    done
popd

install -m 0644 %{name}-%{version}/man/*.5 %{buildroot}%{_mandir}/man5/
install -m 0644 %{name}-%{version}/man/*.7 %{buildroot}%{_mandir}/man7/
install -m 0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/

# make the default tcpsvd environment
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd
echo "localhost" >%{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd/HOSTNAME
echo "0" >%{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd/IP
echo "20" >%{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd/MAX_CONN
echo "5" >%{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd/MAX_PER_HOST
echo "20" >%{buildroot}%{_sysconfdir}/sysconfig/env/tcpsvd/MAX_BACKLOG


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
%dir %{_sysconfdir}/sysconfig/env/tcpsvd
%attr(0640,root,admin) %config(noreplace) %{_sysconfdir}/sysconfig/env/tcpsvd/HOSTNAME
%attr(0640,root,admin) %config(noreplace) %{_sysconfdir}/sysconfig/env/tcpsvd/IP
%attr(0640,root,admin) %config(noreplace) %{_sysconfdir}/sysconfig/env/tcpsvd/MAX_CONN
%attr(0640,root,admin) %config(noreplace) %{_sysconfdir}/sysconfig/env/tcpsvd/MAX_PER_HOST
%attr(0640,root,admin) %config(noreplace) %{_sysconfdir}/sysconfig/env/tcpsvd/MAX_BACKLOG
%attr(0755,root,root) /sbin/ipsvd-cdb
%attr(0755,root,root) /sbin/sslio
%attr(0755,root,root) /sbin/sslsvd
%attr(0755,root,root) /sbin/tcpsvd
%attr(0755,root,root) /sbin/udpsvd
%attr(0644,root,root) %{_mandir}/man5/ipsvd-instruct.5*
%attr(0644,root,root) %{_mandir}/man7/ipsvd.7*
%attr(0644,root,root) %{_mandir}/man8/sslio.8*
%attr(0644,root,root) %{_mandir}/man8/sslsvd.8*
%attr(0644,root,root) %{_mandir}/man8/udpsvd.8*
%attr(0644,root,root) %{_mandir}/man8/ipsvd-cdb.8*
%attr(0644,root,root) %{_mandir}/man8/tcpsvd.8*


%changelog
* Fri Apr 17 2009 Vincent Danen <vdanen-at-build.annvix.org> 0.13.0
- first build for CentOS/RHEL 5

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.13.0
- 0.13.0
- rediff P0

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12.1
- 0.12.1
- build against new matrixssl
- rediff P0

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12.0
- add -doc subpackage
- rebuild with gcc4
- rebuild against new matrixssl

* Sat Feb 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12.0
- Requires(pre): setup because during install ipsvd ends up being
  installed prior to setup and our admin ownerships don't get properly
  set

* Fri Feb 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12.0
- 0.12.0
- rediff P0

* Tue Jan 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11.1
- 0.11.1
- rediff P0

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11.0
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11.0
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11.0
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11.0-2avx
- add /etc/sysconfig/env/tcpsvd with defaults for tcpsvd services

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11.0-1avx
- 0.11.0
- rebuild against new matrixssl
- merge P0 and P1 and update it to work with the new matrixssl

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10.1-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10.1-3avx
- rebuild

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10.1-2avx
- rebuild against new dietlibc

* Thu Jan 20 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10.1-1avx
- 0.10.0
- take an updated P0 from mdk but fix it
- require a newer matrixssl and dietlibc


* Wed Oct 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-2avx
- build against newer matrixssl (1.2.2)

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.6-1avx
- first Annvix build; to eventually replace ucspi-tcp

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
