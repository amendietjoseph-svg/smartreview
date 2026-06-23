import os
import shutil

# Copier tous les fichiers backend à la racine pour Railway
src = 'backend'
for f in os.listdir(src):
    s = os.path.join(src, f)
    d = f
    if os.path.isfile(s):
        shutil.copy2(s, d)
        print(f'Copied {f}')

print('Done!')