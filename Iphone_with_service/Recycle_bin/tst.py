
import mechanize

br = mechanize.Browser()
br.open('http://project-found.com')

response = br.response()
print (response.geturl()) # URL of the page we just opened
print (response.info()) # headers
print (response.read()) # body

br.select_form('myform')

br.form['title'] = 'trip1'
br.form['lat'] = '123'
br.form['lng'] = '312'
br.form['timeStamp'] = '1593815506'
br.form['txt'] = 'WOOOOORK'

br.submit()