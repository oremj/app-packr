from distutils.core import setup


setup(
    name='mozdeploy',
    version='0.0.2',
    description='Deploy tools',
    author='Jeremy Orem',
    author_email='oremj@mozilla.com',
    scripts=['scripts/mozdeploy-build-app',
             'scripts/mozdeploy-install-app'],
    packages=['mozdeploy']
)
