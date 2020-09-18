from canvasapi import Canvas
from datetime import datetime
from subprocess import Popen, PIPE
import os
import pathlib


def collect_todo_list(canvas):
    todo_items = canvas.get_todo_items()
    return todo_items

def reminders_list():
    script = f'''
            tell application "Reminders"
                set listNames to {{}}
                set listName to "Homework"
        
                set hwTasks to ""
                repeat with aList in lists
                    if name of aList as string is equal to listName as string then
                        set listToPrint to aList
                        exit repeat
                    end if
                end repeat
                
                set listItems to reminders of listToPrint
                set reminderStrings to {{}}
                repeat with aReminder in listItems
                    if aReminder is not completed then
                        set reminderText to name of aReminder as string
                        copy reminderText to end of reminderStrings
                    end if
                end repeat
                
                set TID to AppleScript's text item delimiters
                set AppleScript's text item delimiters to ","
                set listText to reminderStrings as text
                set AppleScript's text item delimiters to TID
                set listText to (listText)
                
                return listText as string
            end tell'''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)
    p.wait()
    noNewLine = stdout.rstrip()
    delimitedList = noNewLine.split(',')
    return delimitedList

def reminder_creation(name, due_date, listName):
    script = f'''
            tell application "Reminders"
                set myList to list "{listName}"
                tell myList
                    make new reminder at end with properties {{name: "{name}", due date:date "{due_date}"}}
                end tell
            end tell'''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(script)

def time_cleanup(dueTime):
    hours, minutes, seconds = dueTime.split(":")
    hours, minutes = int(hours), int(minutes)
    setting = "AM"
    if minutes == 59 or hours == 5:
        hours = 11
        setting = "PM"
        return (("%02d:%02d" + " " + setting) % (hours, minutes))
    if hours > 12:
        hours -= 6
        if hours > 12:
            setting = "PM"
            hours -= 12
    return(("%02d:%02d" + " " + setting) % (hours, minutes))

def reminder_exists(cReminders, nReminder):
    if nReminder in cReminders:
        return True
    else:
        return False
    

def reminder_logic():
    currentDir = pathlib.Path(__file__).parent.absolute()
    filePath = currentDir/"api_keys.txt"
    keyFile = open(filePath)
    tagU, url = keyFile.readline().split('=')
    tagK, key = keyFile.readline().split('=')
    tagL, nameL = keyFile.readline().split('=')
    API_URL = url
    API_KEY = key
    LIST_NAME = nameL

    keyFile.close()

    canvas = Canvas(API_URL, API_KEY)
    todo_list = collect_todo_list(canvas)
    currentReminders = reminders_list()

    for item in todo_list:
        assignment = item['assignment']
        name = assignment['name']
        if reminder_exists(currentReminders, name) == False:
            due_date = assignment['due_at']
            date, time = due_date.split('T')
            time = time_cleanup(time)
            year, month, day = date.split('-')
            newDate = month+"/"+day+"/"+year
            dueTimeDate = newDate + " " + time
            reminder_creation(name, dueTimeDate, LIST_NAME)
        else:
            continue
    

def main():
    reminder_logic()
        

if __name__ == "__main__":
    main()