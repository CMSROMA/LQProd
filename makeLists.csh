#!/bin/bash

set Mass = (700 1000 2000 3000 4000 5000)

foreach i ($Mass)
setenv MYDIR /eos/cms/store/group/phys_exotica/lq-LQ-lq/pakrap/messedUpIDs/GEN/fixedL/LeptonInducedLQ_umu_M${i}_Lambda1p0__GEN
ls $MYDIR | grep root | awk '{print "root://xrootd-cms.infn.it//'$MYDIR'/"$0}' > lists/LeptonInducedLQ_umu_M${i}_Lambda1p0_2018__GEN.list
setenv NUMEVT `less lists/LeptonInducedLQ_umu_M${i}_Lambda1p0_2018__GEN.list | wc -l`
echo Created new list $PWD/lists/LeptonInducedLQ_umu_M${i}_Lambda1p0_2018__GEN.list with $NUMEVT files
end
