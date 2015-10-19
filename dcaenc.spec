#
# Conditional build:
%bcond_without	alsa		# alsa output plugin
%bcond_without	static_libs	# static library
#
Summary:	Encoder for DTS Coherent Acoustics audio format
Summary(pl.UTF-8):	Koder formatu dźwięku DTS Coherent Acoustics
Name:		dcaenc
Version:	2
Release:	1
License:	LGPL v2.1+ (but requires patent license in some countries)
Group:		Libraries
Source0:	http://aepatrakov.narod.ru/olderfiles/1/%{name}-%{version}.tar.gz
# Source0-md5:	9da4d1b4716d7ab49b4cb9c6ac9461df
URL:		http://aepatrakov.narod.ru/index/0-2
BuildRequires:	alsa-lib-devel >= 1.0.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dcaenc is an open-source implementation of the DTS Coherent Acoustics
codec. Only the core part of the encoder is implemented, because the
public specification (ETSI TS 102 114 V1.2.1) is insufficient for
implementing anything else.

%description -l pl.UTF-8
dcaenc to mająca otwarte źródła implementacja kodeka DTS Coherent
Acoustics. Zaimplementowana jest tylko główna część kodera, ponieważ
publiczna specyfikacja (ETSI TS 102 114 V1.2.1) jest niewystarczająca
do czegokolwiek więcej.

%package devel
Summary:	Header files for dcaenc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki dcaenc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for dcaenc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dcaenc.

%package static
Summary:	Static dcaenc library
Summary(pl.UTF-8):	Statyczna biblioteka dcaenc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static dcaenc library.

%description static -l pl.UTF-8
Statyczna biblioteka dcaenc.

%package -n alsa-plugins-dca
Summary:	DTS Coherent Acoustics output plugin for ALSA
Summary(pl.UTF-8):	Wtyczka wyjściowa DTS Coherent Acoustics dla systemu ALSA
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib >= 1.0.11

%description -n alsa-plugins-dca
DTS Coherent Acoustics output plugin for ALSA.

%description -n alsa-plugins-dca -l pl.UTF-8
Wtyczka wyjściowa DTS Coherent Acoustics dla systemu ALSA.

%prep
%setup -q

%build
%configure \
	%{!?with_alsa:--disable-alsa} \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies; also, obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdcaenc.la
%if %{with alsa}
# dlopened module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/alsa-lib/libasound_module_pcm_dca.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/alsa-lib/libasound_module_pcm_dca.a
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/dcaenc
%attr(755,root,root) %{_libdir}/libdcaenc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdcaenc.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdcaenc.so
%{_includedir}/dcaenc.h
%{_pkgconfigdir}/dcaenc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdcaenc.a
%endif

%if %{with alsa}
%files -n alsa-plugins-dca
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/alsa-lib/libasound_module_pcm_dca.so
%{_datadir}/alsa/pcm/dca.conf
%endif
