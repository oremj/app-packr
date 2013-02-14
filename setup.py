from distutils.core import setup


setup(
    name='app-packr',
    version='0.0.3',
    description='Tools for building, packaging and deploy applications.',
    author='Jeremy Orem',
    author_email='oremj@mozilla.com',
    scripts=['scripts/apppackr-buildapp',
             'scripts/apppackr-installapp'],
    packages=['apppackr']
)
