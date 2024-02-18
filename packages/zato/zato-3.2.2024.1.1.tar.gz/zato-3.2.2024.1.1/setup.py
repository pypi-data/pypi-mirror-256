# -*- coding: utf-8 -*-

"""
Licensed under AGPLv3, see LICENSE.txt for terms and conditions.
"""

from setuptools import setup

version = '3.2.2024.1.1'

description = 'ESB, SOA, API and Cloud Integrations in Python.'
long_description = """

<a href="https://zato.io">![](https://zato.io/static/img/intro/banner.webp)</a>

# Zato /zɑːtəʊ/

ESB, SOA, API and Cloud Integrations in Python.

Zato is a Python-based, open-source integration platform and enterprise service bus that lets you automate,
integrate and orchestrate business systems,
APIs, workflows as well as hardware assets in industries such as
[airports](https://zato.io/en/industry/airports/index.html),
[defense](https://zato.io/en/industry/defense/index.html),
[health care](https://zato.io/en/industry/healthcare/index.html),
[telecommunications](https://zato.io/en/industry/telecom/index.html),
financial services,
government
and more.

<a href="https://zato.io">![](https://upcdn.io/kW15bqq/raw/root/static/img/intro/bus.png)</a>

## Learn more

Visit https://zato.io for details, including:

* [Downloads](https://zato.io/en/docs/3.2/admin/guide/install/index.html)
* [Screenshots](https://zato.io/en/docs/3.2/intro/screenshots.html)
* [Programming examples](https://zato.io/en/docs/3.2/dev/index.html)
"""
app_name = 'zato'

setup(
      name = app_name,
      version = version,

      author = '',
      description = description,
      long_description = long_description,
      long_description_content_type='text/markdown',
      platforms = ['OS Independent'],
      license = 'AGPLv3',
      zip_safe = False,

      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Database',
        'Topic :: Home Automation',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: System :: Networking',
        'Topic :: Scientific/Engineering',
        'Topic :: Security',
        'Topic :: Software Development',
        'Typing :: Typed',
        ],
)
