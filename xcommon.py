# (c)2025  Henrique Moreira

""" xcommon -- simple functions
"""

import unidecode

def dprint(cond, *args, **kwargs):
    assert isinstance(cond, (bool, int)), "condition is boolean or integer"
    if not cond:
        return False
    print(*args, **kwargs)
    return True

def simple_ascii(astr, default="-"):
    """ Returns string without accents
    """
    if astr is None:
        return default
    if isinstance(astr, (tuple, list)):
        return [simple_ascii(elem, default) for elem in astr]
    if isinstance(astr, str):
        return unidecode.unidecode(astr)
    return astr

if __name__ == "__main__":
    print("Import me!")
