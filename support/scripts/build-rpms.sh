#!/bin/bash
# set -eux
#
# Script to find the RPM sources and iteratively build them
#
###########################################################################
PROGNAME="$( basename "${0}" )"
DEBUG=${DEBUG:-false}
CONTAINERTOP="/project/rpmbuild"
export CONTAINERTOP

# Error handler function
function logIt {
   local ERRSTR="${1}"
   local SCRIPTEXIT=${2:-1}

   ERRCTR=$((ERRCTR+=1))

   if [[ ${DEBUG} == true ]]
   then
      # Our output channels
      echo "Debug: ${ERRSTR}"
   fi

   if [[ ${SCRIPTEXIT} -ne 0 ]]
   then
      logger -i -t "${PROGNAME}" -p user.crit "${ERRSTR}"
      exit ${SCRIPTEXIT}
   fi

}


# Iterate the spec files and build them
for SPEC in $( find ${CONTAINERTOP} -name "*.spec" )
do
   rpmbuild --define="_topdir ${CONTAINERTOP}" \
     --define="my_privroot privtest" \
     --define "my_urlroot yum.private-domain.local" \
     --define="my_pathroot yum/centos" \
     -ba ${SPEC} && logIt "The rpm-build operation succeeded" 0 \
       || logIt "The rpm-build operation failed" 1
done
