import treerec

T = treerec.TreeObj_Cursor()
T.execute('session K')
T.execute('create new Dev .')
T.execute('recroot -n T -p / treerec')
T.execute('cd $ "C:/Program Files (x86)/Steam/steamapps/common"')
T.execute('recroot -n steam .')

T.mainloop()