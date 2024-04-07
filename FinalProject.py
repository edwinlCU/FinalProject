import psycopg

globalEmail = ""

# initialize cursor and conn as global variables
try:
    conn = psycopg.connect("dbname='FitnessClub' user='postgres' password='sdesde' host='localhost' port='5432'")
    conn.adapters.register_loader("numeric", psycopg.types.numeric.IntLoader)
    conn.autocommit = True
    cursor = conn.cursor()
except psycopg.OperationalError as e:
    print(f"Error: {e}")

def main():
    
    # the while loop where the program happens
    keepGoing1 = True
    while keepGoing1:
    
        # get the member, trainer, and admin emails to verify user 
        cursor.execute("SELECT memberemail FROM clubmember")
        memberEmails = []
        memberRows = cursor.fetchall()
        for row in memberRows:
            memberEmails.append(row[0])
        
        cursor.execute("SELECT traineremail FROM trainer")
        trainerEmails = []
        trainerRows = cursor.fetchall()
        for row in trainerRows:
            trainerEmails.append(row[0])
            
        cursor.execute("SELECT adminemail FROM adminstaff")
        adminEmails = []
        adminRows = cursor.fetchall()
        for row in adminRows:
            adminEmails.append(row[0])
        
        rank = "none"
        userFirstname = "none"
        userLastname = "none"
        
        while rank == "none":
            global globalEmail
            globalEmail = input("Please login with your existing email, or enter a new email to begin member registration: ")
            
            # verify the user depending on what email they provided
            if (globalEmail in memberEmails):
                rank = "member"
                cursor.execute("SELECT firstname, lastname FROM clubmember WHERE memberemail = %s;", [globalEmail])
                names = cursor.fetchall()
                userFirstname = names[0][0]
                userLastname = names[0][1]
                print("\nWelcome, Member " + userFirstname + " " + userLastname + "!")
            elif (globalEmail in trainerEmails):
                rank = "trainer"
                cursor.execute("SELECT firstname, lastname FROM trainer WHERE traineremail = %s;", [globalEmail])
                names = cursor.fetchall()
                userFirstname = names[0][0]
                userLastname = names[0][1]
                print("\nWelcome, Trainer " + userFirstname + " " + userLastname + "!")
            elif (globalEmail in adminEmails):
                rank = "admin"
                cursor.execute("SELECT firstname, lastname FROM adminstaff WHERE adminemail = %s;", [globalEmail])
                names = cursor.fetchall()
                userFirstname = names[0][0]
                userLastname = names[0][1]
                print("\nWelcome, Admin " + userFirstname + " " + userLastname + "!")
            # user's email did not match any of the existing emails, so register them as a new member 
            else:
                rank = "member"
                userRegistration()
        
        # a while loop where a user can execute functions related to their rank. Exiting this loop allows them to login with a different email
        keepGoing2 = True
        while keepGoing2:
            print("\nEnter an integer representing what you would like to do: ")
            userChoice = -1
            
            match rank:
                case "member":
                    print("\t1: Profile Management (Update personal information, fitness goals, or health metrics)")
                    print("\t2: Dashboard Display (Display exercise routines, fitness achievements, and health statistics)")
                    print("\t3: Schedule Management (Schedule personal training sessions or group fitness classes)")
                    print("\t4: Logout and switch users")
                    print("\t0: Logout and exit program")
                    
                    while userChoice < 0 or userChoice > 4:
                        userChoice = int(input("Enter here: "))
                    
                    match userChoice:
                        case 1:
                            profileManagement()
                        case 2:
                            dashboardDisplay()
                        case 3:
                            memberScheduleManagement()
                        case 4:
                            keepGoing2 = False
                        case 0:
                            keepGoing2 = False
                            keepGoing1 = False
                
                case "trainer":
                    print("\t1: Schedule Management (Set the time you are available, or manage your classes and sessions)")
                    print("\t2: Member Profile Viewing (View the profile of a member)")
                    print("\t3: Logout and switch users")
                    print("\t0: Logout and exit program")
                    
                    while userChoice < 0 or userChoice > 3:
                        userChoice = int(input("Enter here: "))
                        
                    match userChoice:
                        case 1:
                            trainerScheduleManagement()
                        case 2:
                            memberProfileViewing()
                        case 3:
                            keepGoing2 = False
                        case 0:
                            keepGoing2 = False
                            keepGoing1 = False
                            
                case "admin":
                    print("\t1: Room Booking Management (Manage room bookings)")
                    print("\t2: Equipment Maintenance Monitoring (Maintain, add, or remove an equipment in the system)")
                    print("\t3: Class Schedule Updating (Make updates to a group class or training session)")
                    print("\t4: Billing and Payment Processing (View and create bills)")
                    print("\t5: Logout and switch users")
                    print("\t0: Logout and exit program")
                    
                    while userChoice < 0 or userChoice > 5:
                        userChoice = int(input("Enter here: "))
                        
                    match userChoice:
                        case 1:
                            roomBookingManagement()
                        case 2:
                            equipmentMaintenanceMonitoring()
                        case 3:
                            classScheduleUpdating()
                        case 4:
                            billingAndPaymentProcessing()
                        case 5:
                            keepGoing2 = False
                        case 0:
                            keepGoing2 = False
                            keepGoing1 = False
    
    cursor.close()
    conn.close()

# register a new member
def userRegistration():
    firstname = input("Welcome to the Health and Fitness Club!\nTo continue registration, please tell us your first name: ")
    lastname = input("Now, please tell us your last name: ")
    phonenumber = input("Please enter your phone number: ")
    address = input("Please enter your address: ")
    weight = input("Please enter your weight in pounds: ")
    height = input("Please enter your height in cm: ")
    age = input("Please enter your age: ")
    sex = input("Please enter your sex: ")
    desiredweight = input("Please enter your desired weight in pounds: ")
    dailytime = input("Please enter how many minutes you would like to exercise each day: ")

    if insertMember(globalEmail, firstname, lastname, phonenumber, address, weight, height, age, sex, desiredweight, dailytime):
        print("Thank you for entering your information. The registration was successful. Welcome to the Health and Fitness Club!")
        cursor.execute("INSERT INTO achievements (memberemail, achievementname, dateearned) VALUES (%s, %s, current_date);", (globalEmail, 'Signed Up!'))
    else:
        print("Registration was unsuccessful. Perhaps your email has already been used.")

# inserts a new member into the ClubMember table    
def insertMember(memberemail, firstname, lastname, phonenumber, address, weight, height, age, sex, desiredweight, dailytime):
    try:
        cursor.execute("INSERT INTO clubmember (memberemail, firstname, lastname, phonenumber, address, weight, height, age, sex, desiredweight, dailytime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (memberemail, firstname, lastname, phonenumber, address, weight, height, age, sex, desiredweight, dailytime))
        return True
    except:
        return False
        
# a member can update their personal information, set fitness goals, or set health metrics 
def profileManagement():
    
    profileChoice = 1;
    while profileChoice != 0:
    
        cursor.execute("SELECT * FROM clubmember WHERE memberemail = %s", [globalEmail])
        rows = cursor.fetchall()
                
        print("\nPlease enter an integer from 0 to 3.")
        print("\t1: Update personal information")
        print("\t2: Set fitness goals")
        print("\t3: Set health metrics")
        print("\t0: Quit profile management")
        profileChoice = int(input("Enter here: "))
        
        match profileChoice:
            case 1:
                print("Your personal information is as follows: ")
                print("\t1: Your first name is: " + rows[0][1])
                print("\t2: Your last name is: " + rows[0][2])
                print("\t3: Your phone number is: " + rows[0][3])
                print("\t4: Your address is: " + rows[0][4])
                print("\t0: Go back to previous menu")
                
                editChoice = 1;
                while editChoice != 0:
                    editChoice = int(input("\nEnter an integer to select a field to change: "))
                    
                    match editChoice:
                        case 1:
                            newValue = input("Enter a new first name: ")
                            updateMember("firstname", newValue)
                        case 2:
                            newValue = input("Enter a new last name: ")
                            updateMember("lastname", newValue)                        
                        case 3:
                            newValue = input("Enter a new phone number: ")
                            updateMember("phonenumber", newValue)                    
                        case 4:
                            newValue = input("Enter a new address: ")
                            updateMember("address", newValue)
                            
            case 2:
                print("Your fitness goals are currently: ")
                print("\t1: Your desired weight is: " + str(rows[0][9]) + " pounds.")
                print("\t2: The amount of time you want to spend working out daily is: " + str(rows[0][10]) + " minutes.")
                print("\t0: Go back to previous menu")

                editChoice = 1;
                while editChoice != 0:
                    editChoice = int(input("\nEnter an integer to select a field to change: "))
                    
                    match editChoice:
                        case 1:
                            newValue = input("Enter your new desired weight in pounds: ")
                            updateMember("desiredweight", int(newValue))
                        case 2:
                            newValue = input("Enter the amount of minutes you would like to exercise for each day: ")
                            updateMember("dailytime", int(newValue))
            case 3:
                print("Your health metrics are recorded as: ")
                print("\t1: Your current weight is: " + str(rows[0][5]) + " pounds.")
                print("\t2: Your current height is: " + str(rows[0][6]) + " cm.")
                print("\t3: Your current age is: " + str(rows[0][7]) + " years old.")
                print("\t4: Your sex is: " + rows[0][8])
                print("\t0: Go back to previous menu")

                editChoice = 1;
                while editChoice != 0:
                    editChoice = int(input("\nEnter an integer to select a field to change: "))
                    
                    match editChoice:
                        case 1:
                            newValue = input("Enter your current weight in pounds: ")
                            updateMember("weight", int(newValue))
                        case 2:
                            newValue = input("Enter your height in cm: ")
                            updateMember("height", int(newValue))                
                        case 3:
                            newValue = input("Enter your age: ")
                            updateMember("age", int(newValue))                
                        case 4:
                            newValue = input("Enter your sex: ")
                            updateMember("sex", newValue)    


# updates a member's information in the database 
def updateMember(field, value):
    try:
        cursor.execute("UPDATE clubmember SET " + field + " = %s WHERE memberemail = %s;", [value, globalEmail])
        print("Update successful.")
    except:
        print("Update failed.")

# a member can view their routine, achievements, and health statistics     
def dashboardDisplay():
    cursor.execute("SELECT warmuptime, pushupreps, situpreps, squatreps, weightreps, treadmillmin, cooldowntime, totalminutes, totalcalories, totaldays FROM clubmember WHERE memberemail = %s;", [globalEmail])
    routinesAndStats = cursor.fetchall()[0]
    
    cursor.execute("SELECT * FROM achievements WHERE memberemail = %s;", [globalEmail])
    achievementRows = cursor.fetchall()
    
    
    print("Your routine is as follows: ")
    print("\tWarmup stretch for " + str(routinesAndStats[0]) + " minutes.")
    print("\tPushups for " + str(routinesAndStats[1]) + " reps.")
    print("\tSitups for " + str(routinesAndStats[2]) + " reps.")
    print("\tSquats for " + str(routinesAndStats[3]) + " reps.")
    print("\tWeight lifting for " + str(routinesAndStats[4]) + " reps.")
    print("\tRun on a treadmill for " + str(routinesAndStats[5]) + " minutes.")
    print("\tCooldown stretch for " + str(routinesAndStats[6]) + " minutes.")
    
    print("Your achievements are as follows: ")
    for row in achievementRows:
        print("\t" + row[1] + ": Earned on " + str(row[2]))
        
    print("Your health statistics are as follows:")
    print("\tYou've spent a total of " + str(routinesAndStats[7]) + " minutes exercising.")
    print("\tYou've burnt an estimated total of " + str(routinesAndStats[8]) + " calories exercising.")
    print("\tYou've attended this gym for a total of " + str(routinesAndStats[9]) + " days.")
    
# a member can schedule, reschedule, or cancel a training session. a member may also schedule a new group class, or join an existing one. a member can also unregister themselves from a group class.
def memberScheduleManagement():
    print("\nEnter an integer to select an option.")
    print("\t1: Schedule a training session. ")
    print("\t2: Schedule a new group class. ")
    print("\t3: Join an existing group class. ")
    print("\t4: Reschedule a training session. ")
    print("\t5: Cancel a training session. ")
    print("\t6: Unregister from a group class. ") 
    print("\t0: Go back to previous menu")
            
    try:        
        selectChoice = -1;
        while selectChoice < 0 or selectChoice > 6:

            selectChoice = int(input("Enter here: "))
            match selectChoice:
                
                # user wants to schedule a new training session or new group class
                case 1 | 2:
                    bookDate = input("Please enter your desired date in YYYY-MM-DD format: ")
                    
                    # retrieve all rooms that do not have a training session or group class on that date.
                    availableRooms = getAvailableRooms(bookDate)
                    
                    if not memberCheckConflict(globalEmail, bookDate):
                        print("You already have something scheduled on this date.")
                    elif (len(availableRooms) == 0):
                        print("There are no rooms available on this date.")
                    else:
                        try:
                            # retrieve all trainers that are available to have new sessions on that date. 
                            cursor.execute("SELECT firstname, lastname, traineremail FROM trainer WHERE traineremail IN (SELECT traineremail FROM availabledates WHERE availabledate = %s);", [bookDate])
                            trainerRows = cursor.fetchall()
                            
                            # print out available trainers to user 
                            print("Here are the available trainers on that date: ")
                            count = 1
                            for trainerRow in trainerRows:
                                print("\t" + str(count) + ": " + trainerRow[0] + " " + trainerRow[1])
                                count = count + 1
                            print("\t0: Quit booking and return to previous menu.")
                            
                            # get choice of trainer from user 
                            trainerChoice = -1
                            while trainerChoice < 0 or trainerChoice > count:
                                trainerChoice = int(input("Select a trainer by entering an integer: "))
                            
                            # if user did not choose to exit 
                            if (trainerChoice > 0):
                                # trainerRows start counting at 0, so subtract 1 from trainerChoice
                                trainerChoice = trainerChoice - 1;
                                
                                # get choice of room from user 
                                roomChoice = -1
                                while (roomChoice not in availableRooms and roomChoice != 0):
                                    roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))
                                                                
                                # user did not choose to exit
                                if (roomChoice != 0):
                                    try:
                                        # register a new Training Session, and create a new Bill
                                        if selectChoice == 1:
                                            cursor.execute("INSERT INTO TrainingSessions(DateBooked, TrainerEmail, RoomNumber, MemberEmail) VALUES (%s, %s, %s, %s);", (bookDate, trainerRows[trainerChoice][2], roomChoice, globalEmail))
                                            cursor.execute("DELETE FROM AvailableDates WHERE traineremail = %s AND availabledate = %s", (trainerRows[trainerChoice][2], bookDate))
                                            print("You have successfully booked a Training Session with " + trainerRows[trainerChoice][0] + " " + trainerRows[trainerChoice][1] + " on " + bookDate + " in Room " + str(roomChoice) + ".")
                                            print("A registration fee of $50 was automatically charged to your payment method on file.")
                                            cursor.execute("INSERT INTO bill (amount, memberemail, datepaid) VALUES (50, %s, current_date);", [globalEmail])
                                        
                                        # register a new Group Class, and create a new Bill
                                        else:
                                            cursor.execute("INSERT INTO GroupClasses(DateBooked, TrainerEmail, RoomNumber) VALUES (%s, %s, %s);", (bookDate, trainerRows[trainerChoice][2], roomChoice))
                                            cursor.execute("SELECT GroupID FROM GroupClasses WHERE DateBooked = %s AND TrainerEmail = %s AND RoomNumber = %s;", (bookDate, trainerRows[trainerChoice][2], roomChoice))
                                            newGroupID = cursor.fetchall()[0][0]
                                            cursor.execute("INSERT INTO PartakesIn(GroupID, MemberEmail) VALUES (%s, %s);", (newGroupID, globalEmail))
                                            cursor.execute("DELETE FROM AvailableDates WHERE traineremail = %s AND availabledate = %s", (trainerRows[trainerChoice][2], bookDate))
                                            print("You have successfully booked a new Group Class with " + trainerRows[trainerChoice][0] + " " + trainerRows[trainerChoice][1] + " on " + bookDate + " in Room " + str(roomChoice) + ".")
                                            print("A registration fee of $50 was automatically charged to your payment method on file.")
                                            cursor.execute("INSERT INTO bill (amount, memberemail, datepaid) VALUES (50, %s, current_date);", [globalEmail])
                                    except:
                                        print("An error occured.")
                        except:
                            print("An error occured.")
                
                # user wants to join an existing group class
                case 3:
                    availableGroups = [0]
                    cursor.execute("SELECT * FROM GroupClasses")
                    groupRows = cursor.fetchall()
                    
                    # print out available group classes for the user 
                    print("Here are all the Group Classes that do not conflict with your schedule: ")
                    for groupRow in groupRows:
                        if memberCheckConflict(globalEmail, groupRow[1]):
                            print("\t" + str(groupRow[0]) + ": On " + str(groupRow[1]) + ", lead by " + groupRow[2] + " in Room " + str(groupRow[3]) + ".")
                            availableGroups.append(groupRow[0])
                    print("\t0: Go back to previous menu")
                    
                    # get user's choice of group class
                    groupChoice = -1
                    while groupChoice not in availableGroups:
                        groupChoice = int(input("Enter an integer representing the Group Class you want to join: "))
                    
                    # user did not choose to exit, so register them for the group class
                    if groupChoice != 0:
                        try:
                            cursor.execute("INSERT INTO PartakesIn(GroupID, MemberEmail) VALUES (%s, %s);", (groupChoice, globalEmail))
                            for groupRow in groupRows:
                                if groupRow[0] == groupChoice:
                                    print("You have successfully signed up for the Group Class on " + str(groupRow[1]) + ", lead by " + groupRow[2] + " in Room " + str(groupRow[3]) + ".")
                                    print("A registration fee of $50 was automatically charged to your payment method on file.")
                                    cursor.execute("INSERT INTO bill (amount, memberemail, datepaid) VALUES (50, %s, current_date);", [globalEmail])
                                    break
                        except:
                            print("An error occured.")
                
                # user wants to reschedule or cancel a training session 
                case 4 | 5:
                
                    # print out the training sessions the member is attending
                    cursor.execute("SELECT * FROM trainingsessions NATURAL INNER JOIN trainer WHERE memberemail = %s ORDER BY trainid", [globalEmail])
                    trainingRows = cursor.fetchall()
                    trainingList = [0]
                    print("Here are the training sessions: ")
                    for row in trainingRows:
                        print(str(row[1]) + ": Led by " + row[5] + " " + row[6] + " on " + str(row[2]) + " in Room " + str(row[3]) + ".")
                        trainingList.append(int(row[1]))
                    print("0: Go back to previous menu")
                    trainingChoice = -1
                    
                    # reschedule the training session 
                    if selectChoice == 4:
                        while trainingChoice not in trainingList:
                            trainingChoice = int(input("Enter an integer representing the Training Session you would like to reschedule: "))
                        
                        if (trainingChoice != 0):
                            cursor.execute("SELECT traineremail FROM trainingsessions WHERE trainid = %s", [trainingChoice])
                            trainerEmail = cursor.fetchall()[0][0]
                            
                            # get the dates the trainer is available on 
                            availableDates = ["0"]
                            print("The trainer is also available on these dates: ")
                            cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [trainerEmail])
                            dateRows = cursor.fetchall()
                            
                            for row in dateRows:
                                print(row[0])
                                availableDates.append(str(row[0]))
                            
                            # have user select a date 
                            bookDate = "-1"
                            while bookDate not in availableDates:
                                bookDate = input("Enter one of these dates to change the date of the training session, or 0 to go back: ")
                            
                            # if user did not choose to exit
                            if bookDate != "0":
                                # check if member is available on that date
                                if memberCheckConflict(globalEmail, bookDate):
                                    # retrieve all rooms that do not have a training session or group class on that date.
                                    availableRooms = getAvailableRooms(bookDate)
                                    
                                    if len(availableRooms) == 0:
                                        print("There are no rooms available on this date.")     
                                    else:
                                        # have user select a room 
                                        roomChoice = -1
                                        while (roomChoice not in availableRooms and roomChoice != 0):
                                            roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))
                                        
                                        # user did not choose to exit
                                        if (roomChoice != 0):
                                            try:
                                                # update the Training Session 
                                                cursor.execute("UPDATE trainingsessions SET datebooked = %s, roomnumber = %s WHERE trainid = %s;", [bookDate, roomChoice, trainingChoice])
                                                
                                                cursor.execute("DELETE FROM availabledates WHERE traineremail = %s AND availabledate = %s", (trainerEmail, bookDate))
                                                
                                                print("You have successfully rescheduled the training session.")
                                            except:
                                                print("An error occured.")
                                else:
                                    print("You already have something scheduled on that date. Please try again.")
                    
                    # cancel a training session
                    else:
                        while trainingChoice not in trainingList:
                            trainingChoice = int(input("Enter an integer representing the Training Session you would like to cancel: "))
                        if (trainingChoice != 0):
                            try:
                                cursor.execute("DELETE FROM trainingsessions WHERE trainid = %s;", [trainingChoice])
                                print("The training session was successfully cancelled.")
                            except:
                                print("An error occured.")    
                
                # user wants to unregister from a group class 
                case 6:
                    # print out the group classes the user is attending 
                    cursor.execute("SELECT * FROM trainer NATURAL INNER JOIN (SELECT traineremail, datebooked, roomnumber, groupclasses.groupid FROM groupclasses, partakesin WHERE groupclasses.groupid = partakesin.groupid AND memberemail = %s) ORDER BY groupid", [globalEmail])
                    groupRows = cursor.fetchall()
                    groupList = [0]
                    print("Here are the group classes: ")
                    for row in groupRows:
                        print("\t" + str(row[5]) + ": Led by " + row[1] + " " + row[2] + " on " + str(row[3]) + " in Room " + str(row[4]) + ".")
                        groupList.append(int(row[5]))
                    print("\t0: Go back to previous menu")
                    groupChoice = -1
                    
                    while groupChoice not in groupList:
                        groupChoice = int(input("Enter an integer representing the Group Class you would like to unregister from: "))
                        
                    if (groupChoice != 0):
                        try:
                            cursor.execute("DELETE FROM partakesin WHERE groupid = %s AND memberemail = %s;", [groupChoice, globalEmail])
                            print("You have successfully unregistered from the group class.")
                            
                            # if there are no more members in the group class, cancel the class altogether
                            cursor.execute("SELECT * FROM partakesin WHERE groupid = %s;", [groupChoice])
                            if len(cursor.fetchall()) == 0:
                                cursor.execute("DELETE FROM groupclasses WHERE groupid = %s;", [groupChoice])
                        except:
                            print("An error occured.")
                        
    except:
        print("An error occured.")

# a trainer may update or cancel training sessions or group classes, as well as update the days they are available
def trainerScheduleManagement():
    print("Enter an integer to select an option: ")
    print("\t1: Update a Training Session")
    print("\t2: Update a Group Class")
    print("\t3: Cancel a Training Session")
    print("\t4: Cancel a Group Class")
    print("\t5: Update your availability")
    print("\t0: Go back to previous menu")
    
    choice = -1
    while choice < 0 or choice > 5:
        choice = int(input("Enter here: "))
    
    match choice:
        # user wants to update or cancel a training session 
        case 1 | 3:
        
            # print out all training sessions the trainer is leading
            cursor.execute("SELECT * FROM trainingsessions NATURAL INNER JOIN trainer, clubmember WHERE trainingsessions.memberemail = clubmember.memberemail AND traineremail = %s ORDER BY trainid", [globalEmail])
            trainingRows = cursor.fetchall()
            trainingList = [0]
            print("Here are your training sessions: ")
            for row in trainingRows:
                print("\t" + str(row[1]) + ": On " + str(row[2]) + " in Room " + str(row[3]) + ", attended by " + row[8] + " " + row[9] + ".")
                trainingList.append(int(row[1]))
            print("\t0: Go back to previous menu")
            trainingChoice = -1
            
            # reschedule the training session 
            if choice == 1:
                while trainingChoice not in trainingList:
                    trainingChoice = int(input("Enter an integer representing the Training Session you would like to update the schedule of: "))
                
                if (trainingChoice != 0):
                    
                    availableDates = ["0"]
                    print("Here are the dates where you have indicated you are available: ")
                    cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [globalEmail])
                    dateRows = cursor.fetchall()
                    
                    for row in dateRows:
                        print(row[0])
                        availableDates.append(str(row[0]))
                    
                    # user selects a date
                    bookDate = "-1"
                    while bookDate not in availableDates:
                        bookDate = input("Enter one of these dates to change the date of the training session, or 0 to go back: ")
                    
                    # if user did not choose to exit
                    if bookDate != "0":
                        # check if attending member is available on that date
                        if memberCheckConflict(trainingRows[0][4], bookDate):
                            # retrieve all rooms that do not have a training session or group class on that date.
                            availableRooms = getAvailableRooms(bookDate)
                            
                            if len(availableRooms) == 0:
                                print("There are no rooms available on this date.")     
                            else:
                                roomChoice = -1
                                while (roomChoice not in availableRooms and roomChoice != 0):
                                    roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))
                                
                                # user did not choose to exit
                                if (roomChoice != 0):
                                    try:
                                        # update the Training Session 
                                        cursor.execute("UPDATE trainingsessions SET datebooked = %s, roomnumber = %s WHERE trainid = %s;", [bookDate, roomChoice, trainingChoice])
                                        
                                        cursor.execute("DELETE FROM availabledates WHERE traineremail = %s AND availabledate = %s", (globalEmail, bookDate))
                                        
                                        print("You have successfully updated the date of the training session.")
                                    except:
                                        print("An error occured.")
                        else:
                            print("The member attending the session already has something booked on that date. Please try again.")
            
            # cancel a training session 
            else:
                while trainingChoice not in trainingList:
                    trainingChoice = int(input("Enter an integer representing the Training Session you would like to cancel: "))
                if (trainingChoice != 0):
                    try:
                        cursor.execute("DELETE FROM trainingsessions WHERE trainid = %s;", [trainingChoice])
                        print("The training session was successfully cancelled.")
                    except:
                        print("An error occured.")
        
        # user wants to update or cancel a group class 
        case 2 | 4:
            # print out all the group classes the trainer is leading
            cursor.execute("SELECT * FROM trainer NATURAL INNER JOIN (SELECT traineremail, datebooked, roomnumber, groupclasses.groupid, count(memberemail) FROM groupclasses, partakesin WHERE groupclasses.groupid = partakesin.groupid GROUP BY groupclasses.groupid) WHERE traineremail = %s ORDER BY groupid", [globalEmail])
            groupRows = cursor.fetchall()
            groupList = [0]
            print("Here are your group classes: ")
            for row in groupRows:
                print("\t" + str(row[5]) + ": On " + str(row[3]) + " in Room " + str(row[4]) + ", attended by " + str(row[6]) + " members.")
                groupList.append(int(row[5]))
            print("\t0: Go back to previous menu")
            groupChoice = -1
            
            # reschedule a group class 
            if choice == 2:
                while groupChoice not in groupList:
                    groupChoice = int(input("Enter an integer representing the Group Class you would like to update the schedule of: "))
                    
                if (groupChoice != 0):
                    
                    availableDates = ["0"]
                    print("Here are the dates where you have indicated you are available: ")
                    cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [globalEmail])
                    dateRows = cursor.fetchall()

                    for row in dateRows:
                        print(row[0])
                        availableDates.append(str(row[0]))
                    
                    # user selects a date
                    bookDate = "-1"
                    while bookDate not in availableDates:
                        bookDate = input("Enter one of these dates to change the date of the group class, or 0 to go back: ")
                    
                    # if user did not choose to exit
                    if bookDate != "0":
                        # check if all attending members are available on that date
                        cursor.execute("SELECT memberemail FROM partakesin WHERE groupid = %s", [groupChoice])
                        memberRows = cursor.fetchall()
                        
                        allAreAvailable = True
                        for row in memberRows:
                            if not memberCheckConflict(row[0], bookDate):
                                allAreAvailable = False
                        
                        if allAreAvailable:
                            # retrieve all rooms that do not have a training session or group class on that date.
                            availableRooms = getAvailableRooms(bookDate)
                           
                            if len(availableRooms) == 0:
                                print("There are no rooms available on this date.")     
                            else:
                                roomChoice = -1   
                                while (roomChoice not in availableRooms and roomChoice != 0):
                                    roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))     

                                # user did not choose to exit
                                if (roomChoice != 0):
                                    try:
                                        # update the Group Class 
                                        cursor.execute("UPDATE groupclasses SET datebooked = %s, roomnumber = %s WHERE groupid = %s;", [bookDate, roomChoice, groupChoice])
                                        
                                        cursor.execute("DELETE FROM availabledates WHERE traineremail = %s AND availabledate = %s", (globalEmail, bookDate))
                                        
                                        print("You have successfully updated the date of the group class.")
                                    except:
                                        print("An error occured.")
                        else:
                            print("One of the members attending the class already has something booked on that date. Please try again.")
            
            # cancel the group class 
            else:
                while groupChoice not in groupList:
                    groupChoice = int(input("Enter an integer representing the Group Class you would like to cancel: "))
                    
                if (groupChoice != 0):
                    try:
                        cursor.execute("DELETE FROM partakesin WHERE groupid = %s;", [groupChoice])
                        cursor.execute("DELETE FROM groupclasses WHERE groupid = %s;", [groupChoice])
                        print("The training session was successfully cancelled.")
                    except:
                        print("An error occured.")
        
        # update trainer availability
        case 5:
            availableDates = []
            print("Here are your available dates: ")
            
            # get all available dates for the trainer
            cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [globalEmail])
            rows = cursor.fetchall()
            for row in rows:
                print(row[0])
                availableDates.append(str(row[0]))
            
            print("You may enter: ")
            print("\tA date in the list to remove that date from the list, making you unavailable on that date.")
            print("\tA date not in the list to add that date to the list, making you available on that date.")
            print("\t0 to return to the previous menu.")
            newDate = input("Enter here: ")
            
            # go back to previous menu 
            if (newDate == "0"):
                return
            
            # trainer wants to delete an available date
            if (newDate in availableDates):
                cursor.execute("DELETE FROM AvailableDates WHERE traineremail = %s AND availabledate = %s", (globalEmail, newDate))
                print("The date was successfully removed from the list.")
            
            # trainer wants to add an available date
            else:
                try:
                    # if there are no scheduling conflicts, go ahead and add the date
                    if trainerCheckConflict(globalEmail, newDate):
                        cursor.execute("INSERT INTO AvailableDates(TrainerEmail, AvailableDate) VALUES (%s, %s);", (globalEmail, newDate))
                        print("The date was successfully added to the list.")
                    else:
                        print("You already have something scheduled on that date, so you cannot be available on that date.")
                except Exception as error:
                    print(error)

# a trainer may view the profile of a member by searching them up by name 
def memberProfileViewing():
    firstname = input("Please enter the first name of the member whose profile you would like to view: ")
    lastname = input("Please enter the last name of the member whose profile you would like to view: ")
    cursor.execute("SELECT * FROM clubmember WHERE firstname = %s AND lastname = %s", (firstname, lastname))
    memberRows = cursor.fetchall()
    
    print("The following members match the names you provided: ")
    
    count = 1
    for memberRow in memberRows:
        print("\t" + str(count) + ": " + memberRow[1] + " " + memberRow[2] + ", " + memberRow[0] + ", " + memberRow[3])
        count = count + 1
    print("\t0: Return to previous menu.")
    
    # get choice of member from user 
    memberChoice = -1
    while memberChoice < 0 or memberChoice > count - 1:
        memberChoice = int(input("Select the member you want by entering an integer: "))
    
    # if user did not choose to exit 
    if (memberChoice > 0):
        # memberRows start counting at 0, so subtract 1 from memberChoice
        memberChoice = memberChoice - 1;
        print("Here are the details of your selected member.")
        print("Email: " + memberRows[memberChoice][0])
        print("Name: " + memberRows[memberChoice][1] + " " + memberRows[memberChoice][2])
        print("Phone Number: " + memberRows[memberChoice][3])
        print("Address: " + memberRows[memberChoice][4])
        print("Weight: " + str(memberRows[memberChoice][5]) + " lbs.")
        print("Height: " + str(memberRows[memberChoice][6]) + " cm.")
        print("Age: " + str(memberRows[memberChoice][7])  + " years old.")
        print("Sex: " + memberRows[memberChoice][8])
        print("Desired Weight: " + str(memberRows[memberChoice][9]) + " lbs.")
        print("Desired Daily Exercise Time: " + str(memberRows[memberChoice][10]) + " minutes.")

# an admin can maintain, add, or remove equipment 
def equipmentMaintenanceMonitoring():

    print("Enter an integer to select an option: ")
    print("\t1: Perform maintenance on equipment")
    print("\t2: Add equipment to the system")
    print("\t3: Remove equipment from the system ")
    print("\t0: Go back to previous menu")
    
    choice = -1
    while choice < 0 or choice > 3:
        choice = int(input("Enter here: "))

    match choice:
        # maintain an equipment after seeing when it was last maintained 
        case 1:
            print("Here are the equipment details: ")
            cursor.execute("SELECT * FROM equipment ORDER BY equipID")
            rows = cursor.fetchall()
            
            idList = [0]
            equipChoice = -1
            
            #print out equipment details for user 
            for row in rows:
                print("\t" + str(row[0]) + ": " + row[1] + " in Room " + str(row[3]) + " was last maintained on " + str(row[2]) + ".");
                idList.append(row[0])
            print("\t0: Go back to previous menu")
            
            
            while equipChoice not in idList:
                equipChoice = int(input("Enter an integer representing the equipment you want to maintain here: "))
            
            # user chooses to go back
            if equipChoice == 0:
                return
            
            # maintain the equipment chosen 
            try:
                cursor.execute("UPDATE equipment SET lastmaintained = current_date WHERE equipID = %s;", [equipChoice])
                print("The equipment successfully underwent maintenance.")
            except:
                print("An error occured.")
        
        # add a new equipment into the system 
        case 2:
            equipName = input("Enter the name of the equipment: ")
            
            # parameter is a date where the gym wasn't even open, and so all rooms are available
            availableRooms = getAvailableRooms('1874-05-12')
            
            roomChoice = -1
            while (roomChoice not in availableRooms and roomChoice != 0):
                roomChoice = int(input("Enter an integer representing a room to put the equipment in - "+ str(availableRooms) + ", or 0 to go back: "))
            
            # user did not choose to exit
            if (roomChoice != 0):
                try:
                    cursor.execute("INSERT INTO equipment (equipname, lastmaintained, roomnumber) VALUES (%s, current_date, %s);", (equipName, roomChoice))
                    print("You have successfully added a new equipment into the system.")
                except:
                    print("An error occured.")
         
        # remove an equipment from the system 
        case 3:
            print("Here are the equipment details: ")
            cursor.execute("SELECT * FROM equipment ORDER BY equipID")
            rows = cursor.fetchall()
            
            idList = [0]
            equipChoice = -1
            
            #print out equipment details for user 
            for row in rows:
                print("\t" + str(row[0]) + ": " + row[1] + " in Room " + str(row[3]) + ".");
                idList.append(row[0])
            print("0: Go back to previous menu")
            
            
            while equipChoice not in idList:
                equipChoice = int(input("Enter an integer representing the equipment you want to remove from the system: "))
            
            # user chooses to go back
            if equipChoice == 0:
                return
            
            # delete the equipment chosen 
            try:
                cursor.execute("DELETE FROM equipment WHERE equipID = %s;", [equipChoice])
                print("The equipment was successfully removed from the system.")
            except:
                print("An error occured.")

# an admin may update or cancel a training session or group class 
def classScheduleUpdating():

    print("Enter an integer to select an option: ")
    print("\t1: Update a Training Session")
    print("\t2: Update a Group Class")
    print("\t3: Cancel a Training Session")
    print("\t4: Cancel a Group Class")
    print("\t0: Go back to previous menu")
    
    choice = -1
    while choice < 0 or choice > 4:
        choice = int(input("Enter here: "))
    
    # user wants to update a training session 
    match choice:
        case 1 | 3:
            # get all training sessions, alongside the names of the trainer and member attending 
            cursor.execute("SELECT * FROM trainingsessions NATURAL INNER JOIN trainer, clubmember WHERE trainingsessions.memberemail = clubmember.memberemail ORDER BY trainid")
            trainingRows = cursor.fetchall()
            trainingList = [0]
            print("Here are the training sessions: ")
            for row in trainingRows:
                print("\t" + str(row[1]) + ": Led by " + row[5] + " " + row[6] + " on " + str(row[2]) + " in Room " + str(row[3]) + ", attended by " + row[8] + " " + row[9] + ".")
                trainingList.append(int(row[1]))
            print("\t0: Go back to previous menu")
            trainingChoice = -1
            
            
            if choice == 1:
                while trainingChoice not in trainingList:
                    trainingChoice = int(input("Enter an integer representing the Training Session you would like to update the schedule of: "))
                
                if (trainingChoice != 0):
                    cursor.execute("SELECT traineremail FROM trainingsessions WHERE trainid = %s", [trainingChoice])
                    trainerEmail = cursor.fetchall()[0][0]
                    
                    # print out the dates the trainer is available 
                    availableDates = ["0"]
                    print("The trainer is also available on these dates: ")
                    cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [trainerEmail])
                    dateRows = cursor.fetchall()
                    
                    for row in dateRows:
                        print(row[0])
                        availableDates.append(str(row[0]))
                    
                    # choose a date
                    bookDate = "-1"
                    while bookDate not in availableDates:
                        bookDate = input("Enter one of these dates to change the date of the training session, or 0 to go back: ")
                    
                    # if user did not choose to exit
                    if bookDate != "0":
                        # check if the attending member is available on that date
                        if memberCheckConflict(trainingRows[0][4], bookDate):
                            # retrieve all rooms that do not have a training session or group class on that date.
                            availableRooms = getAvailableRooms(bookDate)
                            
                            if len(availableRooms) == 0:
                                print("There are no rooms available on this date.")     
                            else:
                                roomChoice = -1
                                while (roomChoice not in availableRooms and roomChoice != 0):
                                    roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))
                                
                                # user did not choose to exit
                                if (roomChoice != 0):
                                    try:
                                        # update the Training Session 
                                        cursor.execute("UPDATE trainingsessions SET datebooked = %s, roomnumber = %s WHERE trainid = %s;", [bookDate, roomChoice, trainingChoice])
                                        
                                        cursor.execute("DELETE FROM availabledates WHERE traineremail = %s AND availabledate = %s", (trainerEmail, bookDate))
                                        
                                        print("You have successfully updated the date of the training session.")
                                    except:
                                        print("An error occured.")
                        else:
                            print("The member attending the session already has something booked on that date. Please try again.")
            # cancel a training session 
            else:
                while trainingChoice not in trainingList:
                    trainingChoice = int(input("Enter an integer representing the Training Session you would like to cancel: "))
                if (trainingChoice != 0):
                    try:
                        cursor.execute("DELETE FROM trainingsessions WHERE trainid = %s;", [trainingChoice])
                        print("The training session was successfully cancelled.")
                    except:
                        print("An error occured.")
        # user wants to update a group class 
        case 2 | 4:
            # get all group classes alongside their trainer and number of attending members 
            cursor.execute("SELECT * FROM trainer NATURAL INNER JOIN (SELECT traineremail, datebooked, roomnumber, groupclasses.groupid, count(memberemail) FROM groupclasses, partakesin WHERE groupclasses.groupid = partakesin.groupid GROUP BY groupclasses.groupid) ORDER BY groupid")
            groupRows = cursor.fetchall()
            groupList = [0]
            print("Here are the group classes: ")
            for row in groupRows:
                print("\t" + str(row[5]) + ": Led by " + row[1] + " " + row[2] + " on " + str(row[3]) + " in Room " + str(row[4]) + ", attended by " + str(row[6]) + " members.")
                groupList.append(int(row[5]))
            print("\t0: Go back to previous menu")
            groupChoice = -1
            
            if choice == 2:
                while groupChoice not in groupList:
                    groupChoice = int(input("Enter an integer representing the Group Class you would like to update the schedule of: "))
                    
                if (groupChoice != 0):
                    print("Before you proceed, you should know that the following members are attending this Group Class: ")
                    
                    # print out the names of members attending the group class
                    cursor.execute("SELECT firstname, lastname FROM (SELECT * FROM partakesin WHERE groupid = %s) NATURAL INNER JOIN clubmember;", [groupChoice])
                    for row in cursor.fetchall():
                        print("\t" + row[0] + " " + row[1])
                    
                    cursor.execute("SELECT traineremail FROM groupclasses WHERE groupid = %s", [groupChoice])
                    trainerEmail = cursor.fetchall()[0][0]
                    
                    # print out trainer's available dates
                    availableDates = ["0"]
                    print("The trainer is also available on these dates: ")
                    cursor.execute("SELECT availabledate FROM availabledates WHERE traineremail = %s", [trainerEmail])
                    dateRows = cursor.fetchall()

                    for row in dateRows:
                        print(row[0])
                        availableDates.append(str(row[0]))
                    
                    # choose a date 
                    bookDate = "-1"
                    while bookDate not in availableDates:
                        bookDate = input("Enter one of these dates to change the date of the group class, or 0 to go back: ")
                    
                    # if user did not choose to exit
                    if bookDate != "0":
                        # check if all members are available on that date
                        cursor.execute("SELECT memberemail FROM partakesin WHERE groupid = %s", [groupChoice])
                        memberRows = cursor.fetchall()
                        
                        allAreAvailable = True
                        for row in memberRows:
                            if not memberCheckConflict(row[0], bookDate):
                                allAreAvailable = False
                        
                        if allAreAvailable:
                            # retrieve all rooms that do not have a training session or group class on that date.
                            availableRooms = getAvailableRooms(bookDate)
                           
                            if len(availableRooms) == 0:
                                print("There are no rooms available on this date.")     
                            else:
                                roomChoice = -1   
                                while (roomChoice not in availableRooms and roomChoice != 0):
                                    roomChoice = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))     

                                # user did not choose to exit
                                if (roomChoice != 0):
                                    try:
                                        # update the Group Class 
                                        cursor.execute("UPDATE groupclasses SET datebooked = %s, roomnumber = %s WHERE groupid = %s;", [bookDate, roomChoice, groupChoice])
                                        
                                        cursor.execute("DELETE FROM availabledates WHERE traineremail = %s AND availabledate = %s", (trainerEmail, bookDate))
                                        
                                        print("You have successfully updated the date of the group class.")
                                    except:
                                        print("An error occured.")
                        else:
                            print("One of the members attending the class already has something booked on that date. Please try again.")
            
            # cancel a group class 
            else:
                while groupChoice not in groupList:
                    groupChoice = int(input("Enter an integer representing the Group Class you would like to cancel: "))
                    
                if (groupChoice != 0):
                    try:
                        cursor.execute("DELETE FROM partakesin WHERE groupid = %s;", [groupChoice])
                        cursor.execute("DELETE FROM groupclasses WHERE groupid = %s;", [groupChoice])
                        print("The training session was successfully cancelled.")
                    except:
                        print("An error occured.")

# return true if no date conflicts, return false if there is a conflict 
def trainerCheckConflict(trainerEmail, newDate):
    # check to make sure no classes or sessions already on that date
    cursor.execute("SELECT traineremail FROM trainingsessions WHERE traineremail = %s AND datebooked = %s", (trainerEmail, newDate))
    trainingRows = cursor.fetchall()

    cursor.execute("SELECT traineremail FROM groupclasses WHERE traineremail = %s AND datebooked = %s", (trainerEmail, newDate))
    groupRows = cursor.fetchall()

    if len(trainingRows) == 0 and len(groupRows) == 0:
        return True
    else:
        return False 

# return true if no date conflicts, return false if there is a conflict 
def memberCheckConflict(memberEmail, newDate):
    # check to make sure no classes or sessions already on that date
    cursor.execute("SELECT memberemail FROM trainingsessions WHERE memberemail = %s AND datebooked = %s", (memberEmail, newDate))
    trainingRows = cursor.fetchall()
    
    cursor.execute("SELECT memberemail FROM partakesin WHERE memberemail = %s AND groupid IN (SELECT groupid FROM groupclasses WHERE datebooked = %s)", (memberEmail, newDate))
    groupRows = cursor.fetchall()
    
    if len(trainingRows) == 0 and len(groupRows) == 0:
        return True
    else:
        return False

# get all rooms available on newDate
def getAvailableRooms(newDate):
    # retrieve all rooms that do not have a training session or group class on that date.
    cursor.execute("SELECT roomnumber FROM room WHERE (roomnumber NOT IN (SELECT roomnumber FROM TrainingSessions WHERE DateBooked = %s)) AND (roomnumber NOT IN (SELECT roomnumber FROM GroupClasses WHERE DateBooked = %s));", (newDate, newDate))
    roomRows = cursor.fetchall()
    availableRooms = []
    for roomRow in roomRows:
        availableRooms.append(roomRow[0])
    return availableRooms

# change the rooms of a group class or training session    
def roomBookingManagement():

    # print out the rooms
    allRooms = []
    cursor.execute("SELECT roomnumber FROM room")
    roomRows = cursor.fetchall()
    for row in roomRows:
        allRooms.append(row[0])
    print("Here are the rooms: " + str(allRooms))
    
    # select a room to manage 
    roomChoice = -1
    while (roomChoice not in allRooms and roomChoice != 0):
        roomChoice = int(input("Please enter an integer indicating the room you would like to manage, or 0 to go back: "))
    
    if roomChoice != 0:
        print("Here are the dates of all the training sessions that will be using this room: ")
        trainingList = ["0"];
        cursor.execute("SELECT datebooked FROM trainingsessions WHERE roomnumber = %s", [roomChoice])
        trainingRows = cursor.fetchall()
        for row in trainingRows:
            print(row[0])
            trainingList.append(str(row[0]))
        
        print("Here are the dates of all the group classes that will be using this room: ")
        groupList = ["0"];
        cursor.execute("SELECT datebooked FROM groupclasses WHERE roomnumber = %s", [roomChoice])
        groupRows = cursor.fetchall()
        for row in groupRows:
            print(row[0])
            groupList.append(str(row[0]))        
        
        print("If you would like to free up this room on a particular date, you can assign a different room to a training session or group class.")
        
        # enter a date  
        bookDate = 0
        while (bookDate not in trainingList and bookDate not in groupList) and bookDate != "0":
            bookDate = input("Please enter the date you would like this room to be free on (YYYY-MM-DD), or 0 to go back: ")
        
        if bookDate != "0":
            availableRooms = getAvailableRooms(bookDate)
            if len(availableRooms) == 0:
                print("Sorry, but no other rooms are available on this date. You must cancel this session or class to free up the room.")
                deleteChoice = input("Enter 1 to cancel the session or class. Enter anything else to go back to the previous menu: ")
                if deleteChoice == 1:
                    # cancel a training session 
                    if bookDate in trainingList:
                        try:
                            cursor.execute("DELETE FROM trainingsessions WHERE roomnumber = %s AND datebooked = %s;", [roomChoice, bookDate])
                            print("The training session has successfully been cancelled. Room #" + str(roomChoice) + " has been freed up for " + bookDate + ".")
                        except:
                            print("An error occured.")
                    
                    # cancel a group class 
                    else:
                        try:
                            # find the ID of the group class, and delete everything related to it
                            cursor.execute("SELECT groupid FROM groupclasses WHERE roomnumber = %s AND datebooked = %s;", [roomChoice, bookDate])
                            deleteID = cursor.fetchall()[0][0]
                            cursor.execute("DELETE FROM partakesin WHERE groupid = %s;", [deleteID])
                            cursor.execute("DELETE FROM groupclasses WHERE groupid = %s;", [deleteID])
                        except:
                            print("An error occured.")
            else:
                # get choice of room from user 
                newRoom = -1
                while (newRoom not in availableRooms and newRoom != 0):
                    newRoom = int(input("Enter an integer representing one of the available rooms - "+ str(availableRooms) + ", or 0 to go back: "))
                
                if newRoom != 0:
                    try:
                        # update the training session to have a new room 
                        if bookDate in trainingList:
                            cursor.execute("UPDATE trainingsessions SET roomnumber = %s WHERE roomnumber = %s AND datebooked = %s;", [newRoom, roomChoice, bookDate])
                            print("A different room was successfully assigned to the training session. Room #" + str(roomChoice) + " has been freed up for " + bookDate + ".")
                        
                        # update the group class to have a new room 
                        else:
                            cursor.execute("UPDATE groupclasses SET roomnumber = %s WHERE roomnumber = %s AND datebooked = %s;", [newRoom, roomChoice, bookDate]) 
                            print("A different room was successfully assigned to the group class. Room #" + str(roomChoice) + " has been freed up for " + bookDate + ".")
                    except:
                        print("An error occured.")

# an admin can create, cancel, or update a bill                         
def billingAndPaymentProcessing():
    choice = -1
    
    print("Enter an integer to select an option: ")
    print("\t1: Create a bill")
    print("\t2: Cancel a bill")
    print("\t3: Update a bill")
    print("\t0: Go back to previous menu")
        
    while (choice < 0 or choice > 3):
        choice = int(input("Enter here: "))
    
    match choice:
        # create a new bill 
        case 1:
            print("Note that all bills created will automatically be charged to the member's saved payment method on file.")
            newAmount = int(input("Enter the amount of the new bill in dollars: "))
            newMember = input("Enter the email of the member this bill will be automatically charged to: ")
            newDate = input("Please enter the date the member will be charged at in a YYYY-MM-DD format: ")
            try:
                cursor.execute("INSERT INTO bill (amount, memberemail, datepaid) VALUES (%s, %s, %s);", (newAmount, newMember, newDate))
                print("The bill was successfully created.")
            except:
                print("An error occured. Please double check that you entered an integer and that your date is in the correct format.")
        
        # cancel a bill 
        case 2:
            billChoice = getBillChoice("cancel")
            if billChoice != 0:
                try:
                    cursor.execute("DELETE FROM bill WHERE transactionid = %s", [billChoice])
                    print("The bill was successfully cancelled.")
                except:
                    print("an error occured.")
        
        # update the information for a bill 
        case 3:
            billChoice = getBillChoice("update")
            if billChoice != 0:
                fieldChoice = -1
                print("Enter an integer representing the field you would like to change: ")
                print("\t1: Amount in dollars")
                print("\t2: Member who paid")
                print("\t3: Date of payment")
                print("\t0: Go back to previous menu")
                
                while fieldChoice < 0 or fieldChoice > 3:
                    fieldChoice = int(input("Enter here: "))
                
                match fieldChoice:
                    case 1:
                        try:
                            newAmount = int(input("Enter the new amount in dollars: "))
                            cursor.execute("UPDATE bill SET amount = %s WHERE transactionid = %s;", [newAmount, billChoice])
                            print("Successfully updated the bill.")
                        except:
                            print("An error occured. Maybe you didn't enter an integer?")
                    case 2:
                        newMember = input("Please enter the email of the new member who paid: ")
                        try:
                            cursor.execute("UPDATE bill SET memberemail = %s WHERE transactionid = %s;", [newMember, billChoice])
                            print("Successfully updated the bill.")
                        except:
                            print("An error occured.")
                    case 3:
                        newDate = input("Please enter the new date of payment in a YYYY-MM-DD format: ")
                        try:
                            cursor.execute("UPDATE bill SET datepaid = %s WHERE transactionid = %s;", [newDate, billChoice])
                            print("Successfully updated the bill.")
                        except:
                            print("An error occured. Maybe your date format is incorrect.")

# print out the bills in the database and get the user to pick one 
def getBillChoice(action):
    billChoice = -1
    allBills = [0]
    print("\nHere are all the bills in the system:")
    cursor.execute("SELECT transactionid, amount, datepaid, firstname, lastname FROM bill NATURAL INNER JOIN clubmember ORDER BY transactionid")
    billRows = cursor.fetchall()
    for row in billRows:
        allBills.append(int(row[0]))
        print("\t" + str(row[0]) + ": $" + str(row[1]) + " paid on " + str(row[2]) + " from " + row[3] + " " + row[4])
    print("\t0: go back to previous menu")
    
    while billChoice not in allBills:
        billChoice = int(input("Enter an integer representing the bill to " + action + ": "))
        
    return billChoice
    
main()
