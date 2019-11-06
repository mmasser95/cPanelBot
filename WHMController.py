#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import json
from sys import stdin, stderr, stdout
from os import getcwd, path
from random import choice
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WHMController:
    def __init__(self, cPanelName):
        self.info = self.getcPanelInfo(cPanelName)
        self.info['address'] = f'http://{self.info["name"]}/'
        self.driver = webdriver.Chrome()
        self.driver.get(self.info['address'])
        # self.logincPanel()

    def gotoHome(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a#lnkWHMLogo")))
        elem.click()

    def genPass(self):
        return ''.join([choice(self.charss) for x in range(18)])

    @staticmethod
    def getcPanelInfo(cPanelName):
        if cPanelName == 'p1':
            return {
                'name': 'hdccpa01.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'p2':
            return {
                'name': 'hdccpa02.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'p3':
            return {
                'name': 'hdccpa03.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'p5':
            return {
                'name': 'hdccpa05.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'idm':
            return {
                'name': 'hdcidm01.nunsys.net',
                'login': {
                    'user': 'root',
                    'passw': 'pruebanum1'
                }
            }
        elif cPanelName == 'spb':
            return {
                'name': 'hdcspb01.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'fvmp':
            return {
                'name': 'fvmpcp.nunsys.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        elif cPanelName == 'pruebas':
            return {
                'name': 'trycpanel.net',
                'login': {
                    'user': '',
                    'passw': ''
                }
            }
        else:
            raise Exception('Servidor Incorrecto')

    def logincPanel(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'user')))
        elem.send_keys(self.info['login']['user'])
        elem = self.driver.find_element_by_id('pass')
        elem.send_keys(self.info['login']['passw'])
        elem.send_keys(Keys.RETURN)


class createAccount(WHMController):
    def __init__(self, cPanelName):
        WHMController.__init__(self, cPanelName)
        self.charss = 'abcdefghjkmnpqrstuvwxyz23456789ABCDFGHJKMNPQRSTUVWXYZ'

        self.acconfig = self.parseConf()
        self.gotoHome()
        self.createPackage()
        self.createAccount()

    @staticmethod
    def parseConf():
        return json.loads(open('configCreateAcc.json', 'r').read())

    def saveConf(self, dom, user, pas):
        with open(path.join(getcwd(), 'Credenciales %s.txt' % dom), 'w') as f:
            txt = f"""
---------cPanel---------
URL: https://{dom}/cpanel
User: {user}
Pass: {pas}

----------FTP-----------
Server: ftp.{dom}
Puerto: 21
User: {user}
Pass: {pas}
Recomendamos utilizar Filezilla.""" % ()
            f.write(txt)

    def gotoCreatePackage(self):
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, 'Add a Package')))
        elem.click()

    def createPackage(self):
        for i in self.acconfig:
            self.gotoCreatePackage()
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'input[type="radio"][value="custom"]')))
            for d in elem:
                d.click()
            for (k, j) in i['pack']:
                elem = self.driver.find_element_by_name(k)
                if k == "cgi" and j == "no":
                    elem.click()
                    continue
                elif k == "cgi" and j == "yes":
                    continue
                elif k == "language":
                    sel = Select(elem)
                    sel.select_by_value(j)
                    continue
                elem.clear()
                elem.send_keys(j)
            self.driver.find_element_by_id('submit').click()
            self.gotoHome()

    def gotoCreateAccount(self):
        """elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'account_functions')))
        elem.click()"""
        elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, 'account_functions_create_a_new_account')))
        elem.click()

    def createAccount(self):
        for i in self.acconfig:
            self.gotoCreateAccount()
            passw = self.genPass()
            elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.ID, 'submit')))
            sel = Select(self.driver.find_element_by_id('pkgselect'))
            #sel.select_by_visible_text(i['pack']['name']) #TODO Pa proves no funciona
            sel.select_by_visible_text('default')
            for (k, j) in i['account']:
                elem = self.driver.find_element_by_id(k)
                if k == "dkim" or k == "spf" or k == "useregns" or k == "mxcheck_local" or k == 'mxcheck_remote':
                    elem.click()
                    continue
                elif k == "password" or k == "password2":
                    elem.clear()
                    elem.send_keys(passw)
                    continue
                elem.clear()
                elem.send_keys(j)
            user = self.driver.find_element_by_id('username').get_attribute(
                'value')
            self.saveConf(i['account'][0][1], user, passw)
            self.driver.find_element_by_id('submit').click()
            self.driver.find_element_by_css_selector('input[type=button]').click()
            self.gotoHome()


class addmodule(WHMController):
    def __init__(self, cPanelName):
        WHMController.__init__(self, cPanelName)


if __name__ == "__main__":
    ap = ArgumentParser(epilog="cPanel Bot", description="cPanelBot v2.1")
    ap.add_argument('command', help='create,edit,addmodule')
    ap.add_argument('cPanel', help='p1,p2,p3,p5')
    p = ap.parse_args()
    if p.command == 'create':
        c = createAccount(p.cPanel)
    elif p.command == 'addmodule':
        pass
    else:
        stdout.write('Bad command\n')
