import datetime

mlist = sorted(['20:26','15:26'])
print(mlist)
li = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
events = [
    {
        'todo' : 'task',
        'date' : '2022-05-17',
        'time' : '20:26'
    }
]
for i in li:
    new_event = {
        'todo' : i,
        'date' : i,
        'time' : i    
    }
    events.append(new_event)
print(events)

#OUTPUT - [{'todo': 'task', 'date': '2022-05-17', 'time': '20:26'}, {'todo': 0, 'date': 0, 'time': 0}, {'todo': 1, 'date': 1, 'time': 1}, {'todo': 2, 'date': 2, 'time': 2}, {'todo': 3, 'date': 3, 'time': 3}]
# FORMAT - 2022-05-16T20:26