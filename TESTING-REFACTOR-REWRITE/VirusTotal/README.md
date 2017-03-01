###Malc0de + Virustotal - ArcSight Use Case
 
####Data Sources 
- malc0de.com/rss
- www.virustotal.com

####Installation & Python Environment Configuration
- curl -kL http://xrl.us/pythonbrewinstall | bash
- pythonbrew install 2.7.3
- Add following environment variable setting to ~/.bashrc
**[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc**
- . .bashrc
- pythonbrew use 2.7.3
- pip install -r requirements.txt
- python virustotal.py 
- ps -ef | grep virustotal.py # You should observe the script running as a daemon process

####Use Case Description
The function of this use case is to locate CND threat indicators associated with malware samples collected by Malc0de, that have an Anti Virus detection rate of less than or equal to 15%. Strategically one would infer that indicators culled from malware samples with low AV detection rate have a higher degree of model confidence. 
VirusTotal iterates over malware samples uploaded against the top 45 Anti Virus vendors with current signatures. Within the scope of this use case we pull indicator attribute information from both malc0de and VirusTotal for inclusion into ArcSight/SIEM based real time alerting use cases. Note we have observed in the past malc0de stumbling upon APT/1 indicators of interest, hence the strategic value of the indicator attribute information culled from the data sources. 

####Collection & Processing Methodology 
- Cull indicators from malc0de - HTTP GET Request - Python XML parsing 
- Send MD5 hash to VirusTotal API to pull report data - HTTP REST Request to API - Return report as JSON Object. 
- Generate ArcSight CEF event for malware samples with AV detection rate of less than 15% 
- Scrape same VirusTotal report URL for C2 IP Address Indicators 
- 2 different types of CEF events are generated 
- CEF Exploit events are associated with the exploitation phase - exploit IP/FQDN 
- C2 Exploit events are associated with C2 indicators culled from the Behavioral section of the Virustotal report - VirusTotal detonated malware within a sandbox environment and collects UDP/TCP communications with IP/FQDN C2 assets. 
- CEF events are sent to an ArcSight CEF Smart Connector running on localhost - via a Python TCP syslog client

####Culled Attribute to ArcSight Mappings 
**Python Object - ArcSight Schema Field - Description**
- analysis_date => EndTime => Date and Time malware sample was analized by VirusTotal
- request_url => RequestUrl => Malicious RequestUrl String
- ip_address => SourceAddress => Source IP Address of Malicious RequestUrl at Time www.malc0de.com collected the sample 
- c2_item => DestinationAddress => Destination IP Address for outbound C2 call back from the maleware as observered by VirusTotal when malware sample was detonated in their sandbox 
- asn => SourceHostName => Autonomous System Network number - aka the point of precense where the Exploit vector IP Address originated from 
- sha256_hash => DeviceCustomString1 => hash value from VirusTotal analysis of malware sample
- sha1_hash => DeviceCustomString2 => hash value from VirusTotal analysis of malware sample 
- md5_hash => DeviceCustomString3 => hash value from VirusTotal analysis of malware sample 
- file_size => FileSize => file size in bytes 
- file_name => FileID => file name of the malware sample 
- file_type => FileType => file type of malware as determined by VirusTotal Analysis 
- av_rate => DeviceCustomString4 => AV detection rate from malware iterated against top 45 AV vendors with current AV signatures at VirusTotal 
- vt_link => RequestClientApplication => VirusTotal Request URL to VirusTotal Report 

**ArcSight Only CEF Mappings - Assignment - Description if Any**
- Name => VirusTotal C2 => Only if C2 Attributes 
- Name => VirusTotal Exploit => Only if Exploit Attributes 
- DeviceProduct => VirusTotal 
- DeviceVendor => VirusTotal + Malc0de
- DeviceEventClassID => C2 => Only if C2 Attributes 
- DeviceEventClassID => Exploit => Only if Exploit Attributes 

####ArcSight Content Development 
- Data types that can be correlated against the VirusTotal data type - include any data types with IP/FQDN data focal points 
- Two Real Time Rules iterate and fire aginst the "VirusTotal Exploit" & "VirusTotal C2" events populating two Active Lists 
- Active List #1 => 24 hour aged Active List of Exploit IP/FQD/Hash/Filename attribute information
- Active List #2 => 90 day aged Active List of C2 IP/FQDN indicators - note method needs to be completed to cull FQDN C2 indicators - strategically C2 indicators are utilized longer by actors
- Simple use case would be to alert on any system within customer space communicating with observed culled indicator IP/FQDN's 
- More complex correlation use cases can be created against other data types with IP/FQDN indicators - or other global use cases
- Additionally more complex use case would be to alert if any IP/FQDN has been observed in the past touching the customer infrastructure - Recidivism Use Case 

####Long Term Deployment
- Implementation runs as a daemon process on system

####TODO
- regex method to cull C2 FQDN indicators 
- Include Logging facility 
- Email alerting if network communications fail 
