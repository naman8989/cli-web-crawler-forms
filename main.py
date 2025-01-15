import requests

while input("Enter 'f' to halt the program -: ") != 'f': # Enter f for half the progarm rest to continue
    url = input("Enter the URL -: ")  # Enter the url
    req = requests.get(url) 
    print(req.status_code)
    if req.status_code != 200:
        print(f"URL not found | status code - {req.status_code}")  # Checking the status code of the url request
        continue
    
    print("Enter your credentials ----> ") 
    user = input("Enter the UserName: ")  # Enter the UserName credentials
    password = input("Enter the password: ")  # Enter the Passworkd credentials
    print(f"Your userName: {user} , password: {password}")
    
    
