import cmd
import sys
import re


# list of valid commands to use in the test case file
validCommands = ['friendadd', 'viewby', 'logout', 'listadd', 'friendlist',
                 'postpicture', 'chlst', 'chmod', 'chown', 'readcomments', 'writecomments', 'end']

# list of all profiles online (in the friends.txt file)
friend_txt_list = list()

# list that keeps track of friend lists
listOfFriendLists = dict()

# dictionary that keeps track of picture associated to the owner and the pictures posted
# {}
picture_tracking = dict()

# list to keep track of current picture objects
picture_objects = list()

# boolean values to keep track if someone is existing
is_viewing = False


# track who is viewing
who_is_viewing = []



class AccessControlList(object):
    pass


class Admin(object):
    name = None
    AccessControlList = None
    online_status = False

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_ACL(cls, AccessControlList):
        cls.AccessControlList = AccessControlList

    @classmethod
    def set_online(cls, online_status):
        cls.online_status = online_status


class Picture(object):
    name = ''
    picture_group = None
    owner = ''
    others = None  # TODO: difference of all friends and pricture_group
    permissions = {owner: 'rw', picture_group: '--', others: '--'}

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


"""
Function: friendadd
Description: Creates an instance of a friend profile, not belonging to any list by default
"""


def friendadd(friendname):
    if friendname in friend_txt_list:
        log_message("ERROR Friendadd failed: Username " + "\'" +
                    friendname + "\' already exists.")
        return
    #instance_friend = Friend(friendname)
    friend_txt_list.append(friendname)
    log_message("Friend " + friendname + " added")
    with open('friends.txt', 'a+') as fObj:
        fObj.write(friendname + '\n')


def viewby(friendname):
    """ 
    TODO: GIVE PERMISSIONS TO THE ADMIN friend[0]
    """
    global is_viewing
    global who_is_viewing

    if friendname not in friend_txt_list:
        log_message("ERROR View failed: Username " + "\'" + friendname +
                    "\' is not in friends.txt file.")
        return
        # sys.exit(1)

    if (is_viewing == True):
        log_message("ERROR View failed: Username " + "\'" + who_is_viewing[0] +
                    "\' is viewing right now. " + "\'" + friendname +
                    "\' will not execute any commands then.")
        return
        # sys.exit(1)

    is_viewing = True
    who_is_viewing.append(friendname)
    if friendname == friend_txt_list[0]:
        log_message("Admin user " + "\'" + friendname +
                    "\' is viewing his/her profile.")
    else:
        log_message("Friend " + "\'" + friendname +
                    "\' is viewing the profile.")


def logout():
    """
    A friend or you no longer views your profile
    """
    global is_viewing
    if is_viewing == False or len(who_is_viewing) == 0:
        pass
    else:
        is_viewing = False
        log_message("Friend " + who_is_viewing[0] + " has logged out.")
        who_is_viewing.pop()


def listadd(listname):
    global who_is_viewing
    if who_is_viewing[0] != friend_txt_list[0]:
        log_message("ERROR Listadd failed: Username " + "\'" + who_is_viewing[0] +
                    "\' can't  execute listadd because he/she is not the admin " + friend_txt_list[0])
        return
    if listname == "None" or listname == "nil" or listname == "null":
        log_message(
            "ERROR Listadd failed: Can't create a list called 'None' equivalent")
        return
    if listname in listOfFriendLists:
        log_message("ERROR Listadd: Can't instantiate a list that already exists")
        return
    listOfFriendLists[listname] = list()
    log_message("List " + listname + " created")
    print(str(listOfFriendLists))
    # 4/16/2019 7PM


def friendlist(friendname, listname):
    global who_is_viewing
    if friendname not in friend_txt_list:
        log_message("ERROR Username " + "\'" +
                    friendname + "\' does not exist")
        return
    if listname not in listOfFriendLists:
        log_message("ERROR Listname " + "\'" + listname + "\' does not exist")
        return
    if who_is_viewing[0] != friend_txt_list[0]:
        log_message("ERROR Username " + "'" +
                    who_is_viewing[0] + "' ain't an admin.")
        return
    temp = listOfFriendLists.get(listname)
    temp.append(friendname)
    log_message("Friend " + friendname + " added to list " + listname)
    print(str(listOfFriendLists))


def postpicture(picturename):
    global is_viewing
    if is_viewing:
        temp = picturename
        if picturename.endswith('.txt'):
            temp = picturename.split('.txt')[0]
        if temp in picture_tracking:
            log_message("ERROR Posting picture failed: " + picturename +
                        " already exists. Must give this picture a different name")
            return
        picture_tracking[temp] = who_is_viewing[0]

        if not picturename.endswith('.txt'):
            picturename = picturename + '.txt'
        with open(picturename, 'w+') as fObj:
            fObj.write(temp + '\n')
        
        picture_obj = Picture(temp, who_is_viewing[0])
        picture_objects.append(picture_obj)
        log_message("Picture " + picturename + " with owner " +
                    picture_tracking[temp] + " and default permissions has been posted")
    else:
        log_message(
                "ERROR Posting picture failed: No one is viewing the profile")
        return

def chlst(picturename, listname):
    if is_viewing == False:
        log_message("ERROR chlst failed: Someone needs to view the profile.")
        return

    # if not picturename.endswith('.txt'):
    #     log_message("chlst failed: picturename must end with a .txt")
    #     return

    if listname not in listOfFriendLists:
        log_message("ERROR chlst failed: " + listname + " is not a list")
        return

    # valid
    nameOfPicture = picturename.split(".")[0]
    pic_reference = None
    for pic in picture_objects:
        if pic.name == nameOfPicture:
            pic_reference = pic
    if pic_reference == None:  # didn't find a pic object
        log_message("ERROR chlst failed: Reference to " +
                    picturename + " does not exist.")

    # at this point, we have found a picture object, compare owners
    if pic_reference.owner == picture_tracking[nameOfPicture] or pic_reference.owner == friend_txt_list[0]:
        if listname == "None" or listname == "nil":
            pic_reference.picture_group = None
            log_message(picturename + " is its own boss")
            return
        if who_is_viewing[0] == friend_txt_list[0]:
            pic_reference.picture_group = listOfFriendLists[listname]
            log_message("List for " + picturename + " set to " +
                        listname + " by admin " + who_is_viewing[0])
            return
        elif pic_reference.owner not in listOfFriendLists[listname]:
            log_message("ERROR chlst failed: Owner " + pic_reference.owner + " of " +
                        pic_reference.name + " is not a member of friendlist " + listname)
            return
        else:
            pic_reference.picture_group = listOfFriendLists[listname]
            log_message("List for " + picturename + " set to " +
                        listname + " by " + pic_reference.owner)

    else:
        log_message("ERROR chlst failed: User " +
                    who_is_viewing[0] + " can't chlst " + picturename)
        return


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
        "viewby": lambda: viewby(opt_arg1),
        "logout": logout,
        "listadd": lambda: listadd(opt_arg1),
        "friendlist": lambda: friendlist(opt_arg1, opt_arg2),
        "postpicture": lambda: postpicture(opt_arg1),
        "chlst": lambda: chlst(opt_arg1, opt_arg2),
        "chmod": chmod,
        "chown": chown,
        "readcomments": readcomments,
        "writecomments": writecomments,
        "end": end
    }
    func = switcher.get(command_string, lambda: "Invalid command")
    func()


def log_message(message):
    print(message)
    with open('audit.txt', 'a') as audit:
        audit.write(message + '\n')


def main():
    # Clear and overwrite files
    with open('friends.txt', 'w+'), open('audit.txt.', 'w+'), open('pictures.txt.', 'w+'), open('lists.txt.', 'w+'):
        pass

    # Error Handling
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
                    # this is a valid command!
                    queries.append(line.strip())
                    commands.append(command)
            fObj.close()

            if (len(badCommands) > 0):
                print("You queried some invalid commands!")
                print("List of invalid commands: " + str(badCommands))
                return -1

            # if file is valid, continue checking
            if commands[0] != "friendadd":
                print("First command must be \"friendadd\".")
                # TODO: report error to audit log file
                return -1
            else:  # parse the commands
                # if second command is not equal to viewby, repeat until he successfully goes through
                #admin = Admin(queries[0].split()[1])
                # print(admin.name)

                for query in queries:
                    args = query.split()
                    command_arg = args[0]
                    opt_arg1 = None
                    opt_arg2 = None
                    # TODO: Handle regex for friendname, listname, and picturename args
                    if len(args) == 2:
                        parse = args[1]
                        parse = re.split('[\\s:/]', parse)
                        opt_arg1 = ''.join(parse)
                        # if "viewby" == command_arg and opt_arg1 == friend_txt_list[0]:
                        #     print(opt_arg1 + " now has administrator access!")

                    elif len(args) == 3:
                        parse = re.split('[\\s:/]', args[1])
                        parse2 = re.split('[\\s:/]', args[2])
                        opt_arg1 = ''.join(parse)
                        opt_arg2 = ''.join(parse2)

                    switch_case(command_arg, opt_arg1, opt_arg2)

        except IOError:
            print("File not found.")
            # TODO: report file error to audit log file

    else:
        print("Error: Need to have a test case file as an argument, where file is the one argument.")
        print("Format should be: python access.py [filename]")


if __name__ == "__main__":
    main()
