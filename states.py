import requests, bs4
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

res = requests.get('https://www.citypopulation.de/USA.html#places')
mainWebsite = 'https://www.citypopulation.de/'
soup = bs4.BeautifulSoup(res.text, "html.parser")

stateTags = soup.select('div.col > h2')
head = ET.Element('USA')

for stateTag in stateTags:
	stateName = stateTag.string
	print(stateName)
	placesSibling = stateTag.find_next_sibling()
	placesLink = mainWebsite + placesSibling.select('li a')[0]['href']
	
	
	
	res = requests.get(placesLink)
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	statePopTag = soup.select_one('#adminareas td.prio2')
	statePop = str(statePopTag.string).replace(',','')
	
	stateElement = ET.SubElement(head, 'state', {'name':stateName, 'population':statePop})
	
	cityRowTags = soup.select('section#citysection tbody tr')
	
	for cityRowTag in cityRowTags:
		cityName = str(cityRowTag.select_one('span[itemprop="name"]').string)
		print('\t' + cityName)
		cityPopulation = str(cityRowTag.select_one('td.prio2').string).replace(',','')
		cityAttrs = {'name':cityName, 'population':cityPopulation}
		cityElement = ET.SubElement(stateElement, 'city', cityAttrs)

f = open('cities.xml', 'w+')
xml = parseString(ET.tostring(head).decode())
f.write(xml.toprettyxml())
f.close()
		
