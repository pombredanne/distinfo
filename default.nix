{
  pkgs ? import (builtins.fetchTarball {
  url = "https://github.com/nixos/nixpkgs/archive/a8c71037e041725d40fbf2f3047347b6833b1703.tar.gz";
  sha256 = "1z4cchcw7qgjhy0x6mnz7iqvpswc2nfjpdynxc54zpm66khfrjqw";
}) {}

, python ? pkgs.python3
, lib ? pkgs.lib
}:
let
  nix-gitignore = import (pkgs.fetchFromGitHub {
    owner = "siers";
    repo = "nix-gitignore";
    rev = "6dd9ece00991003c0f5d3b4da3f29e67956d266e";
    sha256 = "0jn5yryf511shdp8g9pwrsxgk57p6xhpb79dbi2sf5hzlqm2csy4";
  }) { inherit lib; };
in
with rec {

  appdirs = python.pkgs.buildPythonPackage rec {
    pname = "appdirs";
    version = "1.4.3";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "9e5896d1372858f8dd3344faf4e5014d21849c756c8d5701f78f8a103b372d92";
    };
    doCheck = false;
    meta = {
      description = "A small Python module for determining appropriate platform-specific dirs, e.g. a \"user data dir\".";
      homepage = http://github.com/ActiveState/appdirs;
      license = lib.licenses.mit;
    };
  };

  atomicwrites = python.pkgs.buildPythonPackage rec {
    pname = "atomicwrites";
    version = "1.1.5";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "240831ea22da9ab882b551b31d4225591e5e447a68c5e188db5b89ca1d487585";
    };
    doCheck = false;
    meta = {
      description = "Atomic file writes.";
      homepage = https://github.com/untitaker/python-atomicwrites;
      license = lib.licenses.mit;
    };
  };

  attrs = python.pkgs.buildPythonPackage rec {
    pname = "attrs";
    version = "18.1.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "e0d0eb91441a3b53dab4d9b743eafc1ac44476296a2053b6ca3af0b139faf87b";
    };
    installPhase = ''
      dst=$out/${python.sitePackages}
      mkdir -p $dst
      export PYTHONPATH="$dst:$PYTHONPATH"
      ${python.interpreter} setup.py install --prefix=$out
    '';
    doCheck = false;
    meta = {
      description = "Classes Without Boilerplate";
      homepage = http://www.attrs.org/;
      license = lib.licenses.mit;
    };
  };

  certifi = python.pkgs.buildPythonPackage rec {
    pname = "certifi";
    version = "2018.4.16";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "13e698f54293db9f89122b0581843a782ad0934a4fe0172d2a980ba77fc61bb7";
    };
    doCheck = false;
    meta = {
      description = "Python package for providing Mozilla's CA Bundle.";
      homepage = http://certifi.io/;
      license = lib.licenses.mpl20;
    };
  };

  chardet = python.pkgs.buildPythonPackage rec {
    pname = "chardet";
    version = "3.0.4";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae";
    };
    doCheck = false;
    meta = {
      description = "Universal encoding detector for Python 2 and 3";
      homepage = https://github.com/chardet/chardet;
      license = lib.licenses.lgpl3;
    };
  };

  click = python.pkgs.buildPythonPackage rec {
    pname = "click";
    version = "6.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "f15516df478d5a56180fbf80e68f206010e6d160fc39fa508b65e035fd75130b";
    };
    buildInputs = [ pkgs.glibcLocales ];
    LANG = "en_US.UTF-8";
    doCheck = false;
    meta = {
      description = "A simple wrapper around optparse for powerful command line utilities.";
      homepage = http://github.com/mitsuhiko/click;
    };
  };

  coloredlogs = python.pkgs.buildPythonPackage rec {
    pname = "coloredlogs";
    version = "10.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "b869a2dda3fa88154b9dd850e27828d8755bfab5a838a1c97fbc850c6e377c36";
    };
    propagatedBuildInputs = [ humanfriendly ];
    doCheck = false;
    meta = {
      description = "Colored terminal output for Python's logging module";
      homepage = https://coloredlogs.readthedocs.io;
      license = lib.licenses.mit;
    };
  };

  contoml = python.pkgs.buildPythonPackage rec {
    pname = "contoml";
    version = "0.32";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "2353275caef3726131c4192379252cc48eb4a15c06df3e1046f783de937eba94";
    };
    propagatedBuildInputs = [ iso8601 pytz six strict-rfc3339 timestamp ];
    doCheck = false;
    meta = {
      description = "Consistent TOML for Python";
      homepage = https://github.com/Jumpscale/python-consistent-toml;
    };
  };

  coverage = python.pkgs.buildPythonPackage rec {
    pname = "coverage";
    version = "4.5.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "56e448f051a201c5ebbaa86a5efd0ca90d327204d8b059ab25ad0f35fbfd79f1";
    };
    doCheck = false;
    meta = {
      description = "Code coverage measurement for Python";
      homepage = https://bitbucket.org/ned/coveragepy;
      license = lib.licenses.asl20;
    };
  };

  distlib = python.pkgs.buildPythonPackage rec {
    pname = "distlib";
    version = "0.2.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "cd502c66fc27c535bab62dc4f482e403e2369c2c05281a79cc2d4e2f42a87f20";
      extension = "zip";
    };
    doCheck = false;
    meta = {
      description = "Distribution utilities";
      homepage = https://bitbucket.org/pypa/distlib;
      license = lib.licenses.psfl;
    };
  };

  docopt = python.pkgs.buildPythonPackage rec {
    pname = "docopt";
    version = "0.6.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "49b3a825280bd66b3aa83585ef59c4a8c82f2c8a522dbe754a8bc8d08c85c491";
    };
    doCheck = false;
    meta = {
      description = "Pythonic argument parser, that will make you smile";
      homepage = http://docopt.org;
      license = lib.licenses.mit;
    };
  };

  fancycompleter = python.pkgs.buildPythonPackage rec {
    pname = "fancycompleter";
    version = "0.8";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "d2522f1f3512371f295379c4c0d1962de06762eb586c199620a2a5d423539b12";
    };
    buildInputs = [ setuptools_scm ];
    doCheck = false;
    meta = {
      description = "colorful TAB completion for Python prompt";
      homepage = http://bitbucket.org/antocuni/fancycompleter;
      license = lib.licenses.bsdOriginal;
    };
  };

  first = python.pkgs.buildPythonPackage rec {
    pname = "first";
    version = "2.0.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "3bb3de3582cb27071cfb514f00ed784dc444b7f96dc21e140de65fe00585c95e";
    };
    doCheck = false;
    meta = {
      description = "Return the first true value of an iterable.";
      homepage = http://github.com/hynek/first/;
      license = lib.licenses.mit;
    };
  };

  humanfriendly = python.pkgs.buildPythonPackage rec {
    pname = "humanfriendly";
    version = "4.16.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "ed1e98ae056b597f15b41bddcc32b9f21e6ab4f3445f9faad1668675de759f7b";
    };
    doCheck = false;
    meta = {
      description = "Human friendly output for text interfaces using Python";
      homepage = https://humanfriendly.readthedocs.io;
      license = lib.licenses.mit;
    };
  };

  idna = python.pkgs.buildPythonPackage rec {
    pname = "idna";
    version = "2.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "684a38a6f903c1d71d6d5fac066b58d7768af4de2b832e426ec79c30daa94a16";
    };
    doCheck = false;
    meta = {
      description = "Internationalized Domain Names in Applications (IDNA)";
      homepage = https://github.com/kjd/idna;
      license = lib.licenses.bsdOriginal;
    };
  };

  iso8601 = python.pkgs.buildPythonPackage rec {
    pname = "iso8601";
    version = "0.1.12";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "49c4b20e1f38aa5cf109ddcd39647ac419f928512c869dc01d5c7098eddede82";
    };
    doCheck = false;
    meta = {
      description = "Simple module to parse ISO 8601 dates";
      homepage = https://bitbucket.org/micktwomey/pyiso8601;
      license = lib.licenses.mit;
    };
  };

  jedi = python.pkgs.buildPythonPackage rec {
    pname = "jedi";
    version = "0.12.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "b409ed0f6913a701ed474a614a3bb46e6953639033e31f769ca7581da5bd1ec1";
    };
    propagatedBuildInputs = [ parso ];
    doCheck = false;
    meta = {
      description = "An autocompletion tool for Python that can be used for text editors.";
      homepage = https://github.com/davidhalter/jedi;
      license = lib.licenses.mit;
    };
  };

  more-itertools = python.pkgs.buildPythonPackage rec {
    pname = "more-itertools";
    version = "4.2.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "2b6b9893337bfd9166bee6a62c2b0c9fe7735dcf85948b387ec8cba30e85d8e8";
    };
    propagatedBuildInputs = [ six ];
    doCheck = false;
    meta = {
      description = "More routines for operating on iterables, beyond itertools";
      homepage = https://github.com/erikrose/more-itertools;
      license = lib.licenses.mit;
    };
  };

  munch = python.pkgs.buildPythonPackage rec {
    pname = "munch";
    version = "2.3.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "6ae3d26b837feacf732fb8aa5b842130da1daf221f5af9f9d4b2a0a6414b0d51";
    };
    propagatedBuildInputs = [ six ];
    doCheck = false;
    meta = {
      description = "A dot-accessible dictionary (a la JavaScript objects).";
      homepage = http://github.com/Infinidat/munch;
      license = lib.licenses.mit;
    };
  };

  packaging = python.pkgs.buildPythonPackage rec {
    pname = "packaging";
    version = "17.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "f019b770dd64e585a99714f1fd5e01c7a8f11b45635aa953fd41c689a657375b";
    };
    propagatedBuildInputs = [ pyparsing six ];
    doCheck = false;
    meta = {
      description = "Core utilities for Python packages";
      homepage = https://github.com/pypa/packaging;
      license = "BSD or Apache License, Version 2.0";
    };
  };

  parso = python.pkgs.buildPythonPackage rec {
    pname = "parso";
    version = "0.3.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "35704a43a3c113cce4de228ddb39aab374b8004f4f2407d070b6a2ca784ce8a2";
    };
    doCheck = false;
    meta = {
      description = "A Python Parser";
      homepage = https://github.com/davidhalter/parso;
      license = lib.licenses.mit;
    };
  };

  pdbpp = python.pkgs.buildPythonPackage rec {
    pname = "pdbpp";
    version = "0.9.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "dde77326e4ea41439c243ed065826d53539530eeabd1b6615aae15cfbb9fda05";
    };
    buildInputs = [ setuptools_scm ];
    propagatedBuildInputs = [ fancycompleter Pygments wmctrl ];
    doCheck = false;
    meta = {
      description = "pdb++, a drop-in replacement for pdb";
      homepage = http://github.com/antocuni/pdb;
      license = lib.licenses.bsdOriginal;
    };
  };

  pipreqs = python.pkgs.buildPythonPackage rec {
    pname = "pipreqs";
    version = "0.4.9";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "cec6eecc4685967b27eb386037565a737d036045f525b9eb314631a68d60e4bc";
    };
    propagatedBuildInputs = [ docopt yarg ];
    doCheck = false;
    meta = {
      description = "Pip requirements.txt generator based on imports in project";
      homepage = https://github.com/bndr/pipreqs;
      license = "Apache License";
    };
  };

  pluggy = python.pkgs.buildPythonPackage rec {
    pname = "pluggy";
    version = "0.6.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "7f8ae7f5bdf75671a718d2daf0a64b7885f74510bcd98b1a0bb420eb9a9d0cff";
    };
    doCheck = false;
    meta = {
      description = "plugin and hook calling mechanisms for python";
      homepage = https://github.com/pytest-dev/pluggy;
      license = lib.licenses.mit;
    };
  };

  prompt_toolkit = python.pkgs.buildPythonPackage rec {
    pname = "prompt_toolkit";
    version = "1.0.15";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "858588f1983ca497f1cf4ffde01d978a3ea02b01c8a26a8bbc5cd2e66d816917";
    };
    propagatedBuildInputs = [ six wcwidth ];
    patchPhase = "rm prompt_toolkit/win32_types.py";
    doCheck = false;
    meta = {
      description = "Library for building powerful interactive command lines in Python";
      homepage = https://github.com/jonathanslenders/python-prompt-toolkit;
    };
  };

  property-manager = python.pkgs.buildPythonPackage rec {
    pname = "property-manager";
    version = "2.3.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "19e1f230f95691ae74123fa43c6928d0f0cc464e841d6375941cda4a0585162f";
    };
    propagatedBuildInputs = [ humanfriendly verboselogs ];
    doCheck = false;
    meta = {
      description = "Useful property variants for Python programming (required properties, writable properties, cached properties, etc)";
      homepage = https://property-manager.readthedocs.org;
      license = lib.licenses.mit;
    };
  };

  ptpython = python.pkgs.buildPythonPackage rec {
    pname = "ptpython";
    version = "0.41";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "a78b27a85c5dbe9d89376e7f3aa70a9d8fa15cb45ee5f73a3cc3963b9b528ac1";
    };
    propagatedBuildInputs = [ docopt jedi prompt_toolkit Pygments ];
    doCheck = false;
    meta = {
      description = "Python REPL build on top of prompt_toolkit";
      homepage = https://github.com/jonathanslenders/ptpython;
    };
  };

  py = python.pkgs.buildPythonPackage rec {
    pname = "py";
    version = "1.5.4";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "3fd59af7435864e1a243790d322d763925431213b6b8529c6ca71081ace3bbf7";
    };
    buildInputs = [ setuptools_scm ];
    doCheck = false;
    meta = {
      description = "library with cross-python path, ini-parsing, io, code, log facilities";
      homepage = http://py.readthedocs.io/;
      license = lib.licenses.mit;
    };
  };

  pycmd = python.pkgs.buildPythonPackage rec {
    pname = "pycmd";
    version = "1.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "adc1976c0106919e9338db20102b91009256dcfec924a66928d7297026f72477";
    };
    propagatedBuildInputs = [ py ];
    doCheck = false;
    meta = {
      description = "pycmd: tools for managing/searching Python related files.";
      license = lib.licenses.mit;
    };
  };

  Pygments = python.pkgs.buildPythonPackage rec {
    pname = "Pygments";
    version = "2.2.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "dbae1046def0efb574852fab9e90209b23f556367b5a320c0bcb871c77c3e8cc";
    };
    doCheck = false;
    meta = {
      description = "Pygments is a syntax highlighting package written in Python.";
      homepage = http://pygments.org/;
      license = lib.licenses.bsdOriginal;
    };
  };

  pyparsing = python.pkgs.buildPythonPackage rec {
    pname = "pyparsing";
    version = "2.2.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "0832bcf47acd283788593e7a0f542407bd9550a55a8a8435214a1960e04bcb04";
    };
    doCheck = false;
    meta = {
      description = "Python parsing module";
      homepage = http://pyparsing.wikispaces.com/;
      license = lib.licenses.mit;
    };
  };

  pytest = python.pkgs.buildPythonPackage rec {
    pname = "pytest";
    version = "3.6.3";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "0453c8676c2bee6feb0434748b068d5510273a916295fd61d306c4f22fbfd752";
    };
    buildInputs = [ setuptools_scm ];
    propagatedBuildInputs = [
      atomicwrites
      attrs
      more-itertools
      pluggy
      py
      setuptools
    ];
    patchPhase = "rm testing/test_argcomplete.py";
    postInstall = "PATH=$out/bin:$PATH";
    doCheck = false;
    meta = {
      description = "pytest: simple powerful testing with Python";
      homepage = http://pytest.org;
      license = lib.licenses.mit;
    };
  };

  pytest-cov = python.pkgs.buildPythonPackage rec {
    pname = "pytest-cov";
    version = "2.5.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "03aa752cf11db41d281ea1d807d954c4eda35cfa1b21d6971966cc041bbf6e2d";
    };
    propagatedBuildInputs = [ coverage pytest ];
    doCheck = false;
    meta = {
      description = "Pytest plugin for measuring coverage.";
      homepage = https://github.com/pytest-dev/pytest-cov;
      license = lib.licenses.mit;
    };
  };

  pytest-sugar = python.pkgs.buildPythonPackage rec {
    pname = "pytest-sugar";
    version = "0.9.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "ab8cc42faf121344a4e9b13f39a51257f26f410e416c52ea11078cdd00d98a2c";
    };
    propagatedBuildInputs = [ pytest termcolor ];
    doCheck = false;
    meta = {
      description = "py.test is a plugin for py.test that changes the default look and feel of py.test (e.g. progressbar, show tests that fail instantly).";
      homepage = http://pivotfinland.com/pytest-sugar/;
      license = lib.licenses.bsdOriginal;
    };
  };

  pytoml = python.pkgs.buildPythonPackage rec {
    pname = "pytoml";
    version = "0.1.18";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "dae3c4e31d09eb06a6076d671f2281ee5d2c43cbeae16599c3af20881bb818ac";
    };
    doCheck = false;
    meta = {
      description = "A parser for TOML-0.4.0";
      homepage = https://github.com/avakar/pytoml;
      license = lib.licenses.mit;
    };
  };

  pytz = python.pkgs.buildPythonPackage rec {
    pname = "pytz";
    version = "2018.5";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "ffb9ef1de172603304d9d2819af6f5ece76f2e85ec10692a524dd876e72bf277";
    };
    doCheck = false;
    meta = {
      description = "World timezone definitions, modern and historical";
      homepage = http://pythonhosted.org/pytz;
      license = lib.licenses.mit;
    };
  };

  PyYAML = python.pkgs.buildPythonPackage rec {
    pname = "PyYAML";
    version = "3.13";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "3ef3092145e9b70e3ddd2c7ad59bdd0252a94dfe3949721633e41344de00a6bf";
    };
    doCheck = false;
    meta = {
      description = "YAML parser and emitter for Python";
      homepage = http://pyyaml.org/wiki/PyYAML;
      license = lib.licenses.mit;
    };
  };

  requests = python.pkgs.buildPythonPackage rec {
    pname = "requests";
    version = "2.19.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "ec22d826a36ed72a7358ff3fe56cbd4ba69dd7a6718ffd450ff0e9df7a47ce6a";
    };
    propagatedBuildInputs = [ certifi chardet idna urllib3 ];
    doCheck = false;
    meta = {
      description = "Python HTTP for Humans.";
      homepage = http://python-requests.org;
      license = lib.licenses.asl20;
    };
  };

  requirements-parser = python.pkgs.buildPythonPackage rec {
    pname = "requirements-parser";
    version = "0.2.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "5963ee895c2d05ae9f58d3fc641082fb38021618979d6a152b6b1398bd7d4ed4";
    };
    doCheck = false;
    meta = {
      description = "Parses Pip requirement files";
      homepage = https://github.com/davidfischer/requirements-parser;
      license = lib.licenses.bsdOriginal;
    };
  };

  requirementslib = python.pkgs.buildPythonPackage rec {
    pname = "requirementslib";
    version = "1.0.11";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "87cd1197cc4b880d710eacbc4fb11fd0564187a1d965382e66cbaa2a1b08744f";
    };
    propagatedBuildInputs = [
      attrs
      contoml
      distlib
      first
      packaging
      requirements-parser
      toml
    ];
    doCheck = false;
    meta = {
      description = "A tool for converting between pip-style and pipfile requirements.";
      homepage = https://github.com/sarugaku/requirementslib;
      license = lib.licenses.mit;
    };
  };

  setuptools = python.pkgs.buildPythonPackage rec {
    pname = "setuptools";
    version = "40.0.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "012adb8e25fbfd64c652e99e7bab58799a3aaf05d39ab38561f69190a909015f";
      extension = "zip";
    };
    installPhase = ''
      dst=$out/${python.sitePackages}
      mkdir -p $dst
      export PYTHONPATH="$dst:$PYTHONPATH"
      ${python.interpreter} setup.py install --prefix=$out
    '';
    doCheck = false;
    meta = {
      description = "Easily download, build, install, upgrade, and uninstall Python packages";
      homepage = https://github.com/pypa/setuptools;
    };
  };

  setuptools_scm = python.pkgs.buildPythonPackage rec {
    pname = "setuptools_scm";
    version = "3.0.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "113cea38b2edba8538b7e608b58cbd7e09bb71b16d968a9b97e36b4805e06d59";
    };
    doCheck = false;
    meta = {
      description = "the blessed package to manage your versions by scm tags";
      homepage = https://github.com/pypa/setuptools_scm/;
      license = lib.licenses.mit;
    };
  };

  six = python.pkgs.buildPythonPackage rec {
    pname = "six";
    version = "1.11.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "70e8a77beed4562e7f14fe23a786b54f6296e34344c23bc42f07b15018ff98e9";
    };
    doCheck = false;
    meta = {
      description = "Python 2 and 3 compatibility utilities";
      homepage = http://pypi.python.org/pypi/six/;
      license = lib.licenses.mit;
    };
  };

  strict-rfc3339 = python.pkgs.buildPythonPackage rec {
    pname = "strict-rfc3339";
    version = "0.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "5cad17bedfc3af57b399db0fed32771f18fc54bbd917e85546088607ac5e1277";
    };
    doCheck = false;
    meta = {
      description = "Strict, simple, lightweight RFC3339 functions";
      homepage = http://www.danielrichman.co.uk/libraries/strict-rfc3339.html;
      license = "GNU General Public License Version 3";
    };
  };

  termcolor = python.pkgs.buildPythonPackage rec {
    pname = "termcolor";
    version = "1.1.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "1d6d69ce66211143803fbc56652b41d73b4a400a2891d7bf7a1cdf4c02de613b";
    };
    doCheck = false;
    meta = {
      description = "ANSII Color formatting for output in terminal.";
      homepage = http://pypi.python.org/pypi/termcolor;
      license = lib.licenses.mit;
    };
  };

  timestamp = python.pkgs.buildPythonPackage rec {
    pname = "timestamp";
    version = "0.0.1";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "b5c7a4539f0d8742b7d6c78febd241ab24903c73c38045690725220ca7eae4ac";
    };
    doCheck = false;
    meta = {
      description = "shortcut for converting datetime to timestamp";
      homepage = http://github.com/jarvys/timestamp;
    };
  };

  toml = python.pkgs.buildPythonPackage rec {
    pname = "toml";
    version = "0.9.4";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "8e86bd6ce8cc11b9620cb637466453d94f5d57ad86f17e98a98d1f73e3baab2d";
    };
    doCheck = false;
    meta = {
      description = "Python Library for Tom's Obvious, Minimal Language";
      homepage = https://github.com/uiri/toml;
      license = "License :: OSI Approved :: MIT License";
    };
  };

  tox = python.pkgs.buildPythonPackage rec {
    pname = "tox";
    version = "3.1.2";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "9f0cbcc36e08c2c4ae90d02d3d1f9a62231f974bcbc1df85e8045946d8261059";
    };
    buildInputs = [ setuptools_scm ];
    propagatedBuildInputs = [ packaging pluggy py virtualenv ];
    patchPhase = "rm tests/test_z_cmdline.py";
    doCheck = false;
    meta = {
      description = "virtualenv-based automation of test activities";
      homepage = https://tox.readthedocs.org/;
      license = "http://opensource.org/licenses/MIT";
    };
  };

  urllib3 = python.pkgs.buildPythonPackage rec {
    pname = "urllib3";
    version = "1.23";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "a68ac5e15e76e7e5dd2b8f94007233e01effe3e50e8daddf69acfd81cb686baf";
    };
    doCheck = false;
    meta = {
      description = "HTTP library with thread-safe connection pooling, file post, and more.";
      homepage = https://urllib3.readthedocs.io/;
      license = lib.licenses.mit;
    };
  };

  verboselogs = python.pkgs.buildPythonPackage rec {
    pname = "verboselogs";
    version = "1.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "e33ddedcdfdafcb3a174701150430b11b46ceb64c2a9a26198c76a156568e427";
    };
    doCheck = false;
    meta = {
      description = "Verbose logging level for Python's logging module";
      homepage = https://verboselogs.readthedocs.io;
    };
  };

  virtualenv = python.pkgs.buildPythonPackage rec {
    pname = "virtualenv";
    version = "16.0.0";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "ca07b4c0b54e14a91af9f34d0919790b016923d157afda5efdde55c96718f752";
    };
    doCheck = false;
    meta = {
      description = "Virtual Python Environment builder";
      homepage = https://virtualenv.pypa.io/;
      license = lib.licenses.mit;
    };
  };

  wcwidth = python.pkgs.buildPythonPackage rec {
    pname = "wcwidth";
    version = "0.1.7";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e";
    };
    doCheck = false;
    meta = {
      description = "Measures number of Terminal column cells of wide-character codes";
      homepage = https://github.com/jquast/wcwidth;
      license = lib.licenses.mit;
    };
  };

  wmctrl = python.pkgs.buildPythonPackage rec {
    pname = "wmctrl";
    version = "0.3";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "d806f65ac1554366b6e31d29d7be2e8893996c0acbb2824bbf2b1f49cf628a13";
    };
    doCheck = false;
    meta = {
      description = "A tool to programmatically control windows inside X";
      homepage = http://bitbucket.org/antocuni/wmctrl;
      license = lib.licenses.bsdOriginal;
    };
  };

  yarg = python.pkgs.buildPythonPackage rec {
    pname = "yarg";
    version = "0.1.9";
    src = python.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "55695bf4d1e3e7f756496c36a69ba32c40d18f821e38f61d028f6049e5e15911";
    };
    propagatedBuildInputs = [ requests ];
    doCheck = false;
    meta = {
      description = "A semi hard Cornish cheese, also queries PyPI (PyPI client)";
      homepage = https://yarg.readthedocs.org/;
      license = lib.licenses.mit;
    };
  };

};
python.pkgs.buildPythonPackage rec {
  pname = "distinfo";
  version = "0.3.0.dev0";
  src = nix-gitignore.gitignoreSource ./.;
  buildInputs = [ pkgs.glibcLocales ];
  propagatedBuildInputs = [
    appdirs
    click
    coloredlogs
    munch
    pdbpp
    pipreqs
    property-manager
    ptpython
    pycmd
    pytest-cov
    pytest-sugar
    pytoml
    PyYAML
    requirementslib
    tox
  ];
  LANG = "en_US.UTF-8";
  checkPhase = "pytest && cp coverage.xml $out";
  meta = {
    description = "Extract metadata, including full dependencies, from source distributions";
    homepage = https://github.com/0compute/distinfo;
    license = "GPL-3.0-or-later";
  };
}
