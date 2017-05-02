"""
TITANIC TASK
CPSC419; Zacharsky
Evan May
Mary Clark
"""

import codecs
import operator

train = {}
trainf = codecs.open("train.csv", 'r', 'utf8')
test = {}
testf = codecs.open("test.csv", 'r', 'utf8')
k = 5 #k in kNN algorithm

"""
Reading the train.csv file and creating a dictionary of people
"""
people = {} #dictionary of all people
values = [] #the names of the types of values; to be used as dictionary keys

firstLine = True
#load train.csv
for line in trainf:
    if firstLine:
        firstLine = False
        values = line.split(',')
        continue
    else:
        #separate line into fields
        fields = line.split(',')
        #fix name (split due to comma in the name)        
        name = fields[3].strip('"') + ', ' + fields[4].strip('"')
        #make temp dictionary for this person
        temp = {values[1]: fields[1], values[2]: fields[2], values[3]: name,
                values[4]: fields[5], values[5]: fields[6], values[6]: fields[7],
                values[7]: fields[8], values[8]: fields[9], values[9]: fields[10],
                values[10]: fields[11], values[11]: fields[12]}
        #add person with PassengerID to the dictionary of people
        people[fields[0]] = temp

"""
Reading the test.csv file and creating a dictionary of people
"""
peopleTest = {}
valuesTest = []

firstLine = True
#load test.csv
for line in testf:
    if firstLine:
        firstLine = False
        valuesTest = line.split(',')
        continue
    else:
        #separate line into fields
        fields = line.split(',')
        #fix name (split due to comma in the name)        
        name = fields[2].strip('"') + ', ' + fields[3].strip('"')
        #make temp dictionary for this person
        temp = {valuesTest[1]: fields[1], valuesTest[2]: name, valuesTest[3]: fields[4],
                valuesTest[4]: fields[5], valuesTest[5]: fields[6], valuesTest[6]: fields[7],
                valuesTest[7]: fields[8], valuesTest[8]: fields[9], valuesTest[9]: fields[10],
                valuesTest[10]: fields[11]}
        #add person with PassengerID to the dictionary of people
        peopleTest[fields[0]] = temp

"""
Normalize numerical values (height, class) and set strings to integers
"""
minAge = 100;
maxAge = 0;

for person in people:
    age = people[person]["Age"]
    if (age != ""):
        age = float(age)
        if (age < minAge):
            minAge = age;
        if (age > maxAge):
            maxAge = age;
    people[person]["Age"] = age

rangeAge = maxAge - minAge
for person in people:
    age = people[person]["Age"]
    if (age != ""):
        #Normalize age
        people[person]["Age"] = (age - minAge) / rangeAge
        #print (people[person]["Age"])

minAge = 100;
maxAge = 0;

for person in peopleTest:
    age = peopleTest[person]["Age"]
    if (age != ""):
        age = float(age)
        if (age < minAge):
            minAge = age;
        if (age > maxAge):
            maxAge = age;
    peopleTest[person]["Age"] = age

rangeAge = maxAge - minAge
for person in peopleTest:
    age = peopleTest[person]["Age"]
    if (age != ""):
        #Normalize age
        peopleTest[person]["Age"] = (age - minAge) / rangeAge
           
"""
Compute k nearest neighbor for each passenger in test.csv
"""

score = 0
kNNresultsA = []
kNNresultsB = []
kNNresults = []

for person1 in peopleTest:
    pclass1 = peopleTest[person1]["Pclass"]
    sex1 = peopleTest[person1]["Sex"]
    age1 = peopleTest[person1]["Age"]
    results = {} #dictionary of the results
    counter = 0
    
    for person2 in people:
        score = 0
        
        pclass2 = people[person2]["Pclass"]
        sex2 = people[person2]["Sex"]
        age2 = people[person2]["Age"]
        survived = people[person2]["Survived"]

        if (pclass1 == pclass2):
            score = score + 1
        if (sex1 == sex2):
            score = score + 1
        if (age1 != "" and age2 != ""):
            ageScore = abs(float(age1) - float(age2))
            ageScore = 1 - ageScore
            score = score + ageScore

        #print (score)
        resultsTemp = {"ID":person2, "Score":score, "Survived":survived}
        #print (resultsTemp)
        results[counter] = resultsTemp
        #print (results[counter])
        counter += 1

    #Sort the nearest neighbors
    resultsSorted = sorted(results.items(), key=lambda x: x[1]["Score"], reverse=True)

    chance = 0
    for i in range (0,k):
        neighbor = resultsSorted[i]
        survived = neighbor[1]["Survived"]
        if (survived == "1"):
            chance += 1

    if (chance >= k/2):
        survived = "1"

    if len(person1) is 3:
        kNNresultsA.append(person1 + "\t" + survived)
    elif len(person1) is 4:
        kNNresultsB.append(person1 + "\t" + survived)

#print (kNNresults)

kNNresultsA.sort()
kNNresultsB.sort()

kNNresults = kNNresultsA + kNNresultsB

"""
Write results of the kNN to results.txt file
"""

#for loop to go through each person in the kNNresults array
#print out each person to a file named "results.txt"
#B)

resultsfile = open("results.txt", 'w')
for item in kNNresults:
    resultsfile.write(item + "\n")
resultsfile.close()
