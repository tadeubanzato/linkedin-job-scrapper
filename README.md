# Linkedin Job Scaping
> I'm not a developer so please contribute to this by improving the code and helping make it optimized.

I started doing this project to study Python, web scraping and database manipulation.
What the script does:
1. Logg into Linkedin with your credentials
2. Goes automatically to the Job Search page
3. Add the information for Tob Title and Location
4. Search for the information and scroll the job opportunities on the left panel of Linkedin to list all 25 items from the first page
5. Build a full list of linkedin URLs, job posting name, job posting location, company name
6. Automatically enter on each position and build a list of the direct URL of the position
7. Verify if the position is recorded or nor in the DataSet, skip positions already recorded and add new positions to the DataSet
8. Record everything in a CSS file


## What will be needed
Python 3 and above
Selenium Driver - For web scraping
Pandas - For DataBase manipulation

All other libraries are captured into the requirements.txt file, to install the requirements run
```bash
sudo pip3 install -r requirements.txt
```
Also the code is developed on a Mac, so you will probably need to change the following code to run in specific systems.

I run the following on an Ubuntu 20.10 Desktop installed on my raspberry pi 4:
```python
if config.get('HEADLESS', 'headless') == 'Yes':
    # install webdrive when needed runing headless
    opts=webdriver.ChromeOptions()
    opts.headless=True
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver" ,options=opts)
else:
    # install webdrive when needed runing browser
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
```
Make sure to change `/usr/lib/chromium-browser/chromedriver` for the path of your driver on Linux

## Config.ini File
This file is where you setup your linkedin information for search,country/region and login
**[LINKEDIN_LOGIN]**
password = `<linkedin password>`
email = `<linkedin email>`
search_term = `<search term example: Supply Chain Manager>`
country = `<Country example: Brazil>`

**[HEADLESS]**
headless = No `<Yes or No>`

## Panda CSV manipulation
With Panda I'm building the CSV file to record the following structure:

| Job Title       | Company Name     | Location     | Direct URL     |Trimmed Linkedin
| :------------: | :----------: | :----------: | :----------: | :----------: |
|  Job Title  | Company Name   | Location of the Position    | Direct URL of the position | Trimmed Linkedin URL


