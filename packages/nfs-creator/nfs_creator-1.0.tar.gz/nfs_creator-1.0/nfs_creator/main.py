'''
nfs_creator.main
=========================

This module contains the main functions for the nfs-creator package.
'''

import sys
from nfs_creator.nfs_service import NFSService
from nfs_creator.cmd_executor import BashExecutor
from nfs_creator.nfs_installation_checker import NFSInstallChecker
from nfs_creator.firewall_settings import configure_firewall_nfs
from nfs_creator.open_permissions import nobody_permissions
from nfs_creator.package_installer import NFSInstaller, is_debian_based, is_rhel_based

class NFSCreator:
    
    def __init__(self, export_dir: str = '/var/data/'):
        self.export_dir = export_dir
    
    def init_nfs(self):
        ''' A function to create an nfs share. '''
        
        if NFSInstallChecker.is_installed():
            print('✅ : NFS package is already installed!')
        else:
            print('✅ : Installing nfs package...')
            NFSInstaller.install_nfs_package()
        
        NFSService.enable_start_service()
        
        print('✅ : NFS server installed and services enabled/started!')
    
    def create_nfs(self):
        ''' A function to create an nfs share. '''
        
        self.init_nfs()
        
        print('ℹ : Creating an nfs share...')
        _, error = BashExecutor.execute_cmd(f'sudo mkdir -p {self.export_dir}')
        if error.decode('utf-8'):
            sys.exit(f'❌ : An error occurred while creating the export directory!. {error.decode("utf-8")}')
        
        _, error = BashExecutor.execute_cmd(f'sudo chmod -R 777 {self.export_dir}')
        if error.decode('utf-8'):
            sys.exit(f'❌ : An error occurred while setting permissions on the export directory!. {error.decode("utf-8")}')
        
        print('✅ : NFS share created successfully!')

        export_cmd = f'{self.export_dir}  *(rw,sync,no_root_squash,no_subtree_check,insecure)'
        _, error = BashExecutor.execute_cmd(f'echo "{export_cmd}" | sudo tee -a /etc/exports')
        if error.decode('utf-8'):
            sys.exit(f'❌ : An error occurred while adding the export to /etc/exports!. {error.decode("utf-8")}')
            
        _, error = BashExecutor.execute_cmd('sudo exportfs -a')
        if error.decode('utf-8'):
            sys.exit(f'❌ : exportfs failed!. {error.decode("utf-8")}')
        
        if is_debian_based():
            _, error = BashExecutor.execute_cmd('sudo systemctl restart nfs-kernel-server')
            if error.decode('utf-8'):
                sys.exit(f'❌ : nfs-kernel-server restart failed!. {error.decode("utf-8")}')
        
        if is_rhel_based():
            _, error = BashExecutor.execute_cmd('sudo systemctl restart nfs-server')
            if error.decode('utf-8'):
                sys.exit(f'❌ : nfs-server restart failed!. {error.decode("utf-8")}')
        
        _, error = BashExecutor.execute_cmd('sudo showmount -e')
        if error.decode('utf-8'):
            sys.exit(f'❌ : showmount command failed!. {error.decode("utf-8")}')
            

def nfs_creator(export_dir: str = '/var/data/'):
    ''' A function to create an nfs share. '''
    n = NFSCreator(export_dir)
    n.create_nfs()
    nobody_permissions(export_dir)
    configure_firewall_nfs()

if __name__ == "__main__":
    nfs_export_dir = sys.argv[1]
    nfs_creator(nfs_export_dir)