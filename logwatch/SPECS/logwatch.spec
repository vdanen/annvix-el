#
# spec file for package logwatch 
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

Summary: A log file analysis program
Name: logwatch
Version: 7.3.6
Release: 1%{dist}
License: MIT
Group: Applications/System
URL: http://www.logwatch.org/
Source: ftp://ftp.kaybee.org/pub/linux/logwatch-%{version}.tar.gz
Patch2: logwatch-7.2.1-nosegfault.patch
Patch6: logwatch-7.3.6-avx-secure.patch
Patch11: logwatch-7.3-man.patch
Patch13: logwatch-7.3.6-avx-oldfiles.patch

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
%patch6 -p1
%patch11 -p1
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
* Sun Feb 22 2009 Vincent Danen <vdanen-at-build.annvix.org> 7.3.6-1
- first Annvix package based on 7.3-6.el5
- 7.3.6
- drop upstream integrated patches P3, P4, P5, P7, P8, P9
- drop P10, P12 due to major changes
- rediff P6, P13

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8

