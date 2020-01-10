%define oname rtslib-fb

Name:           python-rtslib
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        API for RisingTide Systems generic SCSI target
Version:        2.1.fb12
Release:        2%{?dist}
URL:            https://github.com/agrover/rtslib-fb/
Source:         https://github.com/agrover/%{oname}/tarball/v%{version}
Patch1:         %{name}-del-unused-specs.patch
Patch2:         %{name}-fix-nodeacl-dump.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-ipaddr python-ethtool python-configobj python-devel
Requires:       python-ipaddr python-ethtool python-configobj

%description
API for generic Linux SCSI target.

%prep
%setup -q -n agrover-%{oname}-46e1918
%patch1 -p1
%patch2 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/var/lib/target/fabric
cp specs/* %{buildroot}/var/lib/target/fabric


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}
/var/lib/target
%doc COPYING README

%changelog
* Thu Apr 19 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-2
- Add patch fix-nodeacl-dump.patch

* Tue Mar 6 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-1
- New upstream version, from Fedora

* Wed Feb 15 2012 Andy Grover <agrover@redhat.com> - 2.1.fb9-1
- Update from Fedora

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 1.9.9-6
- Update based on review comments
  - Fully document steps to build archive
  - Remove commented-out extraneous text
  - Remove a repeat in Requires line
  - Update git-version.patch to have proper sha1
  - Change location of fabric spec files to /var/lib/target
- Remove unused specs

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.9.9-1
- Initial packaging
