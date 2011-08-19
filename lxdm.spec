Summary:	Light weight X11 display manager
Name:		lxdm
Version:	0.4.1
Release:	4
License:	GPL v3
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	8da1cfc2be6dc9217c85a7cf51e1e821
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.Xsession
Source4:	%{name}.upstart
Patch0:		%{name}-setuid.patch
Patch1:		greeter-skip-services.patch
URL:		http://wiki.lxde.org/en/LXDM
BuildRequires:	ConsoleKit-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
Requires:	xinitrc-ng
Suggests:	%{name}-init
Suggests:	openbox
Provides:	XDM
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Light weight X11 display manager.

%package init
Summary:	Init script for lxdm
Summary(pl.UTF-8):	Skrypt init dla lxdm-a
Group:		X11/Applications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description init
Init script for lxdm.

%description init -l pl.UTF-8
Skrypt init dla lxdm-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f data/lxdm.conf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,init,pam.d,security}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lxdm
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/init/%{name}.conf
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lxdm
install -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/Xsession
touch $RPM_BUILD_ROOT/etc/security/blacklist.lxdm

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lxdm
%attr(755,root,root) %{_bindir}/%{name}-config
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}-binary
%attr(755,root,root) %{_libexecdir}/%{name}-greeter-gtk
%attr(755,root,root) %{_libdir}/%{name}-greeter-gdk
%attr(755,root,root) %{_libdir}/%{name}-numlock
%{_datadir}/%{name}

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/init/%{name}.conf
