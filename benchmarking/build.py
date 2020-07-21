import random;
import itertools;
from collections import defaultdict
from tkinter import *
import time;
def start():
  global rowCounter
  global preferences
  global people
  global root
  global output
  root=Tk()
  root.iconbitmap("lotus-icon.ico")
  backcolour="Azure"
  errorText=StringVar()
  errorText.set("")
  errorMessage=Label(root,textvariable=errorText,fg="RED",bg=backcolour)
  errorMessage.place(x=144,y=28)
  root.geometry("530x200+400+400")
  root.grid_columnconfigure(0,uniform="foo")
  root.configure(bg=backcolour)
  root.winfo_toplevel().title("Desync's Seating Planner")
  tableSizeLabel=Label(root,text="Max seats per table:", bg=backcolour)
  tableSizeLabel.place(x=28,y=4)
  tableSize=Entry(root,width=10)
  tableSize.place(x=144,y=5)

  testSize=Entry(root,width=10)
  testSize.place(x=244,y=5)
  timeTaken=StringVar()
  timeOutput=Label(root,textvariable=timeTaken,fg="RED",bg=backcolour)
  timeOutput.place(x=244,y=28)
  
  spacer=Label(root, bg=backcolour)
  spacer.grid(row=2)
  nameLabel=Label(root,text="Name:",bg=backcolour)
  preferenceLabel=Label(root,text="Preferences:",bg=backcolour)
  nameLabel.place(x=10,y=52)
  preferenceLabel.place(x=144,y=52)
  outerFrame=Frame(root,width=505,height=200,bg=backcolour)
  outerFrame.grid(row=3,column=0,columnspan=4)
  canvas=Canvas(outerFrame,bg=backcolour)
  canvas.pack(side="left")
  scroll=Scrollbar(outerFrame,command=canvas.yview)
  scroll.pack(side="right",fill="y",padx=5)
  canvas.configure(yscrollcommand=scroll.set)
  entryFrame=Frame(canvas,bg=backcolour)
  entryFrame.grid(row=0,column=0,columnspan=4)
  canvas.create_window((0,0),window=entryFrame,anchor="nw")
  def size(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=505,height=105)
  entryFrame.bind("<Configure>",size)
  nameList=[]
  pref1List=[]
  pref2List=[]
  pref3List=[]
  rowCounter=2
  for Row in range(5):
    nameEntry=Entry(entryFrame)
    nameEntry.grid(column=0,row=Row+3,padx=10,pady=1)
    nameList.append(nameEntry)
    pref1Entry=Entry(entryFrame)
    pref1List.append(pref1Entry)
    pref1Entry.grid(column=1,row=Row+3)
    pref2Entry=Entry(entryFrame)
    pref2List.append(pref2Entry)
    pref2Entry.grid(column=2,row=Row+3)
    pref3Entry=Entry(entryFrame)
    pref3List.append(pref3Entry)
    pref3Entry.grid(column=3,row=Row+3)
    rowCounter+=1
  
  def execute():
    with open("names.txt", "r") as f:
      people=[line.strip() for line in f]
    preferences={}
    people=people[:int(testSize.get())]
    for person in people[:int(testSize.get())]:
      #print(person)
      preferences[person]=(people[random.randint(0,int(testSize.get())-1)],people[random.randint(0,int(testSize.get())-1)],people[random.randint(0,int(testSize.get())-1)])
    #print(preferences)
    startTime=time.perf_counter()
    
    for rows,nEntry in enumerate(nameList):
      if nEntry.get()!="":
        if nEntry.get() not in people:
          people.append(nEntry.get())
        preferences[nEntry.get()]=(str(pref1List[rows].get()),str(pref2List[rows].get()),str(pref3List[rows].get()))
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
    for pair in itertools.combinations(people,2):
      try:
        preferences[pair[1]]
      except:
        errorText.set("Invalid Preference")
        raise
      if pair[0] in preferences[pair[1]] and pair[1] in preferences[pair[0]]:
        mutPair.append(pair)
    adj_list = defaultdict(list)
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
    def splitHalf1(listIn):
      half = len(listIn)//2
      return listIn[:half]
    def splitHalf2(listIn):
      half = len(listIn)//2
      return listIn[half:]
    def fullSplit(listIn):
      while any(len(x)>seatingMax for x in listIn):
        for x in listIn:
          listIn.remove(x)
          listIn.append(splitHalf1(x))
          listIn.append(splitHalf2(x))
          break
      return listIn
    mutPref=fullSplit(mutPref)
    ungroupedPeople=list(people)
    for singledPerson in people:
      if any(singledPerson in p for p in mutPref):
        ungroupedPeople.remove(singledPerson)
    for element in ungroupedPeople:
      mutPref.append([element])
    def bysize(words, size):
        return [word for word in words if len(word) == size]
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
    def combineForSort(unsortedList):
      groupWithOptionsWeighted=[]
      for counter,groupOptions in enumerate(detFit(unsortedList, createOptionList(unsortedList))):
        skippedVal=list(groupOptions)
        skippedVal.insert(0,unsortedList[counter])
        groupWithOptionsWeighted.append(skippedVal)
      return groupWithOptionsWeighted
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
    combinedMutualAndOptions=list(combineForSort(mutPref))
    combinedMutualAndOptions.sort(key=worthKey, reverse=True)
    internalCopy=list(combinedMutualAndOptions)

    finished=[]
    forbidden=[]
    timeout=0
    while internalCopy!=[]:
      intermediary=[]
      for singleGroupWithOptions in internalCopy:
        weightedOptions=list(singleGroupWithOptions)
        compGroup=weightedOptions.pop(0)
        weightedOptions.sort(key=takeSecond, reverse=True)
        if compGroup in forbidden:
          continue
        internal2=list(weightedOptions)
        for counter,element in enumerate(weightedOptions):
          if element[1] in forbidden:
            internal2.remove(element)
        weightedOptions=list(internal2)
        if weightedOptions!=[]:
          selectedOption=weightedOptions[0][1]
          intermediary.append(compGroup+selectedOption)
          forbidden.append(compGroup)
          forbidden.append(selectedOption)
        if weightedOptions==[] and len(singleGroupWithOptions[0])>1:
          finished.append(compGroup)
          forbidden.append(compGroup)
        else:
          intermediary.append(compGroup)
      internalCopy=list(combineForSort(intermediary))
      internalCopy.sort(key=worthKey, reverse=True)
    outputString=StringVar()
    outputString.set("No Data Input")
    for end in finished:
      if outputString.get()=="No Data Input":
        outputString.set("Tables:")
      outputString.set(outputString.get()+"\n\n"+str(end))
    outputFrame=Frame(root,bg=backcolour,pady=10)
    outputFrame.grid(row=4,column=0,columnspan=4,sticky=W+E)
    spacer2=Frame(outputFrame, bg=backcolour,width=10)
    spacer2.pack(side="left")
    outputCanvas=Canvas(outputFrame,bg="WHITE",bd=0)
    outputCanvas.pack(side="left")
    outputScroll=Scrollbar(outputFrame,command=outputCanvas.yview)
    outputScroll.pack(side="right",fill="y",padx=10)
    outputCanvas.configure(yscrollcommand=outputScroll.set)
    messageFrame=Frame(outputCanvas)
    messageFrame.pack(fill="x")
    outputCanvas.create_window((0,0),window=messageFrame,anchor="nw")
    def size2(event):
      outputCanvas.configure(scrollregion=outputCanvas.bbox("all"),width=493,height=200)
    messageFrame.bind("<Configure>",size2)
    output=Label(messageFrame,bg="WHITE",textvariable=outputString,justify="left",relief="flat",wraplength=480)
    output.pack()
    root.update()
    root.geometry("")
    root.minsize(root.winfo_width(), root.winfo_height())
    endTime=time.perf_counter()
    totalTime=round(endTime-startTime,5)
    timeTaken.set(totalTime)
  def addRow(key):
    global rowCounter
    for widget in root.winfo_children():
      if isinstance(widget,Message):
        widget.destroy()
    nameEntry=Entry(entryFrame)
    nameEntry.grid(column=0,row=rowCounter+3,pady=1)
    nameList.append(nameEntry)
    pref1Entry=Entry(entryFrame)
    pref1List.append(pref1Entry)
    pref1Entry.grid(column=1,row=rowCounter+3)
    pref2Entry=Entry(entryFrame)
    pref2List.append(pref2Entry)
    pref2Entry.grid(column=2,row=rowCounter+3)
    pref3Entry=Entry(entryFrame)
    pref3List.append(pref3Entry)
    pref3Entry.grid(column=3,row=rowCounter+3)
    rowCounter=rowCounter+1
    nameList[-1].bind("<Key>", addRow)
    nameList[-2].unbind("<Key>")
    root.update()
    canvas.yview_moveto(1)
  runButton=Button(root,text="Execute",bg="WHITE",fg="BLACK",command=execute)
  runButton.configure(height=1,width=8)
  runButton.grid(row=0,column=3,sticky=E,pady=1)
  nameList[-1].bind("<Key>", addRow)
  clearButton=Button(root,text="Clear All",bg="WHITE",fg="RED",command=restart)
  clearButton.configure(height=1,width=8)
  clearButton.grid(row=1,column=3,sticky=SE)
  root.geometry("")
  root.update()
  root.minsize(root.winfo_width()+10, root.winfo_height()+10)
  root.mainloop()
def restart():
  root.destroy()
  start()
start()
