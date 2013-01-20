from subprocess import Popen, PIPE


class BadReturnCodeException(Exception):
    pass


def run(cmd, **kwargs):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, **kwargs)
    out, err = p.communicate()

    if p.returncode != 0:
        raise BadReturnCodeException('Return code: %d' % p.returncode)

    return out, err
