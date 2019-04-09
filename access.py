import cmd, sys

#list of valid commands to use in the test case file
validCommands = ['friendadd', 'viewby', 'logout', 'listadd', 'friendlist', 'postpicture', 'chlst', 'chmod', 'chown', 'readcomments', 'writecomments', 'end']

def main():
    print ('Argument List:', str(sys.argv))

    #Error Handling
    if (len(sys.argv) == 2):
        fileName = sys.argv[1]
        if not(fileName.endswith('.txt')):
            print("Your file should be in .txt format only!!!")
            return -1
        try:
            fObj = open(fileName, 'r')
            badCommands = list()
            for line in fObj:
                command = line.split(' ')[0]
                if command.strip() not in validCommands:
                    badCommands.append(command)
                    
                
        except IOError:
            print("File not found.")
        
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
    


