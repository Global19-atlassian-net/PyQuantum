from PyQuantum.TC.Cavity import *

import unittest
import sys
import os


class TestCavityMethods(unittest.TestCase):
    # -----------------------------------------------------------------------------------------------------------------
    def setUp(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self._original_stdout
    # -----------------------------------------------------------------------------------------------------------------

    # BEGIN----------------------------------------- POSITIVE TESTING -------------------------------------------------
    def test_good_wc(self):
        for wc in (0.1, 1, 100.5):
            Cavity(wc=wc, wa=1, g=1, n_atoms=1)

    def test_good_wa(self):
        for wa in (0.1, 1, 100.5):
            Cavity(wc=1, wa=wa, g=1, n_atoms=1)

    def test_good_g(self):
        for g in (0.1, 1, 100.5):
            Cavity(wc=1, wa=1, g=g, n_atoms=1)

    def test_good_n(self):
        for n_atoms in (1, 5, 10):
            Cavity(wc=1, wa=1, g=1, n_atoms=n_atoms)
    # END------------------------------------------- POSITIVE TESTING -------------------------------------------------

    # BEGIN----------------------------------------- NEGATIVE TESTING -------------------------------------------------
    def test_bad_wc(self):
        for wc in (-5, -2.5, -1, 0):
            try:
                Cavity(wc=wc, wa=1, g=1, n_atoms=1)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'wc <= 0')

        for wc in ['abc']:
            try:
                Cavity(wc=wc, wa=1, g=1, n_atoms=1)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'wc is not numeric')

    def test_bad_wa(self):
        for wa in (-5, -2.5, -1, 0):
            try:
                Cavity(wc=1, wa=wa, g=1, n_atoms=1)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'wa <= 0')

        for wa in ['abc']:
            try:
                Cavity(wc=1, wa=wa, g=1, n_atoms=1)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'wa is not numeric')

    def test_bad_g(self):
        for g in (-5, -2.5, -1, 0):
            try:
                Cavity(wc=1, wa=1, g=g, n_atoms=1)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'g <= 0')

    def test_bad_n_atoms(self):
        for n_atoms in [-5, -1, 0]:
            try:
                Cavity(wc=1, wa=1, g=1, n_atoms=n_atoms)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'n_atoms <= 0')

        for n_atoms in [-0.5, 0.5, 'abc']:
            try:
                Cavity(wc=1, wa=1, g=1, n_atoms=n_atoms)
            except AssertionError as e:
                self.assertEqual(e.args[0], 'n_atoms is not integer')
    # END------------------------------------------- NEGATIVE TESTING -------------------------------------------------


if __name__ == '__main__':
    unittest.main()

# =====================================================================================================================
# class HiddenPrints:
#     def __enter__(self):
#         self._original_stdout = sys.stdout
#         sys.stdout = open(os.devnull, 'w')

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         sys.stdout.close()
#         sys.stdout = self._original_stdout
# =====================================================================================================================
# def test_isupper(self):
#     self.assertTrue('FOO'.isupper())
#     self.assertFalse('Foo'.isupper())


# def test_upper(self):
#     self.assertEqual('foo'.upper(), 'FOO')
# =====================================================================================================================
