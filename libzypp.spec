#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Package management library
Summary(pl.UTF-8):	Biblioteka do zarządzania pakietami
Name:		libzypp
Version:	17.18.0
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/openSUSE/libzypp/releases
Source0:	https://github.com/openSUSE/libzypp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8bbdddd5d7fb9b123c29dbf4da45ae89
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-link.patch
URL:		https://en.opensuse.org/Portal:Libzypp
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	gettext-tools
BuildRequires:	gpgme-devel
BuildRequires:	libproxy-devel
# with helixrepo enabled
BuildRequires:	libsolv-devel >= 0.6.8
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	rpm-devel >= 5
BuildRequires:	udev-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzypp is the package management library that powers applications
like YaST, zypper and the openSUSE/SLE implementation of PackageKit.

%description -l pl.UTF-8
libzypp to biblioteka do zarządzania pakietami wspomagająca aplikacje
takie jak YaST, zypper czy implementacja PackageKit wykorzystywana w
dystrybucjach openSUSE/SLE.

%package devel
Summary:	Header files for Zypp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Zypp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Requires:	curl-devel
Requires:	libsolv-devel >= 0.6.8
Requires:	libstdc++-devel >= 6:5
Requires:	libxml2-devel >= 2.0
Requires:	rpm-devel >= 5

%description devel
Header files for Zypp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Zypp.

%package apidocs
Summary:	Zypp API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Zypp
Group:		Documentation

%description apidocs
API documentation for Zypp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Zypp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	%{?with_apidocs:-DENABLE_BUILD_DOCS=ON} \
	-DENABLE_BUILD_TRANS=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_docdir}/packages/libzypp/libzypp/html $RPM_BUILD_ROOT%{_docdir}/libzypp-apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/packages/libzypp/libzypp/libzypp.doxytag

%find_lang zypp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f zypp.lang
%defattr(644,root,root,755)
%doc COPYING
%dir %{_sysconfdir}/zypp
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/zypp/needreboot
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/zypp/systemCheck
%config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/zypp/zypp.conf
%config(noreplace) %verify(not mtime md5 size) /etc/logrotate.d/zypp-history.lr
%attr(755,root,root) %{_bindir}/zypp-CheckAccessDeleted
%attr(755,root,root) %{_bindir}/zypp-NameReqPrv
%attr(755,root,root) %{_libdir}/libzypp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzypp.so.1712
%{_datadir}/zypp
%{_mandir}/man1/zypp-CheckAccessDeleted.1*
%{_mandir}/man1/zypp-NameReqPrv.1*
%{_mandir}/man5/locks.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzypp.so
%{_includedir}/zypp
%{_pkgconfigdir}/libzypp.pc
%{_datadir}/cmake/Modules/FindZypp.cmake
%{_datadir}/cmake/Modules/ZyppCommon.cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/libzypp-apidocs
%endif
