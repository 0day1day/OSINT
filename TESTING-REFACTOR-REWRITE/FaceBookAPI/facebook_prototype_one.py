"""
Facebook GraphAPI JSON Datastructure Global Keys
about
category
company_overview
cover
id
is_published
likes
link
name
picture
talking_about_count
username
website
"""

import requests, json


def print_facebook_global_keys(search_url):
    request_urlGet = requests.get(search_url)
    if '200' in str(request_urlGet.status_code):
        data = json.loads(request_urlGet.text)
        data_list = data
        element_list = []
        for element in data_list:
            element_list.append(element)
            element_list.sort()
        for item in element_list:
            print(item)
        print(data)

"""
TODO

http://developers.facebook.com/tools/explorer?method=GET&path=me

{
  "id": "100003343741034",
  "name": "Peng Yinan",
  "first_name": "Peng",
  "last_name": "Yinan",
  "link": "http://www.facebook.com/peng.yinan",
  "username": "peng.yinan",
  "birthday": "02/02/1973",
  "gender": "male",
  "email": "coolswallow0@gmail.com",
  "timezone": -4,
  "locale": "en_US",
  "updated_time": "2012-05-22T14:02:53+0000"
}
"""

def pull_user_attributes():
    pass


# Define Main Execution
def main():
    facebook_id = '19292868552'
    search_url = 'http://graph.facebook.com/' + facebook_id
    print_facebook_global_keys(search_url)

# Main Execution
if __name__ == '__main__':
    main()
