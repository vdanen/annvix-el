#
# spec file for package dansguardian
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define name		dansguardian
%define version		2.10.1.1
%define release		1%{?dist}%{?rescue_rel}

Summary:	A content filtering web proxy
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System Environment/Daemons
URL:		http://www.dansguardian.org
Source0:	http://www.dansguardian.org/downloads/2/dansguardian-%{version}.tar.gz
Source1:	dansguardian.init
Source2:	languages.tar.bz2
Source3:        dansguardian-http.conf
Patch0:		dansguardian-mdv_conf.diff
Patch1: 	dansguardian-2.10.0.3-gcc44.patch
BuildRequires:	zlib-devel
BuildRequires:	pcre-devel
BuildRequires:	gcc-c++
Requires:	smtpdaemon
Requires(post): chkconfig >= 0.9, /sbin/service
Requires(pre):	/usr/sbin/useradd
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
DansGuardian is a filtering proxy for Linux, FreeBSD, OpenBSD and Solaris.
It filters using multiple methods. These methods include URL and domain
filtering, content phrase filtering, PICS filtering, MIME filtering, file
extension filtering, POST filtering.

The content phrase filtering will check for pages that contain profanities
and phrases often associated with pornography and other undesirable content.
The POST filtering allows you to block or limit web upload.  The URL and
domain filtering is able to handle huge lists and is significantly faster
than squidGuard.

The filtering has configurable domain, user and ip exception lists.
SSL Tunneling is supported.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

cp %{SOURCE1} %{name}.init

# fix path to the ipc files
perl -pi -e "s|\@localstatedir\@|/var/lib|g" %{name}.init

# mdv design
pushd data
    tar -jxf %{SOURCE2}
popd


%build
%configure \
    --localstatedir=/var/lib \
    --enable-pcre=yes \
    --enable-clamav=no \
    --enable-clamd=yes \
    --enable-icap=yes \
    --enable-kavd=no \
    --enable-commandline=yes \
    --enable-fancydm=yes \
    --enable-trickledm=yes \
    --enable-ntlm=yes \
    --enable-email=yes \
    --enable-orig-ip=yes \
    --with-proxyuser=%{name} \
    --with-proxygroup=%{name} \
    --with-piddir=/var/run/ \
    --with-logdir=/var/log/%{name} \
    --with-sysconfsubdir=%{name} \
    --datadir=%{_sysconfdir}

make


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/{logrotate.d,httpd/conf.d}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/www/%{name}
install -d %{buildroot}/var/lib/%{name}/tmp

make install DESTDIR=%{buildroot}

# cleanup
rm -rf %{buildroot}%{_datadir}/doc/dansguardian*
rm -rf %{buildroot}%{_sysconfdir}/%{name}/scripts

install -m 0755 %{name}.init %{buildroot}%{_initrddir}/%{name}
install -m 0755 data/dansguardian.pl %{buildroot}/var/www/%{name}/
install -m 0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

cat << EOF > %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
/var/log/%{name}/access.log {
    create 644 %{name} %{name}
    rotate 5
    weekly
    sharedscripts
    prerotate
 	service %{name} stop >/dev/null 2>&1
    endscript
    postrotate
	service %{name} start >/dev/null 2>&1
    endscript
}
EOF

# make sure this file is present
echo "localhost" >> %{buildroot}%{_sysconfdir}/%{name}/lists/exceptionfileurllist

# construct file lists
find %{buildroot}%{_sysconfdir}/%{name} -type d | \
    sed -e "s|%{buildroot}||" | sed -e 's/^/%attr(0755,root,root) %dir /' > %{name}.filelist

find %{buildroot}%{_sysconfdir}/%{name} -type f | grep -v "\.orig" | \
    sed -e "s|%{buildroot}||" | sed -e 's/^/%attr(0644,root,root) %config(noreplace) /' >> %{name}.filelist


%pre
/usr/sbin/useradd -c "System user for Dansguardian" -s /sbin/nologin -r -d /var/lib/%{name} %{name} 2>/dev/null || :


%post
/sbin/chkconfig --add %{name}


%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi


%postun
/sbin/service %{name} condrestart >/dev/null 2>&1 || :


%clean
rm -rf %{buildroot}


%files -f %{name}.filelist
%defattr(-,root,root)
%doc AUTHORS COPYING README
%doc doc/AuthPlugins doc/ContentScanners doc/DownloadManagers
%doc doc/FAQ doc/FAQ.html doc/Plugins
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%dir %attr(0755,root,root) /var/www/%{name}
%attr(0755,root,root) /var/www/%{name}/%{name}.pl
%attr(0644,root,root) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(0755,%{name},%{name}) /var/log/%{name}
%dir %attr(0755,%{name},%{name}) /var/lib/%{name}
%dir %attr(0755,%{name},%{name}) /var/lib/%{name}/tmp
%attr(0644,root,root) %{_mandir}/man8/*


%changelog
* Sat Jul 25 2009 Vincent Danen <vdanen-at-build.annvix.org> 2.10.1-1.el5.avx
- first Annvix build based on Mandriva's 2.10.1.1-1mdv2010.0 for CentOS/RHEL 5
- put stuff from /usr/share/dansguardian/ into /etc/dansguardian/
- put the pid file in /var/run, not /var/run/dansguardian
- put the cgi script in /var/www/dansguardian, not /var/www/cgi-bin/
- add a httpd/conf.d/dansguardian.conf as in the rpmforge package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
