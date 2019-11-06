import json
from sys import stdin, stderr, stdout
from os import getcwd, path
from random import choice
from argparse import ArgumentParser
from time import sleep
from OpenSSL import crypto
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class cPanelController:
    def __init__(self, ur, us, ps):
        self.ur = ur
        self.us = us
        self.ps = ps
        self.charss = 'abcdefghjkmnpqrstuvwxyz23456789ABCDFGHJKMNPQRSTUVWXYZ'
        self.driver = webdriver.Chrome()
        self.acts = ActionChains(self.driver)
        self.driver.get(f'https://{ur}/cpanel')
        self.login()

    def genPass(self):
        return ''.join([choice(self.charss) for x in range(18)])

    def gotoHome(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'imgLogo')))
        elem.click()

    def gotoMenu(self, item):
        self.gotoHome()
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, item)))
        elem.click()

    def login(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'user')))
        elem.clear()
        elem.send_keys(self.us)
        elem = self.driver.find_element_by_id('pass')
        elem.clear()
        elem.send_keys(self.ps)
        elem.send_keys(Keys.RETURN)

    def nuevaPestaña(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))
        elem.send_keys(Keys.LEFT_CONTROL + 't')
        self.driver.switch_to.default_content()

    def nextP(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))
        elem.send_keys(Keys.LEFT_CONTROL + Keys.TAB)
        self.driver.switch_to.default_content()

    def prevP(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'body')))
        elem.send_keys(Keys.LEFT_CONTROL + Keys.LEFT_SHIFT + Keys.TAB)
        self.driver.switch_to.default_content()


class uploadFilesToAccount(cPanelController):
    def __init__(self, ur, us, ps):
        cPanelController.__init__(self, ur, us, ps)
        self.gotoMenu('item_file_manager')
        self.nextP()
        self.gotoPHTML()
        self.chrgFile()

    def gotoPHTML(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'span[title="public_html"]')))
        self.acts.double_click(elem)
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'action-upload')))
        elem.click()

    def chrgFile(self):
        pass


class createDatabase(cPanelController):
    def __init__(self, ur, us, ps):
        cPanelController.__init__(self, ur, us, ps)
        self.dbConf = self.parseDBConf()
        self.gotoMenu('item_mysql_databases')
        self.createDB()
        self.createUserDB()
        #       self.linkUserDB()
        self.gotoMenu('item_php_my_admin')
        self.nextP()
        self.dumpDB()

    @staticmethod
    def parseDBConf():
        return json.loads(open('configCreateDB.json', 'r').read())

    def createDB(self):
        for i in self.dbConf:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'dbname')))
            elem.send_keys(i['dbname'])
            elem.send_keys(Keys.RETURN)
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'lnkReturn')))
            elem.click()

    def createUserDB(self):
        for i in self.dbConf:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'user')))
            i['dbpass'] = self.genPass()
            elem.send_keys(i['dbuser'])
            elem = self.driver.find_element_by_id('password')
            elem.send_keys(i['dbpass'])
            elem = self.driver.find_element_by_id('password2')
            elem.send_keys(i['dbpass'])
            sleep(2)
            elem.send_keys(Keys.RETURN)
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'lnkReturn')))
            elem.click()

    def linkUserDB(self):
        for i in self.dbConf:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'dblink')))
            sel1 = Select(elem)
            elem = self.driver.find_element_by_id('dbuser')
            sel2 = Select(elem)
            u = f'{self.us}_{i["dbuser"]}'
            d = f'{self.us}_{i["dbname"]}'
            sel1.select_by_visible_text(d)
            sel2.select_by_visible_text(u)
            elem = self.driver.find_element_by_id('linkclick')
            elem.click()
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "")))

    def dumpDB(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, f'{self.us}_{self.dbConf["dbname"]}')))
        elem.click()


class createFTPAccounts(cPanelController):
    def __init__(self, ur, us, ps):
        cPanelController.__init__(self, ur, us, ps)
        self.gotoMenu('')


class createEmailAccounts(cPanelController):
    def __init__(self, ur, us, ps, ty, ef):
        cPanelController.__init__(self, ur, us, ps)
        self.ty = ty
        self.ef = path.join(getcwd(), ef)
        self.gotoMenu('item_address_importer')
        self.chargeInfo()

    def chargeInfo(self):
        if self.ty == 'email':
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'rbtnTypeEmail')))
        elif self.ty == 'alias':
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'rbtnTypeFwd')))
        elem.click()
        elem = self.driver.find_element_by_id('file_input')
        elem.send_keys(self.ef)
        elem = self.driver.find_element_by_id('')


class createAdditionalDomains(cPanelController):
    def __init__(self, ur, us, ps):
        cPanelController.__init__(self, ur, us, ps)
        self.domains = self.getDomains()
        self.gotoMenu('item_addon_domains')
        self.createAddDom()
        self.gotoMenu('item_redirects')
        self.createRedirects()

    @staticmethod
    def getDomains():
        return [
            i.strip().split(';') for i in open('domains.txt', 'r').readlines()
        ]

    def createAddDom(self):
        for i in self.domains:
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'domain')))
            elem.clear()
            elem.send_keys(i[0])
            elem = self.driver.find_element_by_id('subdomain')
            elem.send_keys(Keys.SPACE)
            elem.clear()
            elem.send_keys(''.join(i[0].split('.')))
            elem = self.driver.find_element_by_id('dir')
            elem.clear()
            elem.send_keys(i[1].lstrip('/'))
            elem.send_keys(Keys.RETURN)
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'lnkReturn')))
            elem.click()

    def createRedirects(self):
        for i in self.domains:
            try:
                if i[2] == '':
                    continue
            except IndexError:
                continue
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'ddlDomains')))
            sel = Select(elem)
            # sel.select_by_visible_text(i[0])
            sel.select_by_visible_text('demo.cpanel.com')
            elem = self.driver.find_elements_by_css_selector(
                'input[name="path"]')[0]
            elem.clear()
            elem.send_keys(i[1].lstrip('/'))
            if i[2].split('/')[-1] == '$1':
                elem = self.driver.find_element_by_id('wildcard')
                elem.click()
                i[2] = i[2].rstrip('$1')
            elem = self.driver.find_element_by_id('url')
            elem.clear()
            elem.send_keys(i[2])
            elem.send_keys(Keys.RETURN)
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'lnkReturn')))
            elem.click()


class installSSL(cPanelController):
    def __init__(self, ur, us, ps, d, pfx, pfxps):
        cPanelController.__init__(self, ur, us, ps)
        self.domain = d
        self.cert = self.pfx2cert(pfx, pfxps)
        self.gotoMenu('item_ssl_tls')
        self.install()

    @staticmethod
    def pfx2cert(pfx, pfxps):
        pfx = crypto.load_pkcs12(
            open(path.join(getcwd(), pfx), 'r').read(), pfxps)
        crt = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                      pfx.get_certificate())
        pvt = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
        return [crt, pvt]

    @staticmethod
    def parseSSLConf(self):
        return json.loads(open('configSSL.json').read())

    def install(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'selectdomain')))
        sel = Select(elem)
        sel.select_by_value(self.domain)
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'incert')))
        sleep(1)
        elem.clear()
        elem.send_keys(self.cert[0])
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'inpvtk')))
        sleep(1)
        elem.clear()
        elem.send_keys(self.cert[1])


if __name__ == "__main__":
    ap = ArgumentParser(epilog='', description='')
    ap.add_argument('command', help='createdb,addom,addssl')
    ap.add_argument('url', help='The url of cPanel')
    ap.add_argument('user', help='The user')
    ap.add_argument('--passw',
                    '-p',
                    default=False,
                    help="If you don't put the pass, will be prompt")
    ap.add_argument('--ssl_dom', '-S', default=False, help='')
    ap.add_argument('--pfx', '-x', default=False, help='')
    ap.add_argument(
        '--pfxps',
        '-P',
        default=False,
        help="If you don't put the pass of the pfx, will be prompt")
    p = ap.parse_args()
    if not p.passw:
        stdout.write('Password: ')
        p.passw = stdin.readline()
    if p.command == 'createdb' or p.command == 'migrate':
        d = createDatabase(p.url, p.user, p.passw)
    if p.command == 'addom' or p.command == 'migrate':
        d = createAdditionalDomains(p.url, p.user, p.passw)
    if p.command == 'addfiles' or p.command == 'migrate':
        d = uploadFilesToAccount(p.url, p.user, p.passw)
    if p.pfx and p.ssl_dom and p.pfxps and p.command == 'addssl':
        d = installSSL(p.url, p.user, p.passw, p.ssl_dom, p.pfx, p.pfxps)
    elif p.command == 'addssl':
        stdout.write('Faltan argumentos\n')
