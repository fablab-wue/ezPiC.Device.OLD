from time import localtime
import json

# Examples for own filter/converter functions for pyHTML templates
# can be used like buildin functions: {{ timeStr(data.time) }}

def noneStr(s):
    if s is None:
        return '-'
    else:
        return str(s)
    
def timeStr(t):
    time_t = localtime(t)
    return "%04d-%02d-%02d %02d:%02d:%02d" % time_t[0:6]

def typeStr(o):
    type_str = str(type(o))
    try:
        parts = type_str.split("'")
        return parts[1]
    except:
        return type_str

def jsonStr(o):
    return json.dumps(o)
