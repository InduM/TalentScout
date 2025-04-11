import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"\+?\d{7,15}", phone)

def validate_name(name):
    return re.match(r"[A-Za-z]{2,25}( [A-Za-z]{2,25})?", name)

def flatten(xss):
    return [x for xs in xss for x in xs]


