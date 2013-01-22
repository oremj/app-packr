import os
from tempfile import NamedTemporaryFile

import requests

from .util import cleanup, mkdirp, run


def get_build_id(pkgroot, build_id):
    if build_id != 'LATEST':
        return build_id

    r = requests.get('%s/LATEST' % pkgroot)
    r.raise_for_status()
    return r.text.strip()


def build_exists(app_dir, build_id):
    return os.path.isdir(os.path.join(app_dir, build_id))


def fetch(pkgroot, build_id):
    r = requests.get('%s/%s/release.tar' % (pkgroot, build_id))
    r.raise_for_status()
    return r.content


def uncompress(content, releases_dir):
    with NamedTemporaryFile() as f:
        f.write(content)
        f.flush()
        run(['tar', 'xf', f.name, '-C', releases_dir])


def symlink_current(app_dir, build_id):
    run(['ln', '-snf', os.path.join('releases', build_id), 'current'],
        cwd=app_dir)


def run_postinstall(releases_dir, build_id):
    build_dir = os.path.join(releases_dir, build_id)
    print build_dir
    if os.path.isfile(os.path.join(build_dir, '.postinstall')):
        print "RUNNING"
        run(['/bin/bash', '.postinstall'], cwd=build_dir)


def install_app(pkghost, env, app_dir, app, build_id, keep=5):
    releases_dir = os.path.join(app_dir, 'releases')
    mkdirp(releases_dir)

    pkgroot = '%s/%s/%s' % (pkghost, env, app)

    build_id = get_build_id(pkgroot, build_id)

    if not build_exists(app_dir, build_id):
        content = fetch(pkgroot, build_id)
        uncompress(content, releases_dir)

    symlink_current(app_dir, build_id)
    run_postinstall(releases_dir, build_id)
    cleanup(releases_dir, build_id, keep)
