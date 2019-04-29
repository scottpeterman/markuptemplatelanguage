import sys
from pprint import pprint as pp
debug = False
verbose = False
#example template rules
'''[[fieldbegin='macaddress', method=MID, match=', address is ']]@[[fieldend='macaddress', match='(bia']]
[[fieldbegin='MTU', method=MID, match='MTU ']]@[[fieldend='MTU', match='bytes, BW']]
[[fieldbegin='inputerrors', method=BOL]]@[[fieldend='inputerrors', match=' input errors']]
[[fieldbegin='description', method=EOL, match='Description: ']]@[[fieldend='description', match=' \\n']]
[[fieldbegin='internetaddress', method=EOL, match='Internet address is ']]@[[fieldend='internetaddress', match=' \\n']]
[[fieldbegin='drops', method=BOL]]@[[fieldend='drops', match='drops for unrecognized']]'''

def loadfile(filename):
    fh = open(filename, 'r')
    result = fh.readlines()
    #result is a list of lines
    return result

def createruleset(template,source):
    ruleset = []
    if debug:
        print(str(template))
        #print(source)

    #process templates line by line(list object)
    for rule in template:
        result = makeRuleFromTemplate(rule)
        ruleset.append(result)
        #print(rule)

    return ruleset

def makeRuleFromTemplate(ruletxt):
    rulepair = {}

    try:
        preruletxt = ruletxt.split('@')[0]
        postruletxt = ruletxt.split('@')[1]

        # process prerule:
        preprops = preruletxt.split(',')
        method = preprops[1].split('=')[1].strip("]]")
        fieldbegin=preprops[0].split('=')[1].strip("'")

        prerule={}
        prerule["method"] = str(method).strip()
        prerule["fieldbegin"] = str(fieldbegin).strip()
        if "BOL" not in method:
            #collect match keyword
            #BOL types don't have a match in the prerule (nothing to match on)
            match = preruletxt.split('match=')[1].strip("]]").strip("'")
            prerule["match"]= match.strip("]]")
        #pp(prerule)
        rulepair['prerule']= prerule

        #process postrule
        postprops = postruletxt.split(',')
        fieldend=postprops[0].split('=')[1]

        postrule={}
        postrule["fieldend"] = str(fieldend).strip().strip("'")
        postrule["match"] = postruletxt.split('match=')[1].strip("\n").strip("]]").strip("'")
        rulepair['postrule'] = postrule

        return rulepair

    except Exception as e:
        print('parsing error:')
        print('message -> ' + str(sys.exc_info()[1]))
        print('processing rule: ' + str(ruletxt))

def markup(rule, source):
    method = rule['prerule']["method"]
    if debug:
        print("process prerule")
        print("processing mode: " + method)
    result = ""

    # ---------------------------- handle "pre rule"
    if "MID" in method:
        pretext = "[[fieldbegin='"+ rule['prerule']["fieldbegin"] + ", method='" +rule['prerule']["method"] \
                  + "', match=' " + rule['prerule']["match"] + "']]"
        posttest = "[[fieldend='"+ rule['postrule']["fieldend"] + "', match=' " + rule['postrule']["match"] + "']]"
        found = False

        for eachline in source:
            if rule['prerule']["match"] in str(eachline) and rule['postrule']["match"] in str(eachline) and not found:
                found = True
                markedprestring = str(eachline).replace(rule['prerule']["match"], rule['prerule']["match"] + pretext)
                markedpoststring = markedprestring.replace(rule['postrule']["match"], posttest + rule['postrule']["match"])
                if debug:
                    print("original line: \n",eachline)
                    print("added pre markdown: \n",markedprestring)
                    print("both pre and post markdown: \n",markedpoststring)
                    #simple data grab:
                    myval = markedpoststring.split("]]")[1].split("[[")[0]
                    print("Value:" + str(myval))
                kvpair = grabdata(markedpoststring, rule)
        return kvpair

    elif "BOL" in method:
        pretext = "[[fieldbegin='"+ rule['prerule']["fieldbegin"] + ", method='" +rule['prerule']["method"] + "']]"
        posttest = "[[fieldend='"+ rule['postrule']["fieldend"] + "', match=' " + rule['postrule']["match"] + "']]"
        found = False

        for eachline in source:
            if rule['postrule']["match"] in str(eachline) and not found:
                found = True
                #find insert point
                point =len(eachline) - len(eachline.lstrip())
                #print("Point: "+ str(point))
                markedprestring = eachline[:point] + pretext+str(eachline).strip("\n").lstrip()
                markedpoststring = str(markedprestring).replace(rule['postrule']["match"], posttest + rule['postrule']["match"])
                if debug:
                    print("original line: \n",eachline)
                    print("added pre markdown: \n",markedprestring)
                    print("both pre and post markdown: \n",markedpoststring)
                    #simple data grab:
                    myval = markedpoststring.split("]]")[1].split("[[")[0]
                    print("Value:" + str(myval))
                kvpair = grabdata(markedpoststring, rule)
        return kvpair

    elif "EOL" in method:
        pretext = "[[fieldbegin='"+ rule['prerule']["fieldbegin"] + ", method='" +rule['prerule']["method"] \
                  + "', match=' " + rule['prerule']["match"] + "']]"
        posttest = "[[fieldend='"+ rule['postrule']["fieldend"] + "', match=' " + rule['postrule']["match"] + "']]"
        found = False

        for eachline in source:
            if rule['prerule']["match"] in str(eachline) and not found:
                found = True
                markedprestring = str(eachline).replace(rule['prerule']["match"], rule['prerule']["match"] + pretext)
                markedpoststring = markedprestring.strip("\n") + posttest
                if debug:
                    print("original line: \n",eachline)
                    print("added pre markdown: \n",markedprestring)
                    print("both pre and post markdown: \n",markedpoststring)
                    #simple data grab:
                    testvalue = markedpoststring.split("]]")[1].split("[[")[0]
                    print("Value:" + str(testvalue))
                kvpair = grabdata(markedpoststring,rule)
        return kvpair
    else:
       #handle others methods not yet implemented
        print("method not implemented...yet..")


    print("process postrule")

def grabdata(markedtext,rule):
    #grab the pre, post and data section from marked up content
    #this would be unnecessary, but its also to build a useful data structure / dictionary to return
    if verbose:
        print("\n\nextracting....")
        for eachline in markedtext.splitlines():
            print(eachline)

    prehitcount=0
    index = 0
    prepositions = []
    while index < len(markedtext):
        index = markedtext.find('[[', index)
        if index == -1:
            break

        index += 2  # +2 because len('[[') == 2
        prehitcount += 1
        prepositions.append(index)
    if debug:
        print("Found {} instances of '[['-> {}".format(prehitcount,prepositions))

    posthitcount = 0
    index = 0
    postpositions = []
    while index < len(markedtext):
        index = markedtext.find(']]', index)
        if index == -1:
            break

        index += 2  # +2 because len('[[') == 2
        posthitcount += 1
        postpositions.append(index)
        if debug:
            print("Found {} instances of ']]'-> {}".format(posthitcount, postpositions))
    if prehitcount == posthitcount:
        #can only apply one tag per line, per pass!!!!!!!!!!!!
        result = {}
        data = str(markedtext[postpositions[0]:prepositions[1]-2]).strip()
        if rule['prerule']['method'] == 'MID' or rule['prerule']['method'] == 'EOL':
            fieldname = rule['prerule']['fieldbegin']
        elif rule['prerule']['method'] == 'BOL':
            fieldname = rule['prerule']['fieldbegin']
        else:
            raise ValueError("Error: Malformed rule set:" + str(rule))
        result['fieldname']=fieldname
        result["data"]=data
        if debug:
            print("Raw Data - > "+ "'" + data + "'")
            pp(result)

        return result

    else:
        raise ValueError("Malformed template!")

def renderValidator(template,source,objname):
    dataset = {}
    dataset[objname]={}
    result = createruleset(template, source)
    testnu = 1
    for rule in result:
        if debug:
            print("=================== begin parse test #" + str(testnu) + " ====================")
        kvdata = markup(rule, source)
        dataset[objname][kvdata['fieldname']]= kvdata['data']
        testnu += 1
        if debug:
            pp(kvdata)
    return dataset

if __name__ == '__main__':
    print("main running ..")
    # source = loadfile("./markup/showinterfacespecific.txt")
    # template = loadfile("./markup/template1.mtl")
    source = loadfile("./markup/test1.cli")
    template = loadfile("./markup/test1.mtl")
    data = renderValidator(template,source,"testMainExample")
    pp(data)
