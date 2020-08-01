import pdfkit
import pandas as pd
import html5lib
import bs4
import sys
from selenium import webdriver
from dotenv import load_dotenv
from os import getenv
from time import sleep
from datetime import datetime

if len(sys.argv) == 1:
    nr_meses = 2
else:
    try:
        nr_meses = int(sys.argv[1]) + 1
    except:
        raise Exception('Parameter entered is not an integer')



def get_value(element):
    """Verifica se o elemento existe, se sim retorna seu valor text se não retorna None

    Args:
        element (xpath): Valor do xpath do elemento a ser verificado

    Returns:
        String: retorna o Valor do elemento selecionado ou None
    """
    try:
        element_value = driver.find_element_by_xpath(element).text
    except:
        return None
    return element_value


load_dotenv()

driver = webdriver.Chrome('./chromedriver')

url = 'https://notaparana.pr.gov.br/'


driver.get(url)
sleep(5)
driver.find_element_by_xpath(
    '//*[@id="attribute"]').send_keys(getenv('user'))
driver.find_element_by_xpath(
    '//*[@id="password"]').send_keys(getenv('password'))
driver.find_element_by_xpath('//*[@id="authForm"]/div[4]/input').click()
sleep(5)
driver.find_element_by_xpath('//*[@id="main"]/ul/li[1]/a').click()
sleep(5)


a_link = '/html/body/div[2]/div[2]/div/div[4]/form/fieldset/div[4]/table/tbody/tr[{}]/td[3]/a'
window_before = driver.window_handles[0]


df = pd.DataFrame(columns=['nf_nr', 'dt_emissao',
                           'place_name', 'vl_nf', 'acess_key', 'qr_code_link'])

for paginas in range(1, nr_meses):
    nr_linhas = pd.read_html(driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div/div[4]/form/fieldset/div[4]/table').get_attribute('outerHTML'))[0].shape[0]
    for nr_row in range(2, nr_linhas):
        driver.find_element_by_xpath(a_link.format(nr_row)).click()
        sleep(2)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        acess_key = driver.find_element_by_xpath(
            '/html/body/div[1]/fieldset/table/tbody/tr/td[1]/span').text

        place_name = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/fieldset[2]/table/tbody/tr/td[2]/span').text

        nf_nr = driver.find_element_by_xpath(
            '/html/body/div[1]/fieldset/table/tbody/tr/td[2]/span').text

        dt_emissao = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/fieldset[1]/table/tbody/tr/td[4]/span').text

        vl_nf = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div/fieldset[1]/table/tbody/tr/td[6]/span').text

        driver.find_element_by_xpath('/html/body/ul/li[8]').click()

        if get_value('/html/body/div[2]/div[7]/div/fieldset/fieldset[3]/table/tbody/tr[1]/td/span') != None:
            qr_code_link = get_value(
                '/html/body/div[2]/div[7]/div/fieldset/fieldset[3]/table/tbody/tr[1]/td/span')
        elif get_value('/html/body/div[2]/div[7]/div/fieldset/fieldset[2]/table/tbody/tr[1]/td/span') != None:
            qr_code_link = get_value(
                '/html/body/div[2]/div[7]/div/fieldset/fieldset[2]/table/tbody/tr[1]/td/span')
        elif get_value('/html/body/div[2]/div[7]/div/fieldset/fieldset/table/tbody/tr[1]/td/span') != None:
            qr_code_link = get_value(
                '/html/body/div[2]/div[7]/div/fieldset/fieldset/table/tbody/tr[1]/td/span')
        else:
            qr_code_link = 'ERROR'

        item = [nf_nr, dt_emissao, place_name, vl_nf, acess_key, qr_code_link]
        print(item[:2])
        df.loc[len(df)] = item
        driver.close()
        driver.switch_to.window(window_before)
    driver.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div/div[4]/form/fieldset/div[5]/button[1]').click()
    sleep(2)

df.to_csv('data_nf.csv', sep=';')
driver.find_element_by_xpath(
    '/html/body/div[2]/div[1]/div/div[2]/div/a[2]').click()
sleep(10)
driver.close()

for index, row in df.iterrows():
    dt_nf = datetime.strptime(row['dt_emissao'][:-6], '%d/%m/%Y %H:%M:%S')
    try:
        pdfkit.from_url(row['qr_code_link'], './nf_pdf/nf_{}_{}_{}.pdf'.format(
            dt_nf.strftime('%Y%m%d'), row['nf_nr'], row['place_name'][:10]))
    except:
        print(row)
