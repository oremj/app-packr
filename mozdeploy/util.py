import os
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


def cleanup(releases_dir, build_id, keep=5):
    if keep == 0:
        return

    releases = os.listdir(releases_dir)
    releases.sort()

    removed = 0
    for r in releases[:-keep]:
        if r != build_id:
            run(['rm', '-rf', os.path.join(releases_dir, r)])
            removed += 1

    print "Removed %d builds" % removed
