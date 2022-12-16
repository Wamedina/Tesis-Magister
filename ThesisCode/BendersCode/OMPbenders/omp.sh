#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/ibm/ILOG/CPLEX_Studio129/cplex/bin/x86-64_linux/

export CPLEX_VERSION=1290



if [ "$CPLEX_VERSION" == "1290" ]
then
	bin/OMP_SOLVER_C1290 $*
elif [ "$CPLEX_VERSION" == "1280" ]
then
	bin/OMP_SOLVER_C1280 $*
else
	echo "CPLEX version ($CPLEX_VERSION) not supported"
	exit 1
fi


