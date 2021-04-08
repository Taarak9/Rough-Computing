import numpy as np
import pandas as pd
import itertools
from collections import Counter

class IND:

  def __init__(self, filename):
    self.filename = filename

  def get_table(self):
    df = pd.read_csv(self.filename, delimiter = " ")
    df.set_index(['U'], inplace=True)
    return df

  def power_set(self, A):
    length = len(A)
    return {
            frozenset({e for e, b in zip(A, f'{i:{length}b}') if b == '1'})
            for i in range(2 ** length)
    }

  def get_IND(self, attribute_set):
    df = self.get_table()

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

  #1. To list out all possible Indiscernibility relation of a given Decision System DS:<U, Union(A,{d})>

  def get_IND_list(self, A):
    p_A = self.power_set(A)

    IND_list = []
    for subset in p_A:
      if ( len(subset) != 0 ):
        #print("B: ", subset)
        #print("IND(B): ", get_IND(df, subset))
        #print("----------------------------------")
        IND_list.append(self.get_IND(subset))

    #print("Total no of Indiscernibility relations possible are: ", len(IND_list))

    return IND_list
  
  # 2. To obtain an equivalence class for a given element x of U with respect to an 
  #Indiscernibility relation “R”.  Say [x]R. from an IND relation we could get the attribute set

  def get_eq_class(self, attribute_set, x):
  
    IND = self.get_IND(attribute_set)

    eq_class = { x }
    for i in IND:
      if x in i:
        if (i[0] != x):
          eq_class.add(i[0])
        if (i[1] != x):
          eq_class.add(i[1])

    return eq_class

  # 3. To demonstrate [x]R = [y]R  if xRy  otherwise Intersection([x]R,[y]R ) = Null_Set

  def check_relation(self, attribute_set, x, y):
    
    x_class = self.get_eq_class(attribute_set, x)
    y_class = self.get_eq_class(attribute_set, y)

    if ( x_class == y_class ):
      print("x and y are related, they belong to same equivalent class. \n")

    if ( len(x_class & y_class) == 0 ):
      print("x and y are not related, they does not belong to same equivalent class \n")

  # 4. To collect all equivalence classes of U with respect to a given indiscernibility relation “R”.
  # Say  U/R={[x]R|x belongs to U}

  def get_partition(self, attribute_set):
    df = self.get_table()

    U = set(df.index.values.tolist())

    partition = []
    eq_class = set()
    for u in U:
      eq_class = self.get_eq_class(attribute_set, u)
      if eq_class not in partition:
        partition.append(eq_class)

    return partition

  # 5. To demonstrate U/R is a partition of U and 
  # further the cardinality of U/R is the same as the cardinality of V(B). 
  # Here R is "INDDS(B)" for a given subset B of A and 
  # V(B) is the unique value combination of domain values of attributes in B realized in DS.

  def check_partition(self, attribute_set):

    partition = self.get_partition(attribute_set)

    union_p = set()
    for p in partition:
      union_p = union_p | set(p)

    # checking if any two eq classes have common elements
    for p1 in partition:
      for p2 in partition:
        if ( p1 != p2 and len( set(p1) & set(p2) ) != 0 ):
          return False
    # checking if union of all eq classes is U
    U = set(ds.index.values.tolist())
    if ( union_p == U ):
      return True

  def check_P_cardinality(self, attribute_set):
    df = self.get_table()

    partition = self.get_partition(attribute_set)

    V_b = df[attribute_set].values.tolist()
    # V_b range and domain has same cardinality
    n_V_b = len(Counter([tuple(i) for i in V_b]))

    if ( len(partition) == n_V_b ):
      return True
    else:
      return False

  # 6. Let IND(B1) and IND(B2) be two Indiscernibility relations where B1, B2 are subsets of A
  #a. To demonstrate “INDDS(B1) and INDDS(B2)”,  is also an Indiscernibility relation equivalent to INDDS(Union(B1 , B2)).

  def check_union_IND_property(self, B1, B2):

    IND_B1 = set(tuple(b1) for b1 in self.get_IND(B1))
    #print("IND_B1", IND_B1)

    IND_B2 = set(tuple(b2) for b2 in self.get_IND(B2))
    #print("IND_B2", IND_B2)

    IND_B = IND_B1 & IND_B2
    #print("IND_B", IND_B)
    
    B = B1 | B2

    INDDS = set(tuple(b) for b in self.get_IND(B))
    #print("INDDS", INDDS)

    if ( IND_B == INDDS ):
      return True
    else:
      return False

  #b. To demonstrate U/INDDS(Union(B1 , B2))  is refinment of U/INDDS(B1) and U/INDDS(B2)

  def check_P_union_refinment(self, B1, B2):

    B = B1 | B2

    P_b = set(tuple(b) for b in self.get_partition(B))
    #print("P_b ", P_b)

    P_b1 = set(tuple(b1) for b1 in self.get_partition(B1))

    P_b2 = set(tuple(b2) for b2 in self.get_partition(B2))

    P_b1_and_b2 = P_b1 & P_b2
    #print("P_b1_and_b2 ", P_b1_and_b2)

    if ( P_b.issuperset(P_b1_and_b2) == True ):
      return True
    else:
      return False

  # 7. To demonstrate U/INDDS(Union(A,{d})) is refinement of all possible partitions 
  # induced by Indiscernibility relations of a given Decision System DS:<U, Union(A,{d})> .

  def check_union_all_refinement(self, attribute_set):

    P_u = set(tuple(u) for u in self.get_partition(attribute_set))

    pow_A = self.power_set(attribute_set)

    P_all_possible = set()
    for s in pow_A:
      P_all_possible = P_all_possible & set(tuple(e) for e in self.get_partition(s))

    if ( P_u.issuperset(P_all_possible) == True ):
      return True
    else:
      return False
