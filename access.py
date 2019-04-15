import cmd, sys
import re


#list of valid commands to use in the test case file
validCommands = ['friendadd', 'viewby', 'logout', 'listadd', 'friendlist', 'postpicture', 'chlst', 'chmod', 'chown', 'readcomments', 'writecomments', 'end']
listOfProfiles = list()
"""
Function: friendadd
Description: Creates an instance of a friend profile, not belonging to any list by default
"""
def friendadd(friendname):
    if friendname in listOfProfiles:
        print("Username " + "\'" +friendname + "\' already exists.")
        #TODO: Report to audit.txt
        return -1
    #instance_friend = Friend(friendname)
    listOfProfiles.append(friendname)
    with open('friends.txt', 'a+') as fObj:
        fObj.write(friendname + '\n')
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
def switch_case(command_string, opt_arg1, opt_arg2):
	switcher = {
		"friendadd": lambda: friendadd(opt_arg1),
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
    #Clear and overwrite files
    with open('friends.txt', 'w+'), open('audit.txt.', 'w+'): pass
    
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
                #if second command is not equal to viewby, repeat until he successfully goes through
                for query in queries: 
                    args = query.split()
                    command_arg = args[0]
                    opt_arg1 = None
                    opt_arg2 = None
                    #TODO: Handle regex for friendname, listname, and picturename args
                    if len(args) == 2:
                        opt_arg1 = args[1]
                    elif len(args) == 3:
                        opt_arg1 = args[1]
                        opt_arg2 = args[2]
                    switch_case(command_arg, opt_arg1, opt_arg2)
                    

            		            
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
class Friend(object):
    name = "admin"
    AccessControlList = None
    def __init__(self, name):
        self.name = name
    @classmethod        
    def from_ACL(cls, AccessControlList):
        cls.AccessControlList = AccessControlList


