#!/usr/bin/env python3
# coding: utf-8

from src import * 
import pytest

def test_pwd() : 
	print(os.getcwd())


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0