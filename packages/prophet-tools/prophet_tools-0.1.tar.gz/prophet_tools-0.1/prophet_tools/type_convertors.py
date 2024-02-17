def cookie_to_dict(cookie):
    lines = cookie.split('; ')
    res = {}
    for line in lines:
        key, value = line.split('=', 1)
        res[key] = value
    return res