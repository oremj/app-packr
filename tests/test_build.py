import os
from shutil import rmtree
from tempfile import mkdtemp

from apppackr import build


ref = '1a2b3c4d5e6f'
build_id = build.get_build_id(ref)

def test_get_clean_version():
    v = build.get_clean_version('abcABC123-.!@#$')
    assert v == 'abcABC123-.....'


def test_get_build_id():
    ts, ref_ = build_id.split('-')
    
    assert ref_ == ref[:10]
    int(ts)


def test_build_app():
    build_dir = mkdtemp()
    build.build_app('echo test_build_app > testfile', ref, build_id, build_dir)

    assert "test_build_app\n" == open(os.path.join(build_dir,
                                                   build_id,
                                                   'testfile')).read()

    rmtree(build_dir)
    

def test_compress_dir():
    build_dir = mkdtemp()
    host_dir = mkdtemp()

    build.build_app('true', ref, build_id, build_dir)
    build.compress_dir(host_dir, build_dir, build_id)

    assert os.path.isfile(os.path.join(host_dir, build_id, 'release.tar'))

    rmtree(build_dir)
    rmtree(host_dir)


def test_set_latest():
    host_dir = mkdtemp()

    build.set_latest(host_dir, build_id)

    assert build_id == open(os.path.join(host_dir, 'LATEST')).read()

    rmtree(host_dir)


def test_cleanup():
    pass
