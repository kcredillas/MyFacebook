import cmd, sys
import re


#list of valid commands to use in the test case file
validCommands = ['friendadd', 'viewby', 'logout', 'listadd', 'friendlist', 'postpicture', 'chlst', 'chmod', 'chown', 'readcomments', 'writecomments', 'end']
"""
Function: friendadd
Description: Creates an instance of a friend profile, not belonging to any list by default
"""
def friendadd():
    pass
def viewby():
    pass
def logout():
    pass
def listadd():
    pass
def friendlist():
    pass
def postpicture():
    pass
def chlst():
    pass
def chmod():
    pass
def chown():
    pass
def readcomments():
    pass
def writecomments():
    pass
def end():
    pass
def switch_case(command_string):
	switcher = {
		"friendadd": friendadd,
		"viewby": viewby,
		"logout": logout,
		"listadd": listadd,
		"friendlist": friendlist,
		"postpicture": postpicture,
		"chlst": chlst,
		"chmod": chmod,
		"chown": chown,
		"readcomments": readcomments,
		"writecomments": writecomments,
		"end": end
		}
	func = switcher.get(command_string, lambda: "Invalid command")
	func() 

def main():
    #print ('Argument List:', str(sys.argv))

    #Error Handling
    if (len(sys.argv) == 2):
        fileName = sys.argv[1]
        if not(fileName.endswith('.txt')):
            print("Your file should be in .txt format only!!!")
            return -1
        try:
            fObj = open(fileName, 'r')
            badCommands = list()
            queries = list()
            commands = list()
            for line in fObj:
                command = line.split(' ')[0]
                if command.strip() not in validCommands:
                    badCommands.append(command)
                else:
                    #this is a valid command!
                    queries.append(line.strip())
                    commands.append(command)
            fObj.close()

            if (len(badCommands) > 0):
                print("You queried some invalid commands!")
                print("List of invalid commands: " + badCommands)
                return -1
            
            #if file is valid, continue checking
            if commands[0] != "friendadd":
                print("First command must be \"friendadd\".")
                #TODO: report error to audit log file
                return -1
            else: #parse the commands
                for arg in commands: 
                    switch_case(arg)

            		            
        except IOError:
            print("File not found.")
            #TODO: report file error to audit log file
        
        
    else:
        print("Error: Need to have a test case file as an argument, where file is the one argument.")
        print("Format should be: python access.py [filename]")

if __name__ == "__main__":
    main()
class AccessControlList(object):
    pass

class Person(object):
    pass
    """
    isFriend = False #default value of a friend
    def __init__(self, name, AccessControlList):
        self.name = name
        self.AccessControlList = AccessControlList

    def is_Friend(self):
        return self.isFriend
    """
    


