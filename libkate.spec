# based on PLD Linux spec git://git.pld-linux.org/packages/libkate.git
Summary:	Libraries to handle the Kate bitstream format
Name:		libkate
Version:	0.4.1
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: http://code.google.com/p/libkate/downloads/list
Source0:	http://libkate.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	1dfdbdeb2fa5d07063cf5b8261111fca
URL:		http://code.google.com/p/libkate/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
This is libkate, the reference implementation of a codec for the Kate
bitstream format. Kate is a karaoke and text codec meant for
encapsulation in an Ogg container. It can carry text, images, and
animate them.

%package devel
Summary:	Header files for Kate libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use Kate libraries.

%package utils
Summary:	Encoder/Decoder utilities for Kate bitstreams
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	liboggz-utils

%description utils
This package contains the katedec/kateenc binaries for Kate streams.

%package docs
Summary:	Documentation for Kate libraries
Group:		Documentation

%description docs
This package contains the documentation for Kate libraries.

%prep
%setup -q

# don't fail on warnings
%{__sed} -i "s|-Werror ||" configure.ac

# force regenerate
%{__rm} tools/kate_parser.{c,h}
%{__rm} tools/kate_lexer.c

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-static	\
	--docdir=%{_docdir}/%{name}-%{version}
%{__make}

%check
%{__make} check

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p"

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h $RPM_BUILD_ROOT%{_includedir}/kate/kate.h

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_docdir}/libkate-%{version}
%exclude %{_docdir}/libkate-%{version}/html
%attr(755,root,root) %ghost %{_libdir}/libkate.so.?
%attr(755,root,root) %ghost %{_libdir}/liboggkate.so.?
%attr(755,root,root) %{_libdir}/libkate.so.*.*.*
%attr(755,root,root) %{_libdir}/liboggkate.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkate.so
%attr(755,root,root) %{_libdir}/liboggkate.so
%{_includedir}/kate
%{_pkgconfigdir}/kate.pc
%{_pkgconfigdir}/oggkate.pc

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/KateDJ
%attr(755,root,root) %{_bindir}/katalyzer
%attr(755,root,root) %{_bindir}/katedec
%attr(755,root,root) %{_bindir}/kateenc
%dir %{py_sitescriptdir}/kdj
%{py_sitescriptdir}/kdj/*.py[co]
%{_mandir}/man1/KateDJ.1*
%{_mandir}/man1/katalyzer.1*
%{_mandir}/man1/katedec.1*
%{_mandir}/man1/kateenc.1*

%files docs
%defattr(644,root,root,755)
%doc %{_docdir}/libkate-%{version}/html

