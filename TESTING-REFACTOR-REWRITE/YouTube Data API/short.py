
import json, httplib2

def shortenUrl(longUrl):
    API_KEY = "AIzaSyCMNKNNuCoLoL6ZtVJvZWUsUce-lMXLoqQ"
    apiUrl = 'https://www.googleapis.com/urlshortener/v1/url'
    headers = {"Content-type": "application/json"}
    data = {"longUrl": longUrl}
    h = httplib2.Http('.cache')
    try:
        headers, response = h.request(apiUrl, "POST", json.dumps(data), headers)
        output = json.loads(response)
        return(output['id'])
    except Exception, e:
        print "unexpected error %s" % e

longUrl = "www.time.com"
print(shortenUrl(longUrl))
