#! /usr/bin/env python

import os
import sys
import optparse
import datetime
import subprocess
import io

from glob import glob

usage = "usage: python submit_crab_miniaod.py -i lists/list_MINIAOD_pps.csv -o /afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/MINIAOD_2022_12_12 -t crab_miniaod_template.py\nThe input csv list should look like this:\n umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER\n umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER\n ..."

parser = optparse.OptionParser(usage)

parser.add_option("-i", "--inputlist", dest="inputlist",
                  help="input list with samples (csv).")

parser.add_option("-o", "--output", dest="outputdir",
                  help="the directory contains the output of the program. Can be AFS or EOS directory.")

parser.add_option("-t", "--template", dest="template",
                  help="crab template")

(opt, args) = parser.parse_args()

if not opt.inputlist:
    parser.error('input list not provided')

if not opt.outputdir:
    parser.error('output dir not provided')

if not opt.template:
    parser.error('crab template not provided')

################################################


print ("mkdir -p "+opt.outputdir)
os.system("mkdir -p "+opt.outputdir)

for line in open(opt.inputlist):

    if ("#" in line):
        continue

    ## Create crab file
    line = line.strip()
    #print line

    samplename = line.split(",")[0]
    inputdatasetname = line.split(",")[1]
    #print samplename, inputdatasetname

    workarea = opt.outputdir+"/"+"crabDir"+"_"+samplename
    #print workarea
    os.system("mkdir -p "+workarea)

    crabFileName = workarea+"/"+"crab_miniaod.py"

    fin = open(opt.template, "rt")
    fout = open(crabFileName, "wt")
    for ll in fin:
        if("DATASETNAME" in ll):
            fout.write(ll.replace('DATASETNAME', "\"" + samplename + "\""))
        elif("INPUTDATASET" in ll):
            fout.write(ll.replace('INPUTDATASET', "\"" + inputdatasetname + "\""))
        elif("WORKAREA" in ll):
            fout.write(ll.replace('WORKAREA', "\"" + workarea + "\""))
        else:
            fout.write(ll)
    fin.close()
    fout.close()

    print "Created "+crabFileName

    
    ## Submit crab job
    command = "crab submit -c " + crabFileName
    print command
    os.system(command)
