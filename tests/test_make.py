import os
from shutil import rmtree
from tempfile import mkdtemp

from mozdeploy import make


def test_build_python_app_package():
    build_dir = mkdtemp()
    make.python_app_package('mozdeploy', 'origin/master',
                            'git://github.com/oremj/mozdeploy.git', build_dir)

    assert os.path.isdir(os.path.join(build_dir, 'mozdeploy', '.git'))
    assert os.path.isfile(os.path.join(build_dir, 'venv', 'bin', 'python'))

    rmtree(build_dir)


