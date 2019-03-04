%define name    gwtrigfind
%define version 0.8.0
%define release 1

Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   Utility to find files archived by GW event trigger generators

License:   GPLv3
Url:       https://pypi.org/project/%{name}/
Source0:   https://pypi.io/packages/source/g/%{name}/%{name}-%{version}.tar.gz

Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
BuildRequires: rpm-build
BuildRequires: python2-rpm-macros
BuildRequires: python-setuptools
#BuildRequires: python2-ligo-segments
#BuildRequires: python2-pytest >= 2.8.0
#BuildRequires: python2-mock

%description
A python module with command-line wrapper used to locate event trigger files
from any of the automatically-running GW event trigger generators.

# -- python2-gwtrigfind

%package -n python2-%{name}
Summary:  %{summary}
Requires: python2-astropy
Requires: python2-ligo-segments
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
A python module with command-line wrapper used to locate event trigger files
from any of the automatically-running GW event trigger generators.

# -- build steps

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build

#%check  - need pytest>=2.8.0
#%{__python2} -m pytest --pyargs %{name}

%install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{_bindir}/*
%{python2_sitelib}/*

# -- changelog

%changelog
* Mon Mar 04 2019 Duncan Macleod <duncan.macleod@ligo.org> - 0.8.0-1
- Updated pycbc.live conventions [https://github.com/gwpy/gwtrigfind/pull/27]

* Mon Jul 30 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 0.6.0 first RPM build
