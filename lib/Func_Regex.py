# -*- coding: utf-8 -*-
import re as re
import numpy as np


class Regex:
    def __init__(self):
        pass

    def extract_numbers(self, string):
        numbers = re.findall(r'\d+', string)

        return "".join(numbers)

    def extract_characters(self, string, return_type):
        try:
            characters = re.findall(r'[a-zA-Z]+', string)

            if return_type == 'str':
                return "".join(characters)
            elif return_type == 'list':
                return characters
        except:
            if string is None:
                return np.nan

    def extract_head_with_nums_and_chars(self, string):
        num = re.findall(r'^\d+', string)
        chars = self.extract_characters(string, return_type='list')
        # chars = re.findall(r'[^\d\W]+', string)
        try:
            head = '{}{}'.format(num[0], chars[0])
        except:
            head = chars[0]

        return head
