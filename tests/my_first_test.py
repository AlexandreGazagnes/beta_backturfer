#!/usr/bin/env python3
# coding: utf-8

from src import * 
import pytest

info(os.getcwd())

# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
