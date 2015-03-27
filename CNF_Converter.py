import json
import sys
'''
Method to open and read file. 
Input: string (the name of the file)
Output: containt of the file in an array
'''
def readFile(inputFile):
  lines=[]
  with open(inputFile) as myFile:
    for line in myFile:
      lines.append(line)
  return lines    

'''
Method to push negations if possible on a propositional sentence:
and or distribution remains the same.
'''
def removeNeg(y):
  if y[0][0].istitle(): #checking if letter is capital
    return y
  if y[0]=="not": # checking if negation literal
    if y[1][0]=="not":
      return removeNeg(y[1][1])
    if y[1][0].istitle():
      return y
  if y[0]=="and":
    return ("and", removeNeg(y[1]), removeNeg(y[2]))
  if y[0]=="or":
    return ("or", removeNeg(y[1]), removeNeg(y[2]))
  if y[0]=="not": # pushing negations inside the clause
    if y[1][0]=="and":
      return ("or", removeNeg(["not", y[1][1]]), removeNeg(["not",y[1][2]]))
    if y[1][0]=="or":
      return ("and", removeNeg(["not",y[1][1]]), removeNeg(["not",y[1][2]]))

'''
Method that returns all the disjunctions in the logical sentence connected by "and"
Helper function for concat
'''
def disjunct(arg1, arg2):
 
  if arg1[0]=="and":
    return ("and",disjunct(arg1[1], arg2), disjunct(arg1[2], arg2))
  elif arg2[0]=="and": 
    return ("and",disjunct(arg1, arg2[1]), disjunct(arg1, arg2[2]))

  else:
  	return concat("or",("or", arg1, arg2)) # if the and clause has more than one or clause
'''
Final step in CNF conversion. Pushes ands and ors. 

'''
def convertCNF(y):
  if y[0][0].istitle(): #check if element is literal if yes return it to complete recursion
    return y
  elif y[0]=="not": #check if element is negated literal. if yes return it to complete recursion
    return y
  elif y[0]=="and": #if recursively investigate the or clauses
    return ["and",convertCNF(y[1]), convertCNF(y[2])]
  elif y[0]=="or": # if or clause push it to disjunct function to distribute ands between the variables
    return disjunct(convertCNF(y[1]), convertCNF(y[2]))

'''
Helper method to eliminate redundant ands/ors. Operator to be eliminated is
specified by the op input variable. y is the logical sentence 
'''
def concat(op,y):
  newList=[]
  for x in range(0,len(y)):
    if y[x][0]==op:
      for j in range(1,len(y[x])):
        newList.append(y[x][j])
    else:
      newList.append(y[x])
  
  if len(y)==1: 
    return y[0]

  return newList;
          
'''
Method to remove iff and implies from a logical sentence. And/Or and negations are kept the same
'''
def removeArrow(y):
  if y[0][0].istitle():#end recursion
    return y
  if y[0]=="not":
    return("not", removeArrow(y[1]))# check if negated element is literal or clause
  if y[0]=="and":
    return("and", removeArrow(y[1]), removeArrow(y[2])) #check if clauses have iff/implies
  if y[0]=="or":
    return ("or", removeArrow(y[1]), removeArrow(y[2])) 
  if y[0]=="implies":
    return removeArrow(["or", ["not", y[1]], y[2]]) #convert =>
  if y[0]=="iff":
    return removeArrow(["and", ["or", ["not", y[1]], y[2]], ["or",y[1], ["not", y[2]]]]) #convert <=>

'''
Helper method to remove duplicates from finalized CNF sentence of the form (and,(or..),(or..),(not .))
Does not work very well need to revisit this.
'''  
def removeDup(myList):
  if myList[0]=="not":#check if element is a negated element if yes just return it
    return myList
  if myList[0]=="or":  #if its an or clause, 
    tempList=[]
    for e in range(1,len(myList)):
      tempList.append(myList[e])
    tempList= [list(t) for t in set(map(tuple, tempList))]#convert it to a set of tuples to eliminate duplicates. Convrt back to list
    finalList=["or"]
    for e in range (0,len(tempList)):
      if tempList[e][0]=="not":
        finalList.append(tempList[e])
      else:
        finalList.append(str(tempList[e][0]))
    return finalList
  if myList[0].istitle():
    return myList
  if myList[0]=="and":#if outer (and) clause, recursively visit every inner clause or literal. 
    newArr=["and"]
    for elem in range(1,len(myList)):
      newArr.append(removeDup(myList[elem]))
    return newArr  
'''
main function converts a logical sentence from input file to CNF and prints to output file
'''
def main():
  line=readFile(sys.argv[2])

  out=open("sentences_CNF.txt","w")
  for x in range(1,int(line[0])+1):
    lineList=eval(line[x]) # convert string line to list.
    output=convertCNF((removeNeg(removeArrow(lineList))))
    output=concat("and",output)
    output=removeDup(output)
    tempStr=json.dumps(output)
    print>>out,tempStr
 

main()
  