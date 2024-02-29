import csv
from datetime import datetime

list = [] #All of the data from the csv files
days = [] #All of Days worked IN OFFICE

year = input('Enter the year: ') #Year of the data

def readIn(csv_file):
    with open(csv_file, 'r') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            list.append(row[0].split(','))
            
while True:
    file_name = input('Enter the name of the file (or type x to exit loop): ')
    if file_name == 'x':
        print("Loop exited")
        break
    readIn(file_name)
        
for i in list:
    days.append(i[1].split())

final_days = [] #Final list of days worked in office (Formatted days < 10 with a 0 in front)
    
for i in days:
    if int(i[1]) < 10:
        i[1] = '0' + i[1]
    final_days.append(i)

all_days = [] #All of the days in the year minus weekends

# Take all of the days in the year and remove the days worked in office

file_name = input('Enter the name of the file with all of the days in the year (or press x): ')
if file_name == 'x':
    print('Using defailt file: Days of the Year.csv')
    file_name = 'Days of the Year.csv'
    
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        temp = (row[0] + ' ' + year) #Formatting the date to be able to use datetime
        date = datetime.strptime(temp, '%B %d %Y') #Converting the date to a datetime object
        if date.weekday() < 5:  #Checking if the date is a weekday
            all_days.append(row[0].split())

for i in range(len(all_days)):
    all_days[i].append('None')

file_name = input('Enter the name of the file with all of the Holidays and Vacation (or press x): ')
if file_name == 'x':
    print('Using defailt file: Holidays and Vacation.csv')
    file_name = 'Holidays and Vacation.csv'


holidays = [] #All of the holidays and vacation days
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        holidays.append(row)
        
holidays1 = [] #List of all the holidays and vacation days (Formatted days < 10 with a 0 in front)
holidays2 = [] #List of all the holidays and vacation day reasons
holidays_temp = []
holidays_final = []

for i in holidays:
    holidays1.append(i[0].split())
for i in holidays:
    holidays2.append(i[1])
for i in range(len(holidays)):
    holidays_temp.append(holidays1[i][0] + ',' + holidays1[i][1] + ',' + holidays2[i])
for i in holidays_temp:
    holidays_final.append(i.split(','))


# Remove days worked in office from list of all days in the year (Change reason for Out of Office to Work From Office)
for i in range(len(all_days)):
    for j in range(len(final_days)):
        if final_days[j][0] == all_days[i][0] and final_days[j][1] == all_days[i][1]: 
            all_days[i][2] = ('Work From Office')
            


# Remove Holidays from list of days worked in office (Change reason for Out of Office to Holiday)
for i in range(len(all_days)):
    for j in range(len(holidays_final)):
        if holidays_final[j][0] == all_days[i][0] and holidays_final[j][1] == all_days[i][1]: 
            all_days[i][2]=(holidays_final[j][2])


# Change reason of all remaining days to Work From Home
for i in all_days:
    if i[2] == 'None':
        i[2] = ('Work From Home')

# Count the number of days worked from home
WFH_count = 0
for i in all_days:
    if i[2] == 'Work From Home':
        WFH_count += 1

# Count the number of days worked from office
WFO_count = 0
for i in all_days:
    if i[2] == 'Work From Office':
        WFO_count += 1
        
# Count the number of bereavement days
bereavement_count = 0
for i in all_days:
    if i[2] == 'Bereavement':
        bereavement_count += 1

# Count the number of holidays
holiday_count = 0
for i in all_days:
    if i[2] != 'Bereavement' and i[2] != 'Work From Home' and i[2] != 'Work From Office' and i[2] != 'None':
        holiday_count += 1


# Removed all values in list with "Worked from Office" as the reason
all_days = [i for i in all_days if i[2] != 'Work From Office']

all_days.append(['Total Work From Home Days:', WFH_count])
all_days.append(['Total Work From Office Days:', WFO_count])
all_days.append(['Total Bereavement Days:', bereavement_count])
all_days.append(['Total Holidays:', holiday_count])

with open('All WFH Days.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Month', 'Day', 'Reason'])
    for i in all_days:
            writer.writerow(i)
            
print('All WFH Days.csv has been created')
