#!/usr/bin/env python3
"""
Fabric script to create and distribute an archive to web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os


# Remote servers
env.hosts = ['100.26.155.19', '100.26.155.19']


def do_pack():
    """
    Create a compressed archive of the web_static folder
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_{}.tgz'.format(timestamp)
    
    local('mkdir -p versions')
    result = local('tar -czvf {} web_static'.format(archive_path))
    
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """
    Distribute the archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        # Upload the archive to the remote server
        put(archive_path, '/tmp/')
            
        # Extract the archive to a new folder
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/{}'.format(filename[:-4])
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(folder_name))
        
        return True
    except Exception as e:
        print(str(e))
        return False
    
    
def deploy():
    """
        Create and distribute the archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
        
