import sys
import json
import httplib2
import Tkinter

#Functions for  
def get(url):
    resp, xml = h.request(
        url,
        method = "GET",
        headers = {'Content-Type' : 'application/json'}
        )
    return xml
def put(url, body):
    resp, content = h.request(
        url, 
        method = "PUT",
        body = body,
        headers = {'Content-Type' : 'application/json', 'Accept':'application/json'}
        )
    return resp, content
def delete(url):
    resp, content = h.request(
        url,
        method = "DELETE"
        )
    return resp

def get_active_hosts():
    resp, content = h.request(sdSalUrl + 'hosttracker/default/hosts/active/', "GET")
    hostConfig = json.loads(content)
    hosts = hostConfig['hostConfig']
    return hosts

def drop_switch():
    drop_body =  {
        "flow": [
            {
                "id": "3",
                "instructions": {
                    "instruction": [
                        {
                            "apply-actions": {
                                "action": [
                                    {
                                        "drop-action": {},
                                        "order": "1"
                                    }
                                ]
                            },
                            "order": "1"
                        }
                    ]
                },
                "flags": "SEND_FLOW_REM",
                "flow-name": "foo3",
                "installHw": "false",
                "barrier": "false",
                "strict": "false",
                "priority": "50",
                "idle-timeout": "0",
                "hard-timeout": "0",
                "cookie": "45",
                "table_id": "0"
            }
        ]
    }
    json_val = json.dumps(drop_body)
    print put(findFlow+'flow/3', json_val)    
    
   

#Base URLs for Config and operational
baseUrl = 'http://127.0.0.1:8181'
confUrl = baseUrl + '/restconf/config/'
operUrl = baseUrl + '/restconf/operational/'

#"Old" REST APIs that still are used
sdSalUrl = baseUrl + '/controller/nb/v2/'

#Specific REST URLs
findNodes = operUrl + '/opendaylight-inventory:nodes/'
findTopo = operUrl + '/network-topology:network-topology/'
findNodeConnector = operUrl + '/opendaylight-inventory:nodes/node/node-connector/'
findTopology = operUrl + '/network-topology:network-topology/topology/flow:1/'
findFlow = confUrl +'/opendaylight-inventory:nodes/node/openflow:1/table/0/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

print get(findFlow)
top = Tkinter.Tk()
top.configure(width=1000, height=1000)

B =[Tkinter.Button(top, text="Drop1", command = drop_switch, width = 8, height = 8),Tkinter.Button(top, text="Drop2", command = drop_switch, width = 8, height = 8)]




B[0].pack()
B[1].pack()

top.mainloop()
