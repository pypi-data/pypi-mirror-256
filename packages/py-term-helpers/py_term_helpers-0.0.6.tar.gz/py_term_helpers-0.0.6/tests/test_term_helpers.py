import pytest
from ipdb import set_trace
from src.py_term_helpers import terminal_size, top_wrap, star_line, kv_print
# needs the '-s' flag to run

top_wrap("TESTING")

def test_term_size():
    term_size = terminal_size()
    print(f'\nterm_size is: {term_size}')
    assert term_size 

def test_star_line():
    assert not star_line()


def test_kv_print():
    my_dict = {'key': "value"}
    assert not kv_print(my_dict)
