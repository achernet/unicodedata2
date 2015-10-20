%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

# Python3 is not supported right now!
%global with_python3 0

Name:           python-unicodedata2
Version:        8.0.0
Release:        1%{?dist}
Summary:        Unicodedata backport for python 2 updated to the latest unicode version.

Group:          System Environment/Libraries
License:        Apache License 2.0
URL:            http://github.org/mikekap/unicodedata2
Source0:        http://pypi.python.org/packages/source/u/unicodedata2/unicodedata2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-nose
%endif # with_python3


%description
unicodedata backport/updates to python 2.

The versions of this package match unicode versions, so unicodedata2==8.0.0 is data from unicode 8.0.0.
Additionally this backports support for named aliases and named sequences to python2.

%if 0%{?with_python3}
%package -n python3-unicodedata2
Summary:        Unicodedata backport for python 2 updated to the latest unicode version.
Group:          System Environment/Libraries

%description -n python3-unicodedata2
unicodedata backport/updates to python 2.

The versions of this package match unicode versions, so unicodedata2==8.0.0 is data from unicode 8.0.0.
Additionally this backports support for named aliases and named sequences to python2.

%endif # with_python3

%prep
%setup -q -n unicodedata2-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root=%{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root=%{buildroot}
popd
%endif # with_python3

%check
env PYTHONPATH=%{buildroot}%{python_sitearch} nosetests -v -v -x tests/*.py

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-%{python3_version} -q
popd
%endif # with_python3

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md CHANGELOG.md
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-unicodedata2
%defattr(-,root,root,-)
%doc LICENSE README.md CHANGELOG.md
%{python3_sitearch}/*
%endif # python3

%changelog
* Tue Oct 20 2015 Alex Chernetz <alex.chernetz@concur.com> - 8.0.0-1
- Add tests to MANIFEST.in

* Tue Sep 15 2015 Mike Kaplinskiy <mkaplinskiy@twitter.com> - 8.0.0
- Upgrade to unicode 8.0.0

* Fri Aug 7 2015 Mike Kaplinskiy <mkaplinskiy@twitter.com> - 7.0.0-2
- Compiles under python 2.6 (and older 2.7). Patch by John Vandenberg. Fixes #2
- Runs regular unicodedata tests. Adds travis and appveyor CI. Patch by John Vandenberg.

* Mon Oct 6 2014 Mike Kaplinskiy <mikekap@vineapp.com> - 7.0.0
- Initial release

