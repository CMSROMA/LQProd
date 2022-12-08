#! /usr/bin/env python

import os
import sys
import optparse
import datetime
import subprocess
import io

from glob import glob

usage = "usage: python submit_crab_publish.py -i lists/list_GEN_publish.csv -o /afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/PublishGEN_2022_12_07 -t crab_publish_template.py\nThe input csv list should look like this: \nLeptonInducedLQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M700_Lambda1p0_2018__GEN.list\nLeptonInducedLQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M1000_Lambda1p0_2018__GEN.list\n..."

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
    listfile = line.split(",")[1]
    #print samplename, listfile

    workarea = opt.outputdir+"/"+"crabDir"+"_"+samplename
    #print workarea
    os.system("mkdir -p "+workarea)

    crabFileName = workarea+"/"+"crab_publish.py"

    fin = open(opt.template, "rt")
    fout = open(crabFileName, "wt")
    for ll in fin:
        if("DATASETNAME" in ll):
            fout.write(ll.replace('DATASETNAME', "\"" + samplename + "\""))
        elif("INPUTLIST" in ll):
            fout.write(ll.replace('INPUTLIST', "\"" + listfile + "\""))
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
