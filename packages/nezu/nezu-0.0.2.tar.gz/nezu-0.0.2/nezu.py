from inspect import currentframe

debug_mode = True


def debug(*keys, note = ...):
    global debug_mode
    if debug:
            LINE = currentframe().f_back.f_lineno
            GLOB = globals()

            prfx = f'@{LINE}'
            desc = ''. join([f'  |  {key}' + (f':{type(GLOB[key]).__name__} {GLOB[key]}'if key in GLOB else ':undefined')for key in keys])
            sufx = f'  |  << {note} >>' if note != ... else ''

            print(f'{prfx}{desc}{sufx}')

if __name__ == '__main__':
      
    x = 5
    d = debug

    d('x')
    d('y')
