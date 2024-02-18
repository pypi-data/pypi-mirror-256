import re
import random
import pandas as pd

class Decoder():
    def decode(self,text, number_mapping):
        for original_number, random_value in number_mapping.items():
            text = re.sub(r'\b' + re.escape(random_value) + r'\b', original_number, text)
    
        return text

    def decode_df(self, encoded_df, number_mapping):
        def decode_cell(cell):
            if isinstance(cell, str) and cell in number_mapping.values():
                for key, value in number_mapping.items():
                    if value == cell:
                        return key
            else:
                return cell

        decoded_df = encoded_df.applymap(decode_cell)
        return decoded_df

    def decode_in_ratio(self, text, number_mapping, ratio):...

class Encoder():
    def __init__(self):
        self.number_mapping = {}

    def encode_number(self, number):
        if number not in self.number_mapping:
            random_value = ''.join(random.choice('0123456789') for _ in range(10))
            self.number_mapping[number] = random_value
        return self.number_mapping[number]

    def encode_str(self, text):
        encoded_text = re.sub(r'\b\d+\b', lambda x: self.encode_number(x.group()), text)
        return encoded_text, self.number_mapping

    def encode_df(self, dataframe):
        def encode_cell(cell):
            if isinstance(cell, (int, float)):
                return self.encode_number(str(cell))
            elif isinstance(cell, str):
                return re.sub(r'\b\d+\b', lambda x: self.encode_number(x.group()), cell)
            else:
                return cell

        encoded_df = dataframe.applymap(encode_cell)
        return encoded_df, self.number_mapping


    def encode_in_ratio(self, text, ratio):...



    
