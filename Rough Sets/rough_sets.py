import numpy as np
import pandas as pd

class ROUGH_SETS:

  def __init__(self, filename, A):
    self.filename = filename
    self.A = A

  def get_table(self):
    df = pd.read_csv(self.filename, delimiter = " ")
    return df

  #1. To provide partition of the tuples of the table for a given attribute
  def get_partition(self, attribute):
    df = self.get_table()
    attribute_values = df[['ID', attribute]].values.tolist()
    #print(attribute_values)

    attribute_types = np.unique(df[attribute].values.tolist())
    #print(attribute_types)

    partition = []
    temp = []

    for t in attribute_types:
      for i in attribute_values:
        if ( t == i[1] ):
          temp.append(i[0])
      partition.append(temp)
      temp = []
  
    del attribute_values
    del attribute_types
    del temp
    del t
    del i

    return partition

  #2. Using the function of task 1, compute partitions for all the attributes of the table
  def all_partitions(self):
    df = self.get_table()
    for attribute in df.columns:
      print("partition w.r.t " + attribute, get_partition(df, attribute))

  #3. To produce a simple set of given set A
  def simple_set(self, setA):
    return set(setA)

  #4. To produce frequency table of elements of given set A
  def freq_table(self, setA):
    f_table = []
    for s in setA:
      f_table.append( [ s, list(setA).count(s) ] )

    f_df = pd.DataFrame(f_table)

    del f_table
    del s

    return f_df


  #5. To get the cardinality of a given set A 
  def get_cardinality(self, setA):
    return len(setA)

  #6. To get the cardinality of the corresponding simple set of a given set A.
  def cardinality_simple_set(self, setA):
    return len(set(setA))
    
  #7. To get the complement of a given set A.
  def complement(self, setA, U):
    return U - setA

  #8. To produce (a) intersection, (b) Union, (c) set difference of given two sets A and B
  def intersection(self, setA, setB):
    return setA & setB

  def union(self, setA, setB):
    return setA | setB

  def set_difference(self, setA, setB):
    return setA - setB

  #9. To develop boolean functions for testing whether (a) is A a subset of B  (b) is A equals to B
  def is_subset(self, setA, setB):
    return setA.issubset(setB)

  def is_equal(self, setA, setB):
    return setA == setB
  
  '''
  10. To develop a boolean flag vector corresponding to elements of a given partition P,
  (a) is A  a super set of element of P 
  (b) is A has a non-trivial intersection with the element of P.
  '''
  def is_superset(self, partitionP):
    vector = []
    for element in partitionP:
      if ((self.A.issuperset(element)) == True):
        vector.append(1)
      else:
        vector.append(0)
    del element

    return vector

  def nt_intersection(self, partitionP):
    vector = []
    for element in partitionP:
      if ( len(self.A & set(element)) == 0 ):
        vector.append(0)
      else:
        vector.append(1)
    del element

    return vector

  '''
  11. To obtain the union of elements of the given partition P for which the flags are one (true) based on  
  (a) super set flags 
  (b) non-trivial intersection flags for a given set A
  The resultant sets will be referred as Lower Approximation of A and Upper Approximation of A respectively with respective to the partition P.
  '''
  def get_LSA(self, partitionP):
    vector = self.is_superset(partitionP)

    LSA = set()
    for index, v in enumerate(vector):
      if (v == 1):
        LSA = self.union(LSA, set(partitionP[index]))
  
    return LSA

  def get_USA(self, partitionP):
    vector = self.nt_intersection(partitionP)

    USA = set()
    for index, v in enumerate(vector):
      if (v == 1):
        USA = self.union(USA, set(partitionP[index]))
  
    return USA

  '''
  12. Develop an algorithm which returns Lower and Upper Approximations of given set A 
  with respective to given Partition P.  Name this function as f_LUSA(A,P)  
  let us denote the return values of the algorithm as LSA and USA
  '''
  def f_LUSA(self, A, P):
    self.A = A
    LSA = self.get_LSA(P)
    USA = self.get_USA(P)

    return LSA, USA

  #13. To obtain the set difference of USA and LSA. Say this resultant set as the Boundary set of A denoted as BNA.
  def get_BNA(self, P):
    LSA, USA = self.f_LUSA(self.A, P)
    BNA = self.set_difference(USA, LSA)

    return BNA

  #14.  To obtain the complement set of USA. Say this resultant set as a Negative set of A denoted as NGA.
  def get_NGA(self, P, U):
    USA = self.get_USA(P)
    return self.complement(USA, U)

  '''
  15. Develop an algorithm to get the Cardinality of sets A, U, LSA, USA,  BNA and NGA 
  with respective to a Partition P obtained from  an attribute 
  of a given Information System or Decision System. Say the output of this algorithm 
  as n_A, N_U, n_LSA, n_USA, n_BNA and n_NGA  respectively.
  '''
  def cardinality_sets(self, attribute, U):

    P = self.get_partition(attribute)

    LSA, USA = self.f_LUSA(self.A, P)
  
    n_A = self.get_cardinality(A)
    n_U = self.get_cardinality(U)
    n_LSA = self.get_cardinality(LSA)
    n_USA = self.get_cardinality(USA)
    n_BNA = self.get_cardinality(self.get_BNA(P))
    n_NGA = self.get_cardinality(self.get_NGA(P, U))

    return n_A, n_U, n_LSA, n_USA, n_BNA, n_NGA

  #16. To verify that LSA, BNA and NGA of given set A with respect to a given Partition P is a partition of U, the Universal set.
  def verify_partition(self, A, P, U):
    self.A = A
    
    LSA = self.get_LSA(P)
 
    BNA = self.get_BNA(P)
 
    NGA = self.get_NGA(P, U)
 

    if ( ( len( LSA & BNA ) == 0 ) and ( len( BNA & NGA ) == 0 ) and ( len( NGA & LSA ) == 0 ) and ( LSA | BNA | NGA == U )):
      return True
    else:
      return False

###

filename = 'info_table.txt'
A = {1, 2, 3}
U = {1, 2, 3, 4, 5, 6}

rough_set = ROUGH_SETS(filename, A)

P = rough_set.get_partition("AOI")
rough_set.cardinality_sets("AOI", U)
print(rough_set.verify_partition(A, P, U))
