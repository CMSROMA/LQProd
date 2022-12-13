# Setup area for private production

```
mkdir privateMCProd
cd privateMCProd
git clone ssh://git@gitlab.cern.ch:7999/cms-exo-mci/EXO-MCsampleProductions.git
cd EXO-MCsampleProductions
```

Update necessary for NanoAODv9.

Edit the file packages/FullSimulation/NanoAODv2/skeleton/cmsdriver_NanoAODv2.dat to use NanoAODv9 configuration:
```
RunIISummer20UL16       --conditions 106X_mcRun2_asymptotic_v17 --era Run2_2016,run2_nanoAOD_106Xv2
RunIISummer20UL16APV    --conditions 106X_mcRun2_asymptotic_preVFP_v11 --era Run2_2016_HIPM,run2_nanoAOD_106Xv2
RunIISummer20UL17       --conditions 106X_mc2017_realistic_v9 --era Run2_2017,run2_nanoAOD_106Xv2
RunIISummer20UL18       --conditions 106X_upgrade2018_realistic_v16_L1v1 --era Run2_2018,run2_nanoAOD_106Xv2
```
(Info about NanoAODv9 at https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv9)

Edit .dat files with the CMSSW release used for NanoAODv9 and MiniAODv2:
write   
```
MiniAOD 10_6_20
NanoAODv2 10_6_27  
```
in all these .dat files:
```
packages/setups/Full/setup_RunIISummer20UL16.dat
packages/setups/Full/setup_RunIISummer20UL16APV.dat 
packages/setups/Full/setup_RunIISummer20UL17.dat 
packages/setups/Full/setup_RunIISummer20UL18.dat
```
(Note: keep the name "MiniAOD" and "NanoAODv2" since I don't know if/where it is hardcoded in the rest of the scripts)

Launch the setup
```
python setup.py
```

You will get this question at the beginning:
``` 
What is your T2/T3 storage site [T2_CH_CERN,T3_KR_KNU,T2_US_FNAL,..]? 
```
Reply with your storage site, i.e. T2_IT_Rome.
The you'll see:
```
[...] Fetching CMSSW releases for Ultra Legacy sample production [...]
```
(Note: usually takes 10 min. lxplus to complete.)

Optional check. Test if you have writing permission on the storage site (i.e. T2_IT_Rome):
```
source /cvmfs/cms.cern.ch/crab3/crab.csh
source /cvmfs/cms.cern.ch/cmsset_default.csh
cmsrel CMSSW_10_6_28
cd CMSSW_10_6_28/src/
cmsenv
crab checkwrite --site=T2_IT_Rome
```

# Publish GEN files on DAS

The first step is actually to produce GEN files and store them on eos at CERN (for example 
following the instructions reported at https://github.com/CMSROMA/LQGen).

Then we need to publish these GEN files stored on eos into DBS.

From EXO-MCsampleProductions:
```
git clone git@github.com:CMSROMA/LQProd.git
cd LQProd
scram p -n CMSSW_10_6_28 CMSSW CMSSW_10_6_28
cd CMSSW_10_6_28/src
cmsenv
cd ../../
```

Setup crab:
```
source /cvmfs/cms.cern.ch/crab3/crab.csh
voms-proxy-init -voms cms
```

Create a list with GEN files (example lists/list_GEN_publish.csv): 
```
umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M700_Lambda1p0_2018__GEN.list
umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M1000_Lambda1p0_2018__GEN.list
umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M2000_Lambda1p0_2018__GEN.list
umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M3000_Lambda1p0_2018__GEN.list
umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M4000_Lambda1p0_2018__GEN.list
umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN,/afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/lists/LeptonInducedLQ_umu_M5000_Lambda1p0_2018__GEN.list
```

each .list file in the csv file should include the list of root files of the GEN step. Example:

```
root://xrootd-cms.infn.it///eos/cms/store/group/phys_exotica/lq-LQ-lq/pakrap/messedUpIDs/GEN/fixedL/LeptonInducedLQ_umu_M3000_Lambda1p0__GEN//LeptonInducedLQ_umu_M3000_Lambda1p0_mod__1.root
root://xrootd-cms.infn.it///eos/cms/store/group/phys_exotica/lq-LQ-lq/pakrap/messedUpIDs/GEN/fixedL/LeptonInducedLQ_umu_M3000_Lambda1p0__GEN//LeptonInducedLQ_umu_M3000_Lambda1p0_mod__2.root
...
...
```

To create these lists of root files you can do it by-hand or can use a script:
```
source makeLists.csh
```
(NOTE: this is just an example, you'll have to edit/adapt the script for your needs.)

Edit crab template if needed 
```
crab_publish_template.py
```

Submit the job and publish GEN files on DAS. From LQProd folder:
```
python submit_crab_publish.py -i lists/list_GEN_publish.csv -o /afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/PublishGEN_2022_12_08 -t crab_publish_template.py
```

You can use the standard crab commands to check the status of the job. For examples:
```
crab status -d PublishGEN_2022_12_08/crabDir_umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/crab_umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/
```

The output GEN files will be atuomatically published on DAS (https://cmsweb.cern.ch/das/). 
Suggest to go directly on DAS and search for the dataset string name in the "prod/phys03" dbs instance, i.e.:
```
dataset=/*umu_LQ_umu**v2*/*/*
``` 
and you'll get the list, i.e.:
```
/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-ea546314c142f997f28c3868a5d30f0b/USER
/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-35f9ffa266f026863f894e10651a0d02/USER
/umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-17918999a0db358f128e81b2894a82c2/USER
/umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-83c28d819a6bc2070f2a59c788d94d20/USER
/umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-548e066aee101d8e548612b3094f690f/USER
/umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-99e593f673f8e0e893ad3902f8d59617/USER
```

# SIM step

From EXO-MCsampleProductions
```
cd  FullSimulation/RunIISummer20UL18/SIM__CMSSW_10_6_17_patch1/src/
source /cvmfs/cms.cern.ch/crab3/crab.csh
voms-proxy-init -voms cms
```

Create a csv list of GEN datasets indicating the name of the output dataset in the first position and the input dataset name in the second position, separate by a ",".

Example:
```
list_SIM_publish.csv 
umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-ea546314c142f997f28c3868a5d30f0b/USER
umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-35f9ffa266f026863f894e10651a0d02/USER
umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-17918999a0db358f128e81b2894a82c2/USER
umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-83c28d819a6bc2070f2a59c788d94d20/USER
umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-548e066aee101d8e548612b3094f690f/USER
umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_SIM,/umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN-99e593f673f8e0e893ad3902f8d59617/USER
```

Edit config_SIM.py, comment out these two lines:
```
  #if checkDASInput.checkDASInput(inputdataset,step,campaign):                                                                                                                        
  #  sys.exit() 
``` 

```
python config_SIM.py list_SIM_publish.csv
```

Setup CRAB in bash:
```
bash
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -voms cms
```

Submit jobs:
```
source submit_crab_list_SIM_publish.sh
```

When the job are finished get from DAS the list of the datasets:
```
/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
/umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
/umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
/umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
/umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_SIM-128efeffab8ceb577467d0e58be013b1/USER
```

# DIGIPremix -> HLT -> RECO -> MiniAOD steps

Repeat the same procedure described above for SIM for the following steps:
DIGIPremix
HLT
RECO
MiniAOD

# Add PPS info to MiniAOD

```
cd EXO-MCsampleProductions/LQProd
scram p -n CMSSW_10_6_28_PPS CMSSW CMSSW_10_6_28
cd CMSSW_10_6_28_PPS/src
cmsenv
git cms-addpkg Validation/CTPPS
cp ../../CTPPSDirectProtonSimulation.cc Validation/CTPPS/plugins
cp ../../ctppsDirectProtonSimulation_cfi.py Validation/CTPPS/python
scram b
```

PPS settings:
```
git clone https://github.com/jan-kaspar/proton_simulation_validation.git
cd proton_simulation_validation/
git checkout 9b2cff77711484e90c2323008eedc8c717cfcc41
cd ../../
```

Choose the PPS configuration (from LQProd folder):
```
cp CMSSW_10_6_28_PPS/src/proton_simulation_validation/settings/MYSET/direct_simu_reco_cff.py .
```
where MYSET is one of these folders depending on the data taking period:
```
2016_postTS2 
2016_preTS2  
2017_postTS2 
2017_preTS2
```
If you are running on 2018 data you should do (from LQProd folder):
```
cp direct_simu_reco_2018_cff.py direct_simu_reco_cff.py
```

Setup crab:
```
source /cvmfs/cms.cern.ch/crab3/crab.csh
voms-proxy-init -voms cms
```

Create a list with MiniAOD datasets (example lists/list_MINIAOD_pps.csv):
```
umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M3000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS,/umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER
```

Edit crab template if needed:
```
crab_miniaod_template.py
```

Submit the job to add PPS info in MINIAOD. From LQProd folder:
```
python submit_crab_miniaod.py -i lists/list_MINIAOD_pps.csv -o /afs/cern.ch/work/s/santanas/Workspace/CMS/privateMCProd/EXO-MCsampleProductions/LQProd/MINIAOD_2022_12_12_v1 -t crab_miniaod_template.py
```

Suggest to go directly on DAS and search for the output dataset string name in the "prod/phys03" dbs instance, i.e.:
```
dataset=/*umu_LQ_umu_M*v2*/*MiniAODv2PPS*/*
```
and you'll get the list, i.e.:
```
/umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M1000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS-967f344fa947ec8b3140605365abc0aa/USER
/umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M2000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS-967f344fa947ec8b3140605365abc0aa/USER
/umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M4000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS-967f344fa947ec8b3140605365abc0aa/USER
/umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M5000_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS-967f344fa947ec8b3140605365abc0aa/USER
/umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_GEN/santanas-umu_LQ_umu_M700_Lambda1p0_2018_POWHEG_Herwig7_v2_MiniAODv2PPS-967f344fa947ec8b3140605365abc0aa/USER
```

# NanoAODv9 with PPS info

From EXO-MCsampleProductions:
```
cd FullSimulation/RunIISummer20UL18/NanoAODv2__CMSSW_10_6_27/src/
cmsenv
mv skeleton/ ../
mv config_NanoAODv2.py ../
git cms-addpkg PhysicsTools/NanoAOD
mv ../skeleton/ .
mv ../config_NanoAODv2.py  .
```

Copy modified files and compile:
```
cp ../../../../LQProd/genparticles_cff.py PhysicsTools/NanoAOD/python/
cp ../../../../LQProd/common_cff.py  PhysicsTools/NanoAOD/python/
cp ../../../../LQProd/nano_cff.py PhysicsTools/NanoAOD/python/
scram b
```
(compiling takes some minutes)

Then follow instructions as for SIM part to produce the NanoAOD datasets and publish them.

