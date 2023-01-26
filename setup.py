from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')

except (IOError, ImportError):
    long_description = open('README.md').read()


classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

extras = {
    'gcs': [
        'google==3.0.0',
        'google-cloud-storage==2.7.0'
    ],
    'aws': ['boto3']
}

setup(
    name='postgres-backup',
    version='0.3.2',
    description='Automation of the creation of backups of Postgres databases',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nil-Andreu/postgres-backup',
    author='Nil Andreu',
    author_email='nilandreug@email.com',
    keywords=[
        'backup',
        'Postgres',
        'SQL',
        'database',
        'PostgreSQL',
        'Data Engineering'
    ],
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'sh',
        'pydantic==1.10.4'
    ],
    extras_require=extras,
    classifiers=classifiers,
)
