import random

def whatToLearn(where,use,learn):
    num1 = random.randint(0,len(where) - 1)
    num2 = random.randint(0,len(use) - 1)
    num3 = random.randint(0,len(learn) - 1)
    return  'Learn ' + learn[num3] + ' with ' +  use[num2] + ' on the ' + where[num1] +' floor of the library.'

def whatToDo(toDoList):
    return toDoList[random.randint(0,len(toDoList) - 1)]
    
where = ['first','second','third','fourth','fifth']
use = ['Text books','Borrowed Books','Surface']
learn = ['JAVA', 'Data Structure', 'Digital Circuit', 'Linear Algebra', 'English']
toDo = ['Wash clothes', 'Take a shower', 'Meditate' , 'Draw pictures' ,'Clean your room', 'Read books']

print(whatToLearn(where,use,learn))
print(whatToDo(toDo))

