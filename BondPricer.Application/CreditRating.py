from enum import Enum

#s&p / fitch ratings
class CreditRating(str, Enum):
    AAAplus = "AAA+"
    AAA = "AAA"
    AAplus = "AA+"
    AA = "AA"
    AAminus = "AA-"
    Aplus = "A+"
    A = "A"
    Aminus = "A-"
    BBBplus = "BBB+"
    BBB = "BBB"
    BBBminus = "BBB-"
    BBplus = "BB+"
    BB = "BB"
    BBminus = "BB-"
    Bplus = "B+"
    B = "B"
    Bminus = "B-"
    CCCplus = "CCC+"
    CCC = "CCC"
    CCCminus = "CCC-"
    CC = "CC"
    C = "C"
    D = "D"