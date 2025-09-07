# Changelog

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.2.0] - 2025-09-07

### ✨ Nowe funkcje - Grafika SVG
- **Kwadratowe punkty dla liczb pierwszych**: Liczby pierwsze są teraz reprezentowane jako kwadraty w SVG
- **Koła dla liczb złożonych**: Liczby złożone pozostają jako koła dla lepszego rozróżnienia
- **Uproszczony design SVG**: Usunięto etykiety, legendę i statystyki dla czystszego wyglądu
- **Białe tło**: SVG używa białego tła z punktami w odcieniach szarości
- **Lepszy kontrast**: Ciemniejsze kwadraty (#333333) dla liczb pierwszych, jaśniejsze koła (#cccccc) dla złożonych

### 🎨 Interfejs użytkownika
- **Minimalistyczny design**: SVG koncentruje się tylko na wzorze spirali bez dodatkowych elementów
- **Intuicyjna wizualizacja**: Kształty pomagają natychmiast rozpoznać liczby pierwsze od złożonych

## [4.1.0] - 2025-09-07

### 🧹 Poprawiono - Zgodność z PEP-8
- **Automatyczne formatowanie kodu**: Wszystkie pliki Python sformatowane zgodnie z PEP-8
- **Usunięte nieużywane importy**: Usunięto nieużywane importy z wszystkich modułów
- **Usunięte nieużywane zmienne**: Wyczyszczono kod z nieużywanych zmiennych lokalnych
- **Poprawione formatowanie**: Jednolite wcięcia, spacje i formatowanie linii
- **Dodane nowe linie**: Każdy plik Python kończy się pojedynczą nową linią

### 🔧 Techniczne Ulepszenia
- **Zastosowane narzędzia**: autopep8, autoflake, flake8 dla automatycznego formatowania
- **Zgodność z standardami**: Kod spełnia wymagania PEP-8 (z wyjątkiem f-stringów dla debugowania)
- **Zachowana funkcjonalność**: Wszystkie 29 testów jednostkowych nadal przechodzą ✅
- **Lepsza czytelność**: Kod jest bardziej czytelny i profesjonalny

### 📊 Poprawa Jakości Kodu
- **Przed**: ~100 naruszeń PEP-8
- **Po**: 0 znaczących naruszeń PEP-8
- **Narzędzia**: flake8 --max-line-length=100 --extend-ignore=E501,F541
- **Status testów**: 29/29 tests passing ✅

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