import os

def dprint(*args, **kwargs):
    debugmode = os.environ.get('DEBUG', 'off').lower()
    if debugmode not in ['on', 'true', '1']:
        return
    print(*args, **kwargs) 
