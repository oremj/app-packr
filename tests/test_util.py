import os
import shutil

from nose.tools import assert_raises
from tempfile import mkdtemp
from mozdeploy import util


def test_mkdirp():
    tmp_dir = mkdtemp()
    test_dir = os.path.join(tmp_dir, 'foo', 'bar', 'baz')
    util.mkdirp(test_dir)

    assert os.path.isdir(test_dir)

    shutil.rmtree(tmp_dir)


def test_run():
    assert_raises(util.BadReturnCodeException, util.run, 'false')
    assert util.run(['echo', '-n', 'test']) == ('test', '')
