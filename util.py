import sqlite3
import traceback
import sys
import time
import traceback
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
import sys
from ncclient import manager
from ncclient.operations import RPCError
import xmltodict
from pprint import pprint as pp
import json
from genie import parsergen
from pprint import pprint as pp
from textfsm import TextFSM
import requests
import mtl
import jinja2
import yaml
import warnings
warnings.filterwarnings("ignore")
print("Ignoring warnings for educational purposes... normally a bad idea!")


#important for robot framework
import pdb
#robot framework controls stdout - you can grab it back for debugging via...
#use : pdb.Pdb(stdout=sys.__stdout__).set_trace()

debug = False
def getcreds(userid , dbname):

    try:
        con = sqlite3.connect(dbname)

        with con:
            # 'row_factory' - allows dictionary based column access by name 'columname' instead of just number
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            sqlquery = "SELECT * FROM ucreds where id = " + str(userid)

            cur.execute(sqlquery)
            row = cur.fetchone()

            try:
                #pdb.Pdb(stdout=sys.__stdout__).set_trace()
                if debug:
                    print("Auth using : " + row['username'])
                    # ipdb.set_trace()
                return row['username'], row['password']
            except:
                print("unable to find userid in database:  " + dbname)
                return '::unkown::'

    # ipdb.set_trace()
    except Exception:
        print('Exit due to Error:', sys.exc_info()[1])
        if debug:
            print('Trace info:')
            print(traceback.format_exc())
        sys.exit()

        # End of getcreds

def getTimeStamp():
    # this routine creates a string timestamp usefull for filenames and other naming
    tmonth = time.localtime().tm_mon
    tday = time.localtime().tm_mday
    # strmonth = ""
    # strday = ""
    stryear = str(time.localtime().tm_year)
    if tmonth < 10:
        strmonth = "0" + str(time.localtime().tm_mon)
    else:
        strmonth = str(time.localtime().tm_mon)

    if tday < 10:
        strday = "0" + str(time.localtime().tm_mday)
    else:
        strday = str(time.localtime().tm_mday)

    tstamp = strmonth + "-" + strday + "-" + stryear + "-" + str(time.time())
    return tstamp

dbname="cmdb.sqlite"

def getCLIOutput(cmd,ip,uid, devtype, quiet = False):
    #pdb.Pdb(stdout=sys.__stdout__).set_trace()
    runcmd = cmd.strip()
    try:
        username, password = getcreds(uid, dbname)

        dut = {'device_type': str(devtype), 'ip': str(ip),'username': str(username), 'password': str(password),}
        if debug:
            print("Netmiko dictionary connection profile structure:")
            pp(dut)
        if debug:
            print(str(runcmd))
        net_connect = ConnectHandler(**dut)
        print("retrieving data...")
        output = str(net_connect.send_command(str(runcmd)))
        print("'" + str(runcmd) + "'" + " command complete...")
        if debug:
            print(output)
        #always disconnect when complete so you don't tie up the vty lines
        net_connect.disconnect()

        #package this up in a nice dictionary
        rdict = {}
        rdict['ip'] = ip
        rdict['command'] = runcmd
        rdict['userid'] = username
        rdict['response'] = output
        return rdict
    except NetMikoTimeoutException as pExcept:
        print(pExcept)


    except Exception as e:
        print("Error while connecting ... : " + sys.exc_info()[1])
        if debug:
            print('Exit due to Error:', sys.exc_info()[1])
            print('Trace info:')
            print(traceback.format_exc())

def getNCoutput(ncXML,ip,uid,devType):
    username, password = getcreds(uid, dbname)

    with manager.connect(host=ip, port='830',
                         username=username, password=password, timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:
        try:
            response = m.get(ncXML).xml
        except RPCError as e:
            print(e.errors)

            # beautify output
        responseDict = xmltodict.parse(response)
        jsonscrub = json.dumps(responseDict, indent=2)
        return json.loads(jsonscrub)

def getRCoutput(rcURI,ip,uid):
    username, password = getcreds(uid, dbname)

    requests.packages.urllib3.disable_warnings()
    # example: configuri = "/restconf/data/Cisco-IOS-XE-native:native?content=config"
    url = "https://" + ip + rcURI

    headers = {
        "Content-Type": "application/vnd.yang.data+json",
        "Accept": "application/vnd.yang.data+json, application/vnd.yang.errors+json, application/yang-data+json",
    }
    try:
        response = requests.request("GET", url, headers=headers, auth=(username, password), verify=False)
        return json.loads(response.text)
    except RPCError as e:
        print(e.errors)
        response=e.errors
        return  response




def runGenieParser(content, columnheaders,index):
    # example columnheaders =  ["Protocol", "Address", "Age (min)", "Hardware", "Addr", "Type", "Interface"]

    try:
        genie_resObj = parsergen.oper_fill_tabular(device_output=str(content),
                                          table_terminal_pattern=r"^\n",
                                          header_fields=columnheaders,
                                          index=index)
    except:
        # old python method, still works in Python 3 print('Error:', sys.exc_info()[1])
        print('Error:', sys.exc_info()[1])

    result = genie_resObj.entries
    resulttxt = json.dumps(result, indent=2)
    return resulttxt

def runMTLParser(outputText, template, objname):
        template = template.splitlines()
        pp(template)
        outputlist = outputText.splitlines()
        #print(str(self.textEdit_2.toPlainText()))
        # QtCore.pyqtRemoveInputHook()
        # pdb.set_trace()
        data = mtl.renderValidator(template, outputlist, objname)
        # QtCore.pyqtRemoveInputHook()
        # pdb.set_trace()
        return json.dumps(data, indent=2)

def runTFSMParser(outputtext,templatefile):
    print("running parser... using file: " + templatefile)
    #open the textfsm template file - TextFSM requires an already open file handle
    template_file_handle = open(templatefile)
    tfsmObject = TextFSM(template_file_handle)
    fsm_results = tfsmObject.ParseText(outputtext)

    resultlist=[]
    for eachline in fsm_results:
        resultitem={}
        current_column = 0
        for eachcolname in tfsmObject.header:
            resultitem[eachcolname]=eachline[current_column]
            current_column = current_column + 1

        resultlist.append(resultitem)
    if debug:
        pp(resultlist)
    return(resultlist)

def runJinjaRender(jinjatxt,yamltxt):
    template = jinja2.Template(jinjatxt)
    # get yaml data and convert to dictionary for jinja to consume
    ydata = yaml.load(yamltxt)
    result = template.render(ydata)
    print(result)
    return result


def writeConfig(cmd,ip,uid, devtype):
    #pdb.Pdb(stdout=sys.__stdout__).set_trace()
    configlist = cmd.splitlines()
    try:
        username, password = getcreds(uid, dbname)

        dut = {'device_type': str(devtype), 'ip': str(ip),'username': str(username), 'password': str(password),}
        if debug:
            print("Netmiko dictionary connection profile structure:")
            pp(dut)
        if debug:
            print(str(configlist))
        net_connect = ConnectHandler(**dut)
        print(net_connect.find_prompt())
        output = net_connect.send_config_set(configlist)
        net_connect.disconnect()
        return output


    except NetMikoTimeoutException as pExcept:
        print(pExcept)


    except Exception as e:
        print("Error while connecting ... : " + sys.exc_info()[1])
        if debug:
            print('Exit due to Error:', sys.exc_info()[1])
            print('Trace info:')
            print(traceback.format_exc())

if __name__ == '__main__':
    # print("main running tests..")
    # fh1 = open('bgp.cli')
    # clioutput = fh1.read()
    # fh2 = open('bgp.mtl')
    # template = fh2.read()
    # result = runMTLParser(clioutput,template,'bgpinfo')
    # print(result)
    # fh1.close()
    # fh2.close()
    #
    # fh1 = open('bgp.jinja')
    # jtxt = fh1.read()
    # fh2 = open('bgp-crs.yml')
    # ytxt = fh2.read()
    # result = runJinjaRender(jtxt,ytxt)
    # print(result)

    commands='''lldp run
cdp run\n'''
    writeConfig(commands, "172.20.2.2", 1, 'cisco_ios')
