from bs4 import BeautifulSoup


with open('index.html', 'r') as file:
    data = file.read()
    

soup = BeautifulSoup(data, 'html.parser')

divs = soup.select('div')
print(divs[0].get_text())

div_2 = divs[1]

paras = div_2.select('p')
print('Paras:')
for p in paras:
    print(p.get_text())
    
    
dailies = soup.select('.daily')
print('Dailies:')
for d in dailies:
    print(d.get_text())
    

print(dailies[-1].attrs['id'])

