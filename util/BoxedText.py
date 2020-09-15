def generateBoxedText(inputString, verticalTerminator="|", lineRuling="="):
    """

        Returns text in a neet box

        Hello, world

        ================
        | Hello, world |    
        ================

    """

    splitString = inputString.split("\n")
    longestSize = 0
    
    for line in splitString:
        if len(line) >= longestSize:
            longestSize = len(line)

    returnString = lineRuling[0] * (longestSize + 4) + "\n"

    for line in splitString:
        spaces = " " * abs(len(line) - longestSize)
        returnString += f"{verticalTerminator} {line} {spaces}{verticalTerminator}\n"

    returnString += lineRuling[0] * (longestSize + 4)
    return returnString