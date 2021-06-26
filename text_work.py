
import re


def min_f(x1: int, x2: int):
    if x1 == -1:
        return x2
    elif x2 == -1:
        return x1
    else:
        return min(x1, x2)


def min3(x1: int, x2: int, x3: int):
    if x1 == x2 == x3 == -1:
        return -1
    else:
        m = 1000000
        if x1 == -1:
            x1 = m
        if x2 == -1:
            x2 = m
        if x3 == -1:
            x3 = m
    return min(x1, x2, x3)


def bracket_hider(text: str):
    text = ' ' + text + ' '
    res = []
    offset_text = 0  # нужно для учета убранного из расмотрения текста
    full_text = text
    bef = text.find('begin')
    cef = text.find('case')
    brf = text.find('(')
    bracket_index = min3(bef, cef, brf)
    if bracket_index == -1:
        return res
    else:
        if bracket_index == bef:
            b_type = 1
            close = 'end'
        elif bracket_index == cef:
            b_type = 2
            close = 'end'
        else:  # brf
            b_type = 3
            close = ')'
    while bracket_index != -1:
        bracket_balance = 1
        min_b = bracket_index + 1  # / () begin case не важно
        while bracket_balance != 0:
            if b_type == 3:
                open_bi = text.find('(', min_b)
            else:
                b = text.find('begin', min_b)
                c = text.find('case', min_b)
                open_bi = min_f(b, c)
            close_bi = text.find(close, min_b)
            if close_bi == open_bi == -1:
                return res
                # raise Exception('Ошибка синтаксиса')
            elif (open_bi < close_bi) and (open_bi != -1):
                bracket_balance += 1
                min_b = open_bi + 1
            else:
                bracket_balance -= 1
                min_b = close_bi + 1
        text = text[0:bracket_index] + '[expr]' + text[close_bi + len(close):]
        res.append((bracket_index - 1 + offset_text, close_bi - 1 + offset_text + len(close)))
        offset_text += close_bi - bracket_index - len('[expr]') + len(close)
        bef = text.find('begin')
        cef = text.find('case')
        brf = text.find('(')
        bracket_index = min3(bef, cef, brf)
        if bracket_index == bef:
            close = 'end'
            b_type = 1
        elif bracket_index == cef:
            close = 'end'
            b_type = 2
        else:  # brf
            close = ')'
            b_type = 3
    res.sort()
    return res

class Segment(object):
    def __init__(self, text, parent: object = None, kind: str = 'procedure', offset: int = -1):
        self.parent = parent
        self.offset = offset
        self.kind = kind
        self.children = []
        self.text = text
        self.len = len(text)
        if kind == 'procedure':
            self.p_start = 0
            self.p_end = self.len
            self.primary = self
        else:
            self.p_start = parent.text.find(text)
            if self.p_start == -1:
                self.p_start = parent.parent.text.find(text)
                self.p_start += parent.parent.p_start
            else:
                self.p_start += parent.p_start
            if self.p_start == -1:
                print('ошибка')
            self.p_end = self.p_start + len(text)
            self.primary = self.parent.primary

    def _find_object_(self, text):
        objs = []
        for el in self.children:
            if el.text.find(text) != -1:
                objs.append(el)
        return objs


    def remove_brackets(self, bracket):
        if bracket not in ('begin', 'begin_transaction', 'begin_try', 'begin_catch'):
            return self
        elif bracket == 'begin':
            x = self.text
            x = x[x.find('begin')+5:x.rfind('end')-1]
            self.text = x
        else:
            x = self.text
            # todo доделать брекеты
            x = x[x.find(bracket)+len(bracket):x.rfind('end')-1]
            self.text = x
        return self

    def show_all(self):
        try:
            count = len(self.children)
        except:
            count = 1
        if self.kind == 'begin':
            print(chr(9)*self.offset + 'begin')
        if count == 0:
            # ! print('[' + str(self.p_start) + ' : ' + str(self.p_end) + ']')
            print(chr(9)*self.offset + self.text)
        else:
            if self.kind not in ('begin', 'procedure'):
                # ! print('[' + str(self.p_start) + ' : ' + str(self.p_end) + ']')
                print(chr(9)*self.offset + self.text)
                if self not in self.parent.children:
                    print('?')
            for obj in self.children:
                try:
                    obj.show_all()
                except:
                    obj.children.show_all()
        if self.kind == 'begin':
            # ! print('[' + str(self.p_start) + ' : ' + str(self.p_end) + ']')
            print(chr(9)*self.offset + 'end')
        return 1

    def create_children(self):
        # найти все вхождения слов
        part = []
        special_commands = ['if', 'else', 'while', 'declare', 'exec', 'insert', 'update', 'select', 'open', 'fetch', 'print',
                            'close', 'deallocate', 'delete', 'set', 'return', 'raiserror', 'begin', 'create', 'values',
                            'begin_transaction', 'begin_try', 'begin_catch']

        gaps = bracket_hider(self.text)
        for command in special_commands:
            for ind in [m.start() for m in re.finditer(' ' + command + ' ', ' ' + self.text + ' ')]: # todo: индекс считается неправильно
                ind_hidden = False
                for gap in gaps:
                    if gap[0] < ind < gap[1]:
                        ind_hidden = True
                if not ind_hidden:
                    part.append((ind, command))
        part.sort()
        for i in range(0, len(part)):
            if i == len(part) - 1:  # последний
                self.children.append(Segment(self.text[part[i][0]:], self, part[i][1], self.offset + 1))
            else:
                self.children.append(Segment(self.text[part[i][0]:part[i+1][0]], self, part[i][1], self.offset + 1))
        self.subm_child()
        return 1

    def subm_child(self):
        elem = 0
        need_to_connect = False
        while elem < len(self.children):
            if need_to_connect:
                obj = unconnected_obj
            else:
                obj = self.children[elem]
                need_to_connect = False
            # todo сегмент типа select, update, exec и другие должны стать классами соответствующего типа
            if elem != len(self.children) - 1:
                if obj.kind in ('if', 'else', 'while', 'insert'):
                    next_obj = self.children[elem + 1]
                    if need_to_connect:
                        next_obj.offset += 1
                    if next_obj.kind in ('begin', 'begin_transaction', 'begin_try', 'begin_catch'):
                        obj.children = Segment(next_obj.remove_brackets(next_obj.kind).text, obj, next_obj.kind, obj.offset + 2)
                        obj.children.create_children()
                        self.children.remove(next_obj)
                    else:
                        next_obj.offset += 1
                        obj.children.append(next_obj)
                        self.children.remove(next_obj)
                        if next_obj.kind in ('insert', 'if'):
                            need_to_connect = True
                            unconnected_obj = next_obj
                            unconnected_obj.parent = obj
                            elem -= 1
                        else:
                            need_to_connect = False
            elem += 1
        return 1


