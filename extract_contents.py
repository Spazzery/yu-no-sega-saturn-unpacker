import os

class ContentExtractor:

    # Smol internal class to house some file info
    class FileInfo:
        name = ""
        unk1 = 0
        unk2 = 0
        raw = bytearray()
        header = ""

        def __init__(self, name, unk1, unk2):
            self.name = name
            self.unk1 = unk1
            self.unk2 = unk2
    
    # Continuing with ContentExtractor class
    
    fileInfoList = []
    hexfile = None
    
    def __init__(self):
        pass

    def extract_contents(self, filename: str):
        with open(filename, "rb") as self.hexfile:
            
            header = self.hexfile.read(16)
            
            magic = bytes.fromhex(header.hex()[:12]).decode("utf-8")  # 12 because when added .hex(), it turns 6 hex bytes into 12 characters, i.e 'A0A1A2' length = 6
            dunno1 = int.from_bytes(header[6:8], byteorder='big')
            dunno2 = int.from_bytes(header[8:12], byteorder='big')
            file_count = int.from_bytes(header[12:], byteorder='big')
            
            print(f'Magic: {magic}')
            print(f'Unknown value 1: {dunno1}')
            print(f'Unknown value 2: {dunno2}')
            print(f'File count: {file_count}\n')
            
            for _ in range(0, file_count):  # if needed, add +1 to file_count so it counts in the "empty" file name too
                hexdata = self.hexfile.read(12)

                if bytes.fromhex(hexdata.hex()[0:16]).decode("utf-8").replace("\0", "") == "":  # tests for empty string
                    fileName = "EMPTY"
                else:
                    fileName = bytes.fromhex(hexdata.hex()[0:16]).decode("utf-8").replace("\0", "")
                    
                unknownNumber1 = int.from_bytes(hexdata[8:10], byteorder='big')  # 2 bytes
                unknownNumber2 = int.from_bytes(hexdata[10:12], byteorder='big')  # 2 bytes
                
                fi = self.FileInfo(fileName, unknownNumber1, unknownNumber2)
                self.fileInfoList.append(fi)

                print(fileName)
                
            self.hexfile.seek(20480)  # first file offset/position is #0x5000
            
            print("Reading all files into memory...")
            
            # First 1220 ABZABG files
            # Following 286 ABZABA files
            # Then, again, 5 ABZABG files
            # Then 10 ABSABG files
            # Then, once again, 62 ABZABG files
            # Finally, 4 ABSABT files (that have other files in them, too)
            # (Asterisk * just differentiates ABZABG from others, as it repeats often, for better code readibility)
            ABZABG = "41425A414247"
            ABZABA = "41425A414241"
            ABSABG = "414253414247"
            ABSABT = "414253414254"
            for i in range(0, file_count): # 1587
                if i < 1220:  
                    self.read_contents(i, ABZABG, ABZABA) # ABZABG*, ABZABA
                elif 1220 <= i < 1506:  
                    self.read_contents(i, ABZABA, ABZABG) # ABZABA, ABZABG*
                elif 1506 <= i < 1511:
                    self.read_contents(i, ABZABG, ABSABG) # ABZABG*, ABSABG
                elif 1511 <= i < 1521:
                    self.read_contents(i, ABSABG, ABZABG) # ABSABG, ABZABG*
                elif 1521 <= i < 1583:
                    self.read_contents(i, ABZABG, ABSABT) # ABZABG*, ABSABT
                elif 1583 <= i < 1587:
                    self.read_contents(i, ABSABT, ABSABT) # ABSABT, ABSABT
                else:
                    pass # all done
             
            # Write all results to file
            for file in self.fileInfoList:
                self.write_to_file(file)
                
            print("Extraction complete!")
            
    def read_contents(self, index, fileHeaderWithSameNameInHex, fileHeaderWithOtherNameInHex):
        raw = []
        header_row_added = False
        
        while True:
            previous_pos = self.hexfile.tell()  # saves position before reading
            row = self.hexfile.read(16)
            
            # Checks against: new entry with same name as it OR new entry with other name OR hexfile is fully read
            if (header_row_added and row.hex()[:12].upper() == fileHeaderWithSameNameInHex) or (header_row_added and row.hex()[:12].upper() == fileHeaderWithOtherNameInHex) or row == b'':
                self.hexfile.seek(previous_pos)
                break
            else:    
                if row.hex()[:12].upper() == fileHeaderWithSameNameInHex:
                    header_row_added = True
                raw.append(row)
            
        # Using a clever hacc from https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists    
        self.fileInfoList[index].raw = [item for sublist in raw for item in sublist]  # add raw data to FileInfo object
        
        # print(f"Reading file no. {index} into memory...")
        
    def write_to_file(self, file):
        dir = os.path.join("out")
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        header = ""
        headerValues = file.raw[:6]
        for integer in headerValues:
            header += chr(integer).encode("utf-8").decode("utf-8") 
            
        filename = file.name + "_" + header
        
        create_file = open("out/" + filename, "wb")

        for i in file.raw:
            create_file.write(i.to_bytes(1, byteorder='big'))
            
        create_file.close()
        print(f"Extracted file: {filename}")
    
    
if __name__ == '__main__':
    ce = ContentExtractor()
    ce.extract_contents("GRAPH.ABL")