# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

import pyodbc
import text_work as tw
import time

text = r''
def conection_test():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=10.121.96.30;DATABASE=USI_KT;UID=admin;PWD=1;')
    cur = cnxn.cursor()
    cur.execute("select id_account, account from dbo.account")
    row = cur.fetchone()
    if row:
        print(row)

def only_spaces(x: str):
    x = x.replace(chr(9), ' ').replace(chr(13), ' ').replace(chr(10), ' ').replace('(', ' ( ').replace(')', ' ) ')
    while x.find('  ') != -1:
        x = x.replace('  ', ' ')
    complex_exp = ['begin transaction', 'begin try', 'begin transaction', 'begin catch', 'end try', 'end catch']
    for exp in complex_exp:
        x.replace(exp, exp.replace(' ', '_'))
    return x

def escaping_words(x: str):
    quotes = ['\'', '\"']
    special_commands = ['if', 'else', 'while', 'declare', 'exec', 'insert', 'update', 'select', 'open', 'fetch',
                        'print', 'close', 'deallocate', 'delete', 'set', 'return', 'raiserror', 'begin', 'create',
                        'values']
    for quote in quotes:
        ind1 = x.find(quote)
        # x = x.replace(quote*3, quote*2 + ' ' + quote)
        while ind1 != -1:
            ind2 = x.find(quote, ind1+1)
            if ind2 == -1:
                raise Exception('кавычки не парные (' + x[ind1-2:ind1+10] + ')')
            # if x[ind2:ind2+1] == quote*2:
              #   ind2 += 2
              #   continue
            for w in special_commands:
                if x[ind1:ind2].find(w) != -1:
                    x = x[:ind1] + x[ind1:ind2].replace(w, '?' + w[:]) + x[ind2:]
                    ind2 += 1
            ind1 = x.find(quote, ind2+1)
    return x



if __name__ == '__main__':
    text_file = open('text_req.txt', 'r', encoding="utf-8")
    # text_file = open('1t.txt', 'r', encoding="utf-8")
    text_full = text_file.read().lower()
    text_full = only_spaces(text_full)
    text_full = escaping_words(text_full)
    # print(text_full)
    s = tw.Segment(text_full)
    s.create_children()
    # a = s._find_object_('swagger')
    s.show_all()