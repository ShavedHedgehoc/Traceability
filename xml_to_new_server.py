import os
import time
import pyodbc as p
import zipfile
from zipfile import ZipFile as zf
import xml.etree.ElementTree as ET


def GetCount(wd):
    files = os.listdir(wd)
    count = 0
    for one_file in files:
        if zipfile.is_zipfile(one_file):
            count += 1
    return count


if __name__ == '__main__':

    doctypes = [
        'VzveshivanieBezPechatiTest',
        'VzveshivaniePechatTest',
        'ZagruzkaEmkosteiVApparat',
        'Vzveshivanie',
        'VzveshivanieKolpino',
        'Priemka',
        'PriemkaT2',

        
    ]

    # server = 'srv-webts'
    # database = 'testdb'
    # # database = 'Load_data_test'
    # conn = p.connect(
    #     'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
    #     server + ';DATABASE='+database+';Trusted_Connection=yes;'
    # )

    # server = '192.168.0.108'
    # database = 'maindb'
    # user = 'data_upload'
    # password = '!python497'
    # conn = p.connect(
    #     'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
    #     server + ';DATABASE='+database+';UID='+user+';PWD='+password+';'
    # )
    server = 'localhost'
    # port = '1402'
    database = 'cleverdata'
    user = 'sa'
    password = '<Strongpass123456>'
    # database = 'Load_data_test'
    conn = p.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
        server + ';DATABASE=' +
        database+';UID='+user+';PWD='+password+';'
    )
    cursor = conn.cursor()

    extrcount = 0
    skipcount = 0
    filecount = 0
    
    work_directory = os.getcwd()
    
    zfiles = GetCount(work_directory)
    files = os.listdir(work_directory)

    for one_file in files:
        if zipfile.is_zipfile(one_file):
            filecount += 1
            with zf(one_file) as myfile:
                f = myfile.namelist()
                myfile_count = len(myfile.infolist())
                incount = 0
                for ff in f:
                    incount += 1
                    if ff[0:7] == 'doc_new':
                        extrcount += 1
                        op_file = myfile.open(ff)
                        tree = ET.parse(op_file)
                        tree = tree.getroot()
                        if tree.attrib['documentTypeName'] in doctypes:
                            mf = ET.tostring(tree,
                                             encoding='unicode',
                                             method='xml'
                                             )
                            sql = "EXEC DocumentCompletedXml @documentXml = ?, @result=? "
                            params = (mf, 0)
                            cursor.execute(sql, params)
                            cursor.commit()
                        else:
                            skipcount += 1
                    else:
                        skipcount += 1
                    print("\r\x1b[K"+'Перебрано %s файлов из %s' %
                          (incount, myfile_count), end=''
                          )
                print('')
            print("\r\x1b[K"+('Обработано %s архивных файлов из %s' %
                              (filecount, zfiles)), end=''
                  )
            print('')
    print('')
    print('Извлечено файлов: %s' % extrcount)
    print('Пропущено файлов: %s' % skipcount)
    conn.close()
