import os

from .util import run


def git_clone_to_version(app_dir, repo, ref):
    run(['git', 'clone', repo, app_dir])
    run(['git', 'reset', '--hard', ref], cwd=app_dir)


def create_virtualenv(build_dir):
    run(['virtualenv', '--distribute', '--never-download',
         '%s/venv' % build_dir])


def pip_install(build_dir, requirements):
    pip = os.path.join(build_dir, 'venv/bin/pip')
    flags = ['--exists-action=w',
             '--no-deps',
             '--no-index',
             '--download-cache=/tmp/pip-cache',
             '-f', 'https://pyrepo.addons.mozilla.org']
    
    if requirements:
        flags += ['-r', requirements]

    run([pip, 'install'] + flags + ['virtualenv'])


def relocatable_virtualenv(build_dir):
    venv = os.path.join(build_dir, 'venv')
    python = os.path.join(venv, 'bin/python')
    run([python, '/usr/bin/virtualenv', '--relocatable', venv])


def install_pip_reqs(build_dir, requirements):
    create_virtualenv(build_dir)

    pip_install(build_dir, requirements)

    run(['rm', '-f',
         os.path.join(build_dir,
                      'venv/lib/python2.6/no-global-site-packages.txt')])
    relocatable_virtualenv(build_dir)


def python_app_package(app, version, repo, build_dir,
                       requirements=None, overlay_dir=None, extra=None):
    """
    Clones app and creates virtualenv
    requirements: this is relative to the clone
    overlay_dir: directory containing settings, etc. It will be rsync'd on top
                 of the app clone. (None means no overlay)
    """

    app_dir = os.path.join(build_dir, app)

    git_clone_to_version(app_dir, repo, version)

    if requirements:
        requirements = os.path.join(app_dir, requirements)

    install_pip_reqs(build_dir, requirements)
    
    if overlay_dir:
        run(['rsync', '-av', '%s/' % overlay_dir, app_dir])

    if extra:
        extra(build_dir)
