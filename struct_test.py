#Check to make sure enum datatypes are correct and double check for spelling errors please!!!

from ctypes import *

class AqReadParameters(Structure):
    _fields_ = [('dataType', c_long),
                ('readMode', c_long),
                ('firstSegment', c_long),
                ('nbrSegments', c_long),
                ('firstSampleInSeg', c_long),
                ('nbrSamplesInSeg', c_long),
                ('segmentOffset', c_long),
                ('dataArraySize', c_long),
                ('segDescArraySize', c_long),
                ('flags', c_long),
                ('reserved', c_long),
                ('reserved2', c_double),
                ('reserved3', c_double)]

class AqWriteParameters(Structure):
    _fields_ = [('dataType', c_long),
                ('writeMode', c_long),
                ('firstSegment', c_long),
                ('nbrSegments', c_long),
                ('firstSampleInSeg', c_long),
                ('nbrSamplesInSeg', c_long),
                ('segmentOffset', c_long),
                ('dataArraySize', c_long),
                ('segDescArraySize', c_long),
                ('flags', c_long),
                ('reserved', c_long),
                ('reserved2', c_double),
                ('reserved3', c_double)]

class AqSegmentDescriptor(Structure):
    _fields_ = [('horPos', c_double),
                ('timeStampLo', c_ulong),
                ('timeStampHi', c_ulong)]

class AqSegmentDescriptorSeqRaw(Structure):
    _fields_ = [('horPos', c_double),
                ('timeStampLo', c_ulong),
                ('timeStampHi', c_ulong),
                ('indexFirstPoint', c_ulong),
                ('actualSegmentSize', c_ulong),
                ('reserved', c_long)]

class AqSegmentDescriptorAvg(Structure):
    _fields_ = [('horPos', c_double),
                ('timeStampLo', c_ulong),
                ('timeStampHi', c_ulong),
                ('actualTriggersInSeg', c_ulong),
                ('avgOvfl', c_long),
                ('avgStatus', c_long),
                ('avgMax', c_long),
                ('flags', c_ulong),
                ('reserved', c_long)]

class AqDataDescriptor(Structure):
    _fields_ = [('returnedSamplesPerSeg', c_long),
                ('indexFirstPoint', c_long),
                ('sampTime', c_double),
                ('vGain', c_double),
                ('vOffset', c_double),
                ('returenedSegments', c_long),
                ('nbrAvgWforms', c_long),
                ('actualTriggersInAcqLo', c_ulong),
                ('actualTriggersInAcqHi', c_ulong),
                ('actualDataSize', c_ulong),
                ('reserved2', c_long),
                ('reserved3', c_double)]

class AqGateParameters(Structure):
    _fields_ = [('GatePos', c_long),
                ('GateLength', c_long)]

#enums for now

#enum AqReadType
ReadInt8 = c_long(0)
ReadInt16 = c_long(1)
ReadInt32 = c_long(2)
ReadReal64 = c_long(3)
ReadRawData = None

#enum AqReadDataMode
ReadModeStdW = c_long(0)
ReadModeSeqW = c_long(1)
ReadModeAvgW = c_long(2)     
ReadModeGateW = c_long(3)     
ReadModePeak = c_long(4)     
ReadModeShAvgW = c_long(5)    
ReadModeSShAvgW = c_long(6)   
ReadModeSSRW = c_long(7)      
ReadModeZsW = None       
ReadModeHistogram = c_long(9)
ReadModePeakPic = c_long(10)
ReadModeSeqRawW = c_long(11)
nbrAqReadDataMode = None

"""
Not sure what to do with these for now

#enum AqReadDataFlags 
AqIgnoreTDC          = 0x0001
AqIgnoreLookUp       = 0x0002
AqSkipClearHistogram = 0x0004
AqSkipCircular2Linear= 0x0008
AqDmaToCompanion     = 0x0010
"""

#Constants for D1 configMode

#enum AqAcqMode
AqAcqModeDigitizer      = c_long(0)
AqAcqModeRepeat         = c_long(1)
AqAcqModeAverager       = c_long(2)
AqAcqModePingPong       = c_long(3)
AqAcqModePeakTDC        = c_long(5)
AqAcqModeFreqCounter    = c_long(6)
AqAcqModeSSR            = c_long(7)

#Constants for power

#enum AqPowerState
AqPowerOff = c_long(0)
AqPowerOn = c_long(1)
nbrAqPowerState = None

# Device type. It determines the API interface that will be used.

#enum AqDevType
AqDevTypeInvalid = c_long(0)
AqD1 = c_long(1)              
AqG2 = c_long(2)
AqD1G2 = c_long(3)
AqT3 = c_long(4)
AqG4 = c_long(5)
AqD1G4 = c_long(6)
AqP5 = c_long(7)
nbrAqDevType = c_long(8)