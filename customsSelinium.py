from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import os
import glob

download_path = os.path.join('bucket/dataset_customs')
if not os.path.exists(download_path):
    os.makedirs(download_path)
os.path.abspath(download_path)

url = 'http://www.customs.go.th/statistic_report.php?ini_content=statistics_report'
prefs = {"download.default_directory" : os.path.abspath(download_path)}
path_to_driver = './chromedriver'

with open('hs_code.txt', 'r') as f:
    txt = f.read()

sh_code_raw = [row.split('\t')[1] for row in txt.split('\n')][1::]
sh_code_raw = [x.split(' ') for x in sh_code_raw]
[x.remove('–') for x in sh_code_raw]
sh_code_raw = [(int(x[0]), int(x[1])) for x in sh_code_raw]


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(executable_path=path_to_driver,options=options)
browser.get(url)

for i in range(3):
    print(f"Please wait {3-i} ... ")
    time.sleep(1)

for imex in ['import', 'export']:
    imex_type = Select(browser.find_element_by_name("imex_type"))
    imex_type.select_by_value(imex)
    
    tariff_code = browser.find_element_by_id("tariff_code")
    for sh_codes in sh_code_raw:
        for sh_code in range(int(sh_codes[0]), int(sh_codes[1])):
            path = os.path.join(download_path, imex, "{:04d}".format(sh_code))
            if not os.path.exists(path):
                os.makedirs(path)
            tariff_code.clear()
            tariff_code.send_keys("{:04d}".format(sh_code))
            time.sleep(1)
            for y in range(2001,2022):
                year = Select(browser.find_element_by_name("year"))
                year.select_by_value("{}".format(y))
                time.sleep(1)
                for m in range(1,13):
                    month=Select(browser.find_element_by_name("month"))
                    month.select_by_value("{}".format(m))
                    time.sleep(1)
                    csv = browser.find_element_by_xpath('//button[text()=" Export CSV"]')
                    csv.click()
                    time.sleep(0.25)
                    csv_files = glob.glob(os.path.join(download_path, '*.csv'))
                    for csv_file in csv_files:
                        os.rename(csv_file, os.path.join(path, csv_file.split('/')[-1]))
    time.sleep(1)

