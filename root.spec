%define name	root
%define version	v5.24.00
%define release	%mkrel 1
%define rootdir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Physics
License:	GPL
Version:	%{version}
Release:	%{release}
Summary:	CERN framework for data processing
URL:		http://root.cern.ch/drupal
Source0:	ftp://root.cern.ch/root/root_v5.24.00.source.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Patch0:		root_v5.24.00-build.patch

BuildRequires:	fftw3-devel
BuildRequires:	GL-devel
BuildRequires:	libiodbc-devel
BuildRequires:	libkrb-devel
BuildRequires:	libldap-devel
BuildRequires:	libqt-devel
BuildRequires:	libxft-devel
BuildRequires:	libxml-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	postgresql-devel
BuildRequires:	ruby-devel
BuildRequires:	tiff-devel
BuildRequires:	zlib-devel
%py_requires	-d

%description
ROOT is a framework for data processing, born at CERN, at the heart of the
research on high-energy physics.  Every day, thousands of physicists use
ROOT applications to analyze their data or to perform simulations.


#------------------------------------------------------------------------
%prep
%setup -q -n %{name}
%patch0 -p1


#------------------------------------------------------------------------
%build
%define common	--prefix=%{_prefix} --libdir=%{_libdir}/root --cintincdir=%{rootdir}/cint

%ifarch %{ix86}
./configure linux %{common}
%endif

%ifarch x86_64
./configure linuxx8664gcc %{common}
%endif

%make


#------------------------------------------------------------------------
%install
%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/%{name}	> %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

perl -pi -e 's|^(cd $ROOTSYS)|ROOTSYS=%{_prefix}\n$1|;' %{buildroot}%{_bindir}/roots

#------------------------------------------------------------------------
%clean
rm -fr %{buildroot}


#------------------------------------------------------------------------
%files
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/aclocal/root.m4
%{_datadir}/emacs/site-lisp/root-help.el
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{rootdir}
 %{rootdir}/*
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
%{_mandir}/man1/*
