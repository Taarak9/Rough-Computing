import numpy as np
import pandas as pd

'''
Consider a Decision System DS: :<U, Union(A,{d})>
Consider B, B1, B2 subset of A
Consider D,D1,D2 as Union(B,{d},  Union(B1,{d}) , Union(B2,{d}) respectively.
'''

def power_set(A):
    length = len(A)
    return {
        frozenset({e for e, b in zip(A, f'{i:{length}b}') if b == '1'})
        for i in range(2 ** length)
    }

def get_IND(df, attribute_set):

    attribute_list = list(attribute_set)

    attribute_values = list(zip( df.index.values.tolist(), df[attribute_list].values.tolist() ))
    #print(attribute_values)

    IND = []

    for v1 in attribute_values:
      for v2 in attribute_values:
        if ( v1[1] == v2[1] ):
          IND.append([ v1[0], v2[0] ])
  
    del attribute_values
    del v1
    del v2
    
    return IND

def get_eq_class(df, attribute_set, x):
   
  IND = get_IND(df, attribute_set)

  eq_class = { x }
  for i in IND:
    if x in i:
      if (i[0] != x):
        eq_class.add(i[0])
      if (i[1] != x):
        eq_class.add(i[1])

  return eq_class

def get_partition(df, attribute_set):

  U = set(df.index.values.tolist())

  partition = []
  eq_class = set()
  for u in U:
    eq_class = get_eq_class(df, attribute_set, u)
    if eq_class not in partition:
      partition.append(eq_class)

  return set(tuple(p) for p in partition)

def get_concepts(df, attribute_set):
  pow_A = list(power_set(attribute_set))
  
  #Let
  B = pow_A[0]
  B1 = pow_A[3]
  B2 = pow_A[6]

  d = set()
  #last column in DS is the d
  d.add(df.columns[-1])

  D = B | d
  D1 = B1 | d
  D2 = B2 | d

  return [B, B1, B2, D, D1, D2, d]

# 1. To obtain P=U/INDDS(B) , P1=U/INDDS(B1), P2=U/INDDS(B2), Q=U/INDDS(D), Q1=U/INDDS(D1),
# Q2=U/INDDS(D2) and S=U/INDDS({d})


def get_partitions(df, attribute_set):

  B, B1, B2, D, D1, D2, d = get_concepts(df, attribute_set)

  P = get_partition(df, B)
  P1 = get_partition(df, B1)
  P2 = get_partition(df, B2)
  Q = get_partition(df, D)
  Q1 = get_partition(df, D1)
  Q2 = get_partition(df, D2)
  S = get_partition(df, d)

  return [P, P1, P2, Q, Q1, Q2, S]

# 2. To demonstrate Q, Q1 and Q2 are refinements of P and S, P1 and S & P2 and S respectively.

def check_refinements(df, attribute_set):

  P, P1, P2, Q, Q1, Q2, S = get_partitions(df, attribute_set)

  if ( Q.issuperset(P & S) and Q1.issuperset(P1 & S) and Q2.issuperset(P2 & S) ):
    return True
  else:
    return False

def is_superset(setA, partitionP):
  vector = []
  for element in partitionP:
    #print("element ", set(element), "set ", setA)
    if ( setA.issuperset( set(element) ) ):
      #print("superset")
      vector.append(1)
    else:
      vector.append(0)
  del element
  #print("vector ", vector)
  return vector

def nt_intersection(setA, partitionP):
  vector = []
  for element in partitionP:
    if ( len(setA & set(element)) == 0 ):
      vector.append(0)
    else:
      vector.append(1)
  del element

  return vector

def get_LSA(setA, partitionP):
  #print("lsa partition ", partitionP)

  vector = is_superset(setA, partitionP)
  #print("vector ", vector)
  LSA = set()
  i = 0
  for p in partitionP:
    if (vector[i] == 1):
      LSA = LSA | set(p)
      #print("LSA ", LSA)
    i = i + 1

  return LSA

def get_USA(setA, partitionP):
  vector = nt_intersection(setA, partitionP)

  USA = set()

  i = 0
  for p in partitionP:
    if (vector[i] == 1):
      USA = USA | set(p)
    i = i + 1
      
  return USA

def get_BNA(setA, P):
    
    LSA = get_LSA(setA, P)
    USA = get_USA(setA, P)

    BNA = USA - LSA

    return BNA

def get_NGA(df, setA, P):
  U = set(df.index.values.tolist())
  USA = get_USA(setA, P)
  return U - USA

# 3. To obtain  LSA,USA,BNA,NGA for each element of S considering the a. P b. P1 c. P2 d. Q e. Q1 f. Q2

def get_approximations(df, setA, P):
  LSA= get_LSA(setA, P)
  USA= get_USA(setA, P)
  BNA= get_BNA(setA, P)
  NGA= get_NGA(df, setA, P)

  approximations = [LSA, USA, BNA, NGA]

  return approximations

def run_approximations(df, attribute_set): 

  P, P1, P2, Q, Q1, Q2, S = get_partitions(df, attribute_set)

  P_appr, P1_appr, P2_appr, Q_appr, Q1_appr, Q2_appr = [], [], [], [], [], []

  for s in S:
    P_appr.append(get_approximations(df, set(s), P))
    P1_appr.append(get_approximations(df, set(s), P1))
    P2_appr.append(get_approximations(df, set(s), P2))
    Q_appr.append(get_approximations(df, set(s), Q))
    Q1_appr.append(get_approximations(df, set(s), Q1))
    Q2_appr.append(get_approximations(df, set(s), Q2))

  approximations = [ P_appr, P1_appr, P2_appr, Q_appr, Q1_appr, Q2_appr ]
  
  return approximations

# 4. To obtain the Accuracy of Approximation of each element of S considering the
# a. P b. P1 c. P2 d. Q e. Q1 f. Q2

def approx_accuracy(appr_list):

  acc = []

  for l in range(len(appr_list)):
    if (len(appr_list[l][0]) == 0):
      acc.append(0)
    else:
      acc.append( len(appr_list[l][0]) / len(appr_list[l][1]) ) 

  return acc

def run_approximations_accuracy(df, attribute_set):

  P, P1, P2, Q, Q1, Q2, S = get_partitions(df, attribute_set)

  P_appr, P1_appr, P2_appr, Q_appr, Q1_appr, Q2_appr = run_approximations(df, attribute_set)

  return [ approx_accuracy(P_appr), approx_accuracy(P1_appr), approx_accuracy(P2_appr),
          approx_accuracy(Q_appr), approx_accuracy(Q1_appr), approx_accuracy(Q2_appr) ]

# 5. To obtain the Rough Membership  of each element of U considering the
# a. P b. P1 c. P2 d. Q e. Q1 f. Q2

def rm(U, X, P):

  #partition = set(tuple(e) for e in partition)
  rm_all = []
  for a in U:
    #print("a: ", a)
    for p in P:
      if a in p:
        x_a = p
        #print("x_a: ", x_a)
        #print("set: ", X)
        rm_all.append( len( set(x_a) & X ) / len(x_a) )

  return rm_all

def run_rm(df, X, attribute_set):

  P, P1, P2, Q, Q1, Q2, S = get_partitions(df, attribute_set)

  U = set(df.index.values.tolist())

  return [ rm(U, X, P), rm(U, X, P1), rm(U, X, P2), rm(U, X, Q),
           rm(U, X, Q1), rm(U, X, Q2), rm(U, X, S) ]

# 6. To obtain the Degree of Dependency  of “d” considering the
# a. B b. B1 c. B2

def posA_B(df, attribute_setA, attribute_setB):
  POS = set()  
  for b in get_partition(df, attribute_setB):
    POS = POS | get_LSA(set(b), get_partition(df, attribute_setA))

  return POS

#degree B depends on A
def degree_of_dependency(df, attribute_setA, attribute_setB):

  U = set(df.index.values.tolist())
  POS = posA_B(df, attribute_setA, attribute_setB)

  degree = len(POS) / len(U)

  return degree

def run_degree(df, attribute_set):
  B, B1, B2, D, D1, D2, d = get_concepts(df, A)

  return [ degree_of_dependency(df, B, d), degree_of_dependency(df, B1, d), degree_of_dependency(df, B2, d) ]

# 7. To obtain Dispensable and Indispensable attributes of DS

def attribute_type(df, attribute_setA, attribute_setB):
 
  A = set(df.columns[:-1].values.tolist())
  dispensable = []
  indispensable = []

  for a in A:
    A_dash = attribute_setA - set({a})

    if ( posA_B(df, attribute_setA, attribute_setB) == posA_B(df, A_dash, attribute_setB) ):
      dispensable.append(a)
    else:
      indispensable.append(a)

  return [ dispensable, indispensable ]
