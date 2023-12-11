import shutil
import os
from sys import argv
import re
import zipfile
from pathlib import Path

print()
errors = 0
for path in argv[1:]:
    if os.path.isfile(path) and path.endswith('.zip'):
        print(f'{path} is already a zip archive')
        continue
    print(f'Zipping {path}')

    # Select name
    global name
    name = re.sub(r'\.zip(?=$)', '', path)
    m = re.match(r'(?<= \()\d+(?=\)$)', name)
    global i
    if m:
        i = int(m.group(0))
        name = re.match(r'.+(?= \()', name).group(0)
    else:
        i = 0
    base_name = name

    # Zip
    if os.path.isdir(path):
        while Path(name + '.zip').exists():
            i += 1
            name = base_name + f' ({i})'
        try:
            shutil.make_archive(name, 'zip', Path(path).parent, Path(path).name)
        except PermissionError:
            errors += 1
            print(f'Cannot zip {path}, insufficient permission')
            if os.path.exists(name + '.zip'):
                os.remove(name + '.zip')
    elif os.path.isfile(path):
        name += '.zip'
        while Path(name).exists():
            i += 1
            name = base_name + f' ({i}).zip'
    
        try:
            with zipfile.ZipFile(name, 'x') as zip:
                zip.write(path, Path(path).name)
        except PermissionError:
            errors += 1
            print(f'Cannot zip {path}, insufficient permission')
            if os.path.exists(name):
                os.remove(name)

print(f'\nCompleted with {errors} error(s)\n')
if errors > 0:
    exit(1)