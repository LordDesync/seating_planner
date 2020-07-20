import random;
import itertools;
from collections import defaultdict
from tkinter import *

def start():
  global rowCounter
  global preferences
  global people
  global root
  root=Tk()

  root.winfo_toplevel().title("Desync's Seating Planner")

  tableSizeLabel=Label(root,text="Max seats per table:")
  tableSizeLabel.grid(row=0,column=0,sticky=E,pady=10)
  tableSize=Entry(root)
  tableSize.grid(row=0,column=1)
  spacer=Label(root)
  spacer.grid(row=1)

  nameLabel=Label(root,text="Name:")
  preferenceLabel=Label(root,text="Preferences:")

  nameLabel.grid(row=2,sticky=W,padx=20)
  preferenceLabel.grid(row=2,column=1,sticky=W)

  rowCounter=3

  nameList=[]
  pref1List=[]
  pref2List=[]
  pref3List=[]

  def clearFields():
    global preferences
    global people
    global rowCounter
    preferences.clear()
    people.clear()
    for row,nEntry in enumerate(nameList):
      nEntry.delete(0,END)
      pref1List[row].delete(0,END)
      pref2List[row].delete(0,END)
      pref3List[row].delete(0,END)

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

  people=[]
  preferences={}


  def dfs(adj_list, visited, vertex, result, key):
    visited.add(vertex)
    result[key].append(vertex)
    for neighbor in adj_list[vertex]:
      if neighbor not in visited:
        dfs(adj_list, visited, neighbor, result, key)
        
  def splitHalf1(listIn):
      half = len(listIn)//2
      return listIn[:half]
  def splitHalf2(listIn):
      half = len(listIn)//2
      return listIn[half:]

  def bysize(words, size):
      return [word for word in words if len(word) == size]

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


  def worthKey(inputlist):
    maximum=0
    for counter,sublist in enumerate(inputlist):
      if counter==0:
        continue
      if sublist[0]>maximum:
        maximum=sublist[0]
    return maximum

  def takeSecond(elem):
    return elem[0]

  def execute():
    for rows,nEntry in enumerate(nameList):
      if nEntry.get()!="":
        if nEntry.get() not in people:
          people.append(nEntry.get())
        preferences[nEntry.get()]=(str(pref1List[rows].get()),str(pref2List[rows].get()),str(pref3List[rows].get()))
        if pref1List[rows].get()=="" or pref2List[rows].get()=="" or pref3List[rows].get()=="":
          errorMessage=Label(root,text="Empty Preference")
          errorMessage.grid(row=1,column=1,sticky=NW)
          raise
    print(preferences)
    print(people)
    try:
      int(tableSize.get())
    except:
      errorMessage=Label(root,text="Input Error")
      errorMessage.grid(row=1,column=1,sticky=NW)
      raise
    seatingMax=int(tableSize.get())
    if seatingMax<3:
      errorMessage=Label(root,text="Tables must be >2")
      errorMessage.grid(row=1,column=1,sticky=NW)
      raise
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
    
    def combineForSort(unsortedList):
      groupWithOptionsWeighted=[]
      for counter,groupOptions in enumerate(detFit(unsortedList, createOptionList(unsortedList))):
        skippedVal=list(groupOptions)
        skippedVal.insert(0,unsortedList[counter])
        groupWithOptionsWeighted.append(skippedVal)
      return groupWithOptionsWeighted
    mutPair=[]
    #Adding people who prefer each other as tuples into a list, mutPair
    for pair in itertools.combinations(people,2):
      try:
        preferences[pair[1]]
      except:
        errorMessage=Label(root,text="Invalid Preference")
        errorMessage.grid(row=1,column=1,sticky=NW)
      if pair[0] in preferences[pair[1]] and pair[1] in preferences[pair[0]]:
        mutPair.append(pair)
    adj_list = defaultdict(list)
    for x, y in mutPair:
      adj_list[x].append(y)
      adj_list[y].append(x)
    result = defaultdict(list)
    visited = set()
    for vertex in adj_list:
      if vertex not in visited:
        dfs(adj_list, visited, vertex, result, vertex)
    mutPref=list(result.values())
    for x in mutPref:
      if len(x)>seatingMax:
        mutPref.remove(x)
        mutPref.append(splitHalf1(x))
        mutPref.append(splitHalf2(x))
    ungroupedPeople=list(people)
    for singledPerson in people:
      if any(singledPerson in p for p in mutPref):
        ungroupedPeople.remove(singledPerson)
    for element in ungroupedPeople:
      mutPref.append([element])
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
        compGroup=weightedOptions.pop(0)
        weightedOptions.sort(key=takeSecond, reverse=True)
  #      print("\n \n \n")
  #      print(compGroup)
  #      print("=============")
        if compGroup in forbidden:
  #        print("Forbidden")
          continue
        internal2=list(weightedOptions)
        for counter,element in enumerate(weightedOptions):
  #        print(element)
          if element[1] in forbidden:
  #          print("^ forbidden")
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
  #        print(compGroup)
  #        print("^ finished Group")
        else:
          intermediary.append(compGroup)
        timeout+=1
        if timeout>100:
          print("timed out")
          raise
      print("\n \n \n \n \n")
      internalCopy=list(combineForSort(intermediary))
      internalCopy.sort(key=worthKey, reverse=True)
    print(finished)
    print(rowCounter)
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
    print("addrow executed")
    print(rowCounter)
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height()+20)
    root.maxsize(root.winfo_width(), root.winfo_height()+20)

  runButton=Button(root,text="Execute",bg="WHITE",fg="BLACK",command=execute)
  runButton.grid(row=0,column=3,sticky=E)


  nameList[-1].bind("<Key>", addRow)
  clearButton=Button(root,text="Clear",fg="RED",command=restart)
  clearButton.grid(row=0,column=2,sticky=E)

  root.update()
  root.minsize(root.winfo_width()+10, root.winfo_height())
  root.maxsize(root.winfo_width()+10, root.winfo_height())
  root.mainloop()

def restart():
  root.destroy()
  start()
start()
