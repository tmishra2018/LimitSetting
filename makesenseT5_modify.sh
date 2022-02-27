#!/bin/bash

export jobNumber=$1
export name_list="cardsSplitted/x${1}"

cd ${_CONDOR_SCRATCH_DIR}
ls -ltrh

echo "source /cvmfs/cms.cern.ch/cmsset_default.sh"
source /cvmfs/cms.cern.ch/cmsset_default.sh

echo "scramv1 project CMSSW CMSSW_10_2_22"
scramv1 project CMSSW CMSSW_10_2_22

echo "cd CMSSW_10_2_22/src/"
cd CMSSW_10_2_22/src/

echo "eval `scramv1 runtime -sh`"
eval `scramv1 runtime -sh`
tar -zxvf ../../higgsCombine.tar.gz
scram b clean
scram b -j4

mv ../../cardsSplitted HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

echo ' ' $name_list 

while IFS= read -r line
do 
	rm filelist
	echo "$line" > filelist
	gluino=`awk -F '[^0-9]*' '{print $4}' filelist`
	chargino=`awk -F '[^0-9]*' '{print $5}' filelist`
	echo "${gluino}"
	echo "${chargino}"
	xrdcp -f root://cmseos.fnal.gov//store/user/tmishra/CombinedLimit/Sensitive_myFile/cardsPlan5/counting_t5Wg_${gluino}_${chargino}.txt .
	combine -M AsymptoticLimits counting_t5Wg_${gluino}_${chargino}.txt -t -1 --expectSignal=1 -n t5wg | tee limit_${gluino}_${chargino}.txt
	xrdcp -f limit_${gluino}_${chargino}.txt root://cmseos.fnal.gov//store/user/tmishra/CombinedLimit/Sensitive_myFile/limitsPlan5
	rm counting_t5Wg_${gluino}_${chargino}.txt
done < "$name_list"

cd ${_CONDOR_SCRATCH_DIR} 
rm -rf CMSSW_10_2_22
echo "End.. Bye now.."
