%{?scl:%scl_package eclipse-ptp}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

%global eclipse_base            %{_datadir}/eclipse
%global cdtreq                  1:8.1.0
%global pdereq                  1:4.2.0
%global ptp_qualifier           201509091505
%global ptp_git_tag             PTP_9_0_1

%ifarch %{ix86}
    %define eclipse_arch x86
%endif
%ifarch %{arm}
    %define eclipse_arch arm
%endif
%ifarch ppc64 ppc64p7
    %define eclipse_arch ppc64
%endif
%ifarch s390 s390x ppc x86_64 aarch64 ppc64le
    %define eclipse_arch %{_arch}
%endif

Summary:        Eclipse Parallel Tools Platform
Name:           %{?scl_prefix}eclipse-ptp
Version:        9.0.1
Release:        1.%{baserelease}%{?dist}
License:        EPL
Group:          Development/Tools
URL:            http://www.eclipse.org/ptp

# The following tarballs were downloaded from the git repositories
Source0:        http://git.eclipse.org/c/ptp/org.eclipse.ptp.git/snapshot/org.eclipse.ptp-%{ptp_git_tag}.tar.xz
# To help generate the needed Requires
Source3:        finddeps.sh

# Remove extra environments from pom.xml
Patch0:         eclipse-ptp-tycho-build.patch
# Add <repository> for tycho-eclipserun-plugin
Patch1:         eclipse-ptp-repository.patch
Patch2:         eclipse-ptp-trim.patch

# Remove some unneeded dependencies
BuildRequires:  %{?scl_prefix_java_common}maven-local
# Need tycho-extras for core/org.eclipse.ptp.doc.isv
BuildRequires:  %{?scl_prefix}tycho-extras
BuildRequires:  %{?scl_prefix}eclipse-cdt-parsers >= %{cdtreq}
BuildRequires:  %{?scl_prefix}eclipse-license
BuildRequires:  %{?scl_prefix}eclipse-jgit
BuildRequires:  %{?scl_prefix}eclipse-pde >= %{pdereq}
BuildRequires:  %{?scl_prefix}eclipse-remote
BuildRequires:  %{?scl_prefix}eclipse-tm-terminal
BuildRequires:  %{?scl_prefix}lpg-java-compat = 1.1.0

Requires:       %{?scl_prefix}eclipse-cdt >= %{cdtreq}
Requires:       %{?scl_prefix}eclipse-remote
# Pulled in by rdt.remotetools being in ptp main
Provides:       %{name}-cdt-compilers = %{version}-%{release}
Obsoletes:      %{name}-cdt-compilers < %{version}-%{release}
Provides:       %{name}-rdt-remotetools = %{version}-%{release}
Obsoletes:      %{name}-rdt-remotetools < %{version}-%{release}
Provides:       %{name}-rdt-sdk = %{version}-%{release}
Obsoletes:      %{name}-rdt-sdk < %{version}-%{release}
Provides:       %{name}-rdt-sync = %{version}-%{release}
Obsoletes:      %{name}-rdt-sync < %{version}-%{release}
Provides:       %{name}-rdt-xlc-sdk = %{version}-%{release}
Obsoletes:      %{name}-rdt-xlc-sdk < %{version}-%{release}

#Obsolete components no longer available in 9.0
Obsoletes:      %{name}-rdt < %{version}-%{release}
Obsoletes:      %{name}-rdt-xlc < %{version}-%{release}
Obsoletes:      %{name}-remote-rse < %{version}-%{release}

%description
The aim of the parallel tools platform project is to produce an open-source
industry-strength platform that provides a highly integrated environment
specifically designed for parallel application development. The project will
provide:

 - a standard, portable parallel IDE that supports a wide range of parallel
   architectures and run-time systems
 - a scalable parallel debugger
 - support for the integration of a wide range of parallel tools
 - an environment that simplifies the end-user interaction with parallel
   systems

This package contains the main PTP run-time features.

%package        master
Summary:        Complete PTP package
Group:          Development/Libraries
Requires:       %{?scl_prefix}eclipse-cdt >= %{cdtreq}
Requires:       %{name} = %{version}-%{release}

#master package is a virtual package that requires all of the components
Requires:       %{name}-rm-contrib = %{version}-%{release}
Requires:       %{name}-sci = %{version}-%{release}
Requires:       %{name}-sdk = %{version}-%{release}
Requires:       %{name}-sdm = %{version}-%{release}

%description    master
The package will bring in all of the PTP components.

%package        core-source
Summary:        PTP Core Components Source
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    core-source
Parallel Tools Platform core components source code.

%package        rm-contrib
Summary:        PTP Contributed Resource Manager Definitions
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    rm-contrib
Adds resource managers for a number of different systems.

%package        sci
Summary:        PTP Scalable Communication Infrastructure (SCI)
Group:          Development/Libraries
BuildArch:      noarch

%description    sci
Parallel Tools Platform components that implements the Scalable Communication
Infrastructure (SCI).

%package        sdk
Summary:        Parallel Tools Platform SDK 
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name}-core-source = %{version}-%{release}

%description    sdk
Eclipse Parallel Tools Platform. Software development kit including source
code and developer documentation.

%package        sdm
Summary:        PTP Scalable Debug Manager (SDM)
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    sdm
Parallel Tools Platform components that implement a parallel debug server
using the Scalable Debug Manager (SDM).

NOTE: The sdm binary for the architecture of the host machine is available
in the sdm plugin and at %{_libdir}/ptp/sdm.  If the target system is of
a different archicture, you will need to build and install it by hand.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n org.eclipse.ptp-%{ptp_git_tag}

%patch0 -p2 -b .tycho-build
%patch1 -p1 -b .repository
%patch2 -p0 -b .fix
sed -i -e 's/<arch>x86<\/arch>/<arch>%{eclipse_arch}<\/arch>/g' pom.xml

%pom_disable_module rdt/org.eclipse.ptp.rdt.sync.fortran.ui
%pom_disable_module releng/org.eclipse.ptp.etfw-feature
%pom_disable_module releng/org.eclipse.ptp.etfw.tau-feature
%pom_disable_module releng/org.eclipse.ptp.etfw.tau.fortran-feature
%pom_disable_module releng/org.eclipse.ptp.etfw.feedback.perfsuite-feature
%pom_disable_module releng/org.eclipse.ptp.fortran-feature
%pom_disable_module releng/org.eclipse.ptp.gem-feature
%pom_disable_module releng/org.eclipse.ptp.pldt-feature
%pom_disable_module releng/org.eclipse.ptp.pldt.fortran-feature
%pom_disable_module releng/org.eclipse.ptp.pldt.upc-feature
%pom_disable_module releng/org.eclipse.ptp.rdt.sync.fortran-feature
%pom_disable_module releng/org.eclipse.ptp.rm.ibm.ll-feature
%pom_disable_module releng/org.eclipse.ptp.rm.ibm.pe-feature
%pom_disable_module releng/org.eclipse.ptp.rm.ibm.platform.lsf-feature
%pom_disable_module releng/org.eclipse.ptp.rm.slurm-feature
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.ll.doc.user
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.ll.ui
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.pe.doc.user
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.pe.ui
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.platform.lsf.doc.user
%pom_disable_module rms/org.eclipse.ptp.rm.ibm.platform.lsf.ui
%pom_disable_module rms/org.eclipse.ptp.rm.slurm.help
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.doc.user
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.feedback
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.feedback.perfsuite
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.parallel
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.jaxb
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.launch
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau.papiselect
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau.perfdmf
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau.selinst
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau.selinstfort
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.tau.ui
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.toolopts
%pom_disable_module tools/gem/org.eclipse.ptp.gem
%pom_disable_module tools/gem/org.eclipse.ptp.gem.help
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.common
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.doc.user
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.mpi.analysis
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.mpi.analysis.cdt
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.mpi.core
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.mpi.fortran
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openacc
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openacc.fortran
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.analysis
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.core
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.fortran
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.ui.pv
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openshmem
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.upc
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.wizards

# Remove dep on ant-trax
%pom_remove_dep ant:ant-trax rms/org.eclipse.ptp.rm.lml.da.server

# Remove bundled binaries
rm -r releng/org.eclipse.ptp.linux/os/linux
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
export JAVA_HOME=%{java_home}
export PATH=/usr/bin:$PATH
export MAVEN_OPTS="-XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"
# Build the sdm binary
pushd debug/org.eclipse.ptp.debug.sdm
export CFLAGS="%{optflags} -fno-strict-overflow"
sh BUILD
popd
mkdir -p releng/org.eclipse.ptp.linux/os/linux/%{_arch}
cp -p debug/org.eclipse.ptp.debug.sdm/bin/sdm releng/org.eclipse.ptp.linux/os/linux/%{_arch}/sdm

# Build the project
%mvn_build -j -- -DforceContextQualifier=%{ptp_qualifier}
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
mkdir -p %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/{features,plugins}

# ptp
for jar in releng/org.eclipse.ptp.repo/target/repository/features/*.jar
do
  name=$(basename $jar .jar)
  # Skip external components
  [ ${name/org.eclipse.photran/} != $name ] && continue
  [ ${name/org.eclipse.rephraserengine/} != $name ] && continue
  [ ${name/org.eclipse.remote/} != $name ] && continue
  unzip -u -d %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/features/$name $jar
  files="files.${name%.*}"
  if [[ $name == org.eclipse.ptp_%{version}.* ]]
  then
    # Group the core features
    sed -ne '/id=/s#.*"\(.*\)"#%{eclipse_base}/dropins/ptp/eclipse/features/\1_*#gp' %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/features/$name/feature.xml | tail -n +2 > $files
    # Add the plugins for those features
    sed -ne '/id=/s#.*"\(.*\)"#\1#gp' %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/features/$name/feature.xml | tail -n +2 | while read f
    do
      [ $f == org.eclipse.ptp ] && continue
      sed -ne '/id=/s#.*"\(.*\)"#%{eclipse_base}/dropins/ptp/eclipse/plugins/\1_*.jar#gp' %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/features/${f}_*/feature.xml | tail -n +2 >> $files
    done
    sort -u -o $files $files
  else
    sed -ne '/id=/s#.*"\(.*\)"#%{eclipse_base}/dropins/ptp/eclipse/plugins/\1_*.jar#gp' %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/features/$name/feature.xml | tail -n +2 > $files
  fi
done
cp -u releng/org.eclipse.ptp.repo/target/repository/plugins/*.jar \
   %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/plugins/

# Remove external plugins
#rm %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/plugins/org.eclipse.photran*

# Remove disabled modules from filelist
sed -i -e '\,plugins/org.eclipse.ptp.remote.remotetools_,d' \
       -e '\,plugins/org.eclipse.ptp.remote_,d' \
       -e '\,plugins/org.eclipse.ptp.remotetools_,d' files.*

# Install sdm binary so debuginfo is created
mkdir -p %{buildroot}%{_libdir}/ptp
cp -p debug/org.eclipse.ptp.debug.sdm/bin/sdm %{buildroot}%{_libdir}/ptp/
%{?scl:EOF}


%files -f files.org.eclipse.ptp_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%dir %{eclipse_base}/dropins/ptp
%dir %{eclipse_base}/dropins/ptp/eclipse
%dir %{eclipse_base}/dropins/ptp/eclipse/features
%dir %{eclipse_base}/dropins/ptp/eclipse/plugins

%files master
%doc releng/org.eclipse.ptp-feature/epl-v10.html

%files core-source -f files.org.eclipse.ptp.core.source_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%{eclipse_base}/dropins/ptp/eclipse/features/org.eclipse.ptp.core.source_*

%files rm-contrib -f files.org.eclipse.ptp.rm.jaxb.contrib_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%{eclipse_base}/dropins/ptp/eclipse/features/org.eclipse.ptp.rm.jaxb.contrib_*

%files sci -f files.org.eclipse.ptp.sci_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%{eclipse_base}/dropins/ptp/eclipse/features/org.eclipse.ptp.sci_*

%files sdk -f files.org.eclipse.ptp.sdk_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%{eclipse_base}/dropins/ptp/eclipse/features/org.eclipse.ptp.sdk_*

%files sdm -f files.org.eclipse.ptp.debug.sdm_%{version}
%doc releng/org.eclipse.ptp-feature/epl-v10.html
%{eclipse_base}/dropins/ptp/eclipse/features/org.eclipse.ptp.debug.sdm_*
%{_libdir}/ptp/

%changelog
* Mon Feb 29 2016 Mat Booth <mat.booth@redhat.com> - 9.0.1-1.2
- Rebuild 2016-02-29

* Mon Feb 29 2016 Mat Booth <mat.booth@redhat.com> - 9.0.1-1.1
- Import latest from Fedora

* Thu Feb 04 2016 Sopot Cela <scela@redhat.com> - 9.0.1-1
- Upgrade to upstrea 9.0.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 9.0.0-1.3
- Disable optimisation that generates no-strict-overflow warning instead of
  simply disabling the warning

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 9.0.0-1.2
- Add -Wno-strict-overflow flag to prevent unnecessary warning

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 9.0.0-1.1
- Fix broken requires on CDT

* Wed Jul 15 2015 Jeff Johnston <jjohnstn@redhat.com> 9.0.0-1
- Import from F23 and SCL-ize.
- Trim out components that don't have dependencies in DTS.
