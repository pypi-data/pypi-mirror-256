'''
nfs_creator.open_permissions
============================

This module contains functions to open permissions on the nfs export directory.
'''

import sys
from nfs_creator.cmd_executor import BashExecutor
from nfs_creator.package_installer import is_debian_based, is_rhel_based

def nobody_permissions(export_dir: str):
    ''' A function to open permissions on the nfs export directory. '''
    
    
    print('ℹ : Opening permissions on the export directory...')
    _, error = BashExecutor.execute_cmd(f'sudo chmod -R 777 {export_dir}')
    if error.decode('utf-8'):
        sys.exit(f'❌ : An error occurred while setting permissions on the export directory!. {error.decode("utf-8")}')
    
    if is_debian_based():
        _, error = BashExecutor.execute_cmd(f'sudo chown -R nobody:nogroup {export_dir}')
        if error.decode('utf-8'):
            sys.exit(f'❌ : An error occurred while changing owner to nobody:nogroup on the export directory!. {error.decode("utf-8")}')
    
    elif is_rhel_based():
        _, error = BashExecutor.execute_cmd(f'sudo chown -R nobody:nobody {export_dir}')
        if error.decode('utf-8'):
            sys.exit(f'❌ : An error occurred while changing owner to nobody:nobody on the export directory!. {error.decode("utf-8")}')
    
    else:
        sys.exit('Unable to set permissions on the export directory!')
    
    print('✅ : Permissions for NFS export dir set successfully!')
    
    return True