import itertools
from collections import defaultdict
from tkinter import *
import webbrowser
#Whole program is in a function to allow for a restart button.
def start():
  global root
  global rowCounter
  #Generating the root window in tkinter.
  root=Tk()
  root.iconbitmap("lotus-icon.ico")
  backcolour="Azure"
  errorText=StringVar()
  errorText.set("")
  errorMessage=Label(root,textvariable=errorText,fg="RED",bg=backcolour)
  errorMessage.place(x=144,y=28)
  root.geometry("530x200+200+200")
  root.grid_columnconfigure(0,uniform="foo")
  root.configure(bg=backcolour)
  root.winfo_toplevel().title("Desync's Seating Planner")
  #Generating labels for buttons.
  #The buttons themselves are generated at the end, due to function dependancies.
  tableSizeLabel=Label(root,text="Max seats per table:", bg=backcolour)
  tableSizeLabel.place(x=30,y=4)
  tableSize=Entry(root,width=10)
  tableSize.place(x=144,y=5)
  spacer=Label(root, bg=backcolour)
  spacer.grid(row=2)
  nameLabel=Label(root,text="Name:",bg=backcolour)
  preferenceLabel=Label(root,text="Preferences:",bg=backcolour)
  nameLabel.place(x=10,y=45)
  preferenceLabel.place(x=144,y=45)
  #Implementing scrollbar functionality for the entry field.
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
  fastMode=IntVar()
  toggle=Checkbutton(root,text="Fast Mode?",variable=fastMode,bg=backcolour,activebackground=backcolour,anchor=W)
  def size(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=505,height=105)
  entryFrame.bind("<Configure>",size)
  nameList=[]
  pref1List=[]
  pref2List=[]
  pref3List=[]
  #Generating 5 initial rows of entries.
  #rowCounter is used later to add more rows.
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
  #people is a list of guests.
  #preferences is a dictionary, keys are guests and values are their preferences.
  people=[]
  preferences={}
  def execute():
    global rowCounter
    for rows,nEntry in enumerate(nameList):
      if nEntry.get()!="":
        if nEntry.get() not in people:
          people.append(nEntry.get())
        preferences[nEntry.get()]=(str(pref1List[rows].get()),
                                   str(pref2List[rows].get()),
                                   str(pref3List[rows].get())
                                   )
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
    adj_list = defaultdict(list)
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
    #Additionally, we prefer to use a splitting approach due to how the groups are formed:
    #If we were to split groups by chunks, we could potentially produce groups of size 1
    def splitHalf1(listIn):
      half = len(listIn)//2
      return listIn[:half]
    def splitHalf2(listIn):
      half = len(listIn)//2
      return listIn[half:]
    #We must have another function to repeat the splitting, as, for example:
    #If we had a max seating size of 3, and had a group of size 8,
    #Two groups of size 4 would be returned. This next function would then repeat,
    #Splitting into 4 groups of size 2, thus fixing the issue.
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
    #Finding all the people who didn't get put into mutPair at the beginning.
    for singledPerson in people:
      if any(singledPerson in p for p in mutPref):
        ungroupedPeople.remove(singledPerson)
    for element in ungroupedPeople:
      mutPref.append([element])
    #Fitting subgroups onto tables is equivalent to a bin packing problem.
    #Popping elements form list of a given size for later use in bin packing.
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
    #Due to the structure of mutPref, the worth, which we wish to sort by, is two layers deep in a list.
    #This function returns it to help with sorting.
    def takeSecond(elem):
      return elem[0]

    
    combinedMutualAndOptions=list(combineForSort(mutPref))
    combinedMutualAndOptions.sort(key=worthKey, reverse=True)
    finished=[]
    forbidden=[]
    print(combinedMutualAndOptions)

    while combinedMutualAndOptions!=[] and fastMode.get()==1:
      intermediary=[]
      for singleGroupWithOptions in combinedMutualAndOptions:
        weightedOptions=list(singleGroupWithOptions)
        compGroup=weightedOptions.pop(0)
        weightedOptions.sort(key=takeSecond, reverse=True)
        print("\n \n \n")
        print(compGroup)
        print("=============")
        if compGroup in forbidden:
          print("Forbidden")
          continue
        removeForbidden=list(weightedOptions)
        #We need to prevent groups (and their selected option) that have already been sorted, so we add it to forbidden.
        #If the program encounters a group in forbidden at any point, it'll break out of that loop.
        for counter,element in enumerate(weightedOptions):
          print(element)
          if element[1] in forbidden:
            print("^ forbidden")
            removeForbidden.remove(element)
        weightedOptions=list(removeForbidden)
        #Combining the selected group with its most optimal partner and pushing it to a temporary list, intermediary.
        #We loop this section repeatedly, until no more combinations are available.
        if weightedOptions!=[]:
          selectedOption=weightedOptions[0][1]
          intermediary.append(compGroup+selectedOption)
          forbidden.append(compGroup)
          forbidden.append(selectedOption)
        if weightedOptions==[]: #and len(singleGroupWithOptions[0])>1:
          finished.append(compGroup)
          forbidden.append(compGroup)
          print(compGroup)
          print("^ finished Group")
        #else:
        #  intermediary.append(compGroup)
      combinedMutualAndOptions=list(combineForSort(intermediary))
      combinedMutualAndOptions.sort(key=worthKey, reverse=True)
    
    while combinedMutualAndOptions!=[] and fastMode.get()==0:
      intermediary=[]
      singleGroupWithOptions=combinedMutualAndOptions.pop(0)
      weightedOptions=list(singleGroupWithOptions)
      compGroup=weightedOptions.pop(0)
      weightedOptions.sort(key=takeSecond, reverse=True)
      #print(compGroup)
      #print(weightedOptions)
      #print("\n\n\n")
      if compGroup in forbidden:
        continue
      removeForbidden=list(weightedOptions)
      for option in weightedOptions:
        if option[1] in forbidden:
          removeForbidden.remove(option)
      weightedOptions=list(removeForbidden)
      if weightedOptions!=[]:
        selectedOption=weightedOptions[0][1]
        intermediary.append(compGroup+selectedOption)
        forbidden.append(compGroup)
        forbidden.append(selectedOption)
      else:
        intermediary.append(compGroup)
      for group in combinedMutualAndOptions:
        intermediary.append(group[0])
      for element in intermediary:
        if element in forbidden:
          intermediary.remove(element)
      checkFinished=list(combineForSort(list(intermediary)))
      checkFinished.sort(key=worthKey, reverse=True)
      for singleGroupWithOptions2 in checkFinished:
        options=list(singleGroupWithOptions2)
        checkGroup=options.pop(0)
        if options==[]:
          finished.append(checkGroup)
          intermediary.remove(checkGroup)
          forbidden.append(checkGroup)
      combinedMutualAndOptions=[x for x in combineForSort(intermediary) if x]
      combinedMutualAndOptions.sort(key=worthKey, reverse=True)
      for group in combinedMutualAndOptions:
        if group[0]==[]:
          combinedMutualAndOptions.remove(group)
      #print(intermediary)
      #print("intermediary^^\n\n\n")
      #print(singleGroupWithOptions)
      #print("singlegroupwithoptions^^\n\n\n")
      #combinedMutualAndOptions.append
    print(finished)
    #Generating a StringVar to output tables.
    outputString=StringVar()
    outputString.set("No Data Input")
    for end in finished:
      if outputString.get()=="No Data Input":
        outputString.set("Tables:")
      outputString.set(outputString.get()+"\n\n"+str(end))
    #Generating frames and scrollbars for output.
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
  #Function to add more rows when the user presses a key when focussed on the bottom name entry.
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
  #Generating various buttons.
  runButton=Button(root,text="Execute",bg="WHITE",fg="BLACK",command=execute)
  runButton.configure(height=1,width=18)
  runButton.place(x=400,y=1)
  spacer3=Label(root,bg=backcolour)
  spacer4=Label(root,bg=backcolour)
  spacer3.grid(row=0,column=2,pady=1,sticky=W)
  spacer4.grid(row=1,column=2)
  #runButton.grid(row=0,column=3,sticky=E,pady=1)
  nameList[-1].bind("<Key>", addRow)
  clearButton=Button(root,text="Clear All",bg="WHITE",fg="RED",command=restart)
  clearButton.configure(height=1,width=8)
  clearButton.place(x=470,y=28)
  #clearButton.grid(row=1,column=3,sticky=SE)
  helpButton=Button(root,text="Help",bg="WHITE",fg="BLACK",command=openHelp)
  helpButton.configure(height=1,width=8)
  helpButton.place(x=400,y=28)
  toggle.place(x=300,y=1)
  root.geometry("")
  root.update()
  root.minsize(root.winfo_width()+10, root.winfo_height()+10)
  root.mainloop()
  
#Function for the restart button
def openHelp():
  webbrowser.open("README.txt")

def restart():
  root.destroy()
  start()
openHelp()
start()
