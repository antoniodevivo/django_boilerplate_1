import os

def loaddata(file):
    print(file)
    if os.path.splitext(file)[1] == '.json' and file != 'initial_data.json':
        os.system('cmd /c "python manage.py loaddata %s"' % file)

files = os.listdir('bp_app/fixtures')
for file in files:
    loaddata(file)