'''
nfs_creator.check_running
==========================

This module contains functions to check if the nfs service is running.
'''

import sys
from nfs_creator.cmd_executor import BashExecutor
from nfs_creator.package_installer import  is_debian_based, is_rhel_based
from nfs_creator.nfs_installation_checker import NFSInstallChecker


class NFSService:
    ''' Enable and run the service on the system.'''
    
    debian_start_cmd = "sudo systemctl start nfs-kernel-server"
    debian_enable_cmd = "sudo systemctl enable nfs-kernel-server"
    
    rhel_start_cmd = "sudo systemctl start nfs-server"
    rhel_enable_cmd = "sudo systemctl enable nfs-server"
    
    
    @staticmethod
    def enable_start_service():
        
        if NFSInstallChecker.is_installed():
            
            if is_debian_based():
                
                _, _ = BashExecutor.execute_cmd(NFSService.debian_enable_cmd)
                
                _, error = BashExecutor.execute_cmd(NFSService.debian_start_cmd)
                if error.decode('utf-8'):
                    sys.exit(f"❌ Error starting nfs-kernel-server: {error}")
            
            elif is_rhel_based():
                
                _, _ = BashExecutor.execute_cmd(NFSService.rhel_enable_cmd)
                
                _, error = BashExecutor.execute_cmd(NFSService.rhel_start_cmd)
                if error.decode('utf-8'):
                    sys.exit(f"❌ Error starting nfs-server: {error}")
                
            
            else:
                sys.exit("❌ This script is only compatible with RPM-based and Debian-based Linux distributions.")
        