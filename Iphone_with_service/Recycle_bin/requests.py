import requests 


# Reach out to the website
response = requests.get('http://192.168.86.199:80/addData.html')

if(response.status_code == 200):
    print('Request was successful')
    parameters = {'title':'Trip1','lat':'127.32','lng':'123.321','timeStamp':'12:59','status':''}
    requests.post('http://192.168.86.199:80/addData.html', data = parameters)
elif(response.status_code == 404):
    print('Site not found')
else:
    print('Some error occured')
    