#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import nose
from nose.plugins.manager import PluginManager
from nose.plugins.doctests import Doctest
from nose.plugins import builtin

simple_nltk_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         "../simple_simple_nltk", ".."))
sys.path.insert(0, simple_nltk_ROOT)

simple_nltk_TEST_DIR = os.path.join(simple_nltk_ROOT, "simple_nltk")

if __name__ == "__main__":
    # there shouldn't be import from simple_nltk for coverage to work properly
    try:
        # Import RedNose plugin for colored test output
        from rednose import RedNose

        rednose_available = True
    except ImportError:
        rednose_available = False

    class simple_nltkPluginManager(PluginManager):
        """
        Nose plugin manager that replaces standard doctest plugin
        with a patched version and adds RedNose plugin for colored test output.
        """

        def loadPlugins(self):
            for plug in builtin.plugins:
                self.addPlugin(plug())
            if rednose_available:
                self.addPlugin(RedNose())

            super(simple_nltkPluginManager, self).loadPlugins()

    manager = simple_nltkPluginManager()
    manager.loadPlugins()

    # allow passing extra options and running individual tests
    # Examples:
    #
    #    python runtests.py semantics.doctest
    #    python runtests.py --with-id -v
    #    python runtests.py --with-id -v simple_nltk.featstruct

    args = sys.argv[1:]
    if not args:
        args = [simple_nltk_TEST_DIR]

    if all(arg.startswith("-") for arg in args):
        # only extra options were passed
        args += [simple_nltk_TEST_DIR]

    # Activate RedNose and hide skipped test messages from output
    if rednose_available:
        args += ["--rednose", "--hide-skips"]

    arguments = [
        "--exclude=",  # why is this needed?
        # '--with-xunit',
        # '--xunit-file=$WORKSPACE/nosetests.xml',
        # '--nocapture',
        "--with-doctest",
        # '--doctest-tests',
        # '--debug=nose,nose.importer,nose.inspector,nose.plugins,nose.result,nose.selector',
        "--doctest-extension=.doctest",
        "--doctest-fixtures=_fixt",
        "--doctest-options=+ELLIPSIS,+NORMALIZE_WHITESPACE,+IGNORE_EXCEPTION_DETAIL",
        # '--verbosity=3',
    ] + args

    nose.main(argv=arguments, plugins=manager.plugins)
