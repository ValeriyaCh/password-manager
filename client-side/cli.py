from helpers import register, update_creds, request_data
import sys


EXIT = 'q'
REGISTER = '-r'
UPDATE_CREDS = '-u'
SHOW = '-s'
UNKNOWN_COMMAND = 'This command is not recognized'

def check_quit(user_input):
    if user_input == EXIT:
        sys.exit()
        
def print_instructions():
    print("Choose the option:")
    print("-r to register")
    print("-u to update/add new credentials")
    print("-s to show all passwords")

print("Welcome to Password Manager")
print_instructions()
option = input()
check_quit(option)
username = input("Enter username:").strip()
check_quit(username)
password = input("Enter  master password:").strip()
check_quit(password)
while(1):
    if option == REGISTER:
        rsp = register(username=username, password=password)
        print(rsp)
    elif option == UPDATE_CREDS:
        url = input("Enter url:")
        check_quit(url)
        url_username = input("Enter username to url:").strip()
        check_quit(url_username)
        url_password = input("Enter password to url:").strip()
        check_quit(url_password)
        update_creds(username, password, url, url_username, url_password)
    elif option == SHOW:
        print(request_data(username=username, password=password))
    else:
        print(UNKNOWN_COMMAND)
    print_instructions()
    option = input()
    check_quit(option)
