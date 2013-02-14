import os
from shutil import rmtree
from tempfile import mkdtemp

from apppackr import make


def test_build_python_app_package():
    build_dir = mkdtemp()
    make.python_app_package('app-packr', 'origin/master',
                            'git://github.com/oremj/app-packr.git', build_dir)

    assert os.path.isdir(os.path.join(build_dir, 'app-packr', '.git'))
    assert os.path.isfile(os.path.join(build_dir, 'venv', 'bin', 'python'))

    rmtree(build_dir)


