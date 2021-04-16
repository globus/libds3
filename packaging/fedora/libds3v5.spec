Name:		libds3v5
%global _commit 8bc3d38c43d80d0910dd04d592a880cf85ef6e4b
%if %{?suse_version}%{!?suse_version:0} >= 1315
%global apache_license Apache-2.0
%else
%global apache_license ASL 2.0
%endif
%global soname 0

#no debug package
%global         debug_package %{nil}

Version:	5.0.0
Release:	4%{?dist}
Vendor:		Globus Support
Summary:	Spectra S3 C SDK

Group:		System Environment/Libraries
License:        %{apache_license}
URL:		https://github.com/SpectraLogic/ds3_c_sdk
Source:		%{_commit}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
BuildRequires:  openssl-devel
BuildRequires:  cmake
Requires:       curl openssl
Conflicts:      libds3


%if %{?suse_version}%{!?suse_version:0} >= 1315
%global mainpkg %{name}-%{soname}
%global nmainpkg -n %{mainpkg}
%else
%global mainpkg %{name}
%endif

%if %{?nmainpkg:1}%{!?nmainpkg:0} != 0
%package %{nmainpkg}
Summary:	Spectra S3 C SDK
Group:          System Environment/Libraries
%description %{nmainpkg}
Spectra S3 C SDK Development Libraries and Headers
%endif

%package devel
Summary:	Spectra S3 C SDK Development Libraries
Group:		Development/Libraries
Requires:	%{mainpkg}%{?_isa} = %{version}-%{release}

%description
Spectra S3 C SDK

%description devel
Spectra S3 C SDK Development Libraries and Headers

%prep
%setup -q -n ds3_c_sdk-%{_commit}

%build

sed -i 's/CURL 7.31 REQUIRED/CURL 7.29 REQUIRED/' src/CMakeLists.txt

cmake -DCMAKE_INSTALL_PREFIX=/usr  .
make

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/
mv %{buildroot}/usr/lib/libds3* %{buildroot}%{_libdir}/
mkdir -p %{buildroot}/usr/include/ds3/
mv %{buildroot}/usr/local/include/ds3* %{buildroot}/usr/include/ds3/

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat<<EOF >  %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
prefix=/usr
exec_prefix=/usr
libdir=%{_libdir}
includedir=%{_includedir}/ds3/

Name: DS3
Description: C SDK for the DS3 REST interface
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -lds3
EOF

%check
make %{?_smp_mflags} test

%clean
rm -rf $RPM_BUILD_ROOT

%post %{?nmainpkg} -p /sbin/ldconfig

%postun %{?nmainpkg} -p /sbin/ldconfig

%files %{?nmainpkg}
%defattr(-,root,root,-)
%{_libdir}/libds3.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/ds3/*.h
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Jun 25 2019 Globus Toolkit <support@globus.org> - 5.0.0-4
- DS3 C SDK v5.0.0

* Tue Mar 20 2018 Globus Toolkit <support@globus.org> - 1.2.0g5-2
- packaging fixes

* Fri Jan 27 2017 Globus Toolkit <support@globus.org> - 1.2.0-9
- fix SLES package

* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 1.2.0-8
- Update to latest upstream

* Fri Dec 11 2015 Globus Toolkit <support@globus.org> - 1.2.0-1
- Initial package
