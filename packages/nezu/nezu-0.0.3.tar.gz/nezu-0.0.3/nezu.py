from inspect import currentframe

debug_mode = True


def debug(*keys, note = ...):
    global debug_mode
    if debug:
            FRAME = currentframe().f_back
            LINE = FRAME.f_lineno
            GLOB = FRAME.f_globals
            # globals()
            # print(GLOB)

            prfx = f'@{LINE}'
            desc = ''. join([f'  |  {key}' + (f':{type(GLOB[key]).__name__} {GLOB[key]}'if key in GLOB else ':undefined')for key in keys])
            sufx = f'  |  << {note} >>' if note != ... else ''

            print(f'{prfx}{desc}{sufx}')

if __name__ == '__main__':
      
    x = 5
    d = debug

    d('x')
    d('y')
