###Tor Router & Exit Node Monitoring - ArcSight Use Case 

####Data Sources
- http://128.31.0.34:9031/tor/status/all
- http://exitlist.torproject.org/exit-addresses
- http://exitlist.torproject.org/exit-addresses.new

####Installation & Python Environment Configuration
- curl -kL http://xrl.us/pythonbrewinstall | bash
- pythonbrew install 2.7.3
- Add following environment variable setting to ~/.bashrc
**[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc**
- . .bashrc
- pythonbrew use 2.7.3
- pip install -r requirements.txt
- python tor_get_current_router_nodes.py
- ps -ef | grep tor_get_current_router_nodes.py # You should observe the script running as a daemon process
- Script is configured to run every 24 hours

####Use Case Description
Harvest actively recorded Tor router and exit nodes. Tor anonymous routing services are often utilized by nefarious actors to conduct hacking operations against customers information systems infrastructure. Strategy is to daily update Active Lists within ArcSight SIEM in an effort to monitor and alert on any customer assets that may communicate with any known Tor router nodes. Additionally monitor and alert on any Tor Exit nodes that may communicate with the customer's information systems infrastructure.

####Collection & Processing Methodology 
- Harvest Tor router and exit node data from data sources monitoring and updating on said registration of Tor assets.

####Culled Attribute to ArcSight Mappings
**Python Object - ArcSight Schema Field - Description**
element - SourceAddress - None 

**ArcSight CEF Mappings - Assignment - Description if Any**
SourceAddress - Tor Router/Exit Node - None
- DeviceProduct => Tor Router Node/Tor Exit Node - None
- DeviceVendor => Tor Exit Node/Tor Router Node - None
- DeviceEventClassID => Exit Node/Router Node - None

####ArcSight Content Development
- Create Real Time Rule to populate Active List 
- Active List Composed of IPAddress - String
- String assignment should be DeviceEventClassID
- Create Real Time Rule to monitor outbound communications of customer assets with Tor Router Nodes 
- Create Real Time Rule to monitor inbound communications of customer assets SourceAddress

####Long Term Deployment 
- Implementation runs as a daemon process on system

####TODO
- None at this point in time
