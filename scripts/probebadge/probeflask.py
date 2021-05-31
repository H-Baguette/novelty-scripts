try:
    import flask
except (ImportError, ModuleNotFoundError):
    from site_packages import flask
from PIL import Image, ImageFont, ImageDraw
import requests
try:
    import requests_cache
except ImportError:
    from site_packages import requests_cache
import html2text
from bs4 import BeautifulSoup
import datetime as dt
import humanize
import re
import os
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

ids = {'userid': 0}
scriptPath = os.path.dirname(__file__)

def generateBadge(userid):
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
    phours  = 0
    pdays   = 0
    pweeks  = 0
    pmonths = 0
    pyears  = 0

    username = 'A Goody Two-Shoes'
    output = ''
    print(scriptPath)
    print(f'{scriptPath}test')

    # cache requests to prevent Shenanigans
    requests_cache.install_cache('sa_cache', backend='sqlite', expire_after=21600)

    # query leper's colony
    try:
        horribleJerk = userid
    except ValueError:
        print("UserIDs can only be integers.")
        return
    print(f'{scriptPath}/badges/{horribleJerk}.png')
    pageNum = 1
    probes=[]
    endOfSheet = False
    while endOfSheet != True:
        URL = f"https://forums.somethingawful.com/banlist.php?&sort=&asc=0&adminid=&ban_month=0&ban_year=0&actfilt=-1&userid={horribleJerk}&pagenumber={str(pageNum)}"
        page = requests.get(URL, headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        
        if re.findall(r'User loses posting privileges for (.*?)\.', soup.prettify()) == []:
            endOfSheet = True
            break

        username = str(soup.find('a', href=f'/member.php?s=&action=getinfo&userid={horribleJerk}').get_text())

        # find probations
        probeScrape = re.findall(r'User loses posting privileges for (.*?)\.', soup.prettify())
        probes += probeScrape
        pageNum += 1
    #print(probes)

    # YES YES I KNOW IM GOING TO TIDY THIS WHEN I KNOW IT WORKS
    for probe in probes:
        timesplit = probe.split(' ')
        timesplit[0] = re.sub('[^0-9]','',timesplit[0])
        if timesplit[1] == 'hours':
            phours += int(timesplit[0])
        elif timesplit[1][0:3] == 'day':
            pdays += int(timesplit[0])
        elif timesplit[1][0:4] == 'week':
            pweeks += int(timesplit[0])
        elif timesplit[1][0:5] == 'month':
            pmonths += int(timesplit[0])
        elif timesplit[1][0:4] == 'year':
            pyears += int(timesplit[0])
    
    output = humanize.naturaldelta(dt.timedelta(hours=phours,days=(pdays + (365 * pyears)),weeks=(pweeks + (4 * pmonths))))

    
    if output == '':
        output = 'This SQUARE hasn\'t been probated before.'

    uNameFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 16)
    timeFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 12)
    noteFont = ImageFont.truetype(f"{scriptPath}/F25_Bank_Printer.ttf", 8)

    img = Image.open(f'{scriptPath}/badgebg_simple.png')

    image_editable = ImageDraw.Draw(img)
    image_editable.text((100,15), username, (0,0,0), font=uNameFont)
    image_editable.text((100,35), 'Total time probated:', (0,0,0), font=timeFont)
    image_editable.text((100,50), output, (0,0,0), font=timeFont)
    #if calcYears > 1:
    #    image_editable.text((100,62), 'Jesus Christ.', (0,0,0), font=timeFont)

    #image_editable.text((275,80), '*only counts last 50 probes', (150,150,150), font=timeFont)

    img.save(f'{scriptPath}/badges/{horribleJerk}.png')
    print(f'{scriptPath}/badges/{horribleJerk}.png')
    return flask.send_file(f'badges/{horribleJerk}.png', mimetype='image/png')
    #return f'<img src="{scriptPath}\\badges\\{horribleJerk}.png">'


@app.route('/', methods=['GET'])
def home():
    return '<html><body style="background-image:url(\'https://anlucas.neocities.org/compspin_e0.gif\');background-size:cover;"><p style="color:white;">User ID here idiot (NOT your username):</p><form action="https://sa-probebadge.herokuapp.com/api/probebadge" method="GET"><input type="text" name="userid"/><input type="submit"/></form><p style="color:white;"><b>MAKE SURE YOU WRAP THE URL YOU\'RE GIVEN IN [IMG] TAGS!</b></p></body><html>'
 
@app.route('/api/probebadge', methods=['POST', 'GET'])
def api_genbadge():
    try:
        if 'userid' not in flask.request.args:
            return "No UserID provided. Get better at computers, loser."
        else:
            return (generateBadge(int(flask.request.args['userid']))), 201, {'Access-Control-Max-Age': '3600'}
    except (ValueError, AttributeError):
        return '<center><h1>Invalid UserID</h1><p>You <i>did</i> enter your UserID, and not your username, <i>right?</i></p><br/><img src="https://i.imgur.com/l0wWcPl.png"></center>'
 
app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
