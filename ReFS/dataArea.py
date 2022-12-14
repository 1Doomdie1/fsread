from typing import Union
from bytesFormater.formater import Formater



'''
This whole class will be refactored but for now it does the job.
It correctly reads data about each Index Entry in the Data Area within the Container Table.

The thing is that there are 13 tables in ReFS and each of them has different structures and the currect state if the class doesn't allow corectly parsing other tables.
'''

class IndexEntries:
    def __init__(self, byteArray:Union[list[bytes], tuple[bytes], set[bytes]], keysBlock, keysNumber, indexHeaderRelativeOffset) -> None:
        self.byteArray = byteArray
        self.formater = Formater()
        self.keysBlock = keysBlock
        self.keysNumber = keysNumber
        self.indexHeaderRelativeOffset = indexHeaderRelativeOffset
        self.entries = []

    def entrySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x0:0x4])
        # return self.formater.toDecimal(self.byteArray[0x0:0x4])

    def keyStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x4:0x6])

    def keySize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0x6:0x8])

    def flag(self, _bytes: bytes) -> int: # This will need to return a string in the future
        flagsStruct = {0x2:"Rightmost extent in a subtree", 0x4:"Deleted Entry", 0x40:"Stream Index Entry"}
        flagValue = self.formater.toDecimal(_bytes[0x8:0xA])
        # return flagsStruct[flagValue]
        # I have to check if I look at the right bytes to determine flag
        # For now the function is returning the flag value not type
        return flagValue

    def vlaueStartOffset(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xA:0xC])

    def valueSize(self, _bytes: bytes) -> int:
        return self.formater.toDecimal(_bytes[0xC:0xE])

    def addEntrieHeader(self, _bytes):
        entryGeneralHeader = {"Entry size": self.entrySize(_bytes),
                              "Key Offset Start":self.keyStartOffset(_bytes),
                              "Key Size":self.keySize(_bytes),
                              "Flag":self.flag(_bytes),
                              "Value Start Offset": self.vlaueStartOffset(_bytes),
                              "Value Size": self.valueSize(_bytes),
                              "Node-Specific Info":{}}
        self.entries.append(entryGeneralHeader)

    def createGeneralEntriesHeader(self):
        for i in range(0, self.keysNumber * 4, 4):
            keyOffset = (self.formater.toDecimal(self.keysBlock[i:i + 4]) & 0x0000ffff) + self.indexHeaderRelativeOffset
            keySize = self.formater.toDecimal(self.byteArray[keyOffset:keyOffset + 4])
            x = self.byteArray[keyOffset:keyOffset + keySize]
            self.addEntrieHeader(x)
