""" Файл для моих личных тестов различного функционала. """
import re


el = '123 sdfsf'
print(int(re.search(r'\d* ', el).group()))