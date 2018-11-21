
%define		rpmalloc_version 1.3.0
%define		qt5_x11embed_version 022b39a1d496d72eb3e5b5188e5559f66afca957

%define		_rc	rc7
%define		rel	1

Summary:	Linux MultiMedia Studio
Summary(pl.UTF-8):	MultiMedialne Studio Linuksa
Name:		lmms
Version:	1.2.0
Release:	0.%{_rc}.%{rel}
License:	GPL V2
Group:		X11/Applications/Sound
Source0:	https://github.com/LMMS/lmms/archive/v%{version}-%{_rc}/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	4d527a7f4fc38b105eac55fbd49cf2bb
Source1:	https://github.com/rampantpixels/rpmalloc/archive/%{rpmalloc_version}/rpmalloc-%{rpmalloc_version}.tar.gz
# Source1-md5:	95109beaddeaafd20345ebe4e10c76ba
Source2:	https://github.com/Lukas-W/qt5-x11embed/archive/%{qt5_x11embed_version}/qt5-x11embed-%{qt5_x11embed_version}.tar.gz
# Source2-md5:	193f7a94d1af51c2f85628fcbbf2bf49
Patch0:		fluidsynth2.patch
Patch1:		bash_completion_install.patch
URL:		https://lmms.io/
BuildRequires:	Carla-devel >= 2.0-0.rc2.3
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake
BuildRequires:	fftw3-single-devel >= 3.0.0
BuildRequires:	fluidsynth-devel >= 1.0.7
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	lame-libs-devel
BuildRequires:	libgig-devel
BuildRequires:	libogg-devel
BuildRequires:	libsamplerate-devel >= 0.1.8
BuildRequires:	libsndfile-devel >= 1.0.11
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
BuildRequires:	xorg-lib-libXft-devel
# the VSD loader requires 32-bit devel files
#BuildRequires:	wine-devel
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
LMMS library.

%description libs -l pl.UTF-8
Biblioteka LMMS.

%prep
%setup -q -n %{name}-%{version}-%{_rc} -a1 -a2

rmdir src/3rdparty/rpmalloc/rpmalloc
ln -s ../../../rpmalloc-%{rpmalloc_version} src/3rdparty/rpmalloc/rpmalloc

rmdir src/3rdparty/qt5-x11embed
ln -s ../../qt5-x11embed-%{qt5_x11embed_version} src/3rdparty/qt5-x11embed

rmdir qt5-x11embed-%{qt5_x11embed_version}/3rdparty/ECM
ln -s %{_datadir}/ECM qt5-x11embed-%{qt5_x11embed_version}/3rdparty/ECM

%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DWANT_QT5=ON \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DWANT_VST_NOWINE=ON \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor/*@2/*/*

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
%{_iconsdir}/hicolor/*/apps/lmms.png
%{_iconsdir}/hicolor/*/mimetypes/application-x-lmms-project.png
%{_iconsdir}/hicolor/*/apps/lmms.svg
%{_iconsdir}/hicolor/*/mimetypes/application-x-lmms-project.svg
%{bash_compdir}/lmms

%files devel
%defattr(644,root,root,755)
%{_includedir}/lmms
%{_libdir}/libqx11embedcontainer.a

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/lmms
%attr(755,root,root)%{_libdir}/lmms/*.so
%attr(755,root,root)%{_libdir}/lmms/RemoteZynAddSubFx
%dir %{_libdir}/lmms/ladspa
%attr(755,root,root)%{_libdir}/lmms/ladspa/*.so
