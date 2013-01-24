from mozdeploy import build


def test_get_clean_version():
    v = build.get_clean_version('abcABC123-.!@#$')
    assert v == 'abcABC123-.....'


def test_get_build_id():
    ref = '1a2b3c4d5e6f'
    build_id = build.get_build_id(ref)

    ts, ref_ = build_id.split('-')
    
    assert ref_ == ref[:10]
    int(ts)


def test_build_app():
    pass


def test_compress_dir():
    pass


def test_set_latest():
    pass


def test_cleanup():
    pass
