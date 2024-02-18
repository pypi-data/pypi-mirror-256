from treerec.trcursor import TreeObj_Cursor

import os
if os.name=='nt':
    try:
        import win32security
    except:
        print('   ***')
        print('WARNING: on Windows systems, `pywin32` package must be installed for treerec to record files'' owners.')
        print('   ***')

C = TreeObj_Cursor()
C.mainloop()