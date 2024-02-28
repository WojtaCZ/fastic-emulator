from bitarray import bitarray, util
import random
import numpy as np



np.set_printoptions(formatter={'int':hex})

#Data Block
#   8 octets of raw data

#Separator block
#   BTF
#   Valid octet count
#   Data octets

#Separator-7 block
#   BTF
#   7 valid octets

# Specify number of frames to generate
framesN = 100

# Randomly shift the created frames by 1-65 bits (used to testy sync algorithms)
randomShift = True

# Randomly introduce error bits
randomError = True
randomErrorBER = 0.0001

# Possible frame types and their probabilities of ocurance
frameTypes = [
    (b'\x01', 30),     #Data block
    (b'\x02', 70)      #Control block
]

#Possible valid BTF (block type fields) and their probabilities of ocurance
blockTypeFields = [
    (b'\x78', 100),    #Idle/not ready/clock compensation
    (b'\xaa', 0),      #Native Flow Control
    (b'\x2d', 0),      #User Flow Control
    (b'\x1e', 0),      #Separator
    (b'\xe1', 0),      #Separator 7
    (b'\xd2', 0),      #User K-Block 0
    (b'\x99', 0),      #User K-Block 1
    (b'\x55', 0),      #User K-Block 2
    (b'\xb4', 0),      #User K-Block 3
    (b'\xcc', 0),      #User K-Block 4
    (b'\x66', 0),      #User K-Block 5
    (b'\x33', 0),      #User K-Block 6
    (b'\x4b', 0),      #User K-Block 7
    (b'\x87', 0),      #User K-Block 8
    (b'\xff', 0)       #Reserved
]







def genFrame(error, ber):
    # Determine if to generate error based on the provided BER
    hasError_ = random.choices([False, True], [1-(66*ber), (66*ber)])[0]

    # If the frame should contain an error
    if(hasError_):
        # Generate an error sync header
        frameType_ = random.choice([b'\x03', b'\x00'])
        # Generate random data
        data_ = bitarray()
        data_.frombytes(random.randbytes(8))
    else:
        # Select the frame type
        frameType_ = random.choices([x[0] for x in frameTypes], [y[1] for y in frameTypes])[0]

        # If the frame is an data block
        if(frameType_ == b'\x01'):
            # Generate random data
            data_ = bitarray()
            #data_.frombytes(b'\x12\x34\x56\x78\x9A\xBC\xDE\xF1')
            data_.frombytes(random.randbytes(8))
        elif(frameType_ == b'\x02'):
            btf_ = random.choices([x[0] for x in blockTypeFields], [y[1] for y in blockTypeFields])[0]
            # Generate random data and place in the BTF
            data_ = bitarray()
            #data_.frombytes(btf_)
            data_.frombytes(random.randbytes(8))
    
    frame_ = bitarray(65)
    frameTypeBits_ = bitarray()
    frameTypeBits_.frombytes(frameType_)
    
    frame_[0:2] = frameTypeBits_[6:8]
    frame_[2:65] = data_[0:64]

    return [frame_, hasError_, frameType_]

def genBitstream(frameNum, randomShift):
    if frameNum < 16:
        raise Exception("The number of generated frames must be larger than 16")
    
    if frameNum % 16:
        raise Exception("The number of generated frames must be a multiple of 16")

    errors_ = 0
    buffer_ = bitarray((frameNum+1)*66)
    
    # Generate N frames (+1 used for the optional bit shift)
    for i in range(0, frameNum+1):
        [frame_, hasError_, frameType_] = genFrame(randomError, randomErrorBER)
        if(hasError_):
            errors_ += 1
            print("Generated error at ", i)
        buffer_[(i*66) : (i*66) + 66] = frame_

    if randomShift: 
        shiftAmmount_ = random.randrange(34, 65)
    else:
        shiftAmmount_ = 66
    
    return [buffer_[0 + shiftAmmount_ : frameNum*66 + shiftAmmount_], errors_, 66-shiftAmmount_]
