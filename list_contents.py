def list_contents(filename: str):
    with open(filename, "rb") as hexfile:
    
        header = hexfile.read(12).hex()
        magic = bytes.fromhex(header[:12]).decode("utf-8")  # 12 because string is 24 characters, 12 bytes
        
        count = 1  # because header2 potenitally is a filename
        
        header2 = hexfile.read(12).hex()
        firstFourBytesOfFirstItem = header2[:8].upper()
        orderNumberOfFirstItem = int(firstFourBytesOfFirstItem[4:].upper(), 16)
        fileNameOfFirstItem = header2[8:].upper()
        print(bytes.fromhex(fileNameOfFirstItem).decode("utf-8").replace("\0", "") + " :" + str(orderNumberOfFirstItem))
        
        set_list = []
        
        # Presumably filenames (dont forget to count error)
        while True:
            hexdata = hexfile.read(12).hex()
            # print(hexdata)
            
            if hexdata[:2] != "01" and hexdata[:2] != "04" and hexdata[:2] != "0B":
                hexdata_upper = hexdata.upper()
                print(f"Hexdata doesnt start with 01 or 04 at offset: {' '.join(hexdata_upper[i:i+2] for i in range(0, len(hexdata_upper), 2))}")
                print(f"Amount of files in this archive: {count}")
                break
            
            firstFourBytes = hexdata[:8].upper()
            orderNumber = int(firstFourBytes[4:].upper(), 16)
            fileName = hexdata[8:].upper()
            # print(firstFourBytes)
            # print(fileName)
            count += 1
            
            filename_as_string = bytes.fromhex(fileName).decode("utf-8").replace("\0", "")
            
            # if filename_as_string not in set_list:
            #     set_list.append(filename_as_string)
            # else:
            #     print(f"{filename_as_string} is a duplicate")
            #     print(f"at address {' '.join(hexdata.upper()[i:i+2] for i in range(0, len(hexdata.upper()), 2))}")
            #     break
            print(filename_as_string + " :" + str(orderNumber) + ", as hex it is: " + str(firstFourBytes[4:].upper()))
            
    
    
    
    
    
if __name__ == '__main__':
    list_contents("GRAPH.ABL")