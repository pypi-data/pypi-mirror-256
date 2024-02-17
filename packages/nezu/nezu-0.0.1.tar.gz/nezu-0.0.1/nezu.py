from inspect import currentframe

debug_mode = True

x = 5

def debug(*keys, note = ...):
    global debug_mode
    if debug:
            LINE = currentframe().f_back.f_lineno
            GLOB = globals()

            prfx = f'@{LINE}'
            desc = ''. join([f'  |  {key}' + (f':{type(GLOB[key]).__name__} {GLOB[key]}'if key in GLOB else ':undefined')for key in keys])
            sufx = f'  |  << {note} >>' if note != ... else ''

            print(f'{prfx}{desc}{sufx}')


d = debug

d('x')
d('y')
