from enum import Enum

from bitarray import bitarray, util
import random

def eventPacket():
    class channel(Enum):
        CH0  = bitarray('0000')
        CH1  = bitarray('0001')
        CH2  = bitarray('0010')
        CH3  = bitarray('0011')
        CH4  = bitarray('0100')
        CH5  = bitarray('0101')
        CH6  = bitarray('0110')
        CH7  = bitarray('0111')
        TRIG = bitarray('1000')

    class type(Enum):
        ToA_nonlinear_ToT   = bitarray('00')
        ToA_only            = bitarray('01')
        linear_ToT          = bitarray('10')
        ToA_linear_ToT      = bitarray('11')

    def generate(channel: channel, type: type, timestamp: int, pulsewidth: int, debug: bool):
        # Check ther bounds
        if timestamp > (2**22)-1 or timestamp < 0:
            raise RuntimeError("TIMESTAMP must be in range 0 to (2^22)-1")
        
        if pulsewidth > (2**14)-1 or pulsewidth < 0:
            raise RuntimeError("PULSE WIDTH must be in range 0 to (2^14)-1")
        
        # Create bit arrays from the numbers
        timestamp_ = bitarray()
        timestamp_.frombytes(timestamp.to_bytes(3))
        pulsewidth_ = bitarray()
        pulsewidth_.frombytes(pulsewidth.to_bytes(2))

        print(timestamp_)
        print(pulsewidth_)
        
        # Generate parities for the fields
        channelParity_ = util.parity(channel.value)
        typeParity_ = util.parity(type.value)
        timestampParity_ = util.parity(timestamp_)
        pulsewidthParity_ = util.parity(pulsewidth_)

        # Create the packet 
        packet_ = bitarray(48)
        packet_[0:4] = channel.value
        packet_[4:6] = type.value
        packet_[6:28] = timestamp_[2:24]
        packet_[28:42] = pulsewidth_[2:16]
        packet_[42:43] = int(debug)
        packet_[43:44] = channelParity_
        packet_[44:45] = typeParity_
        packet_[45:46] = timestampParity_
        packet_[46:47] = pulsewidthParity_
        packet_[47:48] = channelParity_ ^ typeParity_ ^ timestampParity_ ^ pulsewidthParity_

        return packet_
    
    def generateRandom(self):
        # Generate a random channel ID
        channel_ = random.choice(list(self.channel))

        # Generate a random type
        type_ = random.choice(list(self.type))

        # Generate a timestamp
        timestamp_ = random.randint(0, (2**22)-1)

        # Generate a pulse width
        pulsewidth_ = random.randint(0, (2**14)-1)

        print("[ EVNT ]   CHANNEL: " + str(channel_.name) + " TYPE: " + str(type_.name) + " TIMESTAMP: " + str(timestamp_) + " PULSEWIDTH: " + str(pulsewidth_))
        return self.generate(channel_[4:8], type_[6:8], timestamp_[2:24], pulsewidth_[2:16], False)


def genStatPacket(fifoDrop: bitarray, pwidthDrop: bitarray, dcountDrop: bitarray, triggerDrop: bitarray, pulseError: bitarray):
    if len(fifoDrop) != 20:
        raise RuntimeError("FIFO DROP bitarray length must be 20bits long.")
    
    if len(pwidthDrop) != 20:
        raise RuntimeError("PWIDTH DROP bitarray length must be 20bits long.")
    
    if len(dcountDrop) != 20:
        raise RuntimeError("DCOUNT DROP bitarray length must be 20bits long.")
    
    if len(triggerDrop) != 20:
        raise RuntimeError("TRIGGER DROP bitarray length must be 20bits long.")
    
    if len(pulseError) != 16:
        raise RuntimeError("PULSE ERROR bitarray length must be 16bits long.")
    
    # Create the packet
    packet_ = bitarray(96)
    packet_[0:20] = fifoDrop
    packet_[20:40] = pwidthDrop
    packet_[40:60] = dcountDrop
    packet_[60:80] = triggerDrop
    packet_[80:96] = pulseError




def genRandomStatPacket():
    # Generate a fifo drop counter
    fifoDrop_ = bitarray()
    fifoDrop_.frombytes(random.randbytes(3))
    fifoDrop_ >>= 4

    # Generate a pulse width drop counter
    pwidthDrop_ = bitarray()
    pwidthDrop_.frombytes(random.randbytes(3))
    pwidthDrop_ >>= 4

    # Generate a dark count drop counter
    dcountDrop_ = bitarray()
    dcountDrop_.frombytes(random.randbytes(3))
    dcountDrop_ >>= 4

    # Generate a trigger drop counter
    triggerDrop_ = bitarray()
    triggerDrop_.frombytes(random.randbytes(3))
    triggerDrop_ >>= 4

    # Generate a pulse error counter
    pulseError_ = bitarray()
    pulseError_.frombytes(random.randbytes(2))


    print("[ STAT ]   FIFO: " + str(int.from_bytes(fifoDrop_.tobytes())) + " PWIDTH: " + str(int.from_bytes(pwidthDrop_.tobytes())) + " DCOUNT: " + str(int.from_bytes(dcountDrop_.tobytes())) + " TRIGGER: " + str(int.from_bytes(triggerDrop_.tobytes())) + " PULSE: " + str(int.from_bytes(pulseError_.tobytes())))
    
    return genStatPacket(fifoDrop_[4:24], pwidthDrop_[4:24], dcountDrop_[4:24], triggerDrop_[4:24], pulseError_)

def genExtPacket():
    # Generate a fifo drop counter
    packetCount_ = bitarray()
    packetCount_.frombytes(random.randbytes(3))
    packetCount_ >>= 1

    # Generate a pulse width drop counter
    coarseCounter_ = bitarray()
    coarseCounter_.frombytes(random.randbytes(3))

    reset_ = random.randint(0,1)

    # Assempble the packet from the generated fields
    packet_ = bitarray(48)
    packet_[0:23] = packetCount_[1:24]
    packet_[23:47] = coarseCounter_
    packet_[47:48] = reset_

    print("[ EXTE ]   PACKET: " + str(int.from_bytes(packetCount_.tobytes())) + " COARSE: " + str(int.from_bytes(coarseCounter_.tobytes())) + " RST: " + str(reset_))
    
    return packet_
