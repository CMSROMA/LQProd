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

Edit .dat files with the CMSSW release used for NanoAODv9:
write   
```
NanoAODv2       10_6_27  
```
in all these .dat files:
```
packages/setups/Full/setup_RunIISummer20UL16.dat
packages/setups/Full/setup_RunIISummer20UL16APV.dat 
packages/setups/Full/setup_RunIISummer20UL17.dat 
packages/setups/Full/setup_RunIISummer20UL18.dat
```
(Note: keep the name "NanoAODv2" since I don't know if/where it is hardcoded)

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