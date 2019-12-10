#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author : GuanFu Duan
# Email : gfduan178@163.com
# Supervisor : Changge Ji
# All rights reserved 2019
# install the updating ligand charge code in system environment
# Dependencies : opemmm, pdbfixer, openbabel, pybel

if __name__ == '__main__':
    import os, getpass, shutil, sys
    # current username
    username = getpass.getuser()
    # judge whether lib library in HOME directory(mission: copy to it)
    object_file = '/home/%s/.epblib' %username
    if os.path.exists(object_file): shutil.rmtree(object_file)
    shutil.copytree('./epblib', object_file)
    bash_line = [_.rstrip() for _ in open('/home/%s/.bashrc' %username)]
    # add code path to .bashrc file
    label_path = getpass.getpass('>>>\033[1;36m Do you want to add to your path(~/.bashrc) ?\033[0m(Y/N) ')
    if label_path in ['Y', 'y', 'Yes', 'YES', 'yes']:
        if '# add by EPB CHARGE CODE installer' not in bash_line:
            if sys.version_info >= (3, 0):
                with open('/home/%s/.bashrc' %username, 'a') as bash_file:
                    bash_file.write('\n# add by EPB CHARGE CODE installer\n')
                    bash_file.write('export PATH=%s:$PATH\n' %object_file)
                    bash_file.write('export PYTHONPATH=%s' %object_file)
            else:
                bash_file = open('/home/%s/.bashrc' %username, 'a')
                bash_file.write('\n# add by EPB CHARGE CODE installer\n')
                bash_file.write('export PATH=%s:$PATH\n' %object_file)
                bash_file.write('export PYTHONPATH=%s' %object_file)
                bash_file.close()
    # judge the python version and give the suggestion
    sys.stdout.write('\tCurrent Python version:\t\033[1;31m%s\033[0m\n'
                          %('.'.join(list(map(str, sys.version_info[:3])))))
    if sys.version_info < (2, 7):
        sys.stdout.write("\033[1;31m\tYou'd better install python2.7 or high version.\033[0m\n")
