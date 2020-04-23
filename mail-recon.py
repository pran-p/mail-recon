try:
    from bs4 import BeautifulSoup
except:
    print('No module named bs4 found')
import requests
import re
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
from progress.bar import IncrementalBar
"""Below is the custom implementation of google result scraping"""
# """This function get the source code of the search results for future parsing using BeautifulSoup"""
# def get_source_code(search,number):
#     # Generating the list of url to query google
#     try:
#         if number <= 10:
#             url = ['http://www.google.com/search?q='+search+'&start=0']
#         elif number >10:
#             url = []
#             for i in range((number//10)+1):
#                 url.append('http://www.google.com/search?q='+search+'&start='+str((i)*10))
#         source_code = []
#         for i in url:
#             r = requests.get(i)
#             source_code.append(r.content)
#         return source_code
#     except:
#         print('Mostly google banned you from scraping it.')
#         return 0
#
# """Given a list of source codes this function return a list of url results given by google"""
# def get_url(source_code):
#     url=[]
#     for i in source_code:
#         soup = BeautifulSoup(i,'html5lib')
#         cards = soup.find_all('div', attrs={'class':'kCrYT'})
#         for j in range(len(cards)):
#             link_tag=cards[j].find('a')
#             if link_tag:
#                 # If an url tag exists append the url to the url list
#                 url.append(link_tag['href'][7:])
#     return url




def get_url(search_q, number):
    url_list=[]
    for j in search(search_q, stop=number):
        url_list.append(j)
    return url_list


def get_mails_list(url_list,mail):
    mail_list=[]
    bar = IncrementalBar('Countdown', max = len(url_list))
    for i in url_list:
        r=requests.get(i)
        bar.next()
        soup=BeautifulSoup(r.content,'html5lib')
        plain_text=soup.get_text()
        # Now we have the website as a plain text
        # We need to extract the mails from the url
        re_exp='\S+'+mail
        lst = re.findall(re_exp, plain_text)
        for i in lst:
            mail_list.append(i)
    return mail_list



def get_mail_pattern():
    mail=input('Enter the mail pattern to search for(Example:@gmail.com):')
    number=int(input('Enter the approx number of pages to search for:'))
    if not re.search('@\S+.\S',mail):
        print('Input error, enter in the right format')
    else:
        search='intext:"'+mail+'""'
        # source_code=get_source_code(mail,number)
        # url_list=get_url(source_code)
        url_list=get_url(search, number)
        print('[+] Extracted url from google results')
        print('[+] {0} number of urls found'.format(len(url_list)))
        print('[+] Extracting HTML code for the urls')
        mail_list=get_mails_list(url_list,mail)
        print('\n[+] {0} mail addresses found'.format(len(mail_list)))
        print('[+] Results for {0} :'.format(mail))
        print('\n'.join(mail_list))

if __name__=="__main__":
    get_mail_pattern()
