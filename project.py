import subprocess
import os
import time
import datetime
import smtplib
import getpass
import os.path
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

admin_log = r"C:\Users\Public\admin_log.json"
host_log = r"C:\Users\Public\host_log.json"
time_log = r"C:\Users\Public\time_log.txt"
result_log = r"C:\Users\Public\results.txt"

raw_data={}
if os.path.exists(admin_log) == False:
    with open(host_log , "w") as log:
        json.dump(raw_data,log)
    with open(admin_log,"w") as file:
        json.dump(raw_data,file)

with open(host_log,"r") as log: #loading files
    hostInfo=json.load(log)
with open(admin_log,"r") as file:
    info=json.load(file)

def Ping_testing(name,server_ip):   #pinging function/Will ping a specific ip address
    response = os.system("ping -c 1 " + server_ip)
    if response == 0:
        print( name , " is active " )
        return 0
    else:
        print( name , " needs Attention" )
        return 1

def Get_UserData(): # gets all data and then returns it as a combined string
    name=input("Enter login User Name : ")
    password=str(getpass.getpass("Enter login password : "))
    profile=str(name+","+str(password))
    return profile

def Time_feed(choice,menu): #function to store time and choice at a given point of program
    timeNow=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timeNow=timeNow+","+menu+","+choice+"\n"
    file=open(time_log,"a+")
    file.write(timeNow)
    file.close()

def Send_it():  #function to send email
    fromaddr = input("Enter your email(gmail) address : ")
    password=getpass.getpass("Enter your gmail password : ")
    toaddr = fromaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Text file"
    body = "Attached is a file regarding results of pinging the host"
    msg.attach(MIMEText(body, 'plain'))
    filename = "results.txt"
    attachment = open(filename, "rt")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def Time_Display():
    file=open(time_log,"r")
    for line in file:
        line.rstrip('\n')
        timeNow , menu , choice = line.split(',')
        temp = list(choice)
        temp.remove('\n')
        choice = ''.join(temp)
        if menu=='M':
            print("Menu : {}  | choice : {} | Time : {}".format("Main Menu",choice,timeNow))
        elif menu=="A":
            print("Menu : {} | choice : {} | Time : {}".format("Admin Menu",choice,timeNow))
        else:
            print("Menu : {}  | choice : {} | Time : {}".format("Host Menu",choice,timeNow))
    print()
    file.close()

def Main_menu():
    while(1):
        print("1. Admin Options")
        print("2. Host Options")
        print("3. Display Time log")
        print("4. Exit")
        choice=input("Enter Your choice : ")
        Time_feed(choice,'M')
        if choice=='1':
            Admin_Menu()
        elif choice=='2':
            Host_menu()
        elif choice=='3':
            Time_Display()
        else:
            with open(host_log , "w") as log:
                json.dump(hostInfo,log)
            with open(admin_log,"w") as file:
                json.dump(info,file)
            os._exit(1)

def Admin_Menu():
    while 1:
        print("1. Add New User")
        print("2. Delete User")
        print("3. Change password")
        print("4. Print names of all users")
        print("5. Previous Menu")
        print("6. Exit")
        choice=input("Enter choice : ")
        Time_feed(choice,'A')
        if choice=='1':
            str=Get_UserData()
            name,password=str.split(",")
            if name in info and password==info.get(name):
                new_User=input("Enter New Username : ")
                newPassword=getpass.getpass("Enter Password : ")
                newProfile={new_User:newPassword}
                info.update(newProfile)
            else:
                print("Wrong username or password")
        elif choice=='2':
            profile=Get_UserData()
            name,password=profile.split(",")
            if name in info and password==info.get(name):
                print("User which Needs to be deleted")
                profile=Get_UserData()
                name,password=profile.split(",")
                if len(info)>1:
                    if name in info and password==info.get(name):
                        del info[name]
                        print("User deleted.")
                    else:
                        print("User not found")
                else:
                    print("This is the last user can't remove this user")
        elif choice=='3':
            profile=Get_UserData()
            name,password=profile.split(",")
            if name in info and password==info.get(name):
                del info[name]
                password=getpass.getpass("Enter New password")
                profile={name:password}
                info.update(profile)
            else:
                print("No such user exist")
        elif choice=='4':
            for name in info:
                print(name)
        elif choice=='5':
            Main_menu()
        else:
            with open(host_log , "w") as log:
                json.dump(hostInfo,log)
            with open(admin_log,"w") as file:
                json.dump(info,file)
            os._exit(1)

def Host_menu():
    while 1:
        print("1. Enter new host")
        print("2. Delete a host")
        print("3. Ping a host")
        print("4. Ping all hosts")
        print("5. Print all hosts")
        print("6. Previous Menu")
        print("7. Exit")
        choice=input("Enter your choice : ")
        Time_feed(choice,'H')
        if choice=='1':
            name=input("Enter name of host : ")
            ip_add=input("Enter IP address of the host : ")
            newHost={name:ip_add}
            hostInfo.update(newHost)
        elif choice=='2':
            name=input("Enter name of host :")
            if name in hostInfo:
                del hostInfo[name]
                print("Host removed")
            else:
                print("No such host exists")
        elif choice=='3':
            print("1. Ping by name")
            print("2. Ping by IP Address")
            choice=input("Enter choice : ")
            if choice=='1':
                name=input("Enter name of host : ")
                if name in hostInfo:
                    Ping_testing(name,hostInfo[name])
                else:
                    print("No such host exists")
            else:
                ip_add=input("Enter IP address of the host : ")
                Ping_testing("IP address : ",ip_add)
        elif choice=='4':
            file=open(result_log,"w+")
            for name in hostInfo:
                res=Ping_testing(name,hostInfo[name])
                if res==0:
                    result=str(name)+" is ok\n"
                else:
                    result=str(name)+" is not ok\n"
                file.write(result)
            file.close()
            userInput=input("Do you wish to get these results in your email account (y/n) :")
            if userInput=='y' or userInput=='Y':
                name=input("Enter your login username : ")
                password=getpass.getpass("Enter your password : ")
                if name in info and password == info.get(name):
                    Send_it()
                else:
                    print("Wrong password or username")
            file.close()
        elif choice=='5':
            for name in hostInfo:
                print(name,"\t",hostInfo[name])
        elif choice=='6':
            Main_menu()
        elif choice=='7':
            with open(host_log , "w") as log:
                json.dump(hostInfo,log)
            with open(admin_log,"w") as file:
                json.dump(info,file)
            os._exit(1)

def main():
    for i in range(5):
        profile=Get_UserData()
        name,password=profile.split(",")
        if len(info) == 0:
            profile={name:password}
            info.update(profile)
            Main_menu()
            i=-1
        if name in info and password==info.get(name):
            Main_menu()
            i=-1
        else:
            print("sorry wrong user name or password")
            print("You have {} chances left before getting locked out.".format(4-i))
        i=i+1
    if i!=-1:
        print("You have been locked out for 10 mins")
        time.sleep(600)

main()
