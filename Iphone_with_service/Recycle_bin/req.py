import requests 
from requests import *


session = requests.Session()
#http://192.168.86.199/addData.html
parameters = {'title':'Illest','lat':'127.32','lng':'123.321','timeStamp':'12:59','status':'OK'}
r = session.post('http://192.168.86.199/addData.html', data = parameters)

# Reach out to the website
#response = requests.get('http://192.168.86.199/addData.html')

#if(response.status_code == 200):
#    print('Request was successful')
#    parameters = {'title':'Illest','lat':'127.32','lng':'123.321','timeStamp':'12:59','status':'OK'}
#    requests.post('http://192.168.86.199:80/addData.html', data = parameters)
#elif(response.status_code == 404):
#    print('Site not found')
#else:
#    print('Some error occured')
#    
