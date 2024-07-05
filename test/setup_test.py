# nopep8 is a annotation to AUTOPEP8 not move import lines to top of this file, and prevent directory importation of these respectives files
import sys
import os
from os.path import join, dirname, realpath, normpath
import subprocess
import shlex
import io
import copy
import hashlib
import platform
from datetime import date
import unittest
from unittest.mock import Mock, patch, call

# Find relative directory of project
ROOT_DIRECTORY = os.getcwd()
# Insert specific directory of tests
sys.path.insert(0, ROOT_DIRECTORY)
sys.path.insert(0, join(join(ROOT_DIRECTORY, "src"), ''))


CURRENT_DIRECTORY = dirname(realpath(__file__))
INPUT_DIRECTORY = join(join(dirname(realpath(__file__)), "input"), '')
OUTPUT_DIRECTORY = join(join(dirname(realpath(__file__)), "output"), '')


from src.cfg.basic_block import BasicBlock  # nopep8


# Simplify de creation process of basic block
def create_bb(
        id: int, name: str, weight: int, number_executions: int,
        instructions: list, next_blocks):
    bb = BasicBlock()
    bb.set_basic_block(id, name, weight, number_executions,
                       instructions, next_blocks)
    return bb
