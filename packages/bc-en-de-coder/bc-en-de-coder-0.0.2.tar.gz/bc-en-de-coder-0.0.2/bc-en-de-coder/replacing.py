import re
import random
from extract import extract_text_from_pdf

class Decoder:
    def decode(text, number_mapping):
        for original_number, random_value in number_mapping.items():
            text = re.sub(r'\b' + re.escape(random_value) + r'\b', original_number, text)
    
    return text
class Encoder:
    def encode(text):
        number_pattern = re.compile(r'\b\d+\b')
        numbers = number_pattern.findall(text)
        number_mapping = {}
        for number in numbers:
            if number not in number_mapping:
                random_value = ''.join(random.choice('0123456789') for _ in range(10))
                number_mapping[number] = random_value
            
            text = re.sub(r'\b' + re.escape(number) + r'\b', number_mapping[number], text)
        return text, number_mapping

# text = "replace the number 20 ,80,60 ,90 and 60,56,65,65,65,56,90 78 98 678 678 876 "
# pdf_text = extract_text_from_pdf("data.pdf")
# modified_text, mapping = encode(pdf_text)

# print("Modified Text:")
# print(modified_text)

# print("\nNumber Mapping:")
# print(mapping)

# original_text = decode(modified_text, mapping)

# print("Reverted Text:")
# print(original_text)
