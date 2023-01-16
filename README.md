# yu-no-sega-saturn-unpacker
Unpacker for the *images* of a Sega Saturn game called "Yu-No: The Girl Who Chants Love At The Bound of This World".
Specifically, for an archive called GRAPH.ABL.

# Structure

The byte order is BIG ENDIAN

## Header
##### 16 bytes in total
The header of the GRAPH.ABL is

Name | Size | Values |
--- | --- | --- 
Magic | 6 bytes | "ABLINK"
??? | 2 bytes |
Something maybe related to file size | 4 bytes | The value is quite close to 32MB - Hex value is 0x01DA6B52, that's 31091538 in decimal, or roughly 31 MB.
File count | 4 bytes | 1587

## File information
##### After the header, there are filename labels, that are each 12 bytes long. Of those 12 bytes:

Name | Size | Values
--- | --- | ---
Null terminated filename | 8 bytes | 
Resolution? | 2 bytes | Either 256, 1024 or 2816
Index? | 2 bytes | Some growing number, but I couldn't find any consistency to it (first 5 numbers, for example, are 10, 25, 43, 54, 72, etc.)

This repeats for 1587 + 1 times (last File info is empty, with no filename and no resulution value, only and index. Maybe it's used for padding).

## Garbage data
##### After the File information table, there's garbage data, starting from 0x4A80 until first entry at 0x5000.

## Raw file data
##### There are 4 different file types: ABZABG, ABZABA, ABSABG and ABSABT. They are in the respective order in the archive:
* 1220 ABZABG files
* 286 ABZABA files
* 5 ABZABG files
* 10 ABSABG files
* 62 ABZABG files
* 4 ABSABT files
Total: 1587 files

Note: ABSABT files are like small archives, that house even smaller files inside of them. They have their own nametable and files inside of them)

# Usage
Requirement: You need to have Python 3 installed.

To list the contents of the GRAPH.ABL into terminal, you can run the code with "python list_contents.py" or just "list_contents.py". The GRAPH.ABL file needs to be in the same folder as the .py file.
To list the contents into a text file, use this command: "list_contents.py > contents.txt".

To extract the contents of the GRAPH.ABL file, just run "extract_contents.py" in the same folder where the GRAPH.ABL is. The program will automatically create a folder called "out" in the directory, where it will put the extracted files.

Note about extraction: since there are filenames that are repeating (for example, 0050), I had to append their file type to their name. Otherwise they would've overwritten themselves during extraction. If you want to remove those file types from the file names, I suggest using a free program, like ReNamer.

(To create this readme, I used https://github.com/DanOl98/MagesPack/blob/master/README.md as a reference)
