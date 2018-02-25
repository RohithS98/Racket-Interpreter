import math
import operator as op
from lexer import Tokenizer

#Environment contains all Procedures and variables that are locally defined as dictionary
class Environment():
    #Initializes Environment with all local variables and methods
    #Par and args have corresponding values. Current is for direct initialisation of dictionary
    #Outer stores the Environment that is outside of the current
    def __init__(self, par = (), args=(), outer=None, current={}):
        self.d = current
        self.d.update(zip(par,args))
        self.outer = outer

    #Checks if given variable is in local scope. If not then checks in the outer scopes
    def find(self, var):
        if var in self.d:
            return self.d[var]
        elif self.outer == None:
            raise NameError(var + ' not defined')
        else:
            return self.outer.find(var)

#This is the standard environment that contains the functions declared at global scope
def std_env():
    #Standard procedures
    env = dict()
    env.update(vars(math))
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs': abs, 'append' : op.add, 'car': lambda x : x[0], 'cdr': lambda x : x[1:], 'equal?': op.eq,
        'length': len, 'null?': lambda x : x==[], 'cons': lambda x,y : [x]+y, 'map': map, 'expt': pow,
        'list': lambda *x: list(x), 'drop': lambda x,y : x[y:], 'take': lambda x,y : x[:y]
        })
    return env

#Global scope Environment
global1 = Environment((),(),None,std_env())

#Procedures that are defined by the user are defined as objects
class Procedure(object):
    #Used for user-defined procedures
    #Par contains parameters, Body is the function,
    #and env is the environment in which it is defined
    def __init__(self, par, body, env):
        self.par = par
        self.body = body
        self.env = env

    #Function call
    def __call__(self, *args):
        return evaluate(self.body, Environment(self.par, args, self.env))

#Called to evaluate expressions
def evaluate(x, env=global1):
    #Variable Reference or Procedure Reference
    if type(x)==str:
        if x[0] == '"' or x[0] == "'":
            return x
        return env.find(x)

    #Constant
    elif type(x)==int or type(x)==float:
        return x

    #If a single integer/variable/string is in paranthesis
    elif len(x)==1:
        if type(x[0])==str and (x[0][0] == '"' or x[0][0] == "'"):
            return x[0][1:len(x[0])-1]
        return evaluate(x[0])

    #Separate arguments and operator
    op = x[0]
    args = x[1:]

    #If statement
    if op == 'if':
        if evaluate(args[0],env):  #Evaluates the if condition in env
            xt = args[1]
        else:
            xt = args[2]
        return evaluate(xt,env) #Evaluates the relevant statement based on the if condition

    #Conditional statement
    elif op == 'cond':
        for j in args:  #Checks each argument sequentially
            if j[0] == 'else':  #If the cond starts with else, evaluate it
                return evaluate(j[1],env)
                break
            else:
                t = evaluate(j[0],env)  #Evaluate the condition
                if t:   #If condition is true then evaluate the body.
                    return evaluate(j[1],env)
                    break
    
    #Procedure or variable definition
    elif op == 'define':
        (name, expr) = args
        if type(name) == list:
            pass
        else:
            env.d[name] = evaluate(expr, env)

    #Lambda function
    elif op == 'lambda':
        (par,body) = args
        return Procedure(par, body, env)

    #Procedure call
    else:
        procedure = evaluate(op,env)
        val = [evaluate(arg,env) for arg in args]
        return procedure(*val)

#Runs forever
while 1:
    print ">",
    #Takes input, tokenizes it and evaluates it
    temp = raw_input().strip()
    if temp == '':
        continue
    temp = evaluate(Tokenizer.fulltokenize(temp))
    #For statements which return None like define, do not print None
    if temp != None:
        print temp
    
