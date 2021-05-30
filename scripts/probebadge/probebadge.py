from PIL import Image, ImageFont, ImageDraw
import requests
try:
    import requests_cache
except ImportError:
    from requests_toolbelt import requests_cache
import html2text
from bs4 import BeautifulSoup
import re
import os
import sys


# set headers
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

h = html2text.HTML2Text()
h.ignore_links = True

# init counters
hours  = 0
days   = 0
weeks  = 0
months = 0
years  = 0

output = ''
scriptPath = os.path.dirname(__file__)

# cache requests to prevent Shenanigans
requests_cache.install_cache('sa_cache', backend='sqlite', expire_after=21600)

# query leper's colony
try:
    horribleJerk = int(sys.argv[1])
except ValueError:
    print("UserIDs can only be integers.")
    quit()
URL = f"https://forums.somethingawful.com/banlist.php?userid={horribleJerk}"
page = requests.get(URL, headers)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

username = str(soup.find('a', href=f'/member.php?s=&action=getinfo&userid={horribleJerk}').get_text())

# find probations
probes = re.findall(r'User loses posting privileges for (.*?)\.', soup.prettify())
#print(probes)

# YES YES I KNOW IM GOING TO TIDY THIS WHEN I KNOW IT WORKS
for probe in probes:
    timesplit = probe.split(' ')
    timesplit[0] = re.sub('[^0-9]','',timesplit[0])
    if timesplit[1] == 'hours':
        hours += int(timesplit[0])
    elif timesplit[1][0:3] == 'day':
        days += int(timesplit[0])
    elif timesplit[1][0:4] == 'week':
        weeks += int(timesplit[0])
    elif timesplit[1][0:5] == 'month':
        months += int(timesplit[0])
    elif timesplit[1][0:4] == 'year':
        years += int(timesplit[0])

# boring, frustrating math shit
calcHours = int(hours % 24)
calcDays = int((hours - calcHours) / 24)
calcWeeks = int((calcDays - (calcDays % 7)) / 7)
calcDays = int(calcDays % 7)
calcMonths = int((calcWeeks - (calcWeeks % 4)) / 4)
calcWeeks = int(calcWeeks % 4)
calcYears = int((calcMonths - (calcMonths % 12)) / 12)
calcMonths = int(calcMonths % 12)

print(f'\nHours: {calcHours}\nDays: {calcDays}\nWeeks: {calcWeeks}\nMonths: {calcMonths}\nYears: {calcYears}')
#print(h.handle(page))

# figure out what to stick on the badge
probeTimes = [(str(calcYears) + ' Years'),(str(calcMonths) + ' Months'),(str(calcWeeks) + ' Weeks'),(str(calcDays) + ' Days'),(str(calcHours) + ' Hours')]
for sentence in probeTimes:
    if int(re.sub('[^0-9]','',sentence)) > 0:
        if output != '':
            output += f', {str(sentence)}'
        else:
            output += str(sentence)

uNameFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 16)
timeFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 12)
noteFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 8)

img = Image.open(f'{scriptPath}/badgebg_simple.png')

image_editable = ImageDraw.Draw(img)
image_editable.text((100,15), username, (0,0,0), font=uNameFont)
image_editable.text((100,35), 'Total time probated*:', (0,0,0), font=timeFont)
image_editable.text((100,50), output, (0,0,0), font=timeFont)
if calcYears > 1:
    image_editable.text((100,62), 'Jesus Christ.', (0,0,0), font=timeFont)

image_editable.text((275,80), '*only counts last 50 probes', (150,150,150), font=timeFont)

img.save(f'{scriptPath}/probebadge.png')
