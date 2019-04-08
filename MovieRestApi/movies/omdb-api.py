import requests as r
# http://www.omdbapi.com/?t=Predator&apikey=120e2295

api_key = '120e2295'
url = 'http://www.omdbapi.com/?t=Predator&apikey=%s' % api_key
print(url)
response = r.get(url)
if response.status_code == '200':
    print('OK')
else:
    print('Not OK')

data = response.json()
print(data)
