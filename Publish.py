import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("PickEvent")
process.source = cms.Source ("PoolSource",
	  fileNames = cms.untracked.vstring ('file:step1_GEN.root'),
)


process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32 (-1)
)


process.Out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string ('file:step1_GEN_PUB.root')
)


process.end = cms.EndPath(process.Out)
