#Functions are defined with def. __init__ is constructor. @staticmethod means the
#function belongs to the class not the object.__class__ They must be called as
#<Class name>.<Function name>(<param>)
#Other functions can be called as <object>.<Function name>(<param>)
from parsetree import Parser

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
    def tokenizeparse(x):
        tok = Tokenizer()
        temp = tok.check_token(tok.tokenize(x))
        #print temp
        del tok
        par = Parser()
        try:
            temp = par.parse(temp)
        except IndexError:
            raise SyntaxError("Expression not closed")
        except:
            raise SyntaxError("Invalid Syntax")
        #print temp
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
