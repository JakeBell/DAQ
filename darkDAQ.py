#!/usr/bin/env python

import VISA_data_types as visa
import get_xml_data as xml
import ctypes 

#import the driver for use
drivername = "libAqDrv4.so"
ctypes.cdll.LoadLibrary(drivername)
AqDrv4 = ctypes.CDLL(drivername)

#ADD THIS TO __main__ later
MAX_SUPPORTED_DEVICES = 3
InstrumentID = [visa.ViSession()] * MAX_SUPPORTED_DEVICES 
NumInstruments = visa.ViInt32(0)
status = visa.ViStatus(0)
tbNextSegmentPad = visa.ViInt32(1)
VI_TRUE = visa.ViBoolean(True)
VI_FALSE = visa.ViBoolean(False)
VI_SUCCESS = visa.ViInt32(0)

def FindDevices():
    """Find all digitizers connected to the PC"""

    options = visa.ViString("")
    
    status = AqDrv4.AcqrsD1_multiInstrAutoDefine(options, ctypes.byref(NumInstruments))
    
    if (NumInstruments < 1):
        print "Instrument not found!"
    
    #Initialize digitizers
    for instrumentNumber in range(NumInstruments):
        py_resourceName = "PCI::INSTR%s" % instrumentNumber
        c_resourceName = visa.ViString(py_resourceName)
        status = AqDrv4.Acqrs_InitWithOptions(c_resourceName, VI_FALSE, VI_FALSE, options, ctypes.byref(InstrumentID[instrumentNumber]))

#NEED TO MAKE THIS WORK WITH MULTIPLE INSTRUMENTS!!!!
def Configure():
    """Configure the digitizer"""
    
    #Get all of the settings from a settings xml file
    settings_file = "example_file_name.xml"
    settings_dict = xml.get_settings_list(settings_file)
    
    sampInterval = visa.ViReal(settings_dict('sampInterval'))
    delayTime = visa.ViReal(settings_dict('delayTime'))
    
    nbrSamples = visa.ViInt32(settings_dict('nbrSamples'))
    nbrSegments = visa.ViInt32(settings_dict('nbrSegments'))
    
    coupling = visa.ViInt32(settings_dict('coupling'))
    bandwitdth = visa.ViInt32(settings_dict('bandwidth'))
    fullScale = visa.ViReal64(settings_dict('fullScale'))
    offset = visa.ViReal64(settings_dict('offset'))
    
    trigCoupling = visa.ViInt32(settings_dict('trigCoupling'))
    trigSlope = visa.ViInt32(settings_dict('trigSlope'))
    trigLevel = visa.ViReal64(settings_dict('trigLevel'))
            
    #Configure timebase
    status = AqDrv4.AcqrsD1_configHorizontal(InstrumentID[0], sampInterval, delayTime)
    status = AqDrv4.AcqrsD1_configMemory(InstrumentID[0], nbrSamples, nbrSegments)

    #Configure vertical settins
    status = AqDrv4.AcqrsD1_configVertical(InstrumentID[0], visa.ViInt8(1), fullScale, offset, coupling, bandwidth)
    
    #Configure trigger conditions
    setting0 = visa.ViInt8(0)
    setting1 = visa.ViInt8(1)
    setting00 = visa.ViReal32(0.0)
    settingAddr= visa.ViString("0x00000001")

    status = AqDrv4.AcqrsD1_configTrigClass(InstrumentID[0], setting0, settingAddr, setting0, setting0, setting00, setting00)

    #Configure trigger conditions
    status = AqDrv4.AcqrsD1_configTrigSource(InstrumentID[0], setting1, trigCoupling, trigSlope, trigLevel, setting00)

    #Setup for multisegment readout
    status = AqDrv4.Acqrs_getInstrumentInfo(InstrumentID[0], visa.ViString("TbNextSegmentPad"), ctypes.byref(tbNextSegmentPad)

def Acquire():
    """Start the acquisition of the waveform"""

    status = AqDrv4.AcqrsD1_acquire(InstrumentID[0])

    status = AqDrv4.AcqrsD1_waitForEndOfAcquisition(InstrumentID[0], visa.ViInt32(2000))
    
    if status != VI_SUCCESS:
        AqDrv4.AcqrsD1_stopAcquisition(InstrumentID[0])
        print "Acquisition has timed out - Acquisition stopped - Data taken is invalid"

def Readout()
    """Read out the data acquired from the digitizer"""
    
    settings_file = "example_file_name.xml"
    settings_dict = xml.get_settings_list(settings_file)

    channel = visa.ViInt32(settings_dict('channel'))
    nbrSamples = visa.ViInt32(settings_dict('nbrSamples'))
    nbrSegments = visa.ViInt32(settings_dict('nbrSegments'))

    status = AqDrv4.AcqrsD1_getMemory(InstrumentID[0], ctypes.byref(nbrSamples), ctypes.byref(nbrSegments))
    #Still need to figure out the readPar struct datatype to readout

def Close():
    status = AqDrv4.Acqrs_closeAll()
    

if __name__ == __main__:

    print "Starting Acquisition"
    
    FindDevices()
    Configure()
    Acquire()
    ReadOut()
    Close()
    
    print "Finished with Acquisition"
    
    #Note to self - remove globals from top and figure out a way to replicate assert command in python



