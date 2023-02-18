import sys
from random import randint

from selenium import webdriver
from selenium.webdriver.edge.options import Options


def log_in(
        driver: webdriver.Edge or webdriver.Chrome,
        acc,
        pwd):
    driver.get(
        "https://wac.kmu.edu.tw/loginnew.php?PNO=indexstuv2.php&usertype=stu&lang=zh")

    driver.find_element('css selector', 'input[name="userid"]').send_keys(acc)
    driver.find_element('css selector', 'input[name="pwd"]').send_keys(pwd)
    driver.find_element('css selector', 'button[type="submit"]').click()

    # Verify
    driver.get('https://wac.kmu.edu.tw/stu/stuaca/stum0021.php')
    stu_id = driver.find_element(
        'xpath', '/html/body/table[2]/tbody/tr[4]/td[2]/font').text
    print(f'Log in: {stu_id}')

    return


def tempurature_report(driver: webdriver.Edge or webdriver.Chrome):
    driver.get('https://wac.kmu.edu.tw/stu/stusch/stum2906.php')
    append_btn = driver.find_element(
        'xpath', "/html/body/div[6]/form/div[2]/div[2]/table/tbody/tr/td[1]/button")

    try:
        append_btn.click()
    except:
        ...

    tempurature_field = driver.find_element(
        'xpath', '/html/body/div[6]/form/div[3]/table/tbody/tr[8]/td[2]/input')
    tempurature_field.send_keys(randint(355, 369)/10)

    save_btn = driver.find_element(
        'xpath', "/html/body/div[6]/form/div[2]/div[2]/table/tbody/tr/td[2]/button")
    save_btn.click()

    return


def main():
    acc, pwd = sys.argv[1:3]

    # driver = webdriver.Chrome(service=ChromiumService(
    #     ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()))
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(options=chrome_options)

    options = {
        # 'driver_type': browser,
        'headless': True,
        # 'browser_binary_location': shutil.which('microsoft-edge-dev'),
        # 'webdriver_location': shutil.which('msedgedriver'),
        'operating_system': 'LINUX'
    }
    driver = webdriver.Edge(options=options)

    driver.implicitly_wait(30)

    log_in(driver, acc, pwd)
    tempurature_report(driver)


if __name__ == "__main__":
    main()
