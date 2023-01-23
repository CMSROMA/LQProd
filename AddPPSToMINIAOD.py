import FWCore.ParameterSet.Config as cms

# load common code
import direct_simu_reco_cff as profile
process = cms.Process('RERUNPPS', profile.era)
profile.LoadConfig(process)
profile.config.SetDefaults(process)

# minimal logger settings
process.MessageLogger = cms.Service("MessageLogger",
  statistics = cms.untracked.vstring(),
  destinations = cms.untracked.vstring('cerr'),
  cerr = cms.untracked.PSet(
    threshold = cms.untracked.string('WARNING')
  )
)

process.load('Configuration.EventContent.EventContent_cff')

# event source                                                                                                                  
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
      'file:/afs/cern.ch/work/m/mcampana/Lepto/EXO-MCsampleProductions/FullSimulation/RunIISummer20UL18/MiniAOD__CMSSW_10_6_20/src/SingleLQNLO_umuLQumu_M1000_Lambda1p0_MiniAOD.root'
  )
)

process.source.inputCommands = cms.untracked.vstring("keep *","drop *_ctppsProtons_*_RECO")

# number of events
process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(-1)
)

# acceptance plotter
process.ctppsAcceptancePlotter = cms.EDAnalyzer("CTPPSAcceptancePlotter",
  tagHepMC = cms.InputTag("generator", "unsmeared"),
  tagTracks = cms.InputTag("ctppsLocalTrackLiteProducer"),

  rpId_45_F = process.rpIds.rp_45_F,
  rpId_45_N = process.rpIds.rp_45_N,
  rpId_56_N = process.rpIds.rp_56_N,
  rpId_56_F = process.rpIds.rp_56_F,

  outputFile = cms.string("test_acceptance.root")
)

# distribution plotter
process.ctppsTrackDistributionPlotter = cms.EDAnalyzer("CTPPSTrackDistributionPlotter",
  tagTracks = cms.InputTag("ctppsLocalTrackLiteProducer"),
  x_pitch_pixels = cms.untracked.double(80E-3), # to be synchronised with process.ctppsDirectProtonSimulation.pitchPixelsVer

  rpId_45_F = process.rpIds.rp_45_F,
  rpId_45_N = process.rpIds.rp_45_N,
  rpId_56_N = process.rpIds.rp_56_N,
  rpId_56_F = process.rpIds.rp_56_F,

  outputFile = cms.string("test_acceptance_xy.root")
)

# update settings of beam-smearing module
process.beamDivergenceVtxGenerator.src = cms.InputTag("")
process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
    cms.InputTag("genPUProtons","genPUProtons"),
    cms.InputTag("prunedGenParticles")
)

#process.ctppsDirectProtonSimulation.genParticlesInputTag=cms.InputTag("prunedGenParticles")

# do not apply vertex smearing again 
# same for all years
process.ctppsBeamParametersESSource.vtxStddevX = 0
process.ctppsBeamParametersESSource.vtxStddevY = 0
process.ctppsBeamParametersESSource.vtxStddevZ = 0

# undo CMS vertex shift (FIXME, choose the correct year for PPS simulation)
#2016
#process.ctppsBeamParametersESSource.vtxOffsetX45 =  -1.048 * 1E-1
#process.ctppsBeamParametersESSource.vtxOffsetY45 =  -1.686 * 1E-1
#process.ctppsBeamParametersESSource.vtxOffsetZ45 =  +10.04 * 1E-1
#2017
#process.ctppsBeamParametersESSource.vtxOffsetX45 =  +0.24793 * 1E-1
#process.ctppsBeamParametersESSource.vtxOffsetY45 =  -0.692861 * 1E-1
#process.ctppsBeamParametersESSource.vtxOffsetZ45 =  -7.89895 * 1E-1
# 2018
process.ctppsBeamParametersESSource.vtxOffsetX45 = -0.1078 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetY45 = -0.4189 * 1E-1
process.ctppsBeamParametersESSource.vtxOffsetZ45 = -0.2488 * 1E-1

# processing path
process.p = cms.Path(
  #process.generator *
  process.beamDivergenceVtxGenerator
  * process.ctppsDirectProtonSimulation
  * process.reco_local
  * process.ctppsProtons
  #* process.ctppsAcceptancePlotter
  #* process.ctppsTrackDistributionPlotter
)

process.out = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('MiniAODWithPPS.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.out.outputCommands.append('keep *_*_*_*')

process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.p,
    process.outpath
)
