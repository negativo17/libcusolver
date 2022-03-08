%global debug_package %{nil}
%global __strip /bin/true
%global _missing_build_ids_terminate_build 0
%global _build_id_links none
%global major_package_version 11-6

Name:           libcusolver
Epoch:          2
Version:        11.3.3.112
Release:        1%{?dist}
Summary:        NVIDIA cuSOLVER library
License:        CUDA Toolkit
URL:            https://developer.nvidia.com/cuda-toolkit
ExclusiveArch:  x86_64 ppc64le aarch64

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-x86_64/%{name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-ppc64le/%{name}-linux-ppc64le-%{version}-archive.tar.xz
Source2:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-sbsa/%{name}-linux-sbsa-%{version}-archive.tar.xz
Source3:        cusolver.pc

Requires(post): ldconfig
Requires:       libgomp%{_isa}
Conflicts:      %{name}-%{major_package_version} < %{?epoch:%{epoch}:}%{version}-%{release}
# Drop in 11.7:
Provides:       cuda-cusolver = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cusolver < %{?epoch:%{epoch}:}%{version}-%{release}

%description
The NVIDIA cuSOLVER library provides a collection of dense and sparse direct
solvers which deliver significant acceleration for Computer Vision, CFD,
Computational Chemistry, and Linear Optimization applications.

%package devel
Summary:        Development files for NVIDIA cuSOLVER library
Requires:       %{name}%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts:      %{name}-devel-%{major_package_version} < %{?epoch:%{epoch}:}%{version}
# Drop in 11.7:
Provides:       cuda-cusolver-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cusolver-devel < %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides development files for the NVIDIA cuSOLVER library.

%package static
Summary:        Static libraries for NVIDIA cuSOLVER
Requires:       %{name}-devel%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
# Drop in 11.7:
Provides:       cuda-cusolver-static = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      cuda-cusolver-static < %{?epoch:%{epoch}:}%{version}-%{release}

%description static
This package contains static libraries for NVIDIA cuSOLVER.

%prep
%ifarch x86_64
%setup -q -n %{name}-linux-x86_64-%{version}-archive
%endif

%ifarch ppc64le
%setup -q -T -b 1 -n %{name}-linux-ppc64le-%{version}-archive
%endif

%ifarch aarch64
%setup -q -T -b 2 -n %{name}-linux-sbsa-%{version}-archive
%endif

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig/

cp -fr include/* %{buildroot}%{_includedir}/
cp -fr lib/lib* %{buildroot}%{_libdir}/
cp -fr %{SOURCE3} %{buildroot}/%{_libdir}/pkgconfig/

# Set proper variables
sed -i \
    -e 's|CUDA_VERSION|%{version}|g' \
    -e 's|LIBDIR|%{_libdir}|g' \
    -e 's|INCLUDE_DIR|%{_includedir}|g' \
    %{buildroot}/%{_libdir}/pkgconfig/*.pc

%{?ldconfig_scriptlets}

%files
%license LICENSE
%{_libdir}/libcusolver.so.*
%{_libdir}/libcusolverMg.so.*

%files devel
%{_includedir}/cusolver_common.h
%{_includedir}/cusolverDn.h
%{_includedir}/cusolverMg.h
%{_includedir}/cusolverRf.h
%{_includedir}/cusolverSp.h
%{_includedir}/cusolverSp_LOWLEVEL_PREVIEW.h
%{_libdir}/libcusolver.so
%{_libdir}/libcusolverMg.so
%{_libdir}/liblapack_static.a
%{_libdir}/libmetis_static.a
%{_libdir}/pkgconfig/cusolver.pc

%files static
%{_libdir}/libcusolver_static.a

%changelog
* Tue Mar 08 2022 Simone Caronni <negativo17@gmail.com> - 2:11.3.3.112-1
- Update to 11.3.3.112 (CUDA 11.6.1).

* Wed Jan 26 2022 Simone Caronni <negativo17@gmail.com> - 2:11.3.2.55-1
- First build with the new tarball components.

