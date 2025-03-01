import random

def generate_otp():
    return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPKRSTUVWXYZ', k=8))