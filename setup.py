# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016 MIT Probabilistic Computing Project

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# If some modules are not found, we use others, so no need to warn:
# pylint: disable=import-error
try:
    from setuptools import setup
    from setuptools.command.build_py import build_py
    from setuptools.command.sdist import sdist
    from setuptools.command.test import test
except ImportError:
    from distutils.core import setup
    from distutils.cmd import Command
    from distutils.command.build_py import build_py
    from distutils.command.sdist import sdist

    class test(Command):
        def __init__(self, *args, **kwargs):
            Command.__init__(self, *args, **kwargs)
        def initialize_options(self): pass
        def finalize_options(self): pass
        def run(self): self.run_tests()
        def run_tests(self): Command.run_tests(self)
        def set_undefined_options(self, opt, val):
            Command.set_undefined_options(self, opt, val)

import io

def get_version():
    with open('VERSION', 'rb') as f:
        version = f.read().strip()

    full_version = version

    # Strip the local part if there is one, to appease pkg_resources,
    # which handles only PEP 386, not PEP 440.
    if b'+' in full_version:
        pkg_version = full_version[:full_version.find(b'+')]
    else:
        pkg_version = full_version

    # Sanity-check the result.  XXX Consider checking the full PEP 386
    # and PEP 440 regular expressions here?
    assert b'-' not in full_version, '%r' % (full_version,)
    assert b'-' not in pkg_version, '%r' % (pkg_version,)
    assert b'+' not in pkg_version, '%r' % (pkg_version,)

    return pkg_version, full_version

pkg_version, full_version = get_version()

def write_version_py(path):
    try:
        with open(path, 'rb') as f:
            version_old = f.read()
    except IOError:
        version_old = None
    version_new = '__version__ = %r\n' % (full_version,)
    if version_old != version_new:
        print('writing %s' % (path,))
        with open(path, 'wb') as f:
            f.write(version_new)

def readme_contents():
    import os.path
    readme_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'README.md')
    with io.open(readme_path, encoding='UTF-8') as readme_file:
        return readme_file.read()

class local_build_py(build_py):
    def run(self):
        write_version_py(version_py)
        build_py.run(self)

# Make sure the VERSION file in the sdist is exactly specified, even
# if it is a development version, so that we do not need to run git to
# discover it -- which won't work because there's no .git directory in
# the sdist.
class local_sdist(sdist):
    def make_release_tree(self, base_dir, files):
        import os
        sdist.make_release_tree(self, base_dir, files)
        version_file = os.path.join(base_dir, 'VERSION')
        print('updating %s' % (version_file,))
        # Write to temporary file first and rename over permanent not
        # just to avoid atomicity issues (not likely an issue since if
        # interrupted the whole sdist directory is only partially
        # written) but because the upstream sdist may have made a hard
        # link, so overwriting in place will edit the source tree.
        with open(version_file + '.tmp', 'wb') as f:
            f.write('%s\n' % (pkg_version,))
        os.rename(version_file + '.tmp', version_file)

# XXX These should be attributes of `setup', but helpful distutils
# doesn't pass them through when it doesn't know about them a priori.
version_py = 'src/version.py'

setup(
    name='cgpm',
    version=pkg_version,
    description='GPM Crosscat',
    long_description=readme_contents(),
    url='https://github.com/probcomp/cgpm',
    license='Apache-2.0',
    maintainer='Feras Saad',
    maintainer_email='fsaad@remove-this-component.mit.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    packages=[
        'cgpm',
        'cgpm.crosscat',
        'cgpm.dummy',
        'cgpm.factor',
        'cgpm.kde',
        'cgpm.knn',
        'cgpm.mixtures',
        'cgpm.network',
        'cgpm.primitives',
        'cgpm.regressions',
        'cgpm.tests',
        'cgpm.uncorrelated',
        'cgpm.utils',
        'cgpm.venturescript',
    ],
    package_dir={
        'cgpm': 'src',
        'cgpm.tests': 'tests',
    },
    package_data={
        'cgpm.tests': ['graphical/resources/satellites.csv'],
    },
    tests_require=[
        'pytest',
    ],
    cmdclass={
        'build_py': local_build_py,
    },
)
