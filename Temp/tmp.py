import whois


class A(object):
    pass


w = whois.whois('webscraping.com')
w.expiration_date  # dates converted to datetime object