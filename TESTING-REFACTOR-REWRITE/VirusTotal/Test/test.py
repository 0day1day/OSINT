import requests
from bs4 import BeautifulSoup

request_Url = "https://www.virustotal.com/file/30f77c3a0a9b2ddf48c52c39d382039f3cc991800599d39208514bb3f5e31bfa/analysis/1355020755/"
r = requests.get(request_Url)
if r.status_code == 200:
    soup = BeautifulSoup(r.text)
    rows = soup.findAll("pre")
    #print(soup)
    for row in rows:
        element = row.findAll("pre")
        print(element)
#        element_rend = ["".join(x.renderContents().strip(':')) for x in element]
#        keys = element_rend[0::2]
#        values = element_rend[1::2]
#        element_dict = dict(zip(keys, values))
#        detection_ratio = (float(int(element_dict['Detection ratio'][0]))/46.0) * 100
#        detection_ratio_two = '%.2f' % detection_ratio + "%"
#        print(keys)
#        print(element_dict['Analysis date'].strip('\n ')[0:19], element_dict['SHA256'], element_dict['SHA1'], element_dict['MD5'], element_dict['File size'][0:9].strip(' '),
#            element_dict['File name'], element_dict['File type'], detection_ratio_two)

