from setuptools import setup, find_packages

def myversion():
    from setuptools_scm.version import SEMVER_MINOR, guess_next_simple_semver, release_branch_semver_version

    def my_release_branch_semver_version(version):
        v = release_branch_semver_version(version)
        if v == version.format_next_version(guess_next_simple_semver, retain=SEMVER_MINOR):
            return version.format_next_version(guess_next_simple_semver, fmt="{guessed}", retain=SEMVER_MINOR)
        return v

    return {
        'version_scheme': my_release_branch_semver_version,
        'local_scheme': 'no-local-version',
    }

setup(
    name='yap-gcp',
	use_scm_version=myversion,
    setup_requires=['setuptools_scm'],
    author='Hanqing Liu',
    author_email='hanliu@salk.edu',
    description='Pipelines for single nucleus methylome and multi-omic dataset.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lhqing/cemba_data',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=('doc',)),
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.tsv', '*.csv', '*.fa', '*Snakefile', '*ipynb']
    },
    install_requires=['pandas>=1.0',
                      'numpy',
                      'seaborn',
                      'matplotlib',
                      'papermill',
                      'dnaio',
                      'pysam'],
    entry_points={
        'console_scripts': ['yap=cemba_data.__main__:main',
                            'yap-internal=cemba_data._yap_internal_cli_:internal_main',
                            'yap-hisat3n=cemba_data.hisat3n.cli:main',
							'yap-gcp=cemba_data.gcp:main'],
    }
)
