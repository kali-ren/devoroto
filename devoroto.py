import requests, sys, cfscrape, argparse
from bs4 import BeautifulSoup

simple_base = 'https://haveibeenpwned.com/api/v2/breachedaccount/' #email, but pastebin
breach_base = 'https://haveibeenpwned.com/api/v2/breach/'
paste_base  = 'https://haveibeenpwned.com/api/v2/pasteaccount/' #pastebin
domain_base = 'https://haveibeenpwned.com/api/v2/breaches?domain='

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}


def simple_search(email):#Getting all breaches for an account
    r = requests.get(simple_base+email,headers=header)
    print '[+] searching ...'
    
    if r.status_code == 404:
        print 'No results :)'
    else:
        print r.content
    
def breached_site(site):#leaks from site
   r = requests.get(breach_base+site,headers=header)
   print '[+] searching breach site ...'
   
   if r.status_code == 404:
        print 'No results :)'

   if r.status_code == 503:
       r = bypasscf(breach_base+email,headers=header)

   return r.content
    
def paste_account(email):#pastebin email account em uso
    r = requests.get(paste_base+email,headers=header)
    print '[+] searching '+  email +' in pastebin ...\n'

    if r.status_code == 404:
        return 'No results :)\n'
    
    if r.status_code == 503:
        r = bypasscf(paste_base+email,headers=header)
    
    return r.content
    
def all_branches(email):#desuso. API bug?
    r = requests.get(simple_base+email,headers=header)
    print '[+] searching '+ email +' in all haveibeenpwned sources, but pastebin\n'
    
    if r.status_code == 404:
        return 'No results :)\n'
    
    if r.status_code == 503:
        r = bypasscf(simple_base+email,headers=header)
    
    return r.content
    
def domain_breaches(site):#em uso
    r = requests.get(domain_base+site,headers=header)
    print '[+] searching leaks from '+ site + '\n'

    if r.content == '[]':
        return 'No results :)'
        
    if r.status_code == 503:
    	r = bypasscf(domain_base+site,headers=header)
    
    return r.content

def bypasscf(wish):#bypass cloudfare. Node.js must be installed
    scraper = cfscrape.create_scraper()
    r = scraper.get(wish)
    return r.content


def print_logo():
    print("""
 _____     ______     __   __   ______     ______     ______     ______   ______    
/\  __-.  /\  ___\   /\ \ / /  /\  __ \   /\  == \   /\  __ \   /\__  _\ /\  __ \   
\ \ \/\ \ \ \  __\   \ \ '/    \ \ \/\ \  \ \  __<   \ \ \/\ \  \/_/\ \/ \ \ \/\ \  
 \ \____-  \ \_____\  \ \__|    \ \_____\  \ \_\ \_\  \ \_____\    \ \_\  \ \_____\ 
  \/____/   \/_____/   \/_/      \/_____/   \/_/ /_/   \/_____/     \/_/   \/_____/ 
                                                                                    
""")
def main():
    parser = argparse.ArgumentParser(description='Check leaks of email and domain in haveibeenpwned.com')
    parser.add_argument('-e','--email', type=str, help='pass here a valid email', required=False)
    parser.add_argument('-d','--domain',type=str, help='pass here a valid domain',required=False)

    args = parser.parse_args()

    email  = args.email
    domain = args.domain

    if email:
        #to-do: regex email validation
        print """
		*****************************************************
				email leaks
		*****************************************************
	"""
	
	print paste_account(email)
	print all_branches(email)

        print """
		*****************************************************
				email leaks
		*****************************************************
	"""	

    if domain:
       #todo: regex domain validation
        print """
		*****************************************************
				domain leaks
		*****************************************************
	"""       	
        print domain_breaches(domain)

        print """
		*****************************************************
				domain leaks
		*****************************************************
	"""

if __name__ == '__main__':
    if(len(sys.argv[1:])==0):
    	print 'usage: devoroto.py [-h] [-e EMAIL] [-d DOMAIN.com]'
    main()

