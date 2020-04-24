# mail-recon
Great python tool to list out mails of an organization floating out in the open and find the number of breaches the mails were a part of. All this is done by taking the mail pattern as input Eg. @gmail.com. 

## Working of the tool (The boring part)
+ *Step 1* - Input the pattern from the user.
+ *Step 2* - Searches google for the mail patterns using google dorks. Problem with google is that it prevents you from performing google search from your code. To overcome this a randomization techniques has been used, during every new run of the program a new tld of google is randomly selected for the search. This step returns a list of urls that are nothing but the results of the google search.
+ *Step 3* - All the returned urls are scanned(Scraping) to find the potential mail addresses. Scraping is performed in two different ways. One is  the normal way using requests lib, but this is not a great method and might end up missing a lot of mail-ids. The other and robust method is to perform something called the selenium scraping. Selenium scraping can be selected by setting the -s flag. This code used chromedriver to perform the selenium scraping so you will need to have google chrome to run this tool. If you use firefox you can use the geckodriver for it. To use firefox replace all the occurrences of Chrome by Firefox and all occurrences of chromedriver by geckodriver
+ *Step 4* - For breach detection we use https://haveibeenpwned.com/ website. Based on the results from this site we classify a mail as breached or not breached. 
+ *Step 5* - Write the results into files for users. The tool gives out four files. One of then is just a list of mail addresses found other is mail to number of breaches. Next one shows the url where the mail was found and the last one show the complete breach details of the breached mail ids. The last file is just a json dump of the breach details so this can be processed even more to extract potentially useful insights.

## Getting it up and running
- Clone this repo
- Create a virtual env and install the requirements. Then just run the script.
```bash
virtualenv ENV_NAME
source ENV_NAME/bin/activate
pip3 install -r requirements.txt
python3 mail-recon.py -h
```
Once this is completed you will have the help menu shown, something like this:
```console
_  _ ____ _ _       ____ ____ ____ ____ _  _
|\/| |__| | |       |__/ |___ |    |  | |\ |
|  | |  | | |___    |  \ |___ |___ |__| | \|



M4i1 R3c0n: 3xtr4ct m4i1 4ddr3ss3s in th3 0p3n...

usage: mail-recon.py [-h] [-s] [-b] [-n NUMBER] [-f FORMAT] [-fn FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  -s, --selenium        Perform selenium scraping
  -b, --basic           Perform normal scraping(May not be able to scrap all
                        website)
  -n NUMBER, --number NUMBER
                        Approx number of url to search for
  -f FORMAT, --format FORMAT
                        Mail address format (Eg: @gmail.com)
  -fn FILENAME, --fileName FILENAME
                        File name to save the results
```

## Example scan
```bash
python3 mail-recon.py -s -n 10 -f @gmail.com
```
The above command starts the scan in selenium scrap mode and scans 10 websites for mail address of the format @gmail.com.
