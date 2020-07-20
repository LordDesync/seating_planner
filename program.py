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
  global output
  #generating the root window in tkinter.
  root=Tk()
  backcolour="Azure"
  errorText=StringVar()
  errorText.set("")
  errorMessage=Label(root,textvariable=errorText,fg="RED",bg=backcolour)
  errorMessage.grid(row=1,column=1,sticky=NW)
  root.geometry("530x200+1100+200")
#  root.geometry("515x200+200+200")
  root.grid_columnconfigure(0,uniform="foo")
  root.configure(bg=backcolour)
  root.winfo_toplevel().title("Desync's Seating Planner")
  #generating labels for buttons.
  tableSizeLabel=Label(root,text="Max seats per table:", bg=backcolour)
  tableSizeLabel.place(x=28,y=4)
  tableSize=Entry(root,width=10)
  tableSize.place(x=144,y=5)
  spacer=Label(root, bg=backcolour)
  spacer.grid(row=2)
  nameLabel=Label(root,text="Name:",bg=backcolour)
  preferenceLabel=Label(root,text="Preferences:",bg=backcolour)
  nameLabel.place(x=10,y=52)
  preferenceLabel.place(x=144,y=52)
  #implementing scrollbar for the entry fields  
  outerFrame=Frame(root,width=505,height=200)
  outerFrame.grid(row=3,column=0,columnspan=4)
  canvas=Canvas(outerFrame)
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
  people=["Venetia","Jasmine R","Will H","Jonno","Benji","Phil","Frederick B","Frederick E","Teddy","Joe D","Tom S","Mackenzie","Sam S R","Louis P","Jacob E","Ben S","George A","Archie P","Connie","Maisie","Tabby","Libby","Liliane","Katie B","Ann K T","Petra","Esia","Grace","Anna W","Emma G","Guy P","Jack I","Harry J","Reggie","Maya T","Rachel B","Amelia E","Harrison J","Joe R","James G","Matthew O","Josh D","George Sand","Owen G","Ed R","George South","Alex D","Liv F","Hannah B","Cole T S","Kieran","Archie C","Jonny M","Jacob N","Alex H","Josie","Veks","India O","Liv C","Matthew F","Amelia O","Frank","Jerry","Lauren W","Joe A","Oli R","Leon B","Melissa S","Callum P","Lewis W","Nemph","Evie","Georgie W","Hamish","Rob H","Michael","Archie T","Zara","Emily K","Ed L","Gibbo","Anton","Emelia R","Amy P","Thomas D","Alex S","Karan","Steph S","Andy","Angus","Georgie R","Chris J","Jaz","Calum N","Aydan","Martha","Mark","Carys","Jack J"]
  preferences={}
  preferences["Venetia"]=("Jasmine R","Jonno","Will H")
  preferences["Jasmine R"]=("Amy P","Jonno","Katie B")  ###Vegetarian
  preferences["Will H"]=("Jonno","Esia","Grace")  ###Vegetarian
  preferences["Benji"]=("Phil","George A","Josie")
  preferences["Phil"]=("Benji","Archie P","Ben S")
  preferences["Frederick B"]=("Will M","Frederick E","Archie H")
  preferences["Frederick E"]=("Karan","Frank","Frederick B")
  preferences["Teddy"]=("Joe D","Mackenzie","Harrison J")
  preferences["Joe D"]=("Teddy","Tom S","Jack I")
  preferences["Tom S"]=("Mackenzie","Tom S","Teddy")
  preferences["Mackenzie"]=("Teddy","Joe D","Tom S")
  preferences["Sam S R"]=("George South","Jacob E","Finn")
  preferences["Louis P"]=("Jacob E","Finn","Lewis W") ###BLANK
  preferences["Ben S"]=("George A","Archie P","Phil")
  preferences["George A"]=("Reggie","Ed R","Benji")
  preferences["Archie P"]=("Harry J","Reggie","George A")
  preferences["Connie"]=("Maisie","Tabby","Libby")
  preferences["Maisie"]=("Libby","Connie","Tabby")
  preferences["Tabby"]=("Libby","Zara","Jacob N")
  preferences["Libby"]=("Connie","Tabby","Maisie")
  preferences["Liliane"]=("Katie B","Ann K T","BLANK")  ###Lactose Intolerant
  preferences["Ann K T"]=("Liliane","Katie B","Petra")  ###Vegetarian
  preferences["Petra"]=("Cole T S","Darcy","Martha###")  ###Vegetarian
  preferences["Esia"]=("Grace","Anna W","Emma G")
  preferences["Grace"]=("Liv F","Esia","Hannah B")
  preferences["Anna W"]=("Josie","Alex H","Hannah B")
  preferences["Emma G"]=("Alex H","Lauren W","Carys")
  preferences["Guy P"]=("Libby","Jacob N","Ed L]")
  preferences["Jack I"]=("Jonny M","Joe D","Jacob N")
  preferences["Harry J"]=("Ed R","Archie P","BLANK")
  preferences["Reggie"]=("Archie P","George A","Ed R")
  preferences["Maya T"]=("Rachel B","Amelia E","Abbie S")
  preferences["Rachel B"]=("Amelia E","Maya T","Abbie S")
  preferences["Amelia E"]=("Maya T","Leon B","Rachel B")
  preferences["Harrison J"]=("Teddy","Alex D","Rob H")
  preferences["Joe R"]=("James G","Matthew O","Josh D")
  preferences["James G"]=("Matthew O","Maisie","Connie")
  preferences["Matthew O"]=("James G","Maisie","Connie")
  preferences["Josh D"]=("Joe R","James G","Matthew O")  ##BLANK
  preferences["George Sand"]=("Joe R","Matthew O","James G")
  preferences["Owen G"]=("Ed R","Reggie","Harry J")
  preferences["Ed R"]=("Reggie","George A","Archie P")
  preferences["Alex D"]=("Harrison J","Tom S","Teddy")
  preferences["Liv F"]=("Georgie R","Josie","Grace")
  preferences["Hannah B"]=("Alex H","Josie","Grace")
  preferences["Cole T S"]=("Petra","Joe A","Oli R")
  preferences["Kieran"]=("Alex S","Josh B","Matthew F")
  preferences["Archie C"]=("Liv F","Grace","Reggie")
  preferences["Jonny M"]=("Michael","Archie T","Josh D")
  preferences["Jacob N"]=("Tabby","Gibbo","Guy P")
  preferences["Alex H"]=("Lauren W","Hannah B","Emma G")
  preferences["Josie"]=("Lauren W","Hannah B","Alex H")
  preferences["Veks"]=("India O","Liv C","Matthew F")
  preferences["India O"]=("Veks","Liv C","Amelia O")
  preferences["Liv C"]=("Georgie W","Katie B","Amelia O")
  preferences["Matthew F"]=("Thomas D","Mark","Will H")
  preferences["Amelia O"]=("Emily K","India O"," Katie B")
  preferences["Frank"]=("Frederick E","Frederick B","Jerry")
  preferences["Jerry"]=("Frank","Aydan","Frederick E")
  preferences["Lauren W"]=("Josie","Liv F","Hannah B")
  preferences["Joe A"]=("Melissa S","Leon B","Oli R")
  preferences["Oli R"]=("Joe A","Leon B","Callum P")
  preferences["Leon B"]=("Amelia E","Joe A","Cole T S")
  preferences["Melissa S"]=("Darcy","Joe A","Callum P")
  preferences["Callum P"]=("Darcy","Cole T S","Melissa S")
  preferences["Lewis W"]=("Jacob E","Louis P","Sam S R")
  preferences["Nemph"]=("Evie","Georgie W","India Oli")
  preferences["Evie"]=("Nemph","India O","Chloe")
  preferences["Georgie W"]=("Emily K","Alex S","Katie B")
  preferences["Hamish"]=("Katie B","Rob H","Georgie W")
  preferences["Michael"]=("Josh D","Jonny M","Jacob N")
  preferences["Archie T"]=("Guy P","Gibbo","Ed L")
  preferences["Zara"]=("Gibbo","Tabby","Joe R")
  preferences["Emily K"]=("Georgie W","Amy P","Angus")
  preferences["Ed L"]=("Matthew O","Gibbo","Jacob N")
  preferences["Gibbo"]=("Zara","Ed L","Matthew O")
  preferences["Anton"]=("Frederick B","Frederick E","Karan")
  preferences["Emelia R"]=("Georgie W","Katie B","Rob H")
  preferences["Amy P"]=("Katie B","Emily K","Jasmine R")
  preferences["Thomas D"]=("Evie","Emily K","Matthew F")
  preferences["Alex S"]=("Aydan","Matthew F","Mark")
  preferences["Karan"]=("Anton","Frederick E","Frederick B")
  preferences["Steph S"]=("Abbie S","Chris J","Verity")  ###Vegan
  preferences["Angus"]=("Matthew F","Alex S","Emily K")
  preferences["Georgie R"]=("Liv F","Louis P","Emma G")
  preferences["Jaz"]=("Libby","Zara","Tabby")
  preferences["Calum N"]=("Matthew O","James G","Joe R")
  preferences["Aydan"]=("Alex S","Matthew F","Will H")
  preferences["Carys"]=("Emma G","Lauren W","Alex H")
  preferences["Jonno"]=("Will H","Jasmine R","Jaz")  ###Vegetarian
  preferences["Jacob E"]=("Louis P","Sam S R","")
  preferences["Katie B"]=("Emily K","Georgie W","Rob H")  ###Vegan
  preferences["Chris J"]=("Callum P","Hamish","Cole T S")
  preferences["Andy"]=("","","")
  preferences["Rob H"]=("Hamish","Emelia R","Katie B")
  preferences["Martha"]=("","","")
  preferences["Mark"]=("Wil H","Matthew F","Alex S")
  preferences["George South"]=("","","")
  preferences["Jack J"]=("Finn","George S","Sam S R")
  preferences["Ralph"]=("","","")
  def execute():
    for rows,nEntry in enumerate(nameList):
      if nEntry.get()!="":
        if nEntry.get() not in people:
          people.append(nEntry.get())
        preferences[nEntry.get()]=(str(pref1List[rows].get()),str(pref2List[rows].get()),str(pref3List[rows].get()))
        #Ensuring all guests have 3 preferences as to not skew weightings.
        #if pref1List[rows].get()=="" or pref2List[rows].get()=="" or pref3List[rows].get()=="":
        #  errorText.set("Empty Preference")
        #  errorMessage.update()
        #  raise
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
    #Two groups of size 4 would be returned. This next function would then repeat
    #Splitting into 4 groups of size 2.
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
    timeout=0
    while internalCopy!=[]:
      intermediary=[]
      for singleGroupWithOptions in internalCopy:
        weightedOptions=list(singleGroupWithOptions)
        #Combining the selected group with its most optimal partner and pushing it to a temporary list, internal2
        #We loop this section repeatedly, until no more combinations are available.
        compGroup=weightedOptions.pop(0)
        weightedOptions.sort(key=takeSecond, reverse=True)
        print("\n \n \n")
        print(compGroup)
        print("=============")
        if compGroup in forbidden:
          print("Forbidden")
          continue
        internal2=list(weightedOptions)
        #We need to prevent groups (and their selected option) that have already been sorted, so we add it to forbidden.
        #If the program encounters a group in forbidden at any point, it'll break out of that loop.
        for counter,element in enumerate(weightedOptions):
          print(element)
          if element[1] in forbidden:
            print("^ forbidden")
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
          print(compGroup)
          print("^ finished Group")
        else:
          intermediary.append(compGroup)
      internalCopy=list(combineForSort(intermediary))
      internalCopy.sort(key=worthKey, reverse=True)
    #Generating a box for the output.
    outputString=StringVar()
    outputString.set("No Data Input")
    for end in finished:
      print(end)
      if outputString.get()=="No Data Input":
        outputString.set("Tables:")
      outputString.set(outputString.get()+"\n\n"+str(end))
    output=Message(root,bg="WHITE",width=490,textvariable=outputString,justify="left",relief="sunken")
    output.grid(row=rowCounter+3,column=0,columnspan=4,pady=10,padx=10,sticky=W)
    root.update()
    root.geometry("")
    root.minsize(root.winfo_width(), root.winfo_height())
  #Function to add more rows when the user types into the bottom row.
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
    root.geometry("")
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    canvas.yview_moveto(1)
#    root.maxsize(root.winfo_width(), root.winfo_height()+10)
  #Generating buttons.
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
#  root.maxsize(root.winfo_width()+10, root.winfo_height())
  root.mainloop()
#Function for the restart button
def restart():
  root.destroy()
  start()
start()
