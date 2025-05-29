# FIXME: Needed for linking bundled nanovg
%global		_disable_ld_no_undefined	1
%define		oname	BespokeSynth

Summary:		A software modular synth
Name:		bespokesynth
Version:		1.3.0
Release:		1
License:		GPLv3
Group:		Sound
Url:		https://github.com/BespokeSynth
# Submodules are a pain...
#Source0:	https://github.com/BespokeSynth/BespokeSynth/archive/refs/tags/%%{oname}-%%{version}.tar.gz
Source0:	%{oname}-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		bespokesynth-1.3.0-use-webkit2gtk41.patch
BuildRequires:		cmake >= 3.16
BuildRequires:		git
BuildRequires:		imagemagick
BuildRequires:		vst3sdk
BuildRequires:		pkgconfig(flac)
BuildRequires:		pkgconfig(gl)
BuildRequires:		pkgconfig(jsoncpp)
BuildRequires:		pkgconfig(libusb-1.0)
BuildRequires:		pkgconfig(ogg)
BuildRequires:		pkgconfig(pybind11)
BuildRequires:		pkgconfig(python3) >= 3.6
BuildRequires:		pkgconfig(vorbis)
BuildRequires:		pkgconfig(vorbisenc)
BuildRequires:		pkgconfig(vorbisfile)
# All the below are for the bundled JUCE 
BuildRequires:		ladspa-devel
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(cairo)
BuildRequires:		pkgconfig(freetype2)
BuildRequires:		pkgconfig(glib-2.0)
BuildRequires:		pkgconfig(glu)
BuildRequires:		pkgconfig(gtk+-3.0)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(harfbuzz)
BuildRequires:		pkgconfig(libcurl)
BuildRequires:		pkgconfig(libsoup-3.0)
BuildRequires:		pkgconfig(pango)
BuildRequires:		pkgconfig(webkit2gtk-4.1)
BuildRequires:		pkgconfig(x11)
BuildRequires:		pkgconfig(xcomposite)
BuildRequires:		pkgconfig(xcursor)
BuildRequires:		pkgconfig(xext)
BuildRequires:		pkgconfig(xinerama)
BuildRequires:		pkgconfig(xrandr)
BuildRequires:		pkgconfig(xrender)
BuildRequires:		pkgconfig(zlib)

%description
Bespoke is a software modular synthesizer. It contains a bunch of modules,
which you can connect together to create sounds. It's core design is to break
everything into separate modules that can be patched together in a custom
layout, much like a hardware modular. The program is designed to be highly
customizable, with the idea that any of the custom layouts that you create
will be "bespoke" to you as well.
Features:
* live-patchable environment, so you can build while the music is playing.
* VST, VST3, LV2 hosting.
* Python livecoding.
* MIDI & OSC controller mapping.

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/%{oname}
%{_datadir}/%{oname}
%{_datadir}/applications/%{oname}.desktop
%{_datadir}/metainfo/com.%{name}.%{oname}.metainfo.xml
%{_iconsdir}/hicolor/*/apps/bespoke_icon.png

#----------------------------------------------------------------------------

%package libs
Summary:		Libraries used by %{name}
Group:	System/Libraries

%description libs
Bespoke is a software modular synthesizer. This package contains the libraries
needed by the program but not yet provided by OMV.

%files libs
%{_libdir}/*.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-%{version}


%build
%cmake \
	-DBESPOKE_SYSTEM_JSONCPP=ON \
	-DBESPOKE_SYSTEM_PYBIND11=ON

%make_build


%install
%make_install -C build

# Needed libraries not automatically installed
mkdir -p %{buildroot}%{_libdir}
install -m 755 build/libs/freeverb/libfreeverb.so %{buildroot}%{_libdir}
install -m 755 build/libs/nanovg/libnanovg.so %{buildroot}%{_libdir}
install -m 755 build/libs/oddsound-mts/liboddsound-mts.so %{buildroot}%{_libdir}
install -m 755 build/libs/psmove/libpsmove.so %{buildroot}%{_libdir}
install -m 755 build/libs/push2/libpush2.so %{buildroot}%{_libdir}
install -m 755 build/libs/xwax/libxwax.so %{buildroot}%{_libdir}

# Provide more icon sizes
for i in 16 32 48 64 128 256; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
	magick %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/bespoke_icon.png -resize ${i}x${i} %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/bespoke_icon.png
done

# Workaround for wrongly and duplicate installed files
# FIXME: Find why they end up installed twice and in the wrong place
pushd %{buildroot}
	rm -rf builddir/*
#rm -rf ./tmp/*
popd
