#!/usr/bin/env python3
"""
Skrypt uruchamiający wszystkie testy jednostkowe
"""

import unittest
import sys
import os

def discover_and_run_tests():
    """Odkryj i uruchom wszystkie testy."""
    print("🧪 ULAM SPIRAL GENERATOR - PAKIET TESTÓW")
    print("=" * 50)
    
    # Dodaj bieżący katalog do ścieżki Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Odkryj wszystkie testy w plików test_*.py
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Uruchom testy
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False,
        buffer=True  # Przechwytuj stdout/stderr podczas testów
    )
    
    print(f"\n🔍 Znaleziono {suite.countTestCases()} testów")
    print("-" * 50)
    
    result = runner.run(suite)
    
    # Podsumowanie
    print("\n" + "=" * 50)
    print("📊 PODSUMOWANIE TESTÓW")
    print(f"✅ Zaliczone: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Nieudane: {len(result.failures)}")
    print(f"💥 Błędy: {len(result.errors)}")
    print(f"⏭️  Pominięte: {len(result.skipped)}")
    print(f"📈 Całkowite: {result.testsRun}")
    
    if result.failures:
        print(f"\n❌ NIEUDANE TESTY ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  • {test}")
    
    if result.errors:
        print(f"\n💥 BŁĘDY ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  • {test}")
    
    # Określ kod wyjścia
    exit_code = 0 if result.wasSuccessful() else 1
    
    if result.wasSuccessful():
        print(f"\n🎉 WSZYSTKIE TESTY PRZESZŁY! ✅")
    else:
        print(f"\n⚠️  NIEKTÓRE TESTY NIE PRZESZŁY! ❌")
    
    return exit_code


def run_specific_test(test_file):
    """Uruchom testy z określonego pliku."""
    print(f"🧪 URUCHAMIANIE TESTÓW Z: {test_file}")
    print("=" * 50)
    
    # Dodaj bieżący katalog do ścieżki Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Załaduj testy z określonego pliku
    loader = unittest.TestLoader()
    
    try:
        # Usuń .py z nazwy pliku jeśli jest
        module_name = test_file.replace('.py', '')
        suite = loader.loadTestsFromName(module_name)
    except Exception as e:
        print(f"❌ Błąd ładowania testów z {test_file}: {e}")
        return 1
    
    # Uruchom testy
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False,
        buffer=True
    )
    
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def main():
    """Główna funkcja."""
    if len(sys.argv) > 1:
        # Uruchom konkretny plik testowy
        test_file = sys.argv[1]
        if not test_file.startswith('test_'):
            test_file = f'test_{test_file}'
        if not test_file.endswith('.py'):
            test_file = f'{test_file}.py'
        
        exit_code = run_specific_test(test_file)
    else:
        # Uruchom wszystkie testy
        exit_code = discover_and_run_tests()
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()