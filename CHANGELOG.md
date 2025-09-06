# Changelog

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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