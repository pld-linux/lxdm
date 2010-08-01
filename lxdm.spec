# TODO: make it work
Summary:	Light weight X11 display manager
Name:		lxdm
Version:	0.2.0
Release:	0.1
License:	GPL v3
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
# Source0-md5:	e539f81ba691f2b0cb2017b82dfee58f
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.Xsession
URL:		http://lxde.sourceforge.net/
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Light weight X11 display manager

%package init
Summary:	Init script for lxdm
Summary(pl.UTF-8):	Skrypt init dla lxdm-a
Group:		X11/Applications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	open

%description init
Init script for lxdm.

%description init -l pl.UTF-8
Skrypt init dla lxdm-a.

%prep
%setup -q

%build
rm -f data/lxdm.conf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,pam.d}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lxdm
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lxdm
install %{SOURCE3} $RPM_BUILD_ROOT/etc/lxdm/Xsession

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%dir %{_sysconfdir}/lxdm
%attr(755,root,root) %config %{_sysconfdir}/lxdm/LoginReady
%attr(755,root,root) %config %{_sysconfdir}/lxdm/PostLogin
%attr(755,root,root) %config %{_sysconfdir}/lxdm/PostLogout
%attr(755,root,root) %config %{_sysconfdir}/lxdm/PreLogin
%attr(755,root,root) %config %{_sysconfdir}/lxdm/PreReboot
%attr(755,root,root) %config %{_sysconfdir}/lxdm/PreShutdown
%attr(755,root,root) %config %{_sysconfdir}/lxdm/Xsession
%config %{_sysconfdir}/lxdm/lxdm.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lxdm
%attr(755,root,root) %{_sbindir}/lxdm
%attr(755,root,root) %{_sbindir}/lxdm-binary
%{_datadir}/lxdm
%attr(755,root,root) %{_libexecdir}/lxdm-greeter-gtk

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/lxdm
