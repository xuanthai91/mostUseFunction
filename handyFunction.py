# for Logging
import time
from unittest import result


import logging
import warnings

# for data processing
# time processing
import datetime
from time import sleep
import pytz
import shutil

import json
from glob import glob
import requests
import pandas as pd
import openpyxl

# for path processing
import os

# for web url encode
import urllib.parse

import openpyxl.styles as styl


def getWhereIsMain():
    if os.path.exists(os.path.join(os.getcwd(), 'pytweet_base_path.txt')):
        with open(os.path.join(os.getcwd(), 'pytweet_base_path.txt'), 'r', encoding='utf-16') as file:
            base_path = file.read().replace('\n', '')
    else:
        base_path = os.getcwd()
    return base_path


def get_file_info():

    base_path = getWhereIsMain()

    # get main file name from setting json
    with open(os.path.join(base_path, '0_driver', 'setting.json'), encoding='utf-8') as json_file:
        data = json.load(json_file)

    logging.info('Main File -- ' + os.path.join(base_path, data['main_file']))

    wb = openpyxl.load_workbook(os.path.join(base_path, data['main_file']))
    sheet_go = wb['GO']
    login_infos = {
        'account_id': sheet_go['F4'].value,
        'login_id': sheet_go['G4'].value,
        'login_pass': sheet_go['H4'].value,
        'login_mail': sheet_go['I4'].value,
        'order_file': sheet_go['F7'].value,
        'isUpCr': sheet_go['F11'].value,
        'isGetCrURL': sheet_go['G11'].value,
        'isBulk': sheet_go['H11'].value,
        'isTw': sheet_go['I11'].value,
        'filterKey': sheet_go['I7'].value,
        'maxCR': sheet_go['F17'].value,
        'maxTW': sheet_go['G17'].value,
        'isGetTwInfo': sheet_go['J11'].value,
    }

    return login_infos


def changeCl_df(mapping_df, in_df):
    sub_df = pd.DataFrame()
    for cl in mapping_df.columns.tolist():
        if cl == 'FLAG' and 'FLAG' in in_df.columns.tolist():
            sub_df['FLAG'] = in_df['FLAG']
        else:
            if mapping_df[cl][0] != '':
                if mapping_df[cl][0] in in_df.columns.tolist():

                    sub_df[cl] = in_df[mapping_df[cl][0]]

            else:
                sub_df[cl] = ''

    sub_df.fillna('')

    return sub_df


def readMapping(mediaType='SS'):
    mainFolder_path = getWhereIsMain()

    # get main file name from setting json
    with open(os.path.join(mainFolder_path, '0_driver', 'setting.json'), encoding='utf-8') as json_file:
        setting_json = json.load(json_file)

    filePath = os.path.join(
        mainFolder_path, '0_driver', setting_json['columnMapping'])

    mapping_df = pd.read_excel(
        filePath, sheet_name='adsInfoCLMapping', header=0, engine='openpyxl')
    mapping_df = mapping_df.fillna('')
    mapping_df = mapping_df[mapping_df['FLAG']
                            == mediaType].reset_index(drop=True)

    mapping_df.fillna('')

    return mapping_df


def fommatExcelFile(filePath):
    # def style
    allCell_style = styl.NamedStyle(name="allCell_style")
    allCell_style.font = styl.Font(name="メイリオ", size=8)
    allCell_style.alignment = styl.Alignment(
        horizontal="left", vertical="center")

    # open file
    wb1 = openpyxl.load_workbook(filePath)
    for ws in wb1.worksheets:
        for row in ws:
            for cell in row:
                cell.style = allCell_style  # apply style to each cell

    # save wb
    wb1.save(filePath)
    wb1.close()


def makeDirs(inPathList):

    for path in inPathList:
        if not os.path.isdir(path):
            os.makedirs(path)
    logging.info('Create folder: DONE')


def clearFileInDirs(inPathList):
    for delFolder in inPathList:
        for filename in os.listdir(delFolder):
            file_path = os.path.join(delFolder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logging.debug('Failed to delete %s. Reason: %s' %
                              (file_path, e))


def calculate_time(func):

    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner(*args, **kwargs):

        # storing time before function execution
        begin = time.time()

        output = func(*args, **kwargs)

        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
        return output

    return inner
