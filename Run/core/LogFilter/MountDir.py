# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
from cryptocode import decrypt


def bash_comm():
    """define bash comment"""
    key = os.listdir(os.path.join(rootPath, '.pw'))[0]
    with open(os.path.join(rootPath, '.pw', key), 'r') as readfile:
        comm = readfile.readlines()
        mount_comm = comm[0][:-1]
        umount_comm = comm[1][:-1]
    return key, mount_comm, umount_comm


def mount_log():
    """mout server log to /log"""
    key, mount_comm, umount_comm = bash_comm()
    os.system(decrypt(mount_comm, key))


def umount_log():
    """unmount server log"""
    key, mount_comm, umount_comm = bash_comm()
    os.system(decrypt(umount_comm, key))
