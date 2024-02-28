import fastic
import aurora



def convertToArray(values, colcount=8):
    # apply formatting to each element
    values = ['0x' + str(hex(v)[2:].zfill(8)) for v in values]

    # split into rows with up to `colcount` elements per row
    rows = [values[i:i+colcount] for i in range(0, len(values), colcount)]

    # separate elements with commas, separate rows with newlines
    body = ',\n    '.join([', '.join(r) for r in rows])

    # assemble components into the complete string
    return '{} {}[] = {{\n    {} \n}};'.format("std::uint32_t", "auroraData", body)


[frame, errors, shift] = genBitstream(128, False)

dt = np.dtype(np.uint32).newbyteorder('>')
carray = convertToArray(np.frombuffer(frame.tobytes(), dtype=dt))

f = open("inc/databuff.hpp", "w")
f.write("#include <cstdint>")

f.write("\n//Statistics\n")
f.write("//  Bit shift: " + str(shift) + "\n")
f.write("//  Number of generated errors: " + str(errors) + "\n\n")

f.write(carray)


print("Statistics")
print("  Bit shift: " + str(shift))
print("  Number of generated errors: " + str(errors))

fastic.genStatPacket()