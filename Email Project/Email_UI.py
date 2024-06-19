import datetime

####### FUNCTION DEFS ###########

#Username validity function
def valid_username(x):
    
    # must be 5 characters
    if len(x) < 5:
        return False

    # must be alnum
    if x.isalnum() == False:
        return False

    # check first character
    if x[0].isdigit() == True:
        return False

    return True

#Password validity function
def valid_password(x):

    # must be 5 characters
    if len(x) < 5:
        return False

    # must be alnum
    if x.isalnum() == False:
        return False

    # must contain one lowercase
    lower = False
    
    for index in x:
        if index.islower() == True:
            lower = True
    if lower == False:
        return False

    # must contain one uppercase
    upper = False
    
    for index in x:
        if index.isupper() == True:
            upper = True
    if upper == False:
        return False

    #must contain one number
    num = False

    for index in x:
        if index.isdigit() == True:
            num = True
    if num == False:
        return False

    return True
    
#username exist function
def username_exists(x):

    #extract file data
    file = open("user_info.txt", 'r')
    filedata = file.read()
    file.close()

    #create combo list
    combolist = filedata.split('\n')
    userpasslist = []

    #seperate password and user
    for data in combolist:
        data = data.split(',')
        userpasslist += data

    #create username list
    userlist = []
    for index in range(len(userpasslist)):
        if index % 2 == 0:
            userlist.append(userpasslist[index])

    #check if username exists
    if x in userlist:
        return True
    else:
        return False

#password check function
def check_password(x,y):

     #extract file data
    file = open("user_info.txt", 'r')
    filedata = file.read()
    file.close()

    #create combo list
    combolist = filedata.split('\n')
    userpasslist = []

    #combine user and pass to check
    combocheck = x + ',' + y

    #check if userpass combo exists
    if combocheck in combolist:
        return True
    else:
        return False

# Add user function
def add_user(x,y):

    #check if user exists
    if username_exists(x) == True:
        return False

    #add to file
    newcombo = x + ',' + y + '\n'

    file = open("user_info.txt", 'a')
    file.write(newcombo)
    file.close()
    return True
        
#send message function
def send_message(sender, receiver, text):

    #time data
    d = datetime.datetime.now()
    month = str(d.month)
    day = str(d.day)
    year = str(d.year)
    hour = d.hour
    minute = d.minute
    second = d.second

    if second < 10:
        second = '0' + str(second)
    else:
        second = str(second)

    if minute < 10:
        minute = '0' + str(minute)
    else:
        minute = str(minute)

    if hour < 10:
        hour = '0' + str(hour)
    else:
        hour = str(hour)
    
    time = month + '/' + day + '/' + year + ' ' + hour + ':' + minute + ':' + second

    #create message
    message = sender + '|' + time + '|' + text + '\n' 

    #open / create file and send message
    try:
        file = open('messages/' + receiver + '.txt', 'a')

    except:
        file = open('messages/' + receiver + '.txt', 'w')

    file.write(message)
    file.close()


#print messages function
def print_messages(username):

    #open users messages and store in list
    file = open('messages/' + username + '.txt', 'r')
    messagedata = file.read()
    file.close()

    #if inbox is empty
    if messagedata == '':
        print('No messages in your inbox')
        print()

    else:
        messagelist = messagedata.split('\n')
        del messagelist[-1]

        #break down sender, time, and text into separate info
        messagenum = 0

        for index in messagelist:
            sttlist = index.split('|')

            #display message
            messagenum += 1
            print('Message #' + str(messagenum) + ' received from ' + sttlist[0])
            print('Time: ' + sttlist[1])
            print(sttlist[2])
            print()

#delete message function
def delete_messages(username):
    file = open('messages/' + username + '.txt', 'w')
    file.close()



########### Code ############





#loop to login, regis, or quit

while True:

    menu = input("(l)ogin, (r)egister or (q)uit: ")
    print()

    #to register
    if menu == 'r':
        print("Register for an account")
        print()
        #ask for user and pass and validate
        print("Create a username")
        print("Username must be:")
        print("* 5 characters or longer")
        print("* alphanumeric (only letters or numbers)")
        print("* the first character cannot be a number")
        user = input("Username (case sensitive): ")
        print()

        print("Create a password")
        print("Password must be:")
        print("* 5 characters or longer")
        print("* alphanumeric (only letters or numbers)")
        print("* contain at least one lowercase letter")
        print("* contain at least one uppercase letter")
        print("* contain at least one number")
        password = input("Password (case sensitive): ")
        print()
        
        if valid_username(user) == False:
            print("Username is invalid, registration cancelled")
            print()

        elif username_exists(user) == True:
            print("Duplicate username, registration cancelled")
            print()

        elif valid_password(password) == False:
            print("Password is invalid, registration cancelled")
            print()

        else:
            add_user(user,password)
            print("Registration successful!")
            send_message('admin', user, "Welcome to your account!")
            print()

    #to login
    elif menu == 'l':
        print("Log In")

        #prompt to input user and pass and check for combo
        user = input("Username (case sensitive): ")
        password = input("Password (case sensitive): ")

        if check_password(user, password) == True:

            print("You have been logged in successfully as", user)
            
            #loop for login menu
            while True:

                #prompt user to read, send, delete, logout
                logmenu = input("(r)ead messages, (s)end a message, (d)elete messages or (l)ogout: ")

                #to read messages
                if logmenu == 'r':
                    print()
                    print_messages(user)

                #to send a message
                elif logmenu == 's':
                    sendto = input("Username of recipient: ")

                    if username_exists(sendto) == True:
                        message = input("Type your message: ")
                        send_message(user, sendto, message)
                        print("Message sent!")
                        print()

                    else:
                        print("Unknown recipient")
                        print()

                #to delete messages
                elif logmenu == 'd':
                    delete_messages(user)
                    print("Your messages have been deleted")
                    print()

                #to logout
                elif logmenu == 'l':
                    print("Logging out as username", user)
                    print()
                    break

        #if combo doesn't exist                       
        else:
            print("Invalid username password combination")
            print()

    #to quit
    elif menu == 'q':
        print('Goodbye!')
        break

    #invalid input
    else:
        print("Invalid input")
        print()
        
            
        
            

        












