#####Malc0de + Virustotal - ArcSight Use Case 

#####Data Sources 
- www.malc0de.com/rss
- www.virustotal.com

#####Use Case Description
The function of this use case is to locate CND threat indicators associated with malware samples collected by Malc0de, that have an Anti Virus detection rate of less than or equal to 15%. 
VirusTotal iterates over malware samples uploaded against the top 45 Anti Virus vendors with current signatures. Indicators culled from malware samples with low AV detection rate have a higher degree of model confidence. 

#####Collection & Processing Methodology 
- Cull indicators from malc0de - HTTP GET Request - Python XML parsing 
- Send MD5 hash to VirusTotal API to pull report data - HTTP REST Request to API - Return report as JSON Object. 
- Generate ArcSight CEF event for malware samples with AV detection rate of less than 15% 
- Scrape same VirusTotal report URL for C2 IP Address Indicators 
- 2 different types of CEF events are generated 
- CEF Exploit events are associated with the exploitation phase - exploit IP/FQDN 
- C2 Exploit events are associated with C2 indicators culled from the Behavioral section of the Virustotal report - VirusTotal detonated malware within a sandbox environment and collects UDP/TCP communications with IP/FQDN C2 assets. 
- CEF events are sent to an ArcSight CEF Smart Connector running on localhost - via a Python TCP syslog client

#####ArcSight Content Development 
- Data types that can be correlated against the VirusTotal data type - include any data types with IP/FQDN data focal points 
- Real Time Rule iterates and fires aginst the "VirusTotal Exploit" & "VirusTotal C2" events populating an active list 
- Simple use case would be to alert on any system within customer space communicating with observed IP/FQDN indicators 
- More complex correlation use cases can be created against other data types with IP/FQDN indicators - or other global use cases
- Additionally more complex use case would be to alert if any IP/FQDN has been observed in the past touching the customer infrastructure - Recidivism Use Case 

#####Long Term Deployment
- Implementation runs as a daemon process on system

#####TODO
- Include Logging facility 
- Email alerting if network communications fail 


