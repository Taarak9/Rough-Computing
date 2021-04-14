import numpy as np
import pandas as pd

# Using Matrix Simplification method
class COMPUTE_REDUCT:

  def __init__(self, filename):
    self.filename = filename

  def get_table(self):
    df = pd.read_csv(self.filename, delimiter = " ")
    df.set_index(['ID'], inplace=True)
    return df

  def get_discernibilty(self, element):
    df = self.get_table()

    A = df.columns[:-1].values.tolist()
    d = df.columns[-1]
    U = df.index.values.tolist()

    discernibility = []
    for u in U:
      if (u == element or df.loc[u][d] == df.loc[element][d]):
        discernibility.append(set())
      else:
        temp = []
        for a in A:
          if (df.loc[u][a] != df.loc[element][a]):
            temp.append(a)
        discernibility.append(set(temp))
    
    return discernibility

  # 1. To obtain discernibility matrix
  def get_discernibility_matrix(self):
    df = self.get_table()

    U = df.index.values.tolist()

    discernibility_list = []
    for u in U:
      discernibility_list.append(self.get_discernibilty(u))
      
    discernibility_tril = list(np.tril(discernibility_list))

    for dis in discernibility_tril:
      for i in range(len(dis)):
        if (dis[i] == 0):
          dis[i] = set()

    discernibility_matrix = pd.DataFrame(discernibility_tril, index=U, columns=U)

    return discernibility_matrix

  # 2. To construct a Boolean function representing the discernibility of an element x. Say BF(x).
  def BF(self, element):
    df = self.get_table()

    dm = self.get_discernibility_matrix()

    U = df.index.values.tolist()

    bf = set(df.columns[:-1].values.tolist())
    for d in dm.iloc[U.index(element)].values.tolist():
      if (type(d) == set):
        bf = bf & d
    
    return bf
  
  # In decision system IND(A) U IND(D)
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

    attribute_d_values = list(zip( df.index.values.tolist(), df.iloc[:,-1:].values.tolist() ) )
    #print(attribute_d_values)

    for d1 in attribute_d_values:
      for d2 in attribute_d_values:
        if ( d1[1] == d2[1] ):
              if [ d1[0], d2[0] ] not in IND:
                IND.append([ d1[0], d2[0] ])
      
    return IND

  def get_eq_class(self, attribute_set, x):
    df = self.get_table()

    IND = self.get_IND(attribute_set)

    eq_class = { x }
    for i in IND:
      if x in i:
        if (i[0] != x):
          eq_class.add(i[0])
        if (i[1] != x):
          eq_class.add(i[1])

    return eq_class

  # 3. Consider R=IND(B) for an attribute subset B. Write a function to show that BF(x) =BF(y) 
  # if y belongs to [x]R

  def check_bf_property(self, attribute_set, x, y):
    df = self.get_table()

    IND = self.get_IND(attribute_set)

    x_R = self.get_eq_class(attribute_set, x)
    #print("x_R ", x_R)
    if y in x_R:
      #print("BF x", BF(df, x))
      #print("BF y", BF(df, y))

      if (self.BF(df, x) == self.BF(df, y)):
        return True
      else:
        return False

  def attribute_set_deletion(self, dm, attribute_set):

    specification_dm_list = dm.values.tolist()

    for a in attribute_set:
      if {a} in dm.values:
        continue
      else:
        for dis in specification_dm_list:
          for i in range(len(dis)):
            if ({a}.issubset(dis[i])):
              dis[i].remove(a)

    U = dm.index.values.tolist()

    specification_dm = pd.DataFrame(specification_dm_list, index=U, columns=U)

    return specification_dm

  def get_possible_elements(self, dm, length):

    p_list = dm.values.tolist()

    elements = []
    for dis in p_list:
      for i in dis:
        if (len(i) == length):
          elements.append(i)

    return [i for n, i in enumerate(elements) if i not in elements[:n]]

  # argument discernibility_matrix
  def matrix_absorption(self, dm):

    eq_dm_list = dm.values.tolist()

    max_len = len(max(dm.max().values.tolist()))

    possible_len = np.arange(2, max_len)

    for l in possible_len:

      possible_elements = self.get_possible_elements(dm, l)

      for p in possible_elements:
        for dis in eq_dm_list:
          for i in range(len(dis)):
            if (p.issubset(dis[i])):
              dis[i] = p

    U = dm.index.values.tolist()

    eq_dm = pd.DataFrame(eq_dm_list, index=U, columns=U)

    return eq_dm

  def get_del_attributes(self):
    df = self.get_table()

    m = self.get_discernibility_matrix()
    l1 = self.get_possible_elements(m, 1)
    #print(l1)

    A = set(df.columns[:-1].values.tolist())

    del_attributes = set()
    
    if ( len(l1) > 0 ):
      for l in l1:
        for a in A:
          if ( l != {a} ):
            del_attributes.add(a)
    else:
      del_attributes = A
    
    return del_attributes

  def min_discernibility_matrix(self, del_attributes):
    df = self.get_table()

    dm = self.get_discernibility_matrix()
    #print("initial dm\n", dm)

    for a in del_attributes:
      #print("attribute ", a)
      spec_dm = self.attribute_set_deletion(dm, {a})

      #print("dm after deletition \n", spec_dm)

      eq_dm = self.matrix_absorption(spec_dm)

      #print("dm after absorption \n", eq_dm)

      dm = eq_dm
      #print("dm after \n", dm)

    return dm.values.tolist()

  def power_set(self, A):
      length = len(A)
      return {
          frozenset({e for e, b in zip(A, f'{i:{length}b}') if b == '1'})
          for i in range(2 ** length)
      }

  def union_dm(self, dm_list):

    reduct = set()

    for dis in dm_list:
      for e in dis:
        reduct = reduct | e

    return reduct

  # 4. To obtain the characteristic formula of the system DS and its simplification/representation
  # as a normal form

  # 5. To obtain all the basic formulae of the system DS. 
  # Say a set of attributes in a basic formula as one Reduct.

  def compute_reduct(self):

    del_attributes = self.get_del_attributes()
    #print("del attributes ", del_attributes)

    possible_reducts = []

    del_attributes = self.power_set(self.get_del_attributes())

    possible_reducts = []

    for d in del_attributes:
      if (len(d) > 0):
        #print("min dm ", min_discernibility_matrix(df, d))
        possible_reducts.append(self.union_dm(self.min_discernibility_matrix(d)))

    possible_reducts.sort(key=len)

    #print("possible reducts ", possible_reducts)

    min_len = len(min(possible_reducts))

    minimal_reducts = []
    for r in possible_reducts:
      if ( len(r) == min_len and r not in minimal_reducts ):
        minimal_reducts.append(r)

    return minimal_reducts

  # 6. To obtain the intersection of all the sets of attributes corresponding to basic formulae, 
  # That is to compute the intersection of all Reducts.  Say this set as CORE.

  def compute_core(self, minimal_reducts):
    df = self.get_table()

    core = set(df.columns[:-1].values.tolist())
    
    for r in minimal_reducts:
      core = core & r

    return core

filename = 'dm.txt'

red = COMPUTE_REDUCT(filename)

reduct = red.compute_reduct()
print("Reduct: ", reduct)

core = red.compute_core(reduct)
print("Core: ", core)
