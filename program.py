import random;
import itertools;
from collections import defaultdict
from tkinter import *


#whole program is in a function to allow a restart button.
def start():
  global rowCounter
  global preferences
  global people
  global root
  #generating the root window in tkinter.
  root=Tk()
  backcolour="Azure"
  errorText=StringVar()
  errorText.set("")
  errorMessage=Label(root,textvariable=errorText,fg="RED",bg=backcolour)
  errorMessage.grid(row=1,column=1,sticky=NW)
  root.geometry("515x200")
  root.configure(bg=backcolour)
  root.winfo_toplevel().title("Desync's Seating Planner")
  #generating labels for buttons.
  tableSizeLabel=Label(root,text="Max seats per table:", bg=backcolour)
  tableSizeLabel.grid(row=0,column=0,sticky=E,pady=10)
  tableSize=Entry(root)
  tableSize.grid(row=0,column=1)
  spacer=Label(root, bg=backcolour)
  spacer.grid(row=1)
  nameLabel=Label(root,text="Name:",bg=backcolour)
  preferenceLabel=Label(root,text="Preferences:",bg=backcolour)
  nameLabel.grid(row=2,sticky=W,padx=20)
  preferenceLabel.grid(row=2,column=1,sticky=W)

  rowCounter=3

  nameList=[]
  pref1List=[]
  pref2List=[]
  pref3List=[]

  #Generating 5 initial rows of entries.
  #rowCounter is used later to add more rows.
  rowCounter=2
  for Row in range(5):
    nameEntry=Entry(root)
    nameEntry.grid(column=0,row=Row+3,padx=10,pady=1)
    nameList.append(nameEntry)
    pref1Entry=Entry(root)
    pref1List.append(pref1Entry)
    pref1Entry.grid(column=1,row=Row+3)
    pref2Entry=Entry(root)
    pref2List.append(pref2Entry)
    pref2Entry.grid(column=2,row=Row+3)
    pref3Entry=Entry(root)
    pref3List.append(pref3Entry)
    pref3Entry.grid(column=3,row=Row+3)
    rowCounter+=1
  #people is a list of guests.
  #preferences is a dictionary, keys are guests and values are their preferences.
  people=[]
  preferences={}
  def execute():
    for rows,nEntry in enumerate(nameList):
      if nEntry.get()!="":
        if nEntry.get() not in people:
          people.append(nEntry.get())
        preferences[nEntry.get()]=(str(pref1List[rows].get()),str(pref2List[rows].get()),str(pref3List[rows].get()))
        #Ensuring all guests have 3 preferences as to not skew weightings.
        if pref1List[rows].get()=="" or pref2List[rows].get()=="" or pref3List[rows].get()=="":
          errorText.set("Empty Preference")
          errorMessage.update()
          raise
    #Assorted error checks.
    try:
      int(tableSize.get())
    except:
      errorText.set("Input Error")
      raise
    seatingMax=int(tableSize.get())
    if seatingMax<3:
      errorText.set("Tables must be >2")
      raise
    if len(people)<seatingMax:
      errorText.set("Not enough data")
      raise
    mutPair=[]
    #Adding people who prefer each other as length-2 pairs into a list, mutPair.
    for pair in itertools.combinations(people,2):
      try:
        preferences[pair[1]]
      except:
        errorText.set("Invalid Preference")
        raise
      if pair[0] in preferences[pair[1]] and pair[1] in preferences[pair[0]]:
        mutPair.append(pair)
    adj_list = defaultdict(list)#
    #Connecting all pairs which share common elements is equivalent to finding trees in a non-connected graph.
    #Function for depth-first-search is implemented to this end.
    def dfs(adj_list, visited, vertex, result, key):
      visited.add(vertex)
      result[key].append(vertex)
      for neighbor in adj_list[vertex]:
        if neighbor not in visited:
          dfs(adj_list, visited, neighbor, result, key)
    for x, y in mutPair:
      adj_list[x].append(y)
      adj_list[y].append(x)
    result = defaultdict(list)
    visited = set()
    for vertex in adj_list:
      if vertex not in visited:
        dfs(adj_list, visited, vertex, result, vertex)
    mutPref=list(result.values())
    #Splitting subgroups that are too large for a table.
    #Function has to be in two pieces, or the returned value is a tuple.
    def splitHalf1(listIn):
        half = len(listIn)//2
        return listIn[:half]
    def splitHalf2(listIn):
        half = len(listIn)//2
        return listIn[half:]
    for x in mutPref:
      if len(x)>seatingMax:
        mutPref.remove(x)
        mutPref.append(splitHalf1(x))
        mutPref.append(splitHalf2(x))
    ungroupedPeople=list(people)
    #Finding all the people who didn't get put into mutPair at the beginning.
    for singledPerson in people:
      if any(singledPerson in p for p in mutPref):
        ungroupedPeople.remove(singledPerson)
    for element in ungroupedPeople:
      mutPref.append([element])
    #Fitting subgroups onto tables is equivalent to a bin packing problem.
    #Bin packing by inspection is used.
    def bysize(words, size):
        return [word for word in words if len(word) == size]
    #Listing all possible other group placements for each group in mutPref.
    def createOptionList(inputGroupList):
      fitOptions=[]
      for aGroup in inputGroupList:
        c=0
        fit=[]
        while c<(seatingMax-len(aGroup)):
          fit.extend(bysize(inputGroupList,seatingMax-(len(aGroup)+c)))
          c=c+1
        if aGroup in fit:
          fit.remove(aGroup)
        fitNoNull=[n for n in fit if n]
        fitOptions.append(fitNoNull)
      return fitOptions
    #Function to determine compatiblity between possible group pairings.
    #Returned value, worthGroup, is a list containing lists of tuples of possible matches
    #per table with element index 0 (of each tuple) being their relative compatibility.
    #If a fixedGroup has no matching groups, an empty list is returned at its index.
    def detFit(setGroups, testGroups):
      worthGroup=[]
      for fxgCount,fixedGroup in enumerate(setGroups):
        listTogether=[]
        for matchGroup in testGroups[fxgCount]:
          worth=0
          for matchPerson in matchGroup:
            if any(m in preferences[matchPerson] for m in fixedGroup):
              worth=worth+1
          for fixedPerson in fixedGroup:
            if any(n in preferences[fixedPerson] for n in matchGroup):
              worth=worth+1
          goodMatch=[]
          goodMatch.append([p for p in matchGroup])
          goodMatch.insert(0,worth)
          listTogether.append([q for q in goodMatch])
        worthGroup.append([r for r in listTogether if r])
      return worthGroup
    #Function to combine lists together to keep matching groups together during sort.
    def combineForSort(unsortedList):
      groupWithOptionsWeighted=[]
      for counter,groupOptions in enumerate(detFit(unsortedList, createOptionList(unsortedList))):
        skippedVal=list(groupOptions)
        skippedVal.insert(0,unsortedList[counter])
        groupWithOptionsWeighted.append(skippedVal)
      return groupWithOptionsWeighted
    #Function which outputs maximum worth value of a sublist.
    #This is to assign higher priority to groups with higher worths first.
    def worthKey(inputlist):
      maximum=0
      for counter,sublist in enumerate(inputlist):
        if counter==0:
          continue
        if sublist[0]>maximum:
          maximum=sublist[0]
      return maximum
    #Due to the structure of mutPref, the worth, which we wish to sort by, is two layers deep in a list
    #This function returns it to help with sorting.
    def takeSecond(elem):
      return elem[0]
    combinedMutualAndOptions=list(combineForSort(mutPref))
    combinedMutualAndOptions.sort(key=worthKey, reverse=True)
    internalCopy=list(combinedMutualAndOptions)
    finished=[]
    forbidden=[]
    while internalCopy!=[]:
      intermediary=[]
      timeout=0
      for singleGroupWithOptions in internalCopy:
        weightedOptions=list(singleGroupWithOptions)
        #Combining the selected group with its most optimal partner and pushing it to a temporary list, internal2
        #We loop this section repeatedly, until no more combinations are available.
        compGroup=weightedOptions.pop(0)
        weightedOptions.sort(key=takeSecond, reverse=True)
        internal2=list(weightedOptions)
        #We need to prevent groups (and their selected option) that have already been sorted, so we add it to forbidden.
        #If the program encounters a group in forbidden at any point, it'll break out of that loop.
        for counter,element in enumerate(weightedOptions):
          if element[1] in forbidden:
            internal2.remove(element)
        weightedOptions=list(internal2)
        if weightedOptions!=[]:
          selectedOption=weightedOptions[0][1]
          intermediary.append(compGroup+selectedOption)
          forbidden.append(compGroup)
          forbidden.append(selectedOption)
        if weightedOptions==[] and len(singleGroupWithOptions[0])>2:
          finished.append(compGroup)
          forbidden.append(compGroup)
        else:
          intermediary.append(compGroup)
        timeout+=1
        if timeout>100:
          print("timed out")
          raise
      internalCopy=list(combineForSort(intermediary))
      internalCopy.sort(key=worthKey, reverse=True)
    #Generating a box for the output.
    outputString="No Data Input"
    for end in finished:
      if outputString=="No Data Input":
        outputString="Tables:"
      outputString=outputString+"\n"+str(end)
    output=Message(root,bg="WHITE",text=outputString,justify="left",relief="sunken",width=100)
    output.grid(columnspan=4,row=rowCounter+3,column=0,pady=10,padx=10,sticky=W)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height()+60)
    root.maxsize(root.winfo_width(), root.winfo_height()+60)
  #Function to add more rows when the user types into the bottom row.
  def addRow(key):
    global rowCounter
    nameEntry=Entry(root)
    nameEntry.grid(column=0,row=rowCounter+3)
    nameList.append(nameEntry)
    pref1Entry=Entry(root)
    pref1List.append(pref1Entry)
    pref1Entry.grid(column=1,row=rowCounter+3)
    pref2Entry=Entry(root)
    pref2List.append(pref2Entry)
    pref2Entry.grid(column=2,row=rowCounter+3)
    pref3Entry=Entry(root)
    pref3List.append(pref3Entry)
    pref3Entry.grid(column=3,row=rowCounter+3)
    rowCounter=rowCounter+1
    nameList[-1].bind("<Key>", addRow)
    nameList[-2].unbind("<Key>")
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height()+20)
    root.maxsize(root.winfo_width(), root.winfo_height()+20)
  #Generating buttons.
  runButton=Button(root,text="Execute",bg="WHITE",fg="BLACK",command=execute)
  runButton.configure(height=1,width=8)
  runButton.grid(row=0,column=3,sticky=E)
  nameList[-1].bind("<Key>", addRow)
  clearButton=Button(root,text="Clear All",bg="WHITE",fg="RED",command=restart)
  clearButton.configure(height=1,width=8)
  clearButton.grid(row=1,column=3,sticky=SE)
  root.update()
  root.minsize(root.winfo_width()+10, root.winfo_height())
  root.maxsize(root.winfo_width()+10, root.winfo_height())
  root.mainloop()
#Function for the restart button
def restart():
  root.destroy()
  start()
start()
