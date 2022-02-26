from tabulate import tabulate
from itertools import product

def getBrackets(wff):
  ##((~Q|~T)&(~Q|T)) 
  wff = str(wff)
  bracketList = []
  for i in range(len(wff)):
    sum = 0
    if wff[i] == "(":
      for j in range(i+1, len(wff)):
        if wff[j] == "(":
          sum += 1
        elif wff[j] == ")" and (sum == 0):
          bracketList.append((i,j))
          break
        elif wff[j] == ")":
          sum -= 1
  return bracketList

def getAtoms(wff):
  wff = str(wff)
  b = ["(",")","∧", "∨", "¬", "→", ",","⊢","⊨"]
  c = ['P', 'Q', 'R', 'S', 'T']
  a = []
  n = []
  for i in range(len(wff)):
    if wff[i] == '¬':
      if wff[i+1] in c and wff[i+1] not in a:
        n.append(str(wff[i] + wff[i+1]))
    if wff[i] not in b and wff[i] not in a:
      a.append(wff[i])
  return a,n

def getTerms(wff, bracket):
  wff = str(wff)
  terms = []
  for pairs in bracket:
    terms.append(wff[pairs[0]:1+pairs[1]])
  return terms[::-1]

def populateLists(atoms, terms):
  """
  makes 2^n, n = terms, lists and returns them as a list of lists
  """
  print("Generated truth table for %s..." % str(terms[-1]))

  val = [1, 0]
  total = len(atoms) + len(terms)
  total_terms = atoms + terms
  
  l = []
  for i in range(2**(len(atoms))):
    l.append([])

  # Fill a number of different lists based on 2**n power set
  if len(atoms) == 2:
    cart_prod = [(a,b) for a in val for b in val]
    for i in range(0, 2**len(atoms)):
      l[i].append(cart_prod[i][0])
      l[i].append(cart_prod[i][1])
  if len(atoms) == 3:
    cart_prod = [(a,b,c) for a in val for b in val for c in val]
    for i in range(0, 2**len(atoms)):
      l[i].append(cart_prod[i][0])
      l[i].append(cart_prod[i][1])
      l[i].append(cart_prod[i][2])
  # Fill lists.
  for r in range(0,(2**(len(atoms)))):
    for c in range(len(atoms), total):
      try:
        seq = terms[c-len(atoms)]

        l_at = get_relevant_atoms(seq,'l')
        l_neg = False
        if l_at[0] == '¬':
          l_at = l_at[1:]
          l_neg = True
        l_index = total_terms.index(l_at)

        r_at = get_relevant_atoms(seq,'r')
        r_neg = False
        if r_at[0] == '¬':
          r_at = r_at[1:]
          r_neg = True
        r_index = total_terms.index(r_at)
        
        l_val = l[r][l_index]
        r_val = l[r][r_index]

        left = l_at, l_val, l_neg
        right = r_at, r_val, r_neg

        # want to call not Q or T with T, 
        # so fill l[2] with atom(l[0], l[1])
        l[r].append(computeTruth(seq, left, right))
        
      except (IndexError):
        print("@ %d, %d" % (r,c))

  return l
    
def get_relevant_atoms(wff, t):
  str(wff)
  b = getBrackets(wff)
  op = findOperatorIndex(b)

  if len(b) > 1:
    if t == 'l':
      return wff[1:op]
    if t == 'r':
      if wff[op+1] == '¬':
        return wff[op+1:-1]
      else:
        return wff[op+1:-1]

  if len(b) == 1:
    for i in range(len(wff)):
      if wff[i] == '∧' or wff[i] == '∨':
        apexPos = i
        if t == 'l':
          return wff[1:apexPos]
        if t == 'r':
          if wff[apexPos+1] == '¬':
            return wff[apexPos+1:-1]
          else:
            return wff[apexPos+1:-1]

def computeTruth(atom, p, q):
  br = len(getBrackets(atom))
  b = getBrackets(atom)

  l_val = p[1]
  r_val = q[1]
  l_neg = p[2]
  r_neg = q[2]

  if l_neg == True:
    l_val = flipTruthVal(l_val)
  if r_neg == True:
    r_val = flipTruthVal(r_val)

  # Calculate the truth of the statement.
  for i in range(len(atom)):
    if atom[i] == '∧' and br <= 2:
      if l_val + r_val == 2:
        return 1
    elif atom[i] == '∨' and br <= 2:
      if l_val + r_val >= 1:
        return 1
    elif atom[i] == '→' and br <= 2:
      if l_val == 0:
        return 1
      if l_val == 1:
        if r_val == 0:
          return 0
        elif r_val == 0:
          return 0

    if atom[i] == '∧' or atom[i] == '∨' and br == 3:
      op = findOperatorIndex(b)
      if atom[op] == '∨':
        if l_val + r_val >= 1:
          return 1
      elif atom[op] == '∧':
        if l_val + r_val == 2:
          return 1
  return 0

def findOperatorIndex(lis):
  taken = []
  if len(lis) > 1:
    for i in range(1,len(lis)):
      intList = [x for x in range(lis[i][0], lis[i][1]+1)]
      for i in range(len(intList)):
        if intList[i] not in taken:
          taken.append(intList[i])
    for i in range(lis[0][1]):
      if i not in taken and i != 0:
        return i
  
def flipTruthVal(q):
  try:
    if type(q) == int:
      if q == 1:
        return 0
      return 1
  except:
    print("error - atom not literal.")
    
def makeTable(wff):
  # call to make table
  str(wff)
  bracketList = getBrackets(wff)
  atoms, neg_atoms = getAtoms(wff)
  terms = getTerms(wff, bracketList)
  header = atoms + terms
  lis = populateLists(atoms, terms)
  
  table = (tabulate(lis, headers=header, tablefmt="github"))
  return table
