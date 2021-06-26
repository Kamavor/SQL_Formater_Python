from tqdm import tqdm
import time
import main

class SingleComponent(object):
    def __init__(self, text):
        self.text = text
        self.type = 0
        return

    def identify(self):
        tx = self.text
        if tx[0:6] == 'select':
            self = Select(tx)
        elif tx[0:4] == 'case':
            self = Case(tx)
        else:
            print(1)
        return self

class Case(object):
    def __init__(self, text):
        self.type = 10
        self.text = text
        self.elements = []
        self.exec()
        return

    def exec(self):
        tx = self.text
        i_when = tx.find('when')
        sp = [0]
        while i_when != -1:
            sp.append(i_when)
            i_when = tx.find('when', i_when + 5)
        if tx.find('else') != -1:
            sp.append(tx.find('else'))
        sp.append(tx.find('end'))
        sp.append(len(tx))
        self.text = []
        for i in range(len(sp) - 1):
            self.text.append(tx[sp[i]:sp[i + 1]])
        return self

class Try(object):
    def __init__(self, text):
        self.type = 7
        self.text = text
        self.elements = []
        self.exec()
        return

    def exec(self):
        tx = self.text
        elements = []
        els = ['begin_try', 'end_try', 'begin_catch', 'end_catch']
        for el in els:
            if tx.find(el) == -1:
                continue
            elements.append((el, tx.find(el)))
        self.text = []
        for i in range(len(elements)-1):
            self.text.append(tx[elements[i][1]:elements[i + 1][1]])
            self.elements.append(elements[i][0])
        return self


class Insert(object):
    # insert into, (<columns>), [values]
    pass
class Update(object):
    # update <tab>, set, [from], [where]
    pass
class Delete(object):
    pass
class Else(object):
    pass
class Bracket(object):
    def __init__(self, text):
        self.type = 9
        tx = text.strip()
        self.text = tx[1:len(tx)-1]
        self.elements = []
        self.exec()
        return

    def exec(self):
        # если есть еще скобки, разделить по кускам
        pass


class Select(object):
    def __init__(self, text):
        self.type = 1
        self.text = text
        self.elements = []
        self.exec()
        return

    def exec(self):
        tx = self.text
        elements = []
        els = ['select', 'from', 'where', 'group by', 'having']
        for el in els:
            if tx.find(el) == -1:
                continue
            elements.append((el, tx.find(el)))
        elements.append(('end', len(tx)))
        self.text = []
        for i in range(len(elements)-1):
            self.text.append(tx[elements[i][1]:elements[i + 1][1]])
            self.elements.append(elements[i][0])
        return self

class If(SingleComponent):
    def __init__(self):
        self.type = 2
        self.elements = ['if']
        return


text_file = open('try.txt', 'r', encoding="utf-8")
text_full = text_file.read().lower()
text_full = main.escaping_words(text_full)
text_full = main.only_spaces(text_full)

t = Try(text_full)
print(t.elements)
