%{?scl:%scl_package eclipse-ptp}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 4

%global eclipse_base            %{_datadir}/eclipse
%global cdtreq                  1:9.0.0
%global pdereq                  1:4.2.0
%global ptp_qualifier           201606021530
%global ptp_git_tag             PTP_9_1_0

%ifarch %{ix86}
    %global eclipse_arch x86
%endif
%ifarch %{arm}
    %global eclipse_arch arm
%endif
%ifarch ppc64 ppc64p7
    %global eclipse_arch ppc64
%endif
%ifarch s390 s390x ppc x86_64 aarch64 ppc64le
    %global eclipse_arch %{_arch}
%endif

Summary:        Eclipse Parallel Tools Platform
Name:           %{?scl_prefix}eclipse-ptp
Version:        9.1.0
Release:        1.%{baserelease}%{?dist}
License:        EPL
Group:          Development/Tools
URL:            http://www.eclipse.org/ptp

# The following tarballs were downloaded from the git repositories
Source0:        http://git.eclipse.org/c/ptp/org.eclipse.ptp.git/snapshot/org.eclipse.ptp-%{ptp_git_tag}.tar.xz
# To help generate the needed Requires
Source3:        finddeps.sh
Patch0:         eclipse-ptp-trim.patch

# Remove some unneeded dependencies
BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}maven-antrun-plugin
BuildRequires:  %{?scl_prefix_maven}maven-plugin-build-helper
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
Provides:       %{name}-etfw-ppw = %{version}-%{release}
Obsoletes:      %{name}-etfw-ppw < %{version}-%{release}
Provides:       %{name}-gig = %{version}-%{release}
Obsoletes:      %{name}-gig < %{version}-%{release}
Provides:       %{name}-pldt = %{version}-%{release}
Obsoletes:      %{name}-pldt < %{version}-%{release}
Provides:       %{name}-pldt-openacc = %{version}-%{release}
Obsoletes:      %{name}-pldt-openacc < %{version}-%{release}
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
Requires:       %{name} = %{version}-%{release}

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

%patch0 -p0

# Fix target platform environments
TYCHO_ENV="<environment><os>linux</os><ws>gtk</ws><arch>%{eclipse_arch}</arch></environment>"
%pom_xpath_set "pom:configuration/pom:environments" "$TYCHO_ENV"
%pom_xpath_remove "pom:configuration/pom:target"

# Disable Fortran support bits
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
%pom_disable_module tools/etfw/org.eclipse.ptp.etfw.feedback.perfsuite.doc.user
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
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openacc.core
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openacc.fortran
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openacc.ui
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.analysis
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.core
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.fortran
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openmp.ui.pv
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.openshmem
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.upc
%pom_disable_module tools/pldt/org.eclipse.ptp.pldt.wizards
%pom_xpath_remove "feature[@id='org.eclipse.ptp.fortran']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.gem']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.pldt.upc']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.pldt.fortran']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.etfw.tau']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.etfw.tau.fortran']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.etfw.feedback.perfsuite']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.ptp.rdt.sync.fortran']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.photran']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.photran.intel']" releng/org.eclipse.ptp.repo/category.xml
%pom_xpath_remove "feature[@id='org.eclipse.photran.xlf']" releng/org.eclipse.ptp.repo/category.xml

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
export MAVEN_OPTS="-Xmx1024m -XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"
# Build the sdm binary
pushd debug/org.eclipse.ptp.debug.sdm
export CFLAGS="%{optflags} -fno-strict-overflow"
sh BUILD
make clean
popd
mkdir -p releng/org.eclipse.ptp.linux/os/linux/%{_arch}
cp -p debug/org.eclipse.ptp.debug.sdm/bin/sdm releng/org.eclipse.ptp.linux/os/linux/%{_arch}/sdm
echo -e "Eclipse-BundleShape: dir\n\n" >> releng/org.eclipse.ptp.linux/META-INF/MANIFEST.MF

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

# Remove disabled modules from filelist
sed -i -e '\,plugins/org.eclipse.ptp.remote.remotetools_,d' \
       -e '\,plugins/org.eclipse.ptp.remote_,d' \
       -e '\,plugins/org.eclipse.ptp.remotetools_,d' files.*

# Install sdm binary so debuginfo is created
pushd %{buildroot}%{eclipse_base}/dropins/ptp/eclipse/plugins/
sdm=$(ls org.eclipse.ptp.linux_*)
unzip -d ${sdm%.jar} $sdm
rm $sdm
popd
sed -i -e '/plugins\/org\.eclipse\.ptp\.linux_/s/\.jar//' files.*
mkdir -p %{buildroot}%{_libdir}/ptp
ln -s %{eclipse_base}/dropins/ptp/eclipse/plugins/${sdm%.jar}/os/linux/%{eclipse_arch}/sdm \
  %{buildroot}%{_libdir}/ptp/
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
* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 9.1.0-1.4
- Remove exploded jar

* Mon Aug 01 2016 Mat Booth <mat.booth@redhat.com> - 9.1.0-1.3
- Don't package intermediate artifacts, fix binary stripping problems
- Disable compiler optimisation that make assumptions about signed integer
  overflows

* Fri Jul 29 2016 Mat Booth <mat.booth@redhat.com> - 9.1.0-1.2
- Disable all Fortran support bits

* Fri Jul 29 2016 Mat Booth <mat.booth@redhat.com> - 9.1.0-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Jun 22 2016 Mat Booth <mat.booth@redhat.com> - 9.1.0-1
- Update to Neon release

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 9.0.2-3
- Add missing build-requires

* Tue May 03 2016 Mat Booth <mat.booth@redhat.com> - 9.0.2-2
- Backport patch to compensate for API changes in CDT
- Use global instead of define for macros
- Increase max heap used in build for arm

* Mon Apr 25 2016 Alexander Kurtakov <akurtako@redhat.com> 9.0.2-1
- Update to released version.
- Add patch to remove useless dependency.

* Thu Mar 03 2016 Sopot Cela <scela@redhat.com> - 9.0.2-0.2.git88a46f8
- Fixed ptp qualifier

* Thu Mar 03 2016 Sopot Cela <scela@redhat.com> - 9.0.2-0.1.git88a46f8
- Upgrade for Mars.2 release

* Thu Feb 04 2016 Sopot Cela <scela@redhat.com> - 9.0.1-1
- Upgrade to upstrea 9.0.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Alexander Kurtakov <akurtako@redhat.com> 9.0.0-1
- Update to 9.0.0 final.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.0-0.4.gitf349d01
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 5 2015 Alexander Kurtakov <akurtako@redhat.com> 9.0.0-0.3.gitf349d01
- Restore build_id to not make noarch packages have different content.

* Thu Jun 4 2015 Alexander Kurtakov <akurtako@redhat.com> 9.0.0-0.2.gitf349d01
- Drop old build_id and let jgit generate one.
- Build with mvn_build.

* Wed Jun 3 2015 Alexander Kurtakov <akurtako@redhat.com> 9.0.0-0.1.gitf349d01
- Update to 9.0 prerelase to allow compilation against Mars.

* Wed Mar 25 2015 Orion Poplawski <orion@cora.nwra.com> 8.1.1-2
- Update upstream source to fix compilation against CDT
- Use upstream patch for jgit 3.7.0 compatibility
- Remove unavailable components from repository build

* Mon Mar 9 2015 Orion Poplawski <orion@cora.nwra.com> 8.1.1-1
- Update to 8.1.1

* Thu Jan 15 2015 Alexander Kurtakov <akurtako@redhat.com> 8.1.0-3
- Adapt to egit changes.

* Tue Dec 9 2014 Alexander Kurtakov <akurtako@redhat.com> 8.1.0-2
- Fix build.

* Wed Oct 15 2014 Orion Poplawski <orion@cora.nwra.com> 8.1.0-1
- Update to 8.1.0

* Wed Aug 20 2014 Orion Poplawski <orion@cora.nwra.com> 8.0.1-1
- Update to 8.0.1

* Tue Aug 19 2014 Mat Booth <mat.booth@redhat.com> - 8.0.0-2
- Reinstate forceContextQualifier

* Tue Aug 19 2014 Mat Booth <mat.booth@redhat.com> - 8.0.0-1
- Update to latest upstream release
- Fix FTBFS rhbz #1106199

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 8 2014 Orion Poplawski <orion@cora.nwra.com> 7.0.4-1
- Update to 7.0.4

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> 7.0.3-1
- Update to 7.0.3
- Drop deps patch and sysmon changes - removed upstream

* Sat Aug 3 2013 Orion Poplawski <orion@cora.nwra.com> 7.0.2-1
- Update to 7.0.2

* Tue Jul 23 2013 Krzysztof Daniel <kdaniel@redhat.com> 7.0.1-2
- Fix build on ARM (RHBZ#987438).

* Mon Jul 8 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.1-1
- Update to 7.0.1
- Use bz2 compressed sources
- Drop docbuild patch, fixed upstream
- Drop gig sub-package for now

* Tue May 14 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.6.20130514git845dccd
- Update to latest git
- Fix requires corruption

* Sat May 11 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.5.20130511git71cc5a7
- Update to latest git

* Fri May 10 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.5.20130510gitd11d96c
- Update to latest git

* Tue May 7 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.4.20130502gitbd8fbd1
- Drop tycho-extras repository sed - fixed in tycho-extras-0.17.0-2

* Mon May 6 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.3.20130502gitbd8fbd1
- Add patch to add repository info for tycho-eclipserun-plugin
- Add patch and sed to fix doc.isv build

* Thu May 2 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.3.20130502gitbd8fbd1
- Update to latest git
- Drop photran build - now in separate package
- Add patch to fix parent pom paths

* Tue Apr 23 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.2.20130422git
- Update to git master
- Build sdm executable and install it so that debuginfo is generated

* Tue Apr 9 2013 Orion Poplawski <orion@cora.nwra.com> - 7.0.0-0.1.20130409git
- Update to git master

* Mon Apr 8 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.5-1
- Update to PTP 6.0.5, photran 8.0.5
- Remove rdt.remotetools feature beause we are unable to build
  remotejars
- Hande tycho versions automatically

* Fri Feb 8 2013 Alexander Kurtakov <akurtako@redhat.com> 6.0.3-4
- Remove a lot of old stuff.

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 6.0.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Feb 4 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.3-2
- Obsolete/Provide pldt-openacc

* Tue Nov 6 2012 Orion Poplawski <orion@cora.nwra.com> - 6.0.3-1
- Update to PTP 6.0.3, photran 8.0.3
- Use maven/tycho for building, major rework of spec
- Add patch remove ant-trax dependency, fix maven jdk tools.jar dep
- Drop overrides patch
- Move pldt and rdt-sync into the main package
- Add fortran meta sub-package to bring in Fortran support
- Drop cdt-compilers, rdt-sdk, and rdt-xlc-sdk sub-packages

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-0.3.junom6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-0.2.junom6
- Add some new features
- Rework buildid to avoid photran build duplication

* Thu Apr 19 2012 Jeff Johnston <jjohnstn@redhat.com> - 6.0.0-0.1.junom6
- Update to PTP Juno M6 (6.0.0 pre-release)

* Fri Apr 13 2012 Orion Poplawski <orion@cora.nwra.com> - 5.0.7-1
- Update to PTP 5.0.7, photran 7.0.7
- Add %%{pdebuild} macro

* Tue Mar 13 2012 Orion Poplawski <orion@cora.nwra.com> - 5.0.6-1
- Update to PTP 5.0.6, photran 7.0.6

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 5.0.5-1
- Update to PTP 5.0.5, photran 7.0.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Orion Poplawski <orion@cora.nwra.com> - 5.0.4-1
- Update to PTP 5.0.4, photran 7.0.4
- Add pldt-fortran and rm-contrib sub-packages
- Update makesource.sh/spec/finddeps.sh to use git archive
- Unpack cdtdb-4.0.3-eclipse.jar from tar archive
- Remove orbitDeps usage, not needed
- Remove license feature hack, not needed
- Drop defattr, BuildRoot, clean
- Actually build master package

* Tue Oct 25 2011 Orion Poplawski <orion@cora.nwra.com> - 5.0.3-1
- Update to PTP 5.0.3, photran 7.0.3

* Thu Oct 20 2011 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-1
- Update to PTP 5.0.2, photran 7.0.2
- Update deps patch
- Add jaxb to feature build before ptp

* Tue Sep 6 2011 Orion Poplawski <orion@cora.nwra.com> - 5.0.1-2
- Fixup some dependencies

* Wed Aug 31 2011 Orion Poplawski <orion@cora.nwra.com> - 5.0.1-1
- Update to PTP 5.0.1, photran 7.0.1
- Bump CDT and PDE requirement
- Work around issue with pdebuild shared license feature
- Add BR on ws-jaxme, add jaxmeapi and xml-commons-apis to orbitDeps
- Add patch to remove unneeded dependencies
- Add BR on eclipse-jgit
- Add sdk and photran components to ptp-master
- Add rdt-sync, rdt-sync-fortran, and sdk sub-packages
- Fixup some requires
- Improve the finddeps.sh utility script

* Wed May 18 2011 Orion Poplawski <orion@cora.nwra.com> - 4.0.7-1
- Update to PTP 4.0.7, photran 6.0.7

* Wed Mar 2 2011 Orion Poplawski <orion@cora.nwra.com> - 4.0.6-1
- Update to PTP 4.0.6, photran 6.0.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.5-1
- Update to PTP 4.0.5, photran 6.0.5

* Fri Nov 5 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.4-1
- Update to PTP 4.0.4, photran 6.0.4

* Fri Oct 8 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-3
- Fix photran cdt requirement

* Mon Sep 27 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-2
- Make rdt provide/obsolete rdt-remotetools

* Mon Sep 20 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-1
- Update to PTP 4.0.3, photran 6.0.3
- Drop rdt-remotetools now part of rdt

* Fri Sep 3 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-0.3.RC2c
- Fix changelog version

* Thu Sep 2 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-0.2.RC2b
- Fix remote-rse deps

* Wed Sep 1 2010 Orion Poplawski <orion@cora.nwra.com> - 4.0.3-0.1.v201009010938
- Update snapshot
- Re-work build

* Tue Jun 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.2-0.1.v201004302110
- Update snapshot
- Add patch from cvs to fix exception in MPI project wizard

* Fri May 28 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.2-1
- Update to 3.0.1 final
- Rework dependencies

* Mon Feb 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.1-0.4.v201002011019
- Update snapshot

* Tue Jan 26 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.1-0.3.v201001251825
- Update snapshot

* Thu Jan 21 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.1-0.2.v201001152110
- Make photran versions 5.0.1, rephraserengine 1.0.1

* Thu Jan 21 2010 Orion Poplawski <orion@cora.nwra.com> - 3.0.1-0.1.v201001152110
- Update to 3.0.1 snapshot
- Split package
- Make noarch

* Mon Dec 7 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-1
- Update to 3.0.0 final

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-0.5.200911091447
- Update to 200911091447

* Tue Oct 27 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-0.4.200910232110
- Update to 200910232110

* Thu Oct 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-0.3.200910162113
- Update to 200910162113

* Fri Oct 16 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-0.2.200910091648
- Remove gcj - eclipse is not built with it.

* Thu Oct 15 2009 Orion Poplawski <orion@cora.nwra.com> - 3.0.0-0.1.200910091648
- Initial package
