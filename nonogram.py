import numpy as np

class Nonogram:
  
  def __init__(self):

      self.size = int(input("enter size: "))
      self.grid = np.array([[0]*self.size]*self.size)
      self.keys = {'row' : [[2],[1,1],[3],[4],[5]],
                   'column' : [[3,1],[1,3],[3],[1,2],[2]] }
      
      self.restart()

  #re-setup; needs implement to make a game
  def restart(self):

      self.cases = self.generate(self.keys)
      return self.fill()
    
  #returns function: (i-th row or j-th column) -> possible cases
  def generate(self, keys):

      # runs gen2(); converts casesby2 to real cases; stored in cases['axis']
      def gen(axis):
        for key in keys[axis]:
          self.casesby2=[] # temporary storage of a row
          gen2([0]+[1]*(len(key)-1)+[0],
              self.size -sum(key) - len(key) + 1)

          #case_temp to store cases for a line      
          case_temp = []
          for caseby2 in self.casesby2:
            case =[]
            for j in range(len(key)):
              case += [2]*caseby2[j]
              case += [1]*key[j]
            case += [2]*caseby2[-1]
          
            case_temp.append(case)
          cases[axis] += [case_temp]

      # generates cases for a line, by 2(blanks); stored in self.casesby2
      def gen2(ls, n):
        if n==0:
          if ls not in self.casesby2: self.casesby2 += [ls]
          return
        for i in range(len(ls)):
          ls_copy = [j for j in ls]
          ls_copy[i] += 1
          gen2(ls_copy, n -1)

      cases = {'row':[],'column':[]}

      #pop because error; why 'row' is cases + None?
      cases['row'] += [gen('row')] ; cases['row'].pop()
      cases['column'] += [gen('column')] ; cases['column'].pop()

      return cases
  
  # fills every (i-th row or j-th column); if surely filled or blanked
  def fill(self):

    # find sure boxes in a line, in given line and cases
    def sort(line, axis, line_index):
      
      cases = self.cases[axis][line_index]

      # remove cases contradict to given line
      cases_sorted = [i for i in cases]
      for box_index, box_value in enumerate(line):
        if sum(line) ==0 : break
        if box_value ==0 : continue
        for case in cases:
          if (case[box_index] != box_value) and (case in cases_sorted): 
            cases_sorted.remove(case)

      # find intersection in each box; if not, use previous value
      result = []
      for box_index, cases_boxwise in enumerate(zip(*cases_sorted)):
        if (2 not in cases_boxwise) : 
          result.append(1)
        elif (1 not in cases_boxwise):
          result.append(2) 
        else : result.append(line[box_index])

      if set(result) == set(line): delta = False
      else : delta = True

      #update self.grid
      #print(axis,line_index,result)
      if axis == 'row':
        self.grid[line_index,:] = result
      if axis == 'column':
        self.grid[:,line_index] = result

      return delta
    
    # solve every row and column, until there's no change in self.grid
    delta = True
    while delta:
      delta = False
      for i in range(self.size):
        delta1 = sort(self.grid[i,:], 'row'   , i)
        if delta1: delta = True
      for i in range(self.size):
        delta2 = sort(self.grid[:,i], 'column', i)
        if delta1: delta = True

    return

x = Nonogram()
print(x.keys)
print('-------------')
for i in x.grid:
  print(i)
