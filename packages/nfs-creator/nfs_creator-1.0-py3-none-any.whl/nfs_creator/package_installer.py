'''
nfs_creator.nfs_installer
==========================

This module contains functions to install the nfs-utils package.
'''

import sys, distro
from nfs_creator.cmd_executor import BashExecutor

RHEL_BASED_OS   = ['CentOS Linux', 'Red Hat Enterprise Linux', 'Fedora', 'Rocky Linux', 'AlmaLinux', 'centos']
DEBIAN_BASED_OS = ['Ubuntu', 'Debian', 'Linux Mint']

RHEL_BASED_OS   = [os.lower() for os in RHEL_BASED_OS]
DEBIAN_BASED_OS = [os.lower() for os in DEBIAN_BASED_OS]

try:
    CURRENT_OS_NAME = distro.name().lower()
    CURRENT_OS_ID   = distro.id().lower()
except AttributeError as e:
    sys.exit('ERROR: This script is only compatible with Linux distributions.')

def is_debian_based():
    return CURRENT_OS_NAME in DEBIAN_BASED_OS or CURRENT_OS_ID in DEBIAN_BASED_OS

def is_rhel_based():
    return CURRENT_OS_NAME in RHEL_BASED_OS or CURRENT_OS_ID in RHEL_BASED_OS

class NFSInstaller:
    
    rhel_installation_cmd = 'sudo yum install nfs-utils -y'
    debain_installation_cmd = 'sudo apt-get install nfs-common -y && sudo apt install nfs-server -y'
    
    @staticmethod
    def install_nfs_package():
        ''' A function to install the nfs-utils/common package. '''
        
            
        if is_rhel_based():
            _, error = BashExecutor.execute_cmd(NFSInstaller.rhel_installation_cmd)
            if error.decode('utf-8'):
                sys.exit(f'❌ : An error occurred while installing nfs-utils!. {error.decode("utf-8")}')
            print('✅ : nfs-utils has been installed successfully!')
            
        elif is_debian_based():
            
            _, error = BashExecutor.execute_cmd(NFSInstaller.debain_installation_cmd)
            if error.decode('utf-8'):
                sys.exit(f'❌ : An error occurred while installing nfs-common!. {error.decode("utf-8")}')
            print('✅ : nfs-common has been installed successfully!')
            
        else:
            sys.exit('This script is only compatible with RPM-based and Debian-based Linux distributions.')
    