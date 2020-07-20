import random;
import itertools;
from collections import defaultdict

#Enter number of tables here:
tableNum=15
#Number of seats maximum at each table:
seatingMax=10
tables=[]
k=0
while k<tableNum:
  tables.append([])
  k=k+1

class Person:
  def __init__(self, pref1, pref2, pref3):
    self.pref1=pref1
    self.pref3=pref2
    self.pref3=pref3

#Format: People=("Name 1", "Name 2","Name 3", ...)
#N.B. Names must be exactly the same as the preferences below (case sensitive, spacing, etc.)
people=("Venetia","Jasmine R","Will H","Jonno","Benji","Phil","Frederick B","Frederick E","Teddy","Joe D","Tom S","Mackenzie","Sam S R","Louis P","Jacob E","Ben S","George A","Archie P","Connie","Maisie","Tabby","Libby","Liliane","Katie B","Ann K T","Petra","Esia","Grace","Anna W","Emma G","Guy P","Jack I","Harry J","Reggie","Maya T","Rachel B","Amelia E","Harrison J","Joe R","James G","Matthew O","Josh D","George Sand","Owen G","Ed R","George South","Alex D","Liv F","Hannah B","Cole T S","Kieran","Archie C","Jonny M","Jacob N","Alex H","Josie","Veks","India O","Liv C","Matthew F","Amelia O","Frank","Jerry","Lauren W","Joe A","Oli R","Leon B","Melissa S","Callum P","Lewis W","Nemph","Evie","Georgie W","Hamish","Rob H","Michael","Archie T","Zara","Emily K","Ed L","Gibbo","Anton","Emelia R","Amy P","Thomas D","Alex S","Karan","Steph S","Andy","Angus","Georgie R","Chris J","Jaz","Calum N","Aydan","Martha","Mark","Carys","Jack J")

#Format: preferences["Name"]=("Pref 1","Pref 2","Pref 3")
preferences={}
preferences["Venetia"]=("Jasmine R","Jonno","Will H")
preferences["Jasmine R"]=("Amy P","Jonno","Katie B")
preferences["Will H"]=("Jonno","Esia","Grace")
preferences["Benji"]=("Phil","George A","Josie")
preferences["Phil"]=("Benji","Archie P","Ben S")
preferences["Frederick B"]=("Will M","Frederick B","Archie H")
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
preferences["Liliane"]=("Katie B","Ann K T","BLANK")
preferences["Ann K T"]=("Liliane","Katie B","Petra")
preferences["Petra"]=("Cole T S","Darcy","Martha###")
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
preferences["Josh D"]=("Joe R","James G","Matthew O")
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
preferences["Steph S"]=("Abbie S","Chris J","Verity")
preferences["Angus"]=("Matthew F","Alex S","Emily K")
preferences["Georgie R"]=("Liv F","Louis P","Emma G")
preferences["Jaz"]=("Libby","Zara","Tabby")
preferences["Calum N"]=("Matthew O","James G","Joe R")
preferences["Aydan"]=("Alex S","Matthew F","Will H")
preferences["Carys"]=("Emma G","Lauren W","Alex H")
preferences["Jonno"]=("Will H","Jasmine R","Jaz")
preferences["Jacob E"]=("Louis P","Sam S R","")
preferences["Katie B"]=("Emily K","Georgie W","Rob H")
preferences["Chris J"]=("Callum P","Hamish","Cole T S")
preferences["Andy"]=("","","")
preferences["Rob H"]=("Hamish","Emelia R","Katie B")
preferences["Martha"]=("","","")
preferences["Mark"]=("Wil H","Matthew F","Alex S")
preferences["George South"]=("","","")
preferences["Jack J"]=("Finn","George S","Sam S R")
preferences["Ralph"]=("","","")

mutPair=[]

#Adding people who prefer each other as tuples into a list, mutPair
for pair in itertools.combinations(people,2):
  if pair[0] in preferences[pair[1]] and pair[1] in preferences[pair[0]]:
    mutPair.append(pair)

#Combining tuples which share a common element in to list mutPair
#Combining tuples sharing elements is equivalent to finding connected trees in a graph
def dfs(adj_list, visited, vertex, result, key):
    visited.add(vertex)
    result[key].append(vertex)
    for neighbor in adj_list[vertex]:
        if neighbor not in visited:
            dfs(adj_list, visited, neighbor, result, key)
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

#Splitting tables that are too large
#Function has to be in 2 pieces, or the returned value is a tuple (causes issues with bin packing later)
def splitHalf1(listIn):
    half = len(listIn)//2
    return listIn[:half]
def splitHalf2(listIn):
    half = len(listIn)//2
    return listIn[half:]
for x in mutPref:
  if len(x)>10:
    mutPref.remove(x)
    mutPref.append(splitHalf1(x))
    mutPref.append(splitHalf2(x))

#Bin packing by inspection;
#=========================

#Popping elements from list of a given size for later use in bin packing
def bysize(words, size):
    return [word for word in words if len(word) == size]

#Listing all possible other group placements for each group in mutPref
fitOptions=[]
for aGroup in mutPref:
  c=0
  fit=[]
  while c<(seatingMax-len(aGroup)):
    fit.extend(bysize(mutPref,seatingMax-(len(aGroup)+c)))
    c=c+1
  if aGroup in fit:
    fit.remove(aGroup)
    #Stops group from being matched with itself
  fitNoNull=[n for n in fit if n]
  fitOptions.append(fitNoNull)

#Function to determine compatibility between possible group pairings
#Returned value, worthGroup, is a list containing lists of tuples of possible matches per table with element index 0 (of each tuple) being their relative compatibility. Groups with compatibility 0 are pruned. If a fixedGroup has no matching groups, an empty list is returned at its index.
def detFit (setGroups, testGroups):
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
#print(detFit(mutPref, fitOptions))


#Have to combine the two lists together before sorting, then separate them again to keep the matching groups together during the sort.
combinedMutualAndOptions=[]
for counter,groupOptions in enumerate(detFit(mutPref, fitOptions)):
  skippedVal=list(groupOptions)
  skippedVal.insert(0,mutPref[counter])
  combinedMutualAndOptions.append(skippedVal)
#Outputs maximum worth value
def worthKey(inputlist):
  maximum=0
  for counter,sublist in enumerate(inputlist):
    if counter==0:
      continue
    if sublist[0]>maximum:
      maximum=sublist[0]
  return maximum

combinedMutualAndOptions.sort(key=worthKey, reverse=True)
for counter,singleMutualWithOptions in enumerate(combinedMutualAndOptions):
  group1=singleMutualWithOptions[0]
#  print(singleMutualWithOptions)
#  print("\n")



'''
#Extracting the worth values to group
for index, setgroups in enumerate(mutPref):
#  for pop,possiblePair in enumerate(detFit(mutPref, fitOptions)[index]):
  happiness=detFit(mutPref, fitOptions)[index]
  print(happiness)
#  print("\n")

'''




'''

#All the sad lonely people who didn't get paired up at the beginning
#pepehands
#https://xkcd.com/314/
ungroupedPeople=list(people)
for singledPerson in people:
  if any(singledPerson in p for p in mutPref):
    ungroupedPeople.remove(singledPerson)
print(ungroupedPeople)





worthTable=copy.deepcopy(fitOptions)
for i,grouped in enumerate(mutPref):
  #grouped = one mutual-friend-group
  worth=0
  for person in grouped:
    #person = someone in a mutual-friend-group
      #fitOptions[i] returns a list of groups that can possibly be sat with the list "grouped"
    for c,singleGroup in enumerate(fitOptions[i]):
      #singleGroup is one group that can be sat with "grouped"
      for optPerson in singleGroup:
        if preferences[person] in singleGroup:
          worth=worth+1
        #optPerson is one person from singleGroup
  for matchingGroup in worthTable[i]:
    matchingGroup.insert(0,worth)
#    if element in (item for sublist in fitOptions for item in sublist)
  print("Group "+str(grouped))
  print(str(worthTable[i])+"\n \n \n")

'''
