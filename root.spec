%define name	root
%define version	5.28.00
%define release	%mkrel 2
%define rootdir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Physics
License:	GPL
Version:	%{version}
Release:	%{release}
Summary:	CERN framework for data processing
URL:		http://root.cern.ch/drupal
Source0:	ftp://root.cern.ch/root/%{name}_v%{version}.source.tar.xz
Source1:	ftp://root.cern.ch/root/html528.tar.xz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	fftw3-devel
BuildRequires:	freetype2-devel
BuildRequires:	GL-devel
BuildRequires:	libftgl-devel
BuildRequires:	libgsl-devel
BuildRequires:	libhepmc-devel
BuildRequires:	libiodbc-devel
BuildRequires:	libkrb-devel
BuildRequires:	libldap-devel
BuildRequires:	libpng-devel
BuildRequires:	libpythia-devel
BuildRequires:	libqt-devel
BuildRequires:	libxft-devel
BuildRequires:	libxml-devel
BuildRequires:	libxpm-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	ruby-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
BuildRequires:	python-devel

# x3d
Requires:	x11-font-sony-misc

%description
ROOT is a framework for data processing, born at CERN, at the heart of the
research on high-energy physics.  Every day, thousands of physicists use
ROOT applications to analyze their data or to perform simulations.

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/aclocal/root.m4
%{_datadir}/emacs/site-lisp/root-help.el
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{rootdir}
%{rootdir}/*
%doc %{_docdir}/%{name}/BUILDSYSTEM
%doc %{_docdir}/%{name}/cfortran.doc
%doc %{_docdir}/%{name}/ChangeLog*
%doc %{_docdir}/%{name}/INSTALL
%doc %{_docdir}/%{name}/README*
%{_docdir}/%{name}/COPYING.CINT
%{_docdir}/%{name}/CREDITS
%{_docdir}/%{name}/COPYING.CINT
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/test
%{_docdir}/%{name}/tutorials
%{_mandir}/man1/*

#------------------------------------------------------------------------
%package	doc
Group:		Development/Other
Summary:	Documentation for %{name}
BuildArch: noarch

%description	doc
ROOT is a framework for data processing, born at CERN, at the heart of the
research on high-energy physics.  Every day, thousands of physicists use
ROOT applications to analyze their data or to perform simulations.

%files		doc
%defattr(-,root,root)
%doc %{_docdir}/%{name}/htmldoc

#------------------------------------------------------------------------
%prep
%setup -q -n %{name}

#------------------------------------------------------------------------
%build
# not an autotools configure (it just quarks like one)
./configure						\
%ifarch %{ix86}
	linux						\
%endif
%ifarch x86_64
	linuxx8664gcc					\
%endif
	--prefix=%{_prefix} 				\
	--libdir=%{_libdir}/root			\
	--cintincdir=%{rootdir}/cint			\
	--bindir=%{rootdir}/bin				\
	--enable-roofit					\
	--enable-gdml					\
	--enable-minuit2				\
	--enable-table					\
	--enable-unuran					\
	--enable-explicitlink				\
	--enable-gsl-shared				\
	--enable-pythia8				\
	--with-pythia8-incdir=%{_includedir}/pythia	\
	--with-pythia8-libdir=%{_libdir}		\
	--enable-qt					\
	--enable-qtgsi					\
	--enable-ruby

%make

#------------------------------------------------------------------------
%install
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/%{name}	> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# make export ROOTSYS=%{rootdir} functional
for f in test tutorials; do
    # in case of --short-circuit -bi
    rm -f %{buildroot}%{rootdir}/$f
    ln -sf %{_datadir}/doc/%{name}/$f %{buildroot}%{rootdir}/$f
done

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

export ROOTSYS=%{rootdir}
export PATH=%{rootdir}/bin:\$PATH
%{rootdir}/bin/%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
%if %{mdkversion} < 201010
xz -cd %{SOURCE1} | tar -xf -C %{buildroot}%{_docdir}/%{name}
%else
tar Jxf %{SOURCE1} -C %{buildroot}%{_docdir}/%{name}
%endif

#------------------------------------------------------------------------
%clean
rm -fr %{buildroot}
