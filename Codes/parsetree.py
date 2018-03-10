class Parser():
    mat = {']':'[','}':'{'}
    def __init__(self):
        pass

    #Converts the list into a nested list, where sub-expressions are inside lists
    def parse_list(self,lex):
        if len(lex) == 0:
            raise SyntaxError("Invalid Expression")
        
        token = lex.pop(0)
        if token == '(':    #If the character is (, call function recursively till corresponding ) is found
            temp = []
            while lex[0] != ')':
                temp.append(self.parse_list(lex))
            lex.pop(0)      #Removes the )
            return temp
        
        elif token == '[':  #Same as above but for [ instead of (
            temp = []
            while lex[0] != ']':
                temp.append(self.parse_list(lex))
            lex.pop(0)
            return temp
        
        elif token==')' or token==']':      #Found ] or ) without corresponding [ or (
            raise SyntaxError("Found "+token+" without matching "+mat[token])
        
        else:
            return Parser.typer(token)       #Otherwise convert to a int or float if possible

    #Converts token into int float or string
    @staticmethod
    def typer(token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except:
                return str(token)

    def parse(self,temp):
        return self.parse_list(temp)
