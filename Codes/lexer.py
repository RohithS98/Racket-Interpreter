#Functions are defined with def. __init__ is constructor. @staticmethod means the
#function belongs to the class not the object.__class__ They must be called as
#<Class name>.<Function name>(<param>)
#Other functions can be called as <object>.<Function name>(<param>)

class Parser():
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
            raise SyntaxError("Invalid Expression")
        
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

class Tokenizer:    #Class for tokenizer functions
    #String of delimiters
    delimiters="(){}[]"

    def __init__(self):#Creates a tokenizer object
        pass
    
    #Adds spaces on either sides of all the delimiters and then splits the string at spaces
    def tokenize(self,code1):
        for i in Tokenizer.delimiters:
            code1=code1.replace(i,' '+i+' ')
        return code1.split()    #Splits space-seperated string into list of words

    #Checks if a lexeme is a keyword
    @staticmethod
    def keyword(lexeme):
        if lexeme in ["if","define"]:
            return True
        return False

    #Checks if a given lexeme is a valid identifier
    @staticmethod
    def valid_id(x):
        if x[0].isalpha():
            return True
        return False

    #Joins strings which were separated
    def check_token(self,x):
        if type(x)==list and x!=[]:
            i=0
            while i <len(x):
                
                if type(x[i])==list:
                    x[i]=self.check_token(x[i])
                    
                elif type(x[i])==str and x[i][0]=='"' and x[i][-1]!='"':
                    while type(x[i+1]) != str or x[i+1][-1]!='"':
                        x[i]+=" "+str(x.pop(i+1))
                    x[i]+=" "+x.pop(i+1)
                    
                elif type(x[i])==str and x[i][0]=="'" and x[i][-1]!="'":
                    while type(x[i+1]) != str or x[i+1][-1]!="'":
                        x[i]+=" "+str(x.pop(i+1))
                    x[i]+=" "+x.pop(i+1)
                i+=1
        return x

    #Prints each lexeme along with token type. This is for printing token and type. Not important for interpreter
    def print_tok(self,x,met=0):
        if type(x)==list:
            if x!=[]:
                self.print_tok(x[0],1)
            for i in x[1:]:
                self.print_tok(i)
        elif type(x)==int or type(x)==float:
            print x,":Expression"
        elif Tokenizer.keyword(x):
            print x,": Keyword"
        elif met==1:
            print x,": Procedure Call"
        else:
            if Tokenizer.valid_id(x):
                print x,": Identifier"
            else:
                print x,": Expression"

    #Returns fully separated and tokenized string
    @staticmethod
    def fulltokenize(x):
        tok = Tokenizer()
        temp = tok.check_token(tok.tokenize(x))
        del tok
        par = Parser()
        temp = par.parse(temp)
        return temp

'''
#Runs forever until program is stopped
#Tok is a object of class Tokenizer
tok = Tokenizer()
while 1:
    x = raw_input().strip()                #Takes whole line as input
    x = Tokenizer.fulltokenize(x)   #Tokenizes it
    tok.print_tok(x)                         #Prints the output
    print
'''
