###Twitter Real Time Monitoring - ArcSight Use Case

####Data Source
- https://dev.twitter.com/docs/streaming-apis/streams/public

####Installation & Python Environment Configuration
- Twiter username and password 
- Google Developer API key => https://code.google.com/apis/console/
- Google Translate API - will cost $$$ - seems to be around $40 for every 2 million characters translated. 
Given a Tweet is limited to 141 characters, $40 expenditure will translate 14,184 Tweets. 
- curl -kL http://xrl.us/pythonbrewinstall | bash
- pythonbrew install 2.7.3
- Add following environment variable setting to ~/.bashrc
**[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc**
- . .bashrc
- pythonbrew use 2.7.3
- pip install -r requirements.txt
- wget https://google-api-python-client.googlecode.com/files/google-api-python-client-1.0.tar.gz
- gunzip < google-api-python-client-1.0.tar.gz | tar xvf -
- cd google-api-python-client-1.0
- python setup.py build
- python setup.py install
- python script_name.py **Note - There are 4 different scripts that can be daemonized**
- ps -ef | grep virustotal.py # You should observe the script running as a daemon process

####Twitter List Variable Settings
- Twitter ID's List Variable Settings => **follow_ids = [365235743, 739250522, 358381825, 336683669, 16589206]**
- Twitter Keywords List Variable Settings => **keywords = ["pastebin", "Russian hackers", "Chinese hackers", "hacker", "hackers", ""]**

####Use Case Description
The function of this ArcSight Use Case is to monitor Twitter data stream in real time via the Twitter Public Streams API interface. 
Four scripts are included. Two scripts provide tha capability to pass off any Tweets that are not in the source language of English to the Google Translate API. 
This provides the capability to monitor in real time foreign language Tweet's. Tweets are as stated translated by the Google Translate API. 

####Script Name & Function
- **twit_notrans_id.py** => Monitor Twitter Public Stream API via a List of Twitter ID's to be monitored - Google Translate is **NOT** Utilized 
- **twit_notrans_keyword.py** => Monitor Twitter Public Stream API via a List of Keywords to be monitored - Google Translate is **NOT** Utilized
- **twit_trans_id.py** => Monitor Twitter Twitter Public Stream API via a List of Twitter ID's to be monitored - Google Translate **IS** Utilized
- **twit_trans_keyword.py** => Monitor Twitter Public Stream API via a List of Keywords to be monitored - Google Translate is **IS** Utilized
- **twit_notrans_regex_id.py** => Regex Based Twitter Public Stream API via List of Twitter ID's, or monitor entire Twitter Stream Real in Real Time

####Collection & Processing Methodology 
- Twitter Streaming API - Real Time 
- https://dev.twitter.com/docs/streaming-apis

####Culled Attribute to ArcSight Mappings 
**Python Object - ArcSight Schema Field - Description**
- item['Ctime'] - EndTime - End Time of Twitter Tweet 
- item['Platform'] - RequestClientApplication - Application Platform Twitter End User Generated Tweet From
- item['TwitterID'] - SourceUserID - Twitter ID of end user that generated Tweet
- item['ScreenName'] - SourceUserName - Twitter UserName of end user that generated Tweet
- item['ProperName'] - SourcePriviledge - Twitter Proper Name utilized to register Twitter User Account 
- item['ReplyToID'] - DestinationUserID - Destination Twitter ID that Tweet is intended for
- item['ReplyToScreenName'] - DestinationUserName - Destination Twitter UserName Tweet is intended for
- item['SourceLang'] - DestinationPriviledge - Default Source Language Twitter User Configured to Utilize 
- item['Tweet'] - Message - Body of the Tweet Message
- cull_email - DeviceCustomString1 - Email Addresses culled from twitter regex implementation
- cull_phone - DeviceCustomString2 - Phone numbers culled from twitter regex implementation
- cull_ipaddress - DeviceCustomString3 - IP Addresses culled from twitter regex implementation  

**ArcSight Only CEF Mappings - Assignment - Description if Any**
- Name =>  WatchList
- DeviceProduct => Twitter 
- DeviceVendor => Twitter RealTime Stream
- DeviceEventClassID => Twitter Keyword/Twitter ID

####ArcSight Content Development
- Determined or driven by customer requirements 

####Long Term Deployment 
- Implementation runs as a daemon process on system

####TODO
- None at this point in time
 
