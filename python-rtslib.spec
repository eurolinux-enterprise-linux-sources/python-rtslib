%if 0%{?fedora}
%global with_python3 1
%endif

%global oname rtslib-fb

Name:           python-rtslib
License:        ASL 2.0
Group:          System Environment/Libraries
Summary:        API for Linux kernel LIO SCSI target
Version:        2.1.fb63
Release:        11%{?dist}
URL:            https://fedorahosted.org/targetcli-fb/
Source:         https://fedorahosted.org/released/targetcli-fb/%{oname}-%{version}.tar.gz
Source1:        target.service
Patch0:         0001-Turn-off-unsupported-fabrics.patch
Patch1:         0002-Fix-comparisons-to-None.patch
Patch2:         0003-Fix-exception-in-convert_scsi_hctl_to_path.patch
Patch3:         0004-Support-Reconfiguration-of-device-path.patch
Patch4:         0005-Remove-hba-only-directories-in-clear_existing.patch
Patch5:         0006-create-remove-stale-hba-only-dir.patch
Patch6:         0007-alua-enable-alua-for-pscsi-tcmu-if-kernel-reports-su.patch
Patch7:         0008-save_to_file-support-saveconfig-at-storage-object-le.patch
Patch8:         0009-restoreconfig-fix-alua-tpg-config-setup.patch
Patch9:         0010-Support-tcmu-hw-max-sectors.patch
Patch10:        0011-saveconfig-dump-control-string-containing-control-va.patch
Patch11:        0012-tcmu-add-control-constructor-arg.patch
Patch12:        0013-saveconfig-fix-failure-in-absence-of-save-file.patch
BuildArch:      noarch
BuildRequires:  python-devel epydoc python-setuptools systemd-units python-six python-pyudev
Requires:       python-kmod python-six python-pyudev
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%if 0%{?with_python3}
BuildRequires:  python3-devel python-tools python3-setuptools
%endif

%package doc
Summary:        Documentation for python-rtslib
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description
API for generic Linux SCSI kernel target. Includes the 'target'
service and targetctl tool for restoring configuration.

%description doc
API documentation for rtslib, to configure the generic Linux SCSI
multiprotocol kernel target.

%if 0%{?with_python3}
%package -n python3-rtslib
Summary:        API for Linux kernel LIO SCSI target
Group:          System Environment/Libraries

%description -n python3-rtslib
API for generic Linux SCSI kernel target.
%endif

%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build
gzip --stdout doc/targetctl.8 > doc/targetctl.8.gz
gzip --stdout doc/saveconfig.json.5 > doc/saveconfig.json.5.gz
mkdir -p doc/html
epydoc --no-sourcecode --html -n rtslib -o doc/html rtslib/*.py

%if 0%{?with_python3}
pushd %{py3dir}
2to3 --write --nobackups .
%{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/target/backup
mkdir -p %{buildroot}%{_localstatedir}/target/pr
mkdir -p %{buildroot}%{_localstatedir}/target/alua
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/target.service
install -m 644 doc/targetctl.8.gz %{buildroot}%{_mandir}/man8/
install -m 644 doc/saveconfig.json.5.gz %{buildroot}%{_mandir}/man5/

%if 0%{?with_python3}
pushd %{py3dir}
# We don't want py3-converted scripts overwriting py2 scripts
# Shunt them elsewhere then delete
%{__python3} setup.py install --skip-build --root %{buildroot} --install-scripts py3scripts
rm -rf %{buildroot}/py3scripts
popd
%endif

%post
%systemd_post target.service

%preun
%systemd_preun target.service

%postun
%systemd_postun_with_restart target.service

%files
%{python_sitelib}/*
%{_bindir}/targetctl
%{_unitdir}/target.service
%doc COPYING README.md doc/getting_started.md
%{_mandir}/man8/targetctl.8.gz
%{_mandir}/man5/saveconfig.json.5.gz
%dir %{_sysconfdir}/target
%dir %{_sysconfdir}/target/backup
%dir %{_localstatedir}/target
%dir %{_localstatedir}/target/pr
%dir %{_localstatedir}/target/alua

%if 0%{?with_python3}
%files -n python3-rtslib
%{python3_sitelib}/*
%doc COPYING README.md
%endif

%files doc
%doc doc/html

%changelog
* Tue Apr 24 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-11
- Fix a failure in absence of save file

* Thu Apr 19 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-10
- Add missing patch "tcmu: add control constructor arg"

* Fri Apr 13 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-9
- Support tcmu hw max sectors
- saveconfig: dump control string containing control=value tuples

* Wed Apr 11 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-8
- Fix ALUA tpg config setup

* Tue Apr 10 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-7
- Introduce support to saveconfig at the storage object level

* Tue Mar 27 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-6
- enable alua for pscsi/tcmu if kernel reports support 

* Mon Feb 26 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-5
- rtslib never creates hba directories without a storage object within it,
  but if under some circumstance these existed then we should remove them.

* Wed Feb 21 2018 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-4
- Allow users to pass in a string into the attributes.

* Thu Nov 02 2017 Maurizio Lombardi <mlombard@redhat.com> - 2.1.fb63-3
- Enabled qla2xxx target support to fix #1327710

* Wed May 17 2017 Andy Grover <agrover@redhat.com> - 2.1.fb63-2
- Add patch 0003 to fix #1440172

* Thu Mar 2 2017 Andy Grover <agrover@redhat.com> - 2.1.fb63-1
- Rebuild to fix now-fixed issue with redhat-rpm-config in build system

* Fri Jul 29 2016 Andy Grover <agrover@redhat.com> - 2.1.fb57-5
- Rebuild to fix now-fixed issue with redhat-rpm-config in build system

* Wed Jul 27 2016 Andy Grover <agrover@redhat.com> - 2.1.fb57-4
- Add 0003-Fix-regex-in-get_size_for_disk_name.patch

* Wed Oct 28 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-3
- Add 0002-Fix-comparisons-to-None.patch for #1276044

* Mon Aug 24 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-2
- Include missing paths to resolve #1254670

* Tue Jul 14 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-1
- Update to latest Fedora version

* Thu Oct 9 2014 Andy Grover <agrover@redhat.com> - 2.1.fb50-1
- Update to latest Fedora version

* Mon Feb 24 2014 Andy Grover <agrover@redhat.com> - 2.1.fb46-1
- Update to latest Fedora version, fixes rhbz #1064753

* Wed Jan 15 2014 Andy Grover <agrover@redhat.com> - 2.1.fb45-1
- Update to latest Fedora version, to fix rhbz #1048803

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.fb44-2
- Mass rebuild 2013-12-27

* Wed Dec 18 2013 Andy Grover <agrover@redhat.com> - 2.1.fb44-1
- Update to latest Fedora version

* Wed Nov 6 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-3
- Don't overwrite py2 scripts with py3 scripts

* Mon Nov 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-2
- Update rtslib-fix-setup.patch with backported fixups
- Add in missing systemd requires

* Fri Nov 1 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-1
- New upstream version
- Remove obsolete spec stuff: clean, buildroot
- Add target.service

* Mon Sep 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb40-1
- New upstream version, fixes restore of mappedluns

* Wed Sep 11 2013 Andy Grover <agrover@redhat.com> - 2.1.fb39-1
- New upstream version, fixes fcoe

* Tue Sep 10 2013 Andy Grover <agrover@redhat.com> - 2.1.fb38-1
- New upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb37-1
- New upstream version
- License now Apache 2.0

* Tue Jul 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb36-1
- New upstream version
- Remove fix-tabs.patch

* Fri Jun 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb35-1
- New upstream version
- add fix-tabs.patch

* Thu May 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb34-1
- New upstream version

* Thu May 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb33-1
- New upstream version
- Update source file location

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-2
- Add python3 subpackage

* Tue Apr 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-1
- New upstream version

* Tue Feb 26 2013 Andy Grover <agrover@redhat.com> - 2.1.fb30-1
- New upstream version
- Update description and summary
- Remove patch0, upstream doesn't include usb gadget any more

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb28-1
- New upstream version

* Wed Jan 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb27-1
- Specfiles removed upstream, remove handling
- Refresh no-usb.patch

* Thu Dec 20 2012 Andy Grover <agrover@redhat.com> - 2.1.fb26-1
- New upstream release
- Remove kernel dependency
- Remove python-ethtool and python-ipaddr dependencies

* Tue Nov 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb24-1
- New upstream release

* Tue Oct 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb23-1
- New upstream release

* Thu Sep 6 2012 Andy Grover <agrover@redhat.com> - 2.1.fb22-1
- New upstream release

* Wed Aug 8 2012 Andy Grover <agrover@redhat.com> - 2.1.fb21-1
- New upstream release

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-2
- Add patch no-usb.patch

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-1
- New upstream release. Add kernel version dependency.
- Don't claim python_sitelib

* Thu Aug 2 2012 Andy Grover <agrover@redhat.com> - 2.1.fb19-1
- New upstream release. Add kmod dependency.

* Tue Jul 31 2012 Andy Grover <agrover@redhat.com> - 2.1.fb18-1
- New upstream release. Remove configobj dependency

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Andy Grover <agrover@redhat.com> - 2.1.fb17-1
- New upstream release
- Remove patch retry-target-creation.patch, upstream has alternate
  fix.

* Tue Jun 12 2012 Andy Grover <agrover@redhat.com> - 2.1.fb15-1
- New upstream release

* Wed May 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb14-1
- Update Source URL to proper tarball
- Add patch retry-target-creation.patch
- New upstream release

* Mon Apr 9 2012 Andy Grover <agrover@redhat.com> - 2.1.fb13-1
- New upstream release

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-2
- Add -doc package of epydoc-generated html docs

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-1
- New upstream release

* Tue Feb 21 2012 Andy Grover <agrover@redhat.com> - 2.1.fb11-1
- New upstream release

* Fri Feb 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb9-1
- New upstream release

* Fri Feb 3 2012 Andy Grover <agrover@redhat.com> - 2.1.fb8-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb7-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb6-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb5-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb4-1
- New upstream release

* Tue Jan 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb3-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb2-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb1-1
- Change upstream URL
- New upstream release
- Remove upstreamed patches:
  * python-rtslib-git-version.patch
  * python-rtslib-use-ethtool.patch
  * python-rtslib-update-specpath.patch

* Mon Nov 14 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-8
- Change archive instructions to use gzip -n
- Fix issues raised in Fedora package review (#744349)

* Thu Oct 6 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-7
- Remove patch
  * python-rtslib-del-unused-specs.patch

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 1.99-6
- Update based on review comments
  - Fully document steps to build archive
  - Remove commented-out extraneous text
  - Remove a repeat in Requires line
  - Update git-version.patch to have proper sha1
  - Change location of fabric spec files to /var/lib/target
- Remove unused specs

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99-1
- Initial packaging
