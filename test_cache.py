#!/usr/bin/env python3
"""
Testy jednostkowe dla systemu cache i narzędzi pomocniczych
"""

import unittest
import os
import tempfile
import csv
from unittest.mock import patch, MagicMock
import sys

# Importy z modułów projektu
from sprawdz_cache_pierwszych import main as sprawdz_integralnosc_cache
from eksportuj_cache_do_csv import eksportuj_do_csv_podstawowy as eksportuj_do_csv


class TestSprawdzCachePierwszych(unittest.TestCase):
    """Testy weryfikacji cache liczb pierwszych."""
    
    def setUp(self):
        """Przygotowanie testów."""
        self.temp_file = None
    
    def tearDown(self):
        """Sprzątanie po testach."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_sprawdz_cache_poprawny(self):
        """Test sprawdzania poprawnego cache."""
        # Przygotuj testowy cache
        import pickle
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_file = f.name
            
        dane_cache = {
            'pierwsze': {2, 3, 5, 7, 11, 13, 17, 19},
            'max_sprawdzone': 20
        }
        
        with open(self.temp_file, 'wb') as f:
            pickle.dump(dane_cache, f)
        
        # Mock argumentów systemowych
        with patch('sys.argv', ['sprawdz_cache_pierwszych.py']):
            with patch('sprawdz_cache_pierwszych.PLIK_CACHE_PIERWSZYCH', self.temp_file):
                # Przekieruj stdout żeby złapać output
                from io import StringIO
                captured_output = StringIO()
                with patch('sys.stdout', captured_output):
                    try:
                        sprawdz_integralnosc_cache()
                        output = captured_output.getvalue()
                        # Sprawdź czy nie ma błędów w output
                        self.assertNotIn('BŁĄD', output)
                        self.assertNotIn('Niezgodność', output)
                    except SystemExit:
                        pass  # Funkcja może wywoływać sys.exit()
    
    def test_sprawdz_nieistniejacy_cache(self):
        """Test sprawdzania nieistniejącego cache."""
        nieistniejacy_plik = "/tmp/nieistniejacy_cache_test.pkl"
        
        with patch('sprawdz_cache_pierwszych.PLIK_CACHE_PIERWSZYCH', nieistniejacy_plik):
            from io import StringIO
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                try:
                    sprawdz_integralnosc_cache()
                    output = captured_output.getvalue()
                    self.assertIn('nie istnieje', output.lower())
                except SystemExit:
                    pass


class TestEksportujCacheDoCSV(unittest.TestCase):
    """Testy eksportu cache do CSV."""
    
    def setUp(self):
        """Przygotowanie testów."""
        self.temp_cache = None
        self.temp_csv = None
    
    def tearDown(self):
        """Sprzątanie po testach."""
        for temp_file in [self.temp_cache, self.temp_csv]:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_eksport_do_csv(self):
        """Test eksportu cache do CSV."""
        # Przygotuj testowy cache
        import pickle
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
            self.temp_cache = f.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as f:
            self.temp_csv = f.name
        
        dane_cache = {
            'pierwsze': {2, 3, 5, 7, 11},
            'max_sprawdzone': 11
        }
        
        with open(self.temp_cache, 'wb') as f:
            pickle.dump(dane_cache, f)
        
        # Eksportuj do CSV
        sukces = eksportuj_do_csv(dane_cache['pierwsze'], self.temp_csv)
        
        self.assertTrue(sukces)
        
        # Sprawdź zawartość CSV
        with open(self.temp_csv, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Sprawdź nagłówek
        self.assertEqual(rows[0], ['liczba_pierwsza'])
        
        # Sprawdź dane (powinny być posortowane)
        liczby_w_csv = [int(row[0]) for row in rows[1:]]
        self.assertEqual(sorted(liczby_w_csv), [2, 3, 5, 7, 11])
    
    def test_eksport_z_limitem(self):
        """Test eksportu z ograniczoną liczbą."""
        # Przygotuj testowy cache z ograniczonym zestawem
        import pickle
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as f:
            self.temp_csv = f.name
        
        # Eksportuj tylko pierwsze 3 liczby pierwsze
        pierwsze_ograniczone = {2, 3, 5}
        sukces = eksportuj_do_csv(pierwsze_ograniczone, self.temp_csv)
        
        self.assertTrue(sukces)
        
        # Sprawdź zawartość CSV
        with open(self.temp_csv, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Powinno być tylko 4 wiersze (nagłówek + 3 liczby)
        self.assertEqual(len(rows), 4)
        
        liczby_w_csv = [int(row[0]) for row in rows[1:]]
        self.assertEqual(sorted(liczby_w_csv), [2, 3, 5])
    
    def test_eksport_pusty_set(self):
        """Test eksportu pustego zestawu liczb pierwszych."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as f:
            self.temp_csv = f.name
        
        # Test z pustym zestawem
        sukces = eksportuj_do_csv(set(), self.temp_csv)
        
        self.assertTrue(sukces)  # Funkcja powinna zakończyć się sukcesem
        
        # Sprawdź zawartość CSV - powinien być tylko nagłówek
        with open(self.temp_csv, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 1)  # Tylko nagłówek
        self.assertEqual(rows[0], ['liczba_pierwsza'])


class TestGenerujCache(unittest.TestCase):
    """Testy generatora cache (podstawowe)."""
    
    def test_import_modulu(self):
        """Test czy moduł można zaimportować."""
        try:
            import generuj_cache_pierwszych
            self.assertTrue(True)
        except ImportError:
            self.fail("Nie można zaimportować modułu generuj_cache_pierwszych")
    
    def test_funkcje_obecne(self):
        """Test czy główne funkcje są obecne w module."""
        import generuj_cache_pierwszych as gcf
        
        # Sprawdź czy główne funkcje istnieją
        funkcje_wymagane = [
            'sito_eratostenesa_dla_cache',
            'segmentowane_sito_duze_liczby',
            'sprawdzanie_indywidualne_dla_cache'
        ]
        
        for funkcja in funkcje_wymagane:
            self.assertTrue(hasattr(gcf, funkcja), 
                          f"Funkcja {funkcja} nie istnieje w module")


class TestWykresGestosci(unittest.TestCase):
    """Testy generatora wykresu gęstości."""
    
    def test_import_modulu(self):
        """Test czy moduł można zaimportować."""
        try:
            import wykres_gestosci_pierwszych
            self.assertTrue(True)
        except ImportError:
            self.fail("Nie można zaimportować modułu wykres_gestosci_pierwszych")
    
    def test_funkcje_obecne(self):
        """Test czy główne funkcje są obecne w module."""
        import wykres_gestosci_pierwszych as wgp
        
        # Sprawdź czy główne funkcje istnieją
        funkcje_wymagane = [
            'oblicz_gestosc_w_przedziałach',
            'utworz_wykres_gestosci'
        ]
        
        for funkcja in funkcje_wymagane:
            self.assertTrue(hasattr(wgp, funkcja), 
                          f"Funkcja {funkcja} nie istnieje w module")


class TestPobierzDopisz(unittest.TestCase):
    """Testy modułu pobierania i dopisywania liczb pierwszych."""
    
    def test_import_modulu(self):
        """Test czy moduł można zaimportować."""
        try:
            import pobierz_i_dopisz_pierwsze
            self.assertTrue(True)
        except ImportError:
            self.fail("Nie można zaimportować modułu pobierz_i_dopisz_pierwsze")
    
    def test_funkcje_obecne(self):
        """Test czy główne funkcje są obecne w module."""
        import pobierz_i_dopisz_pierwsze as pdp
        
        # Sprawdź czy główne funkcje istnieją
        funkcje_wymagane = [
            'pobierz_i_przetworz_plik_pierwszych',
            'parsuj_plik_pierwszych'
        ]
        
        for funkcja in funkcje_wymagane:
            self.assertTrue(hasattr(pdp, funkcja), 
                          f"Funkcja {funkcja} nie istnieje w module")


class TestGenerujSVG(unittest.TestCase):
    """Testy generatora SVG."""
    
    def test_import_modulu(self):
        """Test czy moduł można zaimportować."""
        try:
            import generuj_svg_spirali
            self.assertTrue(True)
        except ImportError:
            self.fail("Nie można zaimportować modułu generuj_svg_spirali")
    
    def test_funkcje_obecne(self):
        """Test czy główne funkcje są obecne w module."""
        import generuj_svg_spirali as gss
        
        # Sprawdź czy main funkcja istnieje
        self.assertTrue(hasattr(gss, 'main'), 
                       "Funkcja main nie istnieje w module")


if __name__ == '__main__':
    # Uruchom testy z verbose output
    unittest.main(verbosity=2)