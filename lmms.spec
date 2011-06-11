
Summary:	Linux MultiMedia Studio
Summary(pl.UTF-8):	MultiMedialne Studio Linuksa
Name:		lmms
Version:	0.4.11
Release:	1
License:	GPL V2
Group:		X11/Applications/Sound
Source0:	http://downloads.sourceforge.net/project/lmms/lmms/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	b72c3a87a43e7653bf83d13f35c5d963
URL:		http://lmms.sourceforge.net/
BuildRequires:	QtCore-devel >= 4.5
BuildRequires:	QtGui-devel >= 4.5
BuildRequires:	QtXml-devel >= 4.5
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake
BuildRequires:	fftw3-single-devel >= 3.0.0
BuildRequires:	fluidsynth-devel >= 1.0.7
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	libogg-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	xorg-lib-libXft-devel
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LMMS is a free cross-platform program, which allow you to produce
music with your computer.

%description -l pl.UTF-8
LMMS to wolny, międzyplatformowy program, który pozwoli Tobie tworzyć
muzykę na komputerze.

%package devel
Summary:	LMMS header files
Summary(pl.UTF-8):	Pliki nagłówkowe LMMS
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
The header files for LMMS.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla LMMS.

%package libs
Summary:	LMMS library
Summary(pl.UTF-8):	Biblioteka LMMS
Group:		X11/Applications/Sound

%description libs
XMMS library.

%description libs -l pl.UTF-8
Biblioteka LMMS.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root)%{_bindir}/lmms
%{_desktopdir}/lmms.desktop
%{_mandir}/man1/lmms.1*
%{_datadir}/mime/packages/lmms.xml
%{_datadir}/lmms
%{_pixmapsdir}/lmms.png
%exclude %{_datadir}/menu

%files devel
%defattr(644,root,root,755)
%{_includedir}/lmms/*.h
%exclude %{_includedir}/lmms/*.cpp

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/lmms
%attr(755,root,root)%{_libdir}/lmms/*.so
%attr(755,root,root)%{_libdir}/lmms/RemoteZynAddSubFx
%dir %{_libdir}/lmms/ladspa
%attr(755,root,root)%{_libdir}/lmms/ladspa/*.so
