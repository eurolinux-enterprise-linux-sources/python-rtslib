%define oname rtslib-fb

Name:           python-rtslib
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        API for RisingTide Systems generic SCSI target
Version:        2.1.fb21
Release:        3%{?dist}
URL:            https://github.com/agrover/rtslib-fb/
Source:         https://github.com/downloads/agrover/%{oname}/%{oname}-%{version}.tar.gz
Patch0:         %{name}-del-unused-specs.patch
Patch1:         %{name}-fix-exception-in-pscsi-backstore.patch
Patch2:         %{name}-fix-pscsi-1.patch
Patch3:         %{name}-fix-pscsi-2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-ipaddr python-ethtool python-devel
Requires:       python-ipaddr python-ethtool

%description
API for generic Linux SCSI target.

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
%{python_sitelib}/*
/var/lib/target
%doc COPYING README

%changelog
* Tue Jun 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb21-3
- Add patches:
  * fix-pscsi-1.patch
  * fix-pscsi-2.patch

* Fri Mar 1 2013 Andy Grover <agrover@redhat.com> - 2.1.fb21-2
- Add patch fix-exception-in-pscsi-backstore.patch

* Wed Aug 8 2012 Andy Grover <agrover@redhat.com> - 2.1.fb21-1
- Update for new upstream version

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-1
- Update to new upstream version
- Remove patches
  * fix nodeacl-dump.patch
  * retry-target-creation.patch

* Thu May 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-3
- Add patch retry-target-creation.patch for bz 815981

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
