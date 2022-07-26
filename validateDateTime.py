#Importing basic modules
from datetime import datetime, timedelta

#Assumption: input file is .txt format
#Importing txt file from user's input
testData = open(input('Please enter name of file with date/time values to test: '), 'r')

#Set to store all date/time formatted incorrectly 
formatError = set()

#Set to store all unique date/time
uniques = set()

#Set to store all duplicates found
duplicates = set()

#Assumption: Date/time is stored in row by row format
#Reading each line of date time 
dateTimes = testData.readlines()

#Itterating through all datetimes in input file
for currentDateTime in dateTimes:
    #Edge Case: string does not contain 'T'(formatted incorrectly)
    if 'T' not in currentDateTime:
        formatError.add(currentDateTime)
        continue

    #Split date time to date
    currentDate, currentTime = currentDateTime.split('T')

    #Convert current date into datetype type
    currentDate = datetime.strptime(currentDate, '%Y-%m-%d')

    #Creating base time to add time to; base time is 00:00:00
    utcTime = timedelta()

    #Case 1: currentTime has 'Z'; already in UTC
    if 'Z' in currentTime:
        #Dropping 'Z' from time string
        modifedCurrentTime = currentTime.replace('Z', '') 
        #Splitting modified current time into hour, minute and second
        hour, minute, second = modifedCurrentTime.split(':')
        #Adding curernt time to base time
        utcTime += timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
    else: #NOTE: REPETITION IN THIS ELSE STATEMENT; CAN REDUCE BY USING HELPER FUNCTION
        if '+' in currentTime: #Noting that the offset is positive
            #Splitting current time in time and offset
            time, offset = currentTime.split('+') 
            #Splitting time into hours, minutes, seconds
            timeHour, timeMinute, timeSecond = time.split(':')
            #Splitting offset into hours, minutes, seconds
            offsetHour, offSetMinute = offset.split(':')
            #Adding time and offset hours, minutes, seconds and adding to base time
            utcTime += timedelta(hours=int(timeHour) + int(offsetHour), minutes=int(timeMinute) + int(offSetMinute), seconds=int(timeSecond))
        elif '-' in currentTime: #Noting that the offset is positive
            #Splitting current time in time and offset
            time, offset = currentTime.split('-')
            #Splitting time into hours, minutes, seconds
            timeHour, timeMinute, timeSecond = time.split(':')
            #Splitting offset into hours, minutes, seconds
            offsetHour, offSetMinute = offset.split(':')
            #Adding time and offset hours, minutes, seconds and adding to base time
            utcTime += timedelta(hours=int(timeHour) - int(offsetHour), minutes=int(timeMinute) - int(offSetMinute), seconds=int(timeSecond))
        else: #Error with time format; add to error set and go to next itteration
            formatError.add(currentTime)
            continue
    #Add current date with the converted/formatted time 
    dateTimeConverted = currentDate + utcTime

    #If converted/formatted datetime not in uniques; add to uniques
    if dateTimeConverted not in uniques:
        uniques.add(dateTimeConverted)
    #Else add orignal datetime to duplicates to keep track
    else:
        duplicates.add(currentDateTime)

#Providing results
print('There are ' + str(len(duplicates)) + ' duplicate values')
print('There are ' + str(len(uniques) - len(duplicates)) + ' unique values')
print('There are ' + str(len(formatError)) + ' date/time values with incorrect format')

#Exporting the duplicates set for developer to reference 
with open('Duplicates Found.txt', 'w') as f:
    for dups in duplicates:
        f.write('%s\n' % dups)
   