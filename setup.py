from distutils.core import setup


setup(
    name='mozdeploy',
    version='0.0.1',
    description='Deploy tools',
    author='Jeremy Orem',
    author_email='oremj@mozilla.com',
    scripts=['scripts/build-app',
             'scripts/install-app'],
    packages=['mozdeploy']
)
