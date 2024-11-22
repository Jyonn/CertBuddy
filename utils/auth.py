with open('.auth') as f:
    auth_data = f.read()

AUTHENTICATION = {}
for line in auth_data.strip().split('\n'):
    name, key = line.split('=')
    AUTHENTICATION[name.strip()] = key.strip()
