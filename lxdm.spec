#
# Conditional build:
%bcond_without	gtk3	# use GTK+3 instead of GTK+2

Summary:	Light weight X11 display manager
Summary(pl.UTF-8):	Lekki zarządca ekranów X11
Name:		lxdm
Version:	0.5.3
Release:	2
License:	GPL v3+
Group:		X11/Applications
Source0:	https://downloads.sourceforge.net/lxdm/%{name}-%{version}.tar.xz
# Source0-md5:	061caae432634e6db38bbdc84bc6ffa0
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.Xsession
Patch0:		%{name}-setuid.patch
Patch1:		greeter-skip-services.patch
URL:		http://www.lxde.org/
BuildRequires:	ConsoleKit-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.12.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes
BuildRequires:	libxcb-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.627
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	/usr/bin/X
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.12.0}
Requires:	iso-codes
Requires:	xinitrc-ng >= 1.0
Suggests:	%{name}-init = %{version}-%{release}
Suggests:	openbox
Provides:	XDM
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Light weight X11 display manager.

%description -l pl.UTF-8
Lekki zarządca ekranów X11.

%package init
Summary:	Init script for lxdm
Summary(pl.UTF-8):	Skrypt init dla lxdm-a
Group:		X11/Applications
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38

%description init
Init script for lxdm.

%description init -l pl.UTF-8
Skrypt init dla lxdm-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__rm} data/lxdm.conf

%build
%configure \
	--with-pam \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,pam.d,security} \
	$RPM_BUILD_ROOT{/etc/systemd/system,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lxdm
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lxdm
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/Xsession
touch $RPM_BUILD_ROOT/etc/security/blacklist.lxdm

ln -s /dev/null $RPM_BUILD_ROOT/etc/systemd/system/lxdm.service

# duplicate of ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
%service -n %{name} restart
%systemd_reload

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	%service %{name} stop
fi

%postun init
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %config %{_sysconfdir}/%{name}/LoginReady
%attr(755,root,root) %config %{_sysconfdir}/%{name}/PostLogin
%attr(755,root,root) %config %{_sysconfdir}/%{name}/PostLogout
%attr(755,root,root) %config %{_sysconfdir}/%{name}/PreLogin
%attr(755,root,root) %config %{_sysconfdir}/%{name}/PreReboot
%attr(755,root,root) %config %{_sysconfdir}/%{name}/PreShutdown
%attr(755,root,root) %config %{_sysconfdir}/%{name}/Xsession
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lxdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lxdm
%attr(755,root,root) %{_bindir}/lxdm-config
%attr(755,root,root) %{_sbindir}/lxdm
%attr(755,root,root) %{_sbindir}/lxdm-binary
%attr(755,root,root) %{_libexecdir}/lxdm-greeter-gtk
%attr(755,root,root) %{_libexecdir}/lxdm-greeter-gdk
%attr(755,root,root) %{_libexecdir}/lxdm-numlock
%attr(755,root,root) %{_libexecdir}/lxdm-session
%{_datadir}/%{name}
%{systemdunitdir}/lxdm.service

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/lxdm
%config(noreplace) %verify(not md5 mtime size) /etc/systemd/system/lxdm.service
