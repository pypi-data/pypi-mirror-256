# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = 'doCheck',
    version = '0.1.3',
    keywords = ['type',"check","value","constraint"],
    description = 'Check the value both type and value and then constraint it.',
    long_description = open("README.md","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/do-check-pages/",
    install_requires = [
    ],
    long_description_content_type="text/markdown",
    packages = ['doCheck'],
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        "Natural Language :: English",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ],
    entry_points = {

    }
)
