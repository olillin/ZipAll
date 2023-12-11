import shutil
import os
from sys import argv
import re
import zipfile
from pathlib import Path

for path in argv[1:]:
    if os.path.isfile(path) and path.endswith('.zip'):
        print(f'{path} is already a zip archive')
        continue
    print(f'Zipping {path}')
    name = re.sub(r'\.[^\.]+$', '', path)
    if os.path.isdir(path):
        shutil.make_archive(name, 'zip', Path(path).parent, Path(path).name)
    elif os.path.isfile(path):
        with zipfile.ZipFile(name + '.zip', 'x') as zip:
            zip.write(path, Path(path).name)
