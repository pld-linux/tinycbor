#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Tiny Concise Binary Object Representation (CBOR) Library
Summary(pl.UTF-8):	Mała biblioteka CBOR (Concise Binary Object Representation)
Name:		tinycbor
Version:	7.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/intel/tinycbor/releases
Source0:	https://github.com/intel/tinycbor/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	518d694ff138835dbcdf46562358a752
URL:		https://github.com/intel/tinycbor
BuildRequires:	cjson-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tiny Concise Binary Object Representation (CBOR) Library.

%description -l pl.UTF-8
Mała biblioteka CBOR (Concise Binary Object Representation - zwięzłej
binarnej reprezentacji obiektów).

%package devel
Summary:	Header files for TinyCBOR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki TinyCBOR
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for TinyCBOR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki TinyCBOR.

%package static
Summary:	Static TinyCBOR library
Summary(pl.UTF-8):	Statyczna biblioteka TinyCBOR
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static TinyCBOR library.

%description static -l pl.UTF-8
Statyczna biblioteka TinyCBOR.

%package apidocs
Summary:	API documentation for TinyCBOR library
Summary(pl.UTF-8):	Dokumentacja API biblioteki TinyCBOR
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for TinyCBOR library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki TinyCBOR.

%prep
%setup -q

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DBUILD_TOOLS=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
doxygen ../Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install build/tools/json2cbor/json2cbor $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README TODO
%attr(755,root,root) %{_bindir}/cbordump
%attr(755,root,root) %{_bindir}/json2cbor
%{_libdir}/libtinycbor.so.*.*.*
%ghost %{_libdir}/libtinycbor.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtinycbor.so
%{_includedir}/tinycbor
%{_pkgconfigdir}/tinycbor.pc
%{_libdir}/cmake/tinycbor

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtinycbor.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*.{css,html,js,png}
%endif
