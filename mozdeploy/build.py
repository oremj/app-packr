import os
import time

from util import run


def get_build_id(version):
    return ("%d-%s" % (time.time(), version))[:31]


def build_app(command, version, build_id, build_dir):
    """command should be a format string i.e., ./build_app %s %s %s"""
    run(command % (version, build_id, build_dir), shell=True)


def compress_dir(hostroot, build_dir, build_id):
    build_host_dir = os.path.join(hostroot, build_id)
    run(['mkdir', '-p', build_host_dir])
    run(['tar', 'cf', '%s/release.tar' % build_host_dir,
         '-C', build_dir, build_id])


def set_latest(hostroot, build_id):
    with open(os.path.join(hostroot, 'LATEST'), 'w') as f:
        f.write(build_id)


def package_app(hostroot, command, version, build_dir, env, app):
    app_hostroot = os.path.join(hostroot, env, app)
    build_id = get_build_id(version)
    build_app(command, version, build_id, build_dir)
    compress_dir(app_hostroot, build_dir, build_id)
    set_latest(app_hostroot, build_id)
