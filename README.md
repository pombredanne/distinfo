# Distinfo

[![Build Status](https://travis-ci.org/0compute/distinfo.svg?branch=master)](https://travis-ci.org/0compute/distinfo)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6e4440a1903408842141/test_coverage)](https://codeclimate.com/github/0compute/distinfo/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/6e4440a1903408842141/maintainability)](https://codeclimate.com/github/0compute/distinfo/maintainability)

`distinfo` is a tool for extracting dependencies and metadata from Python
source distributions.

## Usage

### CLI

Dump json metadata to stdout:

    $ distinfo /path/to/package/source

### Library

Print dependencies and metadata:

``` python
>>> from distinfo import Requirement, dump
>>> 
>>> req = Requirement.from_source(".")
>>> dump(req.dist.depends)
{
  "build": [
    "setuptools-scm"
  ],
  "dev": [
    "pycmd",
  ],
  "run": [
    "click",
    "requests",
  ],
  "test": [
    "pytest",
  ]
}
>>> print(req.dist.metadata)
{
  "author": "A N Other",
  "author_email": "a@example.org",
  "extensions": {
    "distinfo": {
      "imports": {
        "distinfo": [
          "click",
          "requests"
        ],
        "tests": [
          "pytest",
        ]
      },
      "tests": true
    }
  },
  "license": "GPL-3.0-or-later",
  "metadata_version": "2.1",
  "name": "example",
  "provides_extra": [
      "build",
      "dev",
      "test"
  ],
  "requires_dist": [
      "click",
      "pycmd; extra == 'dev'",
      "pytest; extra == 'test'",
      "requests"
      "setuptools-scm; extra == 'build'",
  ],
  "summary": "Example package",
  "version": "0.0.0"
}
```

## Specifications

https://packaging.python.org/specifications/

### Metadata

* [PEP 241 - Metadata for Python Software Packages 1.0](https://www.python.org/dev/peps/pep-0241/)
* [PEP 314 - Metadata for Python Software Packages 1.1](https://www.python.org/dev/peps/pep-0314/)
* [PEP 345 - Metadata for Python Software Packages 1.2](https://www.python.org/dev/peps/pep-0345/)
* [PEP 426 - Metadata for Python Software Packages 2.0](https://www.python.org/dev/peps/pep-0426/)
* [PEP 566 - Metadata for Python Software Packages 2.1](https://www.python.org/dev/peps/pep-0566/)
* [PEP 459 -- Standard Metadata Extensions for Python Software Packages](https://www.python.org/dev/peps/pep-0459/)

### Dependencies

* [PEP 440 - Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/)
* [PEP 508 - Dependency specification for Python Software Packages](https://www.python.org/dev/peps/pep-0508/)
* [PEP 518 - Specifying Minimum Build System Requirements for Python Projects](https://www.python.org/dev/peps/pep-0518/)
