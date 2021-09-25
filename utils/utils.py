from const.privileges import Privileges, prv_list
def parseArgs(args:list, allowed_args:list):
    """Parse list of non-positional arguments and return a dictionary, inputs are args and allowed args"""
    dic = {}
    try:
        current_key = None
        for el in args:
            if el in allowed_args:
                current_key = el
                dic[current_key] = []
            else:
                dic[current_key].append(el)
            
        for key, val in dic.items():
            dic[key] = " ".join(val)
    except KeyError:
        raise KeyError
    finally:
        return dic

def usernameConverter(arg):
    """Fix those stupid usernames to make them work with non positional args"""
    if type(arg) is list:
        for i in arg:
            spaced = ' '.join(i)
    else:
        spaced = arg
    if spaced.startswith('"') and spaced.endswith('"'):
        spaced = spaced[1:-1]
    return spaced

def determine_plural(number:int):
    if int(number) != 1:
        return 's'
    else:
        return ''

def getUserGroupList(priv:int):
    """Convert user privileges to list"""
    priv_res = []
    if priv == 0 or priv == 2:
        priv_res = ["Restricted"]
        return priv_res
    if Privileges.Dangerous in Privileges(priv):
        priv_res.append("Developer")
    if Privileges.Admin in Privileges(priv):
        priv_res.append("Admin")
    if Privileges.Mod in Privileges(priv):
        priv_res.append("GMT")
    if Privileges.Nominator in Privileges(priv):
        priv_res.append("BAT")
    if Privileges.Tournament in Privileges(priv):
        priv_res.append("Tournament")
    if Privileges.Alumni in Privileges(priv):
        priv_res.append("Alumni")
    if Privileges.Premium in Privileges(priv):
        priv_res.append("Premium")
    if Privileges.Supporter in Privileges(priv):
        priv_res.append("Supporter")
    if Privileges.Whitelisted in Privileges(priv):
        priv_res.append("Verified")
    if Privileges.Verified in Privileges(priv) or Privileges.Normal in Privileges(priv):
        priv_res.append("User")
    return priv_res
