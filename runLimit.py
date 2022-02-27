import os
from os import system, environ
import numpy as np

import os.path
from os import path

submitFileTT="""
universe              = vanilla
Executable            = makesenseT5_modify.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files  = higgsCombine.tar.gz, cardsSplitted
x509userproxy = $ENV(X509_USER_PROXY)
+JobFlavour            = "nextweek"
"""


os.system("rm logs/*")
os.system("rm /eos/uscms/store/user/tmishra/susy/*")

os.system("rm cardsSplitted/* DatacardList.txt")
os.system("mkdir -p cardsSplitted")

#Path = '/eos/uscms/store/user/tmishra/CombinedLimit/Sensitive_myFile/cardsANbins2/'
Path = '/eos/uscms/store/user/tmishra/CombinedLimit/Sensitive_myFile/cardsPlan5/'

os.system("ls -d -1 {}*  >> DatacardList.txt".format(Path))
os.system("cd cardsSplitted && split -l 10 -d -a 3 ../DatacardList.txt")

for i in range(0, 10):
               os.system("cd cardsSplitted && mv x00{} x{}".format(i,i))
for i in range(10, 100):
               os.system("cd cardsSplitted && mv x0{} x{}".format(i,i))

njobs = os.system("ls -l cardsSplitted | wc -l")
print njobs

njobs = 58
jobNumber = 0

while jobNumber < njobs-1 : 
	fileParts = [submitFileTT]
	#fileParts.append("Output    = logs/job{}.stdout\n".format(jobNumber))
	#fileParts.append("error     = logs/job{}.stderr\n".format(jobNumber))
    	#fileParts.append("Log       = logs/job{}.log\n".format(jobNumber))

	fileParts.append("Arguments = {}\n".format(jobNumber))
        fileParts.append("Queue \n \n")
        fout = open("/eos/uscms/store/user/tmishra/susy/condor_sub_{}.txt".format(jobNumber),"w")
        fout.write(''.join(fileParts))

        fout.close()
        fileParts.pop(-1)
        fileParts.pop(-1)
        command = 'condor_submit /eos/uscms/store/user/tmishra/susy/condor_sub_{}.txt'.format(jobNumber)
        del fileParts
        jobNumber+=1
	os.system(command)
