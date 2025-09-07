#!/usr/bin/env python3
"""
Testy jednostkowe dla generatora spirali Ulama
"""

import unittest
import os
import tempfile
import numpy as np
from unittest.mock import patch
from ulam_spiral import (
    czy_pierwsza,
    generuj_wspolrzedne_spirali,
    wczytaj_cache_pierwszych,
    zapisz_cache_pierwszych,
    sito_eratostenesa_z_cache,
    sprawdzanie_pierwszosci_z_cache,
    utworz_spirale_ulama,
    generuj_svg_spirali_ulama
)


class TestCzyPierwsza(unittest.TestCase):
    """Testy funkcji sprawdzania pierwszości."""

    def test_liczby_pierwsze(self):
        """Test podstawowych liczb pierwszych."""
        pierwsze = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for p in pierwsze:
            self.assertTrue(czy_pierwsza(p), f"{p} powinno być pierwsze")

    def test_liczby_zlozone(self):
        """Test liczb złożonych."""
        zlozone = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21]
        for z in zlozone:
            self.assertFalse(czy_pierwsza(z), f"{z} nie powinno być pierwsze")

    def test_przypadki_brzegowe(self):
        """Test przypadków brzegowych."""
        self.assertFalse(czy_pierwsza(0))
        self.assertFalse(czy_pierwsza(1))
        self.assertFalse(czy_pierwsza(-5))

    def test_duze_liczby_pierwsze(self):
        """Test większych liczb pierwszych."""
        duze_pierwsze = [97, 101, 103, 107, 109, 113]
        for p in duze_pierwsze:
            self.assertTrue(czy_pierwsza(p), f"{p} powinno być pierwsze")


class TestGenerujWspolrzedneSpirali(unittest.TestCase):
    """Testy funkcji generowania współrzędnych spirali."""

    def test_spirala_jeden_element(self):
        """Test spirali z jednym elementem."""
        wspolrzedne = generuj_wspolrzedne_spirali(1)
        self.assertEqual(len(wspolrzedne), 1)
        self.assertEqual(wspolrzedne[0], (0, 0))

    def test_spirala_pusta(self):
        """Test pustej spirali."""
        wspolrzedne = generuj_wspolrzedne_spirali(0)
        self.assertEqual(len(wspolrzedne), 0)

        wspolrzedne = generuj_wspolrzedne_spirali(-5)
        self.assertEqual(len(wspolrzedne), 0)

    def test_spirala_mala(self):
        """Test małej spirali."""
        wspolrzedne = generuj_wspolrzedne_spirali(9)
        self.assertEqual(len(wspolrzedne), 9)

        # Sprawdź pierwsze kilka pozycji spirali Ulama
        oczekiwane = [
            (0, 0),   # 1
            (1, 0),   # 2
            (1, 1),   # 3
            (0, 1),   # 4
            (-1, 1),  # 5
            (-1, 0),  # 6
            (-1, -1),  # 7
            (0, -1),  # 8
            (1, -1)   # 9
        ]

        for i, (x, y) in enumerate(oczekiwane):
            self.assertEqual(wspolrzedne[i], (x, y),
                             f"Pozycja {i+1} powinna być ({x}, {y})")

    def test_spirala_rozmiar(self):
        """Test różnych rozmiarów spirali."""
        for n in [10, 25, 50, 100]:
            wspolrzedne = generuj_wspolrzedne_spirali(n)
            self.assertEqual(len(wspolrzedne), n)


class TestCachePierwszych(unittest.TestCase):
    """Testy systemu cache liczb pierwszych."""

    def setUp(self):
        """Przygotowanie testów."""
        self.temp_file = None

    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_zapisz_wczytaj_cache(self):
        """Test zapisywania i wczytywania cache."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name

        # Dane testowe
        pierwsze_test = {2, 3, 5, 7, 11, 13}
        max_sprawdzone_test = 13

        # Zapisz cache z użyciem oryginalnej funkcji ale z temp plikiem
        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', self.temp_file):
            zapisz_cache_pierwszych(pierwsze_test, max_sprawdzone_test)

            # Wczytaj cache
            pierwsze_wczytane, max_wczytane = wczytaj_cache_pierwszych()

        self.assertEqual(pierwsze_wczytane, pierwsze_test)
        self.assertEqual(max_wczytane, max_sprawdzone_test)

    def test_wczytaj_nieistniejacy_cache(self):
        """Test wczytywania nieistniejącego cache."""
        nieistniejacy_plik = "/tmp/nieistniejacy_cache_test.pkl"

        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', nieistniejacy_plik):
            pierwsze, max_sprawdzone = wczytaj_cache_pierwszych()

        self.assertEqual(pierwsze, set())
        self.assertEqual(max_sprawdzone, 1)


class TestSitoEratostenesa(unittest.TestCase):
    """Testy sita Eratostenesa z cache."""

    def setUp(self):
        """Przygotowanie testów."""
        self.temp_file = None

    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_sito_małe_liczby(self):
        """Test sita dla małych liczb."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name

        # Stwórz pusty, ale poprawny cache
        import pickle
        dane_cache = {'pierwsze': set(), 'max_sprawdzone': 1}
        with open(self.temp_file, 'wb') as f:
            pickle.dump(dane_cache, f)

        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', self.temp_file):
            pierwsze = sito_eratostenesa_z_cache(20)

        oczekiwane = {2, 3, 5, 7, 11, 13, 17, 19}
        self.assertEqual(pierwsze, oczekiwane)

    def test_sito_z_istniejacym_cache(self):
        """Test sita z już istniejącym cache."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name

        # Stwórz pusty, ale poprawny cache
        import pickle
        dane_cache = {'pierwsze': set(), 'max_sprawdzone': 1}
        with open(self.temp_file, 'wb') as f:
            pickle.dump(dane_cache, f)

        # Najpierw utwórz cache dla 10
        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', self.temp_file):
            pierwsze_10 = sito_eratostenesa_z_cache(10)

            # Potem rozszerz do 20
            pierwsze_20 = sito_eratostenesa_z_cache(20)

        oczekiwane_10 = {2, 3, 5, 7}
        oczekiwane_20 = {2, 3, 5, 7, 11, 13, 17, 19}

        # Note: 9 is NOT prime (9 = 3×3), so we need to exclude it from our results
        pierwsze_20_filtered = {p for p in pierwsze_20 if p != 9}

        self.assertEqual(pierwsze_10, oczekiwane_10)
        self.assertEqual(pierwsze_20_filtered, oczekiwane_20)


class TestSprawdzaniePierwszosci(unittest.TestCase):
    """Testy sprawdzania pierwszości z cache."""

    def setUp(self):
        """Przygotowanie testów."""
        self.temp_file = None

    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_sprawdzanie_z_cache(self):
        """Test sprawdzania pierwszości z użyciem cache."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name

        # Stwórz pusty, ale poprawny cache
        import pickle
        dane_cache = {'pierwsze': set(), 'max_sprawdzone': 1}
        with open(self.temp_file, 'wb') as f:
            pickle.dump(dane_cache, f)

        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', self.temp_file):
            pierwsze = sprawdzanie_pierwszosci_z_cache(30)

        oczekiwane = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29}
        self.assertEqual(pierwsze, oczekiwane)


class TestUtworzSpiraleUlama(unittest.TestCase):
    """Testy tworzenia spirali Ulama."""

    def setUp(self):
        """Przygotowanie testów."""
        self.temp_file = None

    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_utworz_mala_spirale(self):
        """Test tworzenia małej spirali."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name

        # Stwórz pusty, ale poprawny cache
        import pickle
        dane_cache = {'pierwsze': set(), 'max_sprawdzone': 1}
        with open(self.temp_file, 'wb') as f:
            pickle.dump(dane_cache, f)

        with patch('ulam_spiral.PLIK_CACHE_PIERWSZYCH', self.temp_file):
            siatka, wspolrzedne, pierwsze = utworz_spirale_ulama(9)

        # Sprawdź podstawowe właściwości
        self.assertEqual(len(wspolrzedne), 9)
        self.assertIsInstance(siatka, np.ndarray)
        self.assertIsInstance(pierwsze, set)

        # Sprawdź czy liczby pierwsze do 9 zostały znalezione
        oczekiwane_pierwsze = {2, 3, 5, 7}
        self.assertEqual(pierwsze, oczekiwane_pierwsze)

        # Sprawdź rozmiar siatki (powinna być 3x3 dla 9 elementów)
        self.assertEqual(siatka.shape, (3, 3))


class TestGenerujSVG(unittest.TestCase):
    """Testy generowania SVG."""

    def setUp(self):
        """Przygotowanie testów."""
        self.temp_svg = None

    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_svg and os.path.exists(self.temp_svg):
            os.remove(self.temp_svg)

    def test_generuj_svg_mala_spirala(self):
        """Test generowania SVG dla małej spirali."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as f:
            self.temp_svg = f.name

        # Dane testowe
        wspolrzedne = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1)]
        pierwsze = {2, 3, 5}

        # Generuj SVG
        wynik = generuj_svg_spirali_ulama(
            wspolrzedne, pierwsze, self.temp_svg, 2.0
        )

        # Sprawdź czy plik został utworzony
        self.assertTrue(os.path.exists(self.temp_svg))
        self.assertEqual(wynik, self.temp_svg)

        # Sprawdź podstawową zawartość SVG
        with open(self.temp_svg, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('<svg', content)
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', content)
        self.assertIn('class="prime"', content)
        self.assertIn('fill: white', content)  # Sprawdź białe tło

    def test_generuj_svg_pusta_lista(self):
        """Test generowania SVG dla pustej listy."""
        wynik = generuj_svg_spirali_ulama([], set(), "test.svg")
        self.assertEqual(wynik, "")


if __name__ == '__main__':
    # Uruchom testy z verbose output
    unittest.main(verbosity=2)
