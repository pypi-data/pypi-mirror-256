import re
import random
import pandas as pd


class Decoder():
    def decode_str(self, text, number_mapping):
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

        decoded_df = encoded_df.map(decode_cell)
        return decoded_df

    
    def decode_in_ratio(self, data, ratio):
        if ratio == 0 or ratio == 1:
            raise ValueError("Ratio should not be 0 and 1")
        
        if isinstance(data, str):
            def decode_number(match):
                original_number = int(match.group())
                decoded_number = original_number / ratio
                return str(int(decoded_number)) if decoded_number.is_integer() else str(decoded_number)

            decoded_text = re.sub(r'\b\d+(\.\d+)?\b', decode_number, data)
            return decoded_text

        elif isinstance(data, pd.DataFrame):
            def decode_in_ratio_cell(cell):
                if isinstance(cell, (int, float)):
                    decoded_number = cell / ratio
                    # Remove decimal part if it's zero
                    return int(decoded_number) if decoded_number.is_integer() else decoded_number
                else:
                    return cell

            decoded_df = data.map(decode_in_ratio_cell)
            return decoded_df

        else:
            raise ValueError("Unsupported data type. Only string or DataFrame is allowed.")

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

        encoded_df = dataframe.map(encode_cell)
        return encoded_df, self.number_mapping

    
    def encode_in_ratio(self, data, ratio):
        if ratio == 0 or ratio == 1:
            raise ValueError("Ratio should not be 0 and 1")

        print("bale ba")

        if isinstance(data, str):
            def encode_number(match):
                original_number = int(match.group())
                encoded_number = original_number * ratio
                return str(encoded_number)

            encoded_text = re.sub(r'\b\d+\b', encode_number, data)
            return encoded_text

        elif isinstance(data, pd.DataFrame):
            def encode_in_ratio_cell(cell):
                if isinstance(cell, (int, float)):
                    return cell * ratio
                else:
                    return cell

            encoded_df = data.map(encode_in_ratio_cell)
            return encoded_df

        else:
            raise ValueError("Unsupported data type. Only string or DataFrame is allowed.")
