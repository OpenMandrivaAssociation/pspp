%define _disable_ld_no_undefined 1

%bcond_with	doc

Summary:	A program for statistical analysis of sampled data
Name:		pspp
Version:	1.6.2
Release:	1
License:	GPLv3+
Group:		Sciences/Mathematics
URL:		https://www.gnu.org/software/pspp/
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Patch1:		%{name}-1.6.2-clang.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
#BuildRequires:	gnulib-devel
BuildRequires:	perl-devel
BuildRequires:	perl(Config::Perl::V)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Text::Diff)
BuildRequires:	plotutils-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(libxml-2.0) 
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(spread-sheet-widget)
#%%if %{with doc}
BuildRequires:	texinfo
#BuildRequires:	texlive
BuildRequires:	texlive-ec
#%%endif

%description
PSPP is a program for statistical analysis of sampled data.  It is
a free replacement for the proprietary program SPSS.

PSPP supports T-tests, ANOVA and GLM analyses, factor analysis,
non-parametric tests, linear and logistic regression, clustering, 
and other statistical features.  PSPP produces statistical reports in
plain text, PDF, PostScript, CSV, HTML, SVG, and OpenDocument formats.
It can import data from OpenDocument, Gnumeric, text and SPSS formats.

PSPP has both text-based and graphical user interfaces.  The PSPP
user interface has been translated into a number of languages.

%files -f %{name}.lang
%license COPYING
%{_bindir}/%{name}*
%{_libdir}/%{name}/lib%{name}-%{version}.so
%{_libdir}/%{name}/lib%{name}-core-%{version}.so
%{_datadir}/%{name}/
%{_datadir}/applications/org.gnu.%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/org.gnu.%{name}.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/apps/org.gnu.%{name}.svg
#{_datadir}/icons/hicolor/scalable/mimetypes/*.svg
%{_datadir}/mime/packages/org.gnu.%{name}.xml
%{_metainfodir}/org.gnu.%{name}.metainfo.xml
%{_infodir}/*
%{_mandir}/man1/%{name}*.1*
%doc doc/%{name}.xml
%if %{with doc}
%doc doc/pspp.html
%doc doc/%{name}.pdf
%endif

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for PSPP
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for developping applications that require PSPP.

%files devel
%license COPYING
%doc AUTHORS ChangeLog NEWS README ONEWS THANKS
%{_libdir}/%{name}/lib%{name}.so
%{_libdir}/%{name}/lib%{name}-core.so
%if %{with doc}
%doc doc/pspp-dev.html
%doc doc/%{name}-dev.pdf
%endif

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -fgnu89-inline -fcommon `pkg-config --cflags gl pango cairo pangocairo cairo-ps`"
export LDFLAGS="%{ldflags} `pkg-config --libs gl pango cairo pangocairo cairo-ps`"

%config_update
%configure \
	--disable-relocatable \
	--without-libreadline-prefix
%make_build

%if %{with doc}
%make_build html pdf
%endif

%install
%make_install

# .desktop
desktop-file-install \
	--add-category Education \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/org.gnu.%{name}.desktop

# remove static lib stuff
find %{buildroot}%{_libdir} -name \*.la -delete

# locales
%find_lang %{name}

%check
%if %{with tests}
%make check || true
%endif

