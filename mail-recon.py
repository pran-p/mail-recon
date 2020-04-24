# Importing the required modules
try:
    from bs4 import BeautifulSoup
except ImportError:
    print('No module named bs4 found')
import requests
import re
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
try:
    from progress.bar import IncrementalBar
except ImportError:
    print('No module named "progress.bar" found')
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except ImportError:
    print('No module named "selenium" found')
try:
    import argparse
except ImportError:
    print('No module named "argparse" found')
try:
    import pyfiglet
except ImportError:
    print('No module named "pyfiglet" found')
import sys
import time
import json
# from breach-check import get_breach_data
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



"""This function performs the google search using google dorks and returns the result urls"""
def get_url(search_q, number):
    url_list=[]
    for j in search(search_q, tld='co.in',stop=number):
        url_list.append(j)
    return url_list


"""This module performs breach check from haveibeenpwned.com website"""
def get_breach_data(mail_list):

    breach_data=[]
    mail_breach_mapping=[]
    driver = webdriver.Chrome(executable_path=r'./chromedriver')
    for i in mail_list:
        tempo={}
        tp={}
        url='https://haveibeenpwned.com/unifiedsearch/'+str(i)
        driver.get(url)
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        soup=BeautifulSoup(source_code,'html5lib')
        pre_tag=soup.find('pre')
        # If breaches found
        if pre_tag:
            json_data=json.loads(pre_tag.text)
            tempo=len(json_data['Breaches'])
            breach_data.append(tempo)
            tp['mail']=i
            tp['Breaches']=json_data
            mail_breach_mapping.append(tp)

        # If no breach found
        else:
            breach_data.append(0)
    return breach_data, mail_breach_mapping


"""This function opens the urls and returns the mail list"""
def get_mails_list_requests(url_list,mail):
    mail_list=[]
    bar = IncrementalBar('Countdown', max = len(url_list))
    for i in url_list:
        r=requests.get(i)
        bar.next()
        soup=BeautifulSoup(r.content,'html5lib')
        plain_text=soup.get_text()
        # Now we have the website as a plain text
        # We need to extract the mails from the url
        # re_exp='\S+'+mail
        re_exp='[a-zA-Z0-9_.]+?'+mail
        lst = re.findall(re_exp, plain_text)
        for i in lst:
            mail_list.append(i)
    return mail_list


"""This function returns a list of source codes from a list of urls supplied"""
def get_source_code_list(url_list=[]):
    source_code_list=[]
    if type(url_list)==list and len(url_list)==0:
        print('Parameter is empty, you need to pass a list of urls')
    elif type(url_list)!=list:
        print('You need to pass a list of urls as a paramenter to this function')
    else:
        # Initializing the progress bar
        bar = IncrementalBar('Countdown', max = len(url_list))
        driver = webdriver.Chrome(executable_path=r'./chromedriver')
        # Extracting the souce code of the given urls
        for i in url_list:
            driver.get(i)
            elem = driver.find_element_by_xpath("//*")
            source_code = elem.get_attribute("outerHTML")
            source_code_list.append(source_code)
            # Updating the progress bar
            bar.next()
            # TAB1.update_idletasks()
            # Adding a time delay of 1 seconds between multiple requests

    driver.close()
    bar.finish()
    return source_code_list

"""This function opens the urls and returns the mail list by performing selenium scraping"""
def get_mails_list_selenium(url_list,mail):
    mail_list=[]
    source_code_list=get_source_code_list(url_list)
    for i in source_code_list:
        soup=BeautifulSoup(i,'html5lib')
        plain_text=soup.get_text()
        # Now we have the website as a plain text
        # We need to extract the mails from the url
        re_exp='[a-zA-Z0-9_.]+?'+mail
        lst = re.findall(re_exp, plain_text)
        for i in lst:
            mail_list.append(i)
    return mail_list

"""This function saves the extracted mail addresses to a file"""
def save_file(mail_list,f_name, number_breach, breach_data):
    # Save only the list of mails
    f=open('./data/'+f_name+'.txt','w')
    f.write('\n'.join(mail_list))
    f.close()

    # Save the mail and number of breaches
    f=open('./data/'+f_name+'_number_breaches.txt','w')
    for i in range(len(number_breach)):
        f.write(mail_list[i]+'\t'+str(number_breach[i])+'\n')
    f.close()


    # Save the breach data
    f=open('./data/'+f_name+'_breach_data.txt','w')
    json_dump=json.dumps(breach_data)
    f.write(json_dump)
    f.close()
    print('[+] Extracted files saved to file: {0} in the data folder'.format(f_name))

"""This function is responsible to get the mail pattern from the user and combine the functionality of the above two functions"""
def get_mail_pattern():
    f=pyfiglet.Figlet(font='cybermedium')
    print(f.renderText('Mail Recon'))
    print ('\033[1m')
    print("M4i1 R3c0n: 3xtr4ct m4i1 4ddr3ss3s in th3 0p3n...")
    print ('\033[0m')
    # Taking the arguments
    parser=argparse.ArgumentParser()
    parser.add_argument('-s','--selenium',action='store_true',  help="Perform selenium scraping")
    parser.add_argument('-b','--basic', action='store_true', help="Perform normal scraping(May not be able to scrap all website)")
    parser.add_argument('-n','--number', help="Approx number of url to search for")
    parser.add_argument('-f','--format', help="Mail address format (Eg: @gmail.com)")
    parser.add_argument('-fn','--fileName',help="File name to save the results")
    # parser.add_argument('-m','--multiple', nargs=2, metavar=('port1,port2,...','ip'),help='enter the list of port number separated by comma and the ip of the system for port scan')
    # parser.add_argument('-r','--range', nargs=3, metavar=('start-port', 'end-port', 'ip1,ip2,...'), help='enter the start port and the end port range and the ip of the system for port scan')
    args=parser.parse_args()
    # Performs selenium scan
    if args.selenium and args.format and args.number:
        mail=args.format
        number=int(args.number)
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
            mail_list=get_mails_list_selenium(url_list,mail)
            print('\n[+] {0} mail addresses found'.format(len(mail_list)))
            print('[+] Results for {0} :'.format(mail))
            number_breach, breach_data=get_breach_data(mail_list)
            print('\n[+] {0} mail addresses found'.format(len(mail_list)))
            print('[+] Results for {0} :'.format(mail))
            for i in range(len(mail_list)):
                print(mail_list[i]+'\t'+str(number_breach[i]))
            tempo=time.localtime()
            # Default name if no file name given by user
            f_name=mail+'-mail-recon-res-'+str(tempo.tm_hour)+'-'+str(tempo.tm_min)+'-'+str(tempo.tm_sec)
            if args.fileName:
                f_name=args.fileName
            save_file(mail_list,f_name, number_breach, breach_data)

    # Performs the basic scans
    elif args.basic and args.format and args.number:
        mail=args.format
        number=int(args.number)
        if not re.search('@\S+.\S',mail):
            print('Input error, enter in the right format')
        else:
            search='intext:"'+mail+'""'
            # source_code=get_source_code(mail,number)
            # url_list=get_url(source_code)
            url_list=get_url(search, number)
            print('[+] Extract URL from google results')
            print('[+] {0} number of urls found'.format(len(url_list)))
            print('[+] Performings scraping')
            mail_list=get_mails_list_requests(url_list,mail)
            number_breach, breach_data=get_breach_data(mail_list)
            print('\n[+] {0} mail addresses found'.format(len(mail_list)))
            print('[+] Results for {0} :'.format(mail))
            for i in range(len(mail_list)):
                print(mail_list[i]+'\t'+str(number_breach[i]))
            tempo=time.localtime()
            # Default name if no file name given by user
            f_name=mail+'-mail-recon-res-'+str(tempo.tm_hour)+'-'+str(tempo.tm_min)+'-'+str(tempo.tm_sec)
            if args.fileName:
                f_name=args.fileName
            save_file(mail_list,f_name, number_breach, breach_data)


    # When invalid arguments are passed
    else:
        print('Invalid arguments')
        print('To see all the options enter: python3 mail-recon.py -h')
        print('-n and -f flag are mandatory and you have to choose between -s and -b flags')




if __name__=="__main__":
    get_mail_pattern()
