import re

regexx = re.compile("a(b|c)*a")
input_str = input("Enter sentence:")
if regexx.match(input_str):
    print("It forms part of")
else:
    print('Okay dokay')
