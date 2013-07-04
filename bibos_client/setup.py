from setuptools import setup

setup(
    name='bibos_client',
    version='0.0.1.12',
    description='Clients for the BibOS system',
    url='https://github.com/magenta-aps/',
    author='C. Agger and J.U.B. Krag, Magenta ApS',
    author_email='carstena@magenta-aps.dk',
    license='GPLv3',
    packages=['bibos_client'],
    install_requires=['netifaces', 'bibos_utils', 'lockfile'],
    scripts=['bin/bibos_register_in_admin', 'bin/bibos_upload_packages',
            'bin/bibos_upload_dist_packages',
            'bin/register_new_bibos_client.sh',
            'bin/bibos_find_gateway',
            'bin/jobmanager'],
    zip_safe=False
)
