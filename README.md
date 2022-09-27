# yu-no-sega-saturn-unpacker
Unpacker for the *images* of a Sega Saturn game called "Yu-No: The Girl Who Chants Love At The Bound of This World"

# Structure (WHAT I KNOW AS OF NOW)

## Header
##### 12 bytes in total
The header of the MPK is

Name | Size | Values |
--- | --- | --- 
Magic | 6 bytes | "ABLINK"
??? | 6 bytes |

## File count
##### No idea yey

## File information
##### Currently, I've found that starting right after the header, there are filename labels, that are each 12 bytes long. Of those 12 bytes:

Name | Size |
--- | --- 
?? | 2 bytes
Growing number | 2 bytes
Null terminated filename | 8 bytes

(To create this readme, I used https://github.com/DanOl98/MagesPack/blob/master/README.md as a reference)
