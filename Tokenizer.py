"""Used to parse text against lexemes"""
import re
"""Pulls in command line arguments"""
import sys


class Tokenizer:
    """Parses a custom language into tokens"""

    filename = ""
    lookupTable = {
        "INT": "int",  # the identifier
        "FLOAT": "float",  # the identifier
        "REAL": "(\d.\d)+",  # a floating point number
        "INTEGER": "[\d]+",  # a whole number
        "LSQB": "^\[$",  # [
        "RSQB": "^\]$",  # ]
        "EQUAL": "=",  # =
        "TAB": "\t",  # \t
        "NL": "\n",  # \n
        "OP": "[-+=*/]",  # +/*/etc…
        "LPAREN": "\(",  # (
        "RPAREN": "\)",  # )
        "LCURL": "\{",  # {
        "RCURL": "\}",  # }
        "IF": "if",  # if
        "COMPARISON": "[=><(!=)(>=)(<=)(==)(===)(!==)]",  # all of them!
        "ID": "^([_\w\d])+$",  # any variable
    }

    # Tokens that will use the symbol table
    symbolTableTokens = [
        "ID",
        "INTEGER",
        "COMPARISON"
    ]

    symbolTable = []
    parsed_target_str = ""
    target_str = ""
    tokens = []

    # def __init__(self):
    # if(len(sys.argv) > 1):
    #     self.filename = self.prompt_for_file_name()
    #     target_strings = self.readfile(self.filename)
    #     tokens = self.getTokens(target_strings)
        # print(tokens)

    def get_token(self, test_str):
        for key in self.lookupTable:
            pattern = self.lookupTable[key]
            results = re.match(pattern, test_str)

            if results:
                # print("getToken: " + str(results.group(0)) +
                    #   " pattern: " + pattern +
                    #   " string pulled: " + self.target_str[:len(results.group(0))])

                #Removing string that has had a token found for it
                self.target_str = self.target_str[len(results.group(0)):]
                self.parsed_target_str += self.target_str[:len(results.group(0))]


                if key in self.symbolTableTokens:
                    self.symbolTable.append(results.group(0))
                    return '<' + key + ', ' + str(len(self.symbolTable) - 1) + '>'
                elif key == "OP":
                    self.symbolTable.append(results.group(0))
                    return '<' + key + ', ' + results.group(0) + '>'

                else:
                    return '<' + key + '>'


        return None

    def getTokens(self):
        # print("\n\ntarget string: " + str(self.target_str))
        # print("tokens: " + str(self.tokens))
        # print("symbol table: " + str(self.symbolTable))
        while len(self.target_str) > 0:
            token = self.get_token(self.target_str)
            # print("token: " + str(token))
            if token:
                # print("Normal Token: " + token)
                self.tokens.append(token)
            else:
                self.getTokensCharByChar()

    def getTokensCharByChar(self):
        i = 1
        while i <= len(self.target_str):

            test_str = self.target_str[:i]

            # print("Test Str: \'" + test_str +"\' ")

            #Skipping spaces...SPPAAACCCEEEEE
            if test_str != ' ':
                token = self.get_token(test_str)
            else:
                self.target_str = self.target_str[1:]
                token = None

            # print(token)

            if token:
                if self.isIdToken(token):
                    # Checking to see if previous token is also an ID
                    if len(self.tokens) > 0 and self.isIdToken(self.tokens[-1]):
                        #Remove previous ID token because it is part of this token
                        self.tokens.pop()
                        self.symbolTable.pop()


                        #Trying previous char preppended to this one
                        self.target_str = self.target_str[i - 1:i]
                        self.getTokens()
                        i = len(self.target_str) + 1
                    else:
                        self.tokens.append(token)
                        self.target_str = self.target_str[i-1:]
                        # print("here: " + str(self.target_str))
                        # print("ID  but prev is not: " + str(self.target_str))
                        i = len(self.target_str) + 1
                else:
                    # print("Not ID Token:" + str(token))
                    self.tokens.append(token)
                    i = len(self.target_str)
                    self.getTokens()
            i += 1
            self.getTokens()

    def isIdToken(self, potentialFuckingIdTokenTheSheerAudacityOfTheseSadisticBastardsIMeanFUCK):
        return potentialFuckingIdTokenTheSheerAudacityOfTheseSadisticBastardsIMeanFUCK[:3] == "<ID"

    def readfile(self, fname):
        with open(fname) as target_file:
            return target_file.readlines()


    def prompt_for_file_name(self):
        # self.filename = input("Enter File Name: ")
        return "sample-input.txt"


myT = Tokenizer()

test_strings = myT.readfile("sample-input.txt")

for test in test_strings:
    print("".join(test.split()))
    myT.target_str = test
    myT.getTokens()
# myT.target_str = "\n"
print(myT.tokens)
print(myT.symbolTable)




