def list_contents(filename: str):

    with open(filename, "rb") as hexfile:
    
        header = hexfile.read(16)
        
        magic = bytes.fromhex(header.hex()[:12]).decode("utf-8")  # 12 because when added .hex(), it turns 6 hex bytes into 12 characters, i.e 'A0A1A2' length == 6
        dunno1 = int.from_bytes(header[6:8], byteorder='big')
        dunno2 = int.from_bytes(header[8:12], byteorder='big')
        file_count = int.from_bytes(header[12:], byteorder='big')
        
        print(f'Magic: {magic}')
        print(f'Unknown value 1: {dunno1}')
        print(f'Unknown value 2: {dunno2}')
        print(f'File count: {file_count}\n')
        
        ABZABGnames1 = []
        ABZABAnames = []
        ABZABGnames2 = []
        ABSABGnames = []
        ABZABGnames3 = []
        ABSABTnames = []
        for _ in range(0, file_count + 1):  # if needed, add +1 to file_count so it counts in the "empty" file name too (it doesn't seem to have any corresponding file in the archive, though)
            hexdata = hexfile.read(12)

            if bytes.fromhex(hexdata.hex()[0:16]).decode("utf-8").replace("\0", "") == "":  # tests for empty file
                fileName = "EMPTY"
            else:
                fileName = bytes.fromhex(hexdata.hex()[0:16]).decode("utf-8").replace("\0", "")
                
            unknownNumber1 = int.from_bytes(hexdata[8:10], byteorder='big')  # 2 bytes
            unknownNumber2 = int.from_bytes(hexdata[10:12], byteorder='big')  # 2 bytes
            
            print(f'Filename: {fileName}')
            print(f'File resolution?: {unknownNumber1}')
            print(f'File index: {unknownNumber2}')
            print('--------------------')
            
            if len(ABZABGnames1) != 1220:
                ABZABGnames1.append(fileName)
            elif len(ABZABAnames) != 286:
                ABZABAnames.append(fileName)
            elif len(ABZABGnames2) != 5:
                ABZABGnames2.append(fileName)
            elif len(ABSABGnames) != 10:
                ABSABGnames.append(fileName)
            elif len(ABZABGnames3) != 62:
                ABZABGnames3.append(fileName)
            elif len(ABSABTnames) != 4:
                ABSABTnames.append(fileName)
            else:
                pass
        
        print("\n")        
        print("First 1220 Names (ABZABG):")
        print(ABZABGnames1)
        print("\n")
        print("286 Names (ABZABA)")
        print(ABZABAnames)
        print("\n")
        print("Second 5 Names (ABZABG)")
        print(ABZABGnames2)
        print("\n")
        print("10 Names (ABSABG)")
        print(ABSABGnames)
        print("\n")
        print("Third 62 Names (ABZABG)")
        print(ABZABGnames3)
        print("\n")
        print("4 Names (ABSABT)")
        print(ABSABTnames)
        print("\n")
        print("Total file count:")
        print(len(ABZABGnames1) + len(ABZABAnames) + len(ABZABGnames2) + len(ABSABGnames) + len(ABZABGnames3) + len(ABSABTnames))
    
if __name__ == '__main__':
    list_contents("GRAPH.ABL")