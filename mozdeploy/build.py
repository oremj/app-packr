import os
import re
import time

from .util import mkdirp, run
import util


def get_clean_version(version):
    return re.sub(r'[^A-Za-z0-9\.-]', '.', version)


def get_build_id(version):
    return ("%d-%s" % (time.time(), get_clean_version(version)))[:21]


def build_app(command, version, build_id, build_dir):
    """command should be a format string i.e., ./build_app %s %s %s"""
    command = command.format(version=version, build_id=build_id,
                             build_dir=build_dir)

    print "Running: %s" % command
    install_dir = os.path.join(build_dir, build_id)
    mkdirp(install_dir)
    out, err = run(command, stderr_to_stdout=True, shell=True, cwd=install_dir)

    with open(os.path.join(build_dir, build_id, '.build.out'), 'w') as f:
        f.write(out)


def compress_dir(hostroot, build_dir, build_id):
    build_host_dir = os.path.join(hostroot, build_id)
    mkdirp(build_host_dir)
    run(['tar', 'cf', '%s/release.tar' % build_host_dir,
         '-C', build_dir, build_id])


def set_latest(hostroot, build_id):
    with open(os.path.join(hostroot, 'LATEST'), 'w') as f:
        f.write(build_id)


def cleanup(app_hostroot, build_dir, build_id, keep):
    build_dir = os.path.join(build_dir, build_id)
    run(['rm', '-rf', build_dir])

    util.cleanup(app_hostroot, build_id, keep)


def package_app(hostroot, command, version, build_dir, app, keep=5):
    app_hostroot = os.path.join(hostroot, app)
    build_id = get_build_id(version)
    build_app(command, version, build_id, build_dir)
    compress_dir(app_hostroot, build_dir, build_id)
    set_latest(app_hostroot, build_id)
    cleanup(app_hostroot, build_dir, build_id, keep)
