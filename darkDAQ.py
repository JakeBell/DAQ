#!/usr/bin/env python

from datetime import datetime

import VISA_data_types as visa
import get_xml_data as xml
import struct_test as structs
import ctypes

#import the driver for use
drivername = "libAqDrv4.so"
ctypes.cdll.LoadLibrary(drivername)
AqDrv4 = ctypes.CDLL(drivername)

#ADD THIS TO __main__ later
MAX_SUPPORTED_DEVICES = 3
InstrumentID_type = structs.InstrumentIDArray()
InstrumentID = InstrumentID_type.get_data_type(MAX_SUPPORTED_DEVICES)
NumInstruments = visa.ViInt32(0)
status = visa.ViStatus(0)
tbNextSegmentPad = visa.ViInt32(1)
VI_TRUE = visa.ViBoolean(True)
VI_FALSE = visa.ViBoolean(False)
VI_SUCCESS = visa.ViInt32(0)


#write function to check status and print out error codes!!!!
def FindDevices(simulation=False):
    """Find all digitizers connected to the PC"""

    if simulation:
        simulated = visa.ViString("PCI::DP211")
        options = visa.ViString("simulate=TRUE")
        NumInstruments = visa.ViInt32(1)
        status = AqDrv4.Acqrs_setSimulationOptions(visa.ViString(""))
        if status != 0:
            print "error defining instruments: error code %s" % status
        
        for instrumentNumber in range(NumInstruments.value):
            status = AqDrv4.Acqrs_InitWithOptions(simulated, VI_FALSE, VI_FALSE, options, ctypes.byref(InstrumentID[instrumentNumber]))
            if status != 0:
                print "error initializing devices: error code %s" % status
    
    else:
        options = visa.ViString("")
        NumInstruments = visa.ViInt32(0)
        status = AqDrv4.AcqrsD1_multiInstrAutoDefine(options, ctypes.byref(NumInstruments))
        if status != 0:
            print "error defining instruments: error code %s" % status
        
        if (NumInstruments < 1):
            print "Instrument not found!"
        else:
            print "Found %s instruments!" % NumInstruments.value
        #Initialize digitizers
        for instrumentNumber in range(NumInstruments.value):
            py_resourceName = "PCI::INSTR%s" % instrumentNumber
            c_resourceName = visa.ViString(py_resourceName)
            status = AqDrv4.Acqrs_InitWithOptions(c_resourceName, VI_FALSE, VI_FALSE, options, ctypes.byref(InstrumentID[instrumentNumber]))
            if status != 0:
                print "error initializing devices: error number %s" % status
#NEED TO MAKE THIS WORK WITH MULTIPLE INSTRUMENTS!!!!
def Configure():
    """Configure the digitizer"""

    #Get all of the settings from a settings xml file
    settings_file = "settings_example.xml"
    settings_dict = xml.get_settings_list(settings_file)

    sampInterval = visa.ViReal64(float(settings_dict[0]['sampInterval']))
    delayTime = visa.ViReal64(float(settings_dict[0]['delayTime']))

    nbrSamples = visa.ViInt32(int(settings_dict[0]['nbrSamples']))
    nbrSegments = visa.ViInt32(int(settings_dict[0]['nbrSegments']))

    coupling = visa.ViInt32(int(settings_dict[0]['coupling']))
    bandwidth = visa.ViInt32(int(settings_dict[0]['bandwidth']))
    fullScale = visa.ViReal64(float(settings_dict[0]['fullScale']))
    offset = visa.ViReal64(float(settings_dict[0]['offset']))

    trigCoupling = visa.ViInt32(int(settings_dict[0]['trigCoupling']))
    trigSlope = visa.ViInt32(int(settings_dict[0]['trigSlope']))
    trigLevel = visa.ViReal64(float(settings_dict[0]['trigLevel']))

    #Configure timebase
    status = AqDrv4.AcqrsD1_configHorizontal(InstrumentID[0], sampInterval, delayTime)
    if status != 0:
        print "error code: %s" % status
    status = AqDrv4.AcqrsD1_configMemory(InstrumentID[0], nbrSamples, nbrSegments)
    if status != 0:
        print "error code: %s" % status
    #Configure vertical settins
    status = AqDrv4.AcqrsD1_configVertical(InstrumentID[0], visa.ViInt8(1), fullScale, offset, coupling, bandwidth)
    if status != 0:
        print "error code: %s" % status
    #Configure trigger conditions
    setting0 = visa.ViInt8(0)
    setting1 = visa.ViInt8(1)
    setting00 = visa.ViReal32(0.0)
    settingAddr= visa.ViString("0x00000001")

    status = AqDrv4.AcqrsD1_configTrigClass(InstrumentID[0], setting0, settingAddr, setting0, setting0, setting00, setting00)
    if status != 0:
        print "error code: %s" % status
    #Configure trigger conditions
    status = AqDrv4.AcqrsD1_configTrigSource(InstrumentID[0], setting1, trigCoupling, trigSlope, trigLevel, setting00)
    if status != 0:
        print "error code: %s" % status
    #Setup for multisegment readout
    status = AqDrv4.Acqrs_getInstrumentInfo(InstrumentID[0], visa.ViString("TbNextSegmentPad"), ctypes.byref(tbNextSegmentPad))
    if status != 0:
        print "error code: %s" % status
        
def Acquire():
    """Start the acquisition of the waveform"""

    status = AqDrv4.AcqrsD1_acquire(InstrumentID[0])
    if status != 0:
        print "error code: %s" % status
        
    status = AqDrv4.AcqrsD1_waitForEndOfAcquisition(InstrumentID[0], visa.ViInt32(2000))
    if status != 0:
        print "error code: %s" % status
        
    if status != 0:
        AqDrv4.AcqrsD1_stopAcquisition(InstrumentID[0])
        print "Acquisition has timed out - Acquisition stopped - Data taken is invalid"

def ReadOut():
    """Read out the data acquired from the digitizer"""

    channel = visa.ViInt32(1)
    nbrSamples = visa.ViInt32(0)
    nbrSegments = visa.ViInt32(0)

    status = AqDrv4.AcqrsD1_getMemory(InstrumentID[0], ctypes.byref(nbrSamples), ctypes.byref(nbrSegments))
    if status != 0:
        print "error code: %s" % status

    readPar = structs.AqReadParameters()
    dataDesc = structs.AqDataDescriptor()
    # AqSegmentDescriptor* segDesc = new AqSegmentDescriptor[nbrSegments];
    segDescType = structs.AqSegmentDescriptor * nbrSegments.value
    segDesc = segDescType()

    readPar.dataType = ctypes.c_long(0)
    readPar.readMode = ctypes.c_long(1)
    readPar.firstSegment = ctypes.c_long(0)
    readPar.nbrSegments = ctypes.c_long(nbrSegments.value)
    readPar.firstSampleInSeg = ctypes.c_long(0)
    readPar.nbrSamplesInSeg = nbrSamples
    readPar.segmentOffset = nbrSamples
    #THIS HAS TO BE THE SIZE OF adcArray!!!!!! FIGURE IT OUT
    readPar.dataArraySize = ctypes.c_long((nbrSamples.value * tbNextSegmentPad.value) * (nbrSegments.value + 1) * (readPar.dataType +1))
    readPar.segDescArraySize = ctypes.c_long((nbrSegments.value * ctypes.sizeof(structs.AqSegmentDescriptor)))
    readPar.flags = ctypes.c_long(0)
    readPar.reserved = ctypes.c_long(0)
    readPar.reserved2 = ctypes.c_double(0)
    readPar.reserved3 = ctypes.c_double(0)

    # ViInt8* adcArray = new ViInt8[(nbrSamples + tbNextSegmentPad)*(nbrSegments + 1)];
    adcArrayType = ctypes.c_byte * readPar.dataArraySize
    adcArray = adcArrayType()

    status = AqDrv4.AcqrsD1_readData(InstrumentID[0], channel, ctypes.byref(readPar), adcArray, ctypes.byref(dataDesc), segDesc)
    if status != 0:
        print "error code: %s" % status
        
    #Write Data to a file
    now = str(datetime.now())
    filename = ("/home/darkdaq1/Acqiris %s.data" % now).replace(" ", "_")
    file = open(filename, 'w')
    file.write("# Acqiris Waveforms")
    file.write("# Channel: %s" % channel)
    file.write("# Samples acquired: %s" % dataDesc.returnedSamplesPerSeg)
    file.write("# Segments acquired: %s" % dataDesc.returnedSegments)

    file.write("# ADC counts")
    for j in range(dataDesc.returnedSegments):
        for i in range(dataDesc.returnedSamplesPerSeg):
            file.write(str(int(adcArray[j * readPar.segmentOffset + i])))

    file.write("# Voltage")
    for j in range(dataDesc.returnedSegments):
        for i in range(dataDesc.returnedSamplesPerSeg):
            file.write(str(int(adcArray[j * readPar.segmentOffset + i]) * dataDesc.vGain - dataDesc.vOffset))

    file.close()

def Close():
    status = AqDrv4.Acqrs_closeAll()
    if status != 0:
        print "error code: %s" % status

if __name__ == '__main__':

    print "Starting Acquisition"

    FindDevices()
    Configure()
    Acquire()
    ReadOut()
    Close()

    print "Finished with Acquisition"

    #Note to self - remove globals from top and figure out a way to replicate assert command in python



