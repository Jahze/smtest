cfgValues = {}

def read_config():
    f = open('config.ini', 'r')
    for line in f:
        key,value = line.split('=', 2)
        if value[len(value)-1] == "\n":
            value = value[0:len(value)-1]
        cfgValues[key] = value

def config_value( key ):
    return cfgValues[key]

read_config()
