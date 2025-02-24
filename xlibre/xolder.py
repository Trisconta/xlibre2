# (c)2025  Henrique Moreira

""" xolder -- Old Excel (xls) reader; yet another xlrd wrapper!
"""

# pylint: disable=missing-function-docstring

import xlrd


class BasicObj():
    """ Basic object with a name, abstract class """
    def __init__(self, name):
        self._aname = name

    def get_aname(self):
        return self._aname


class ABook(BasicObj):
    """ Old Excel book content, wrapper """
    def __init__(self, name=""):
        super().__init__(name)
        self._workbook = None
        self.ibook = None

    def get_book_type(self):
        return "xls"

    def load(self, fname:str, debug:int=0) -> bool:
        """ Load xls book """
        if debug > 0:
            print("load():", fname)
        book = xlrd.open_workbook(fname)
        self._workbook = book
        self.ibook = OldBook(book, self._aname)
        self.ibook.first()
        return True

    def book(self):
        assert self._workbook is not None, self._aname
        return self._workbook


class OldBook(BasicObj):
    """ Old Excel book content, wrapper """
    def __init__(self, book=None, name=""):
        super().__init__(name)
        self._skel = book
        self.current = None	# Current sheet
        self._sheet_list = book._sheet_list

    def first(self):
        return self._get_by_index(0)

    def goto_sheet(self, idx=0):
        return self._get_by_index(idx)

    def _get_by_index(self, idx:int):
        sht = self._skel.sheet_by_index(idx)
        position = sht._position
        self.current = OldSheet(sht, (self._skel, position, sht.name, sht.number))
        return sht


class OldSheet(BasicObj):
    """ Old xlrd excel Sheet """
    def __init__(self, sht, tup=None):
        self._sheet = sht
        self._skel = None
        self._lines = []
        name = ""
        if tup is None:
            self._original_sheet = None
        else:
            book, position, name, number = tup
            self._original_sheet = xlrd.sheet.Sheet(book, position, name, number)
        super().__init__(name)
        self._parse_lines()

    def content(self):
        return self._sheet

    def lines(self):
        return self._lines

    def _parse_lines(self):
        if self._sheet is None:
            return False
        res, lst = [], self._sheet._cell_values
        for line in lst:
            row = [better_content(ala) for ala in line]
            res.append(row)
        self._lines = res
        return True

def better_content(new):
    """ Returns slightly improved cell content. """
    #print(":::", type(new), new)
    try:
        astr = new.rstrip()
    except AttributeError:
        astr = new
    return astr


if __name__ == "__main__":
    print("Import me!")
