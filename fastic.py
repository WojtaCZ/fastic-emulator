from bitarray import bitarray, util
import random

def genRandomEventPacket():
    # Generate a random channel ID
    channel_ = bitarray()
    channel_.frombytes(random.randrange(7, 9).to_bytes())
    channelParity_ = util.parity(channel_)

    # Generate a random type
    type_ = bitarray()
    type_.frombytes(random.randrange(0, 4).to_bytes())
    typeParity_ = util.parity(type_)

    # Generate a timestamp
    timestamp_ = bitarray()
    timestamp_.frombytes(random.randbytes(3))
    timestamp_ >>= 2
    timestampParity_ = util.parity(timestamp_)

    # Generate a pulse width
    pulsewidth_ = bitarray()
    pulsewidth_.frombytes(random.randbytes(2))
    pulsewidth_ >>= 2
    pulsewidthParity_ = util.parity(pulsewidth_)

    # Assempble the packet from the generated fields
    packet_ = bitarray(48)
    packet_[0:4] = channel_[4:8]
    packet_[4:6] = type_[6:8]
    packet_[6:28] = timestamp_[2:24]
    packet_[28:42] = pulsewidth_[2:16]
    packet_[42:43] = 0
    packet_[43:44] = channelParity_
    packet_[44:45] = typeParity_
    packet_[45:46] = timestampParity_
    packet_[46:47] = pulsewidthParity_
    packet_[47:48] = channelParity_ ^ typeParity_ ^ timestampParity_ ^ pulsewidthParity_

    print("[ EVNT ]   CHANNEL: " + str(int.from_bytes(channel_.tobytes())) + " TYPE: " + str(int.from_bytes(type_.tobytes())) + " TIMESTAMP: " + str(int.from_bytes(timestamp_.tobytes())) + " PULSEWIDTH: " + str(int.from_bytes(pulsewidth_.tobytes())))
    print("           PARITIES   CH: " + str(int(channelParity_)) + " TY: " + str(int(typeParity_)) + " TS: " + str(int(timestampParity_)) + " PW: " + str(int(pulsewidthParity_)) + " PA: " + str(int(channelParity_ ^ typeParity_ ^ timestampParity_ ^ pulsewidthParity_))) 

    return packet_

def genStatPacket():
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

    # Assempble the packet from the generated fields
    packet_ = bitarray(96)
    packet_[0:20] = fifoDrop_[4:24]
    packet_[20:40] = pwidthDrop_[4:24]
    packet_[40:60] = dcountDrop_[4:24]
    packet_[60:80] = triggerDrop_[4:24]
    packet_[80:96] = pulseError_

    print("[ STAT ]   FIFO: " + str(int.from_bytes(fifoDrop_.tobytes())) + " PWIDTH: " + str(int.from_bytes(pwidthDrop_.tobytes())) + " DCOUNT: " + str(int.from_bytes(dcountDrop_.tobytes())) + " TRIGGER: " + str(int.from_bytes(triggerDrop_.tobytes())) + " PULSE: " + str(int.from_bytes(pulseError_.tobytes())))
    
    return packet_

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
