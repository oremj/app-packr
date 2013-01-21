from subprocess import Popen, PIPE, STDOUT


class BadReturnCodeException(Exception):
    pass


def run(cmd, stderr_to_stdout=False, **kwargs):
    if stderr_to_stdout:
        kwargs['stderr'] = STDOUT
    else:
        kwargs['stderr'] = PIPE

    p = Popen(cmd, stdout=PIPE, **kwargs)
    out, err = p.communicate()

    if p.returncode != 0:
        raise BadReturnCodeException('Return code: %d' % p.returncode)

    return out, err


def mkdirp(d):
    run(['mkdir', '-p', d])
