# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import doctest
import unittest

import trytond.tests.test_tryton

from trytond.tests.test_tryton import (
    ModuleTestCase, doctest_checker, doctest_teardown)


class PositionNumbersTestCase(ModuleTestCase):
    'Test Position Numbers module'
    module = 'position_numbers'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader(
            ).loadTestsFromTestCase(PositionNumbersTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_position_numbers.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite
