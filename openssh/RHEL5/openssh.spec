#
# spec file for package openssh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

# Do we want SELinux & Audit

%define WITH_SELINUX 1

# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 0

# Do we want to link against a static libcrypto? (1=yes 0=no)
%define static_libcrypto 0

# Do we want smartcard support (1=yes 0=no)
%define scard 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%define gtk2 1

# Build position-independent executables (requires toolchain support)?
%define pie 1

# Do we want kerberos5 support (1=yes 0=no)
%define kerberos5 1

# Do we want libedit support
%define libedit 0

# Do we want NSS tokens support
%define nss 1

# Whether or not /sbin/nologin exists.
%define nologin 1

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_gnome_askpass:%define no_gnome_askpass 1}

# Add option to build without GTK2 for older platforms with only GTK+.
# Red Hat Linux <= 7.2 and Red Hat Advanced Server 2.1 are examples.
# rpm -ba|--rebuild --define 'no_gtk2 1'
%{?no_gtk2:%define gtk2 0}

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%define static_libcrypto 1}

# Options for Smartcard support: (needs libsectok and openssl-engine)
# rpm -ba|--rebuild --define "smartcard 1"
%{?smartcard:%define scard 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%define rescue 1}
%{?build_rescue:%define rescue_rel rescue}

# Turn off some stuff for resuce builds
%if %{rescue}
%define kerberos5 0
%define libedit 0
%endif

Summary: The OpenSSH implementation of SSH protocol versions 1 and 2
Name: openssh
Version: 5.3p1
Release: 1%{?dist}%{?rescue_rel}
URL: http://www.openssh.com/portable.html
#Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
#Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
# This package differs from the upstream OpenSSH tarball in that
# the ACSS cipher is removed by running openssh-nukeacss.sh in
# the unpacked source directory.
Source0: openssh-%{version}-noacss.tar.bz2
Source1: openssh-nukeacss.sh
Source2: sshd.pam
Source3: sshd.init
Patch0: openssh-5.2p1-redhat.patch
Patch2: openssh-5.3p1-skip-initial.patch
Patch4: openssh-5.2p1-vendor.patch
Patch12: openssh-5.2p1-selinux.patch
Patch13: openssh-5.1p1-mls.patch
Patch16: openssh-5.3p1-audit.patch
Patch17: openssh-4.3p2-cve-2007-3102.patch
Patch18: openssh-5.0p1-pam_selinux.patch
Patch22: openssh-3.9p1-askpass-keep-above.patch
Patch24: openssh-4.3p1-fromto-remote.patch
Patch27: openssh-5.1p1-log-in-chroot.patch
Patch30: openssh-4.0p1-exit-deadlock.patch
Patch35: openssh-5.1p1-askpass-progress.patch
Patch38: openssh-4.3p2-askpass-grab-info.patch
Patch39: openssh-4.3p2-no-v6only.patch
Patch44: openssh-4.3p2-allow-ip-opts.patch
Patch49: openssh-4.3p2-gssapi-canohost.patch
Patch51: openssh-5.2p1-nss-keys.patch
Patch54: openssh-5.1p1-gssapi-role.patch
Patch55: openssh-5.1p1-cloexec.patch
Patch62: openssh-5.1p1-scp-manpage.patch

License: BSD
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{nologin}
Requires: /sbin/nologin
%endif

Requires: initscripts >= 5.20

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if %{scard}
BuildRequires: sharutils
%endif
BuildRequires: autoconf, automake, openssl-devel, perl, zlib-devel
BuildRequires: audit-libs-devel
BuildRequires: util-linux, groff, man
BuildRequires: pam-devel
BuildRequires: tcp_wrappers

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{nss}
BuildRequires: nss-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 1.27.7
BuildRequires: libselinux-devel >= 1.27.7
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth

%package clients
Summary: The OpenSSH client applications
Requires: openssh = %{version}-%{release}
Group: Applications/Internet

%package server
Summary: The OpenSSH server daemon
Group: System Environment/Daemons
Requires: openssh = %{version}-%{release}
Requires(post): chkconfig >= 0.9, /sbin/service
Requires(pre): /usr/sbin/useradd
#Requires: pam >= 1.0.1-3

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to separate libraries.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.
You'll also need to install the openssh package on OpenSSH clients.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server. You also need to have the openssh
package installed.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%prep
%setup -q
%patch0 -p1 -b .redhat
%patch2 -p1 -b .skip-initial
%patch4 -p1 -b .vendor

%if %{WITH_SELINUX}
#SELinux
%patch12 -p1 -b .selinux
%patch13 -p1 -b .mls
%patch16 -p1 -b .audit
%patch17 -p1 -b .inject-fix
%patch18 -p1 -b .pam_selinux
%endif

%patch22 -p1 -b .keep-above
%patch24 -p1 -b .fromto-remote
%patch27 -p1 -b .log-chroot
%patch30 -p1 -b .exit-deadlock
%patch35 -p1 -b .progress
%patch38 -p1 -b .grab-info
%patch39 -p1 -b .no-v6only
%patch44 -p1 -b .ip-opts
%patch49 -p1 -b .canohost
%patch51 -p1 -b .nss-keys
%patch54 -p1 -b .gssapi-role
%patch55 -p1 -b .cloexec
%patch62 -p1 -b .manpage

autoreconf

%build
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%if %{rescue}
CFLAGS="$CFLAGS -Os"
%endif
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIE"
%else
CFLAGS="$CFLAGS -fpie"
%endif
export CFLAGS
LDFLAGS="$LDFLAGS -pie"; export LDFLAGS
%endif
%if %{kerberos5}
source /etc/profile.d/krb5-devel.sh
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-tcp-wrappers \
	--with-rsh=%{_bindir}/rsh \
	--with-default-path=/usr/local/bin:/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--enable-vendor-patchlevel="FC-%{version}-%{release}" \
	--disable-strip \
	--without-zlib-version-check \
%if %{nss}
	--with-nss \
%endif
%if %{scard}
	--with-smartcard \
%endif
%if %{rescue}
	--without-pam \
%else
	--with-pam \
%endif
%if %{WITH_SELINUX}
	--with-selinux --with-linux-audit \
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

make

# Define a variable to toggle gnome1/gtk2 building.  This is necessary
# because RPM doesn't handle nested %if statements.
%if %{gtk2}
	gtk2=yes
%else
	gtk2=no
%endif

%if ! %{no_gnome_askpass}
pushd contrib
if [ $gtk2 = yes ] ; then
	make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
else
	make gnome-ssh-askpass1
	mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%if ! %{no_gnome_askpass}
install -s contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{scard}
	rm -f $RPM_BUILD_ROOT%{_datadir}/openssh/Ssh.bin
%endif

%if ! %{no_gnome_askpass}
ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

%if %{no_gnome_askpass}
rm -f $RPM_BUILD_ROOT/etc/profile.d/gnome-ssh-askpass.*
%endif

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

rm -f README.nss.nss-keys
%if ! %{nss}
rm -f README.nss
%endif
%clean
rm -rf $RPM_BUILD_ROOT

%triggerun server -- ssh-server
if [ "$1" != 0 -a -r /var/run/sshd.pid ] ; then
	touch /var/run/sshd.restart
fi

%triggerun server -- openssh-server < 2.5.0p1
# Count the number of HostKey and HostDsaKey statements we have.
gawk	'BEGIN {IGNORECASE=1}
	 /^hostkey/ || /^hostdsakey/ {sawhostkey = sawhostkey + 1}
	 END {exit sawhostkey}' /etc/ssh/sshd_config
# And if we only found one, we know the client was relying on the old default
# behavior, which loaded the the SSH2 DSA host key when HostDsaKey wasn't
# specified.  Now that HostKey is used for both SSH1 and SSH2 keys, specifying
# one nullifies the default, which would have loaded both.
if [ $? -eq 1 ] ; then
	echo HostKey /etc/ssh/ssh_host_rsa_key >> /etc/ssh/sshd_config
	echo HostKey /etc/ssh/ssh_host_dsa_key >> /etc/ssh/sshd_config
fi

%triggerpostun server -- ssh-server
if [ "$1" != 0 ] ; then
	/sbin/chkconfig --add sshd
	if test -f /var/run/sshd.restart ; then
		rm -f /var/run/sshd.restart
		/sbin/service sshd start > /dev/null 2>&1 || :
	fi
fi

%pre server
%if %{nologin}
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
%else
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /dev/null -r -d /var/empty/sshd sshd 2> /dev/null || :
%endif

%post server
/sbin/chkconfig --add sshd

%postun server
/sbin/service sshd condrestart > /dev/null 2>&1 || :

%preun server
if [ "$1" = 0 ]
then
	/sbin/service sshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del sshd
fi

%files
%defattr(-,root,root)
%doc CREDITS ChangeLog INSTALL LICENCE OVERVIEW PROTOCOL* README* TODO WARNING*
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(4755,root,root) %{_libexecdir}/openssh/ssh-keysign
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%endif
%if %{scard}
%attr(0755,root,root) %dir %{_datadir}/openssh
%attr(0644,root,root) %{_datadir}/openssh/Ssh.bin
%endif

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0755,root,root) %{_bindir}/slogin
%attr(0644,root,root) %{_mandir}/man1/slogin.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%if ! %{rescue}
%attr(2755,root,nobody) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%endif

%if ! %{rescue}
%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0755,root,root) /etc/rc.d/init.d/sshd
%endif

%if ! %{no_gnome_askpass}
%files askpass
%defattr(-,root,root)
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif

%changelog
* Thu Oct 1 2009 Vincent Danen <vdanen-at-build.annvix.org> 5.3p1-1.el5.avx
- 5.3p1
- rediff P2, P16
- drop P3, merged upstream

* Thu Apr 16 2009 Vincent Danen <vdanen-at-build.annvix.org> 5.2p1-1.el5.avx
- 5.2p1
- merged patches from Fedora 5.2p1-2.fc11

* Thu Apr 16 2009 Vincent Danen <vdanen-at-build.annvix.org> 5.1p1-1.el5.avx
- first Annvix build for CentOS 5.2 (based on Fedora)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
