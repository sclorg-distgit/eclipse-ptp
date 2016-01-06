#!/bin/sh
# Figures out where the various features end up.
# Make sure you've done a fedpkg prep as well as installed 
# the packages

# Get some variables from the specfile
eval `awk '$1 == "%global" { print $2 "=" $3 }' eclipse-ptp.spec`

# Go through all of the features
find eclipse-ptp-${ptpver} -name feature.xml | sort | while read f
do
  fname=$(awk -F\" '/id=/ { print $2; exit }' $f)
  echo -n "Feature $fname "
  dir=`find /usr/*/eclipse -name ${fname}_\* | grep -F /features/`
  if [ -z "$dir" ]
  then
     echo -n "(not found): "
  else
    rpm=$(rpm -qf $dir --qf '%{NAME}\n')
    echo -n "($rpm): "
  fi
  pdeps=$(grep -F 'import plugin' $f | sed -e 's,.*plugin=",,' -e 's,".*,,' | while read p
  do
     jar=`find /usr/*/eclipse -name ${p}_\* | grep plugin`
     if [ -z "${jar}" ]
     then
        echo Searching for plugin $p found nothing 1>&2
        continue
     fi
     rpm=$(rpm -qf $jar --qf '%{NAME}\n')
     if [ "${rpm/ /}" != "${rpm}" ]
     then
        echo Searching for plugin $p found $jar in rpms $rpm 1>&2
     fi
     echo $rpm
  done | sort -u)
  fdeps=$(grep -F 'import feature' $f | sed -e 's,.*feature=",,' -e 's,".*,,' -e 's/_feature//' | while read p
  do
     jar=`find /usr/*/eclipse -name ${p}_\* | grep feature`
     if [ -z "${jar}" ]
     then
        echo Searching for feature $p found nothing 1>&2
        continue
     fi
     rpm=$(rpm -qf $jar --qf '%{NAME}\n')
     if [ "${rpm/ /}" != "${rpm}" ]
     then
        echo Searching for feature $p found $jar in rpms $rpm 1>&2
     fi
     echo $rpm
  done | sort -u)
  echo $pdeps / $fdeps
done

# Make sure no duplicates
find /usr/share/eclipse/dropins/org.eclipse.{ptp,photran}*/plugins -name \*.jar | sed s/_.*/_/ | sort -u | while read jardir
do
  jar=`basename $jardir`
  n=`find /usr/*/eclipse/dropins/org.eclipse.{ptp,photran}*/plugins -name ${jar}\* | wc -l`
  [ $n -gt 1 ] && echo $jar is duplicated && find /usr/*/eclipse/dropins/org.eclipse.{ptp,photran}*/plugins -name ${jar}\*
done
