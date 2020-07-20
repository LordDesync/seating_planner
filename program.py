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
preferences["Ben S"]=("George A","Archie P","[Bagi]")
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
preferences["Josh D"]=("Joe R","James G","Matthew O")  ##BLANK
preferences["George Sand"]=("Joe R","Matthew O","James G")
preferences["Owen G"]=("Ed R","Reggie","Harry J")
preferences["Ed R"]=("Reggie","George A","Archie P")
preferences["Alex D"]=("Harrison J","Tom S","Teddy")
preferences["Liv F"]=("Georgie R","Josie","Grace")
preferences["Hannah B"]=("Alex H","Josie","Grace")
preferences["Cole T S"]=("Petra","Joe A","Oli R")
preferences["Kieran"]=("Alex S","Josh B","Matthew O")
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
preferences["Chris J"]=("","","")
preferences["Andy"]=("","","")
preferences["Rob H"]=("Hamish","Emelia R","Katie B")
preferences["Martha"]=("","","")
preferences["Mark"]=("Wil H","Matthew F","Alex S")
preferences["George South"]=("","","")
preferences["Jack J"]=("Finn","George S","Sam S R")
preferences["Ralph"]=("","","")

mutPair=[]
mutEight=[]

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

#Popping elements from list of a given size for later use in bin packing
def bysize(words, size):
    return [word for word in words if len(word) == size]



#Bin packing by inspection;

#Listing possible other group placements for every group in mutual
fitOptions=[]
for x in mutPref:
  c=0
#  print("Group "+str(x))
  fit=[]
  while c<(seatingMax-len(x)):
    fit.extend(bysize(mutPref,seatingMax-(len(x)+c)))
    c=c+1
  if x in fit:
    fit.remove(x)
  fitNoNull=[n for n in fit if n]
  fitOptions.append(fitNoNull)
#  print(str(fitNoNull)+"\n \n \n \n \n")
for i,x in enumerate(mutPref,0):
  print("Group "+str(x))
  print(str(fitOptions[i]))

#Testing compatibility between group options
#Determining how happy people are with their table, with preferences as metric
def tableWorth (friends, table):
  worth=0
  for person in table:
    if preferences[person] in table:
      worth = worth + 1
  return worth
