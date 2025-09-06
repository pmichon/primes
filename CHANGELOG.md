# Changelog

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-01-09

### 🧪 Dodane - Kompleksowy Pakiet Testów Jednostkowych
- **Główny pakiet testów** (`test_ulam_spiral.py`):
  - 17 testów jednostkowych dla podstawowej funkcjonalności spirali Ulama
  - Testy funkcji sprawdzania pierwszości liczb (`czy_pierwsza`)
  - Testy generowania współrzędnych spirali (`generuj_wspolrzedne_spirali`)
  - Kompleksowe testy systemu cache liczb pierwszych
  - Testy sita Eratostenesa z mechanizmem cache
  - Testy funkcji tworzenia spirali Ulama
  - Testy generowania plików SVG z wizualizacją

- **Testy narzędzi pomocniczych** (`test_cache.py`):
  - 12 testów dla narzędzi weryfikacji i eksportu cache
  - Testy weryfikacji integralności cache liczb pierwszych
  - Testy eksportu cache do formatu CSV
  - Testy importu wszystkich modułów projektu
  - Weryfikacja dostępności kluczowych funkcji w modułach

- **Unified Test Runner** (`run_tests.py`):
  - Automatyczne odkrywanie i uruchamianie testów
  - Szczegółowe raportowanie wyników testów z emoticons
  - Obsługa uruchamiania konkretnych plików testowych
  - Kolorowe podsumowanie wyników z diagnostyką błędów

### ✅ Jakość Kodu
- **Pokrycie testami**: 29 testów jednostkowych covering all major functionality
- **Wszystkie testy przechodzą**: 100% success rate przy uruchomieniu
- **Izolacja testów**: Użycie temporary files i unittest.mock dla czystych testów
- **Kompleksowe przypadki testowe**: Pozytywne, negatywne i brzegowe scenariusze

### 🔧 Techniczne Ulepszenia
- Testy wykorzystują Python `unittest` framework ze standard library
- Mockowanie plików cache i zmiennych środowiskowych dla izolacji
- Obsługa różnych scenariuszy błędów i warunków wyjątkowych
- Weryfikacja poprawności struktur danych i formatów wyjściowych

### 📊 Statystyki Wersji 4.0.0
- **Łącznie testów**: 29 comprehensive unit tests
- **Pliki testowe**: 3 (test_ulam_spiral.py, test_cache.py, run_tests.py) 
- **Linie kodu testów**: ~700 lines of testing code
- **Pokrycie modułów**: Wszystkie główne komponenty projektu

## [3.1.0] - 2025-09-07

### Dodane
- Rozbudowany .gitignore dla lepszej higieny repozytorium
- Automatyczne ignorowanie plików wyjściowych (*.png, *.svg)

### Usunięte
- Wszystkie przykładowe pliki PNG i SVG z repozytorium
- Katalog downloaded_primes/ z danymi testowymi
- Pliki systemowe (.DS_Store) z repozytorium

### Zmienione
- Repozytorium zawiera teraz tylko kod źródłowy i dokumentację
- Znacznie zmniejszony rozmiar repozytorium

## [3.2.1] - 2025-09-07

### Zmienione
- Usunięto wzmianki o narzędziach zewnętrznych z dokumentacji
- Zaktualizowana sekcja współpracy w README.md

## [3.2.0] - 2025-09-07

### Dodane
- CHANGELOG.md - dokumentacja wszystkich zmian w projekcie
- CONTRIBUTING.md - wytyczne dla współpracowników
- setup.py + pyproject.toml - pełna konfiguracja pakietu Python
- Rozszerzony .gitignore dla ekosystemu Python

### Zmienione
- README.md - zaktualizowane funkcjonalności i instrukcje
- Profesjonalizacja całej struktury projektu

## [3.1.0] - 2025-09-07

### Dodane
- Rozbudowany .gitignore dla lepszej higieny repozytorium
- Automatyczne ignorowanie plików wyjściowych (*.png, *.svg)

### Usunięte
- Wszystkie przykładowe pliki PNG i SVG z repozytorium
- Katalog downloaded_primes/ z danymi testowymi
- Pliki systemowe (.DS_Store) z repozytorium

### Zmienione
- Repozytorium zawiera teraz tylko kod źródłowy i dokumentację
- Znacznie zmniejszony rozmiar repozytorium

## [3.0.0] - 2025-09-07

### Dodane
- Generator grafiki wektorowej SVG (`generuj_svg_spirali.py`)
- Funkcja `generuj_svg_spirali_ulama()` w module głównym
- Automatyczne generowanie PNG i SVG w głównym generatorze
- Tooltips i interaktywność w plikach SVG
- Legenda i statystyki wbudowane w SVG

### Zmienione
- Poprawiona wizualizacja - równomierna widoczność liczb pierwszych
- Czarne tło dla lepszego kontrastu (PNG i SVG)
- Eliminacja problemu "jasnego środka" w wizualizacjach
- Jednolite wartości kolorów bez gradacji intensywności

### Poprawione
- Optymalizacja generowania SVG dla dużych zbiorów danych
- Automatyczne skalowanie rozmiaru punktów w zależności od liczby danych

## [2.0.0] - 2024

### Dodane
- Rozszerzone funkcje spirali Ulama
- System cache dla liczb pierwszych
- Narzędzia do pobierania i eksportu liczb pierwszych
- Generator wykresu gęstości liczb pierwszych
- Kompletna dokumentacja README.md

## [1.0.0] - 2024

### Dodane
- Pierwszy release: Generator Spirali Ulama
- Podstawowa funkcjonalność generowania spirali
- Wizualizacja liczb pierwszych