import sys
'''
recursively check if the CNF sentence evaluates to true
Input: CNF sentence, literal value assignemnts (model)
Output:evaluation, 0 for False, 1 for True

'''
def evaluateTrue(sentence,model):

  if sentence[0].istitle(): #Check if first element is literal
    if sentence[0] in model: #check if the literal is in the model, return the value of literal
      
      if model[sentence]==1: 
         return 1
      elif model[sentence]==0:
         return 0
    else:
      return None
  elif sentence[0]=="not": #if negated literal, return reverse value from the one in the model
    res=evaluateTrue(sentence[1], model)
    if res==None: return None
    else: 
      res=1-res
      return res
  elif sentence[0]=="or": # if 1 element is true the whole clause is true
    for literal in range(1, len(sentence)):
      res=evaluateTrue(sentence[literal],model)
      if res==None: return None
      elif res==1: return 1
    return 0  
  
  elif sentence[0]=="and": #if 1 element is false the whole clause is false
    for clause in sentence:
      res=evaluateTrue(clause,model)
      if res==0: return 0
      if res==None: return None
    return 1    

'''
Method that returns all clauses in a CNF sentence
Input: CNF sentence y
Output: Array of clauses
'''
def getClauses(y):
  newArr=[]
  if (y[0]=="and"):
    for i in range(1,len(y)):
      newArr.append(y[i])
  elif y[0]=="not":
    newArr.append(y)
  elif y[0]=="or":
    newArr.append(y)
  else:
    for i in range(0, len(y)):
      newArr.append(y[i])
  return newArr
  
'''
Method that returns a unique set of all the literals in a CNF-Sentence
Input: CNF sentence y
Output: list of symbols
'''
def getSymbols(y):
  if isinstance(y,list):
    symbols=set(())
    for i in range(0,len(y)): #check all clauses
      for symb in getSymbols(y[i]): #check all items in clause
        if symb.istitle():
          symbols.add(symb)
    return list(symbols) #convert set to list and return it
  elif y.istitle(): #if original expression is only 1 literal
    return [y]
  return y
    
'''
Helper method to open a text file and return a line
'''
def readFile(inputFile):
  lines=[]
  with open(inputFile) as myFile:
    for line in myFile:
      lines.append(line)
  return lines    
'''
Method that finds and eliminates unit clauses from CNF sentence.
It is used as a heuristic for SAT solver.

Input: clauses( array of CNF "or" clauses), model (set of values for the literals in clauses)
Output: P,Value. Literal and value to be assigned if found
'''
def findUnitClause(clauses,model):
  for clause in clauses:
    count=0 #counter of number of instances of specific literal
    if len(clause)==2 and clause[0]=="not": #check for ~literal not in a "or" clause
      if clause[1] not in model: #if found save it with value of false
        P,value=clause[1],0
        count=count+1
    else:
      for lit in range(0,len(clause)): 
        if isinstance(clause[lit],list):
          if clause[lit][1] not in model: # check for ~literal in "or" clause
            P,value=clause[lit][1], 0
            count=count+1
        elif clause[lit] not in model and clause[lit].istitle(): #check for literal in clause
          count=count+1
          P,value=clause[lit],1
      if count==1: #if only one instance of literal is found return literal and its assigned value
        return P,value
  return None,None
       
'''
Method that finds and returns a pure symbol from a set of claues.
A pure symbol is a Literal appears as only on of: Y or ~Y in all clauses.
If there is such Literal a true or ~true value can be assigned to it respectively. 

Inputs: array of unique symbols, array of clauses
Outputs: P,Value (Literal, Value of literal)
'''      
def pureSymbol(symbols,clauses):
  for literal in symbols:
    literalExists=False # true if Y exist
    invertLiteralExists=False #true if ~Y exists
    for clause in clauses:
      if literal in clause and not literalExists: #check if Y is in a clause
          literalExists=True
      if isinstance(clause,list) or clause[0]=="not": #check if ~Y is in a clause
        if clause[1]==literal and not invertLiteralExists:
          invertLiteralExists=True
    if literalExists!=invertLiteralExists: #if only Y or only ~Y exist return literal and value
      return literal, literalExists
  return None, None

#remove item from array  
def removeSymbol(literal,symbols):
  if literal in symbols: symbols.remove(literal)
  return symbols
    
#helper method, copy original model, add new literal and value.
#return the new method set
def addToModel(model,P,value):
  newMod=model.copy()
  newMod[P]=value
  return newMod

'''
Main recursive function to calculate SAT assignment of a CNF sentence. 
Inputs: array of "or " claues, array of unique symbols in clauses, a model set of symbol value assignments
'''
  
def dpllAlgo(clauses, symbols, model):
  i=0
  j=0
  for clause in clauses:
    value=evaluateTrue(clause,model)
    if value==0: #if one clause evaluates to false return false
      return False
    if value==1:
      i=i+value
    j=j+1
  if i==j: #if all clause evaluate to true return true along with the assigned model
    return "true",model
#recursively populate model set, using heuristics: pure symbol , unit clause
  P,value=pureSymbol(symbols,clauses) 
  if P:
    return dpllAlgo(clauses,removeSymbol(P,symbols),addToModel(model,P,value)) 
  P,value=findUnitClause(clauses,model)
  if P:
    return dpllAlgo(clauses,removeSymbol(P,symbols),addToModel(model,P,value)) 
  P=symbols.pop()
  return (dpllAlgo(clauses,symbols, addToModel(model,P,1))) or (dpllAlgo(clauses,symbols,addToModel(model,P,0)))

'''
Helper function to modify string output to appropriate format.
Input: out array of boolean value and model set (out). Array of unique symbols in 
CNF-sentence
output: array of modified strings 
'''
def fixOutput(out,symbols):
  if out==False:
    return ["false"]
  else:
    outArr=["true"]
    for i in symbols:
      if i in out[1]:
      	if out[1][i]==1:
          str1=i+"="+"true"
        else: 
          str1=i+"="+"false"
        outArr.append(str1)
      else: #default value. If no value assigned to literal assign true. 
        str1=i+"="+"true"
        outArr.append(str1)
  return outArr

def main():

  line=readFile(sys.argv[2])
  out=open("CNF_satisfiability.txt","w")
  for x in range(1,int(line[0])+1):
    lineList=eval(line[x])
    symbols=getSymbols(lineList)
    clauses=getClauses(lineList)
    result = (dpllAlgo(clauses,symbols,{}))
    out.write(str(fixOutput(result,getSymbols(lineList))))
    out.write('\n')
 

  
main()