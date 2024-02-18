import copy
import html
import re
from copy import copy

def filter(node, implamentationGuidance: bool):
    if isinstance(node, dict):
        retVal = {}
        for key in node:
            if key == 'desc':
                if '#text' in node[key][0]:
                    retVal['description'] = html.unescape(node[key][0]['#text'])
            elif key == 'conformance':
                retVal['mro'] = node[key]
            elif key == 'name':
                if '#text' in node[key][0]:
                    retVal['name'] = html.unescape(node[key][0]['#text'])
                else:
                    retVal['name'] = node[key]
            elif key == 'shortName':
                retVal['name'] = node[key]
            elif key == 'operationalization':
                retVal['valueSets'] = re.sub(r'(?<=release=)[a-z][0-9]*', '', html.unescape(node[key][0]['#text'])).replace('&amp;','&')
            elif key == 'minimumMultiplicity':
                retVal[key] = node[key]
            elif key == 'maximumMultiplicity':
                retVal[key] = node[key]
            elif key == 'type': 
                retVal['type'] = node[key]
            elif key == 'valueSets':
                retVal['valueSets'] = node[key]
            elif key == 'valueDomain':
                if node[key][0]['type'] != 'code':
                    if node[key][0]['type'] != 'ordinal':
                        retVal[key] = copy(node[key])
            elif key == 'context':
                if implamentationGuidance:
                    retVal['implamentationGuidance'] = re.sub(r'(?<=release=)[a-z][0-9]*', '', html.unescape(node[key][0]['#text'])).replace('&amp;','&')
            elif isinstance(node[key], dict) or isinstance(node[key], list):
                if key not in ['relationship', 'implementation']:
                    child = filter(node[key], implamentationGuidance)
                    if child:
                        retVal[key] = child
            
        if retVal:
            return retVal
        else:
            return None


    elif isinstance(node, list):
        retVal = []
        for entry in node:
            if isinstance(entry, str):
                retVal.append(entry)
            elif isinstance(entry, dict) or isinstance(entry, list):
                child = filter(entry, implamentationGuidance)
                if child:
                    retVal.append(child)
        if retVal:
            return retVal
        else:
            return None

