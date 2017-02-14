"""Used to parse text against lexemes"""
import re
import sys

class Tokenizer:
    """Parses a custom language into tokens"""

    # File to parse
    filename = ""

    # Regexs used identify tokens we know about
    lookupTable = {
        "COLON": ":",
        "COMMA": ",",
        "INT": "int",
        "FLOAT": "float",
        "REAL": "(\d.\d)+",
        "INTEGER": "[\d]+",
        "LSQB": "^\[$",
        "RSQB": "^\]$",
        "EQUAL": "=",
        "TAB": "\t",
        "NL": "\n",
        "OP": "[-+=*/]",
        "LPAREN": "\(",
        "RPAREN": "\)",
        "LCURL": "\{",
        "RCURL": "\}",
        "IF": "if",
        "COMPARISON": "[=><(!=)(>=)(<=)(==)(===)(!==)]",
        "ID": "^([_\w\d])+$",
    }

    # Tokens that will use the symbol table
    symbol_table_tokens = [
        "ID",
        "INTEGER"
    ]

    # Holds found symbols
    symbol_table = []

    #string to parse
    target_str = ""

    # Holds found Tokens
    tokens = []

    def get_token(self, test_str):
        for key in self.lookupTable:
            pattern = self.lookupTable[key]
            results = re.match(pattern, test_str)

            if results:
                # Removing string that has had a token found for it
                self.target_str = self.target_str[len(results.group(0)):]

                if key in self.symbol_table_tokens:
                    symbol_table_id = self.put_symbol_table_token(results.group(0), key)
                    return '<' + key + ', ' + str(symbol_table_id) + '>'
                elif key == "OP" or key == "EQUAL" or key == "COMPARISON":
                    return '<' + key + ', ' + results.group(0) + '>'

                else:
                    return '<' + key + '>'

        return None

    def getTokens(self):
        while len(self.target_str) > 0:
            token = self.get_token(self.target_str)
            if token:
                self.tokens.append(token)
            else:
                self.getTokensCharByChar()

    def getTokensCharByChar(self):
        i = 1
        while i <= len(self.target_str):

            test_str = self.target_str[:i]


            # Skipping spaces...SPPAAACCCEEEEE
            if test_str != ' ':
                token = self.get_token(test_str)
            else:
                self.target_str = self.target_str[1:]
                token = None


            if token:
                if self.isIdToken(token):
                    # Checking to see if previous token is also an ID
                    if len(self.tokens) > 0 and self.isIdToken(self.tokens[-1]):
                        # Remove previous ID token because it is part of this
                        self.tokens.pop()
                        self.symbol_table.pop()

                        # Trying previous char preppended to this one
                        self.target_str = self.target_str[i - 1:i]
                        self.getTokens()
                        i = len(self.target_str) + 1
                    else:
                        self.tokens.append(token)
                        self.target_str = self.target_str[i - 1:]
                        i = len(self.target_str) + 1
                else:
                    self.tokens.append(token)
                    i = len(self.target_str)
                    self.getTokens()
            i += 1
            self.getTokens()

    def get_tokens_from_file(self):
        print(len(sys.argv))
        print(sys.argv)
        if len(sys.argv) > 1:
            if  sys.argv[1]:
                file = sys.argv[1]
        else:
            file = self.prompt_for_file_name()

        test_strings = self.readfile(file)

        for test in test_strings:
            self.target_str = test
            self.getTokens()

    def isIdToken(self, token):
        return token[:3] == "<ID"

    def put_symbol_table_token(self, token, token_type):
        for index, symbol in enumerate(self.symbol_table):
            if symbol[1] == token:
                return index

        new_token = [token_type, token]
        self.symbol_table.append(new_token)
        return len(self.symbol_table)-1

    def print_pretty_tokens(self):
        for token in self.tokens:
            if token == "<NL>":
                print(str(token) + "\n")
            else:
                print(token, end=" ")
        print("\n")

    def print_pretty_symbol_table(self):
        for index, symbol in enumerate(self.symbol_table):
            if index % 3 >= 2:
                print(str(symbol) + "\n")
            else:
                print(symbol, end=" ")
        print("\n")

    def prompt_for_file_name(self):
        return input("Enter File Name: ")

    def readfile(self, f):
        with open(f) as target_file:
            return target_file.readlines()

