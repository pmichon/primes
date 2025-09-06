# Contributing to Ulam Spiral Generator

Dziękujemy za zainteresowanie wkładem w projekt! Ten dokument zawiera wytyczne dotyczące współtworzenia.

## 🚀 Jak zacząć

1. **Fork projektu** na GitHubie
2. **Klonuj swój fork** lokalnie
3. **Utwórz branch funkcjonalności** (`git checkout -b feature/amazing-feature`)
4. **Wprowadź zmiany** i przetestuj je
5. **Commit zmian** (`git commit -m 'Dodaj amazing feature'`)
6. **Push do brancha** (`git push origin feature/amazing-feature`)
7. **Otwórz Pull Request**

## 📋 Standardy kodu

### Python
- Używaj Python 3.8+ syntax
- Przestrzegaj PEP 8 (formatowanie kodu)
- Dodawaj docstrings do funkcji
- Używaj type hints gdzie to możliwe
- Nazwy zmiennych i funkcji po polsku (zgodnie z konwencją projektu)

### Commit Messages
- Używaj polskich komunikatów commit
- Format: `Typ: krótki opis`
- Przykłady:
  - `Dodaj: nowa funkcja generowania SVG`
  - `Popraw: optymalizacja algorytmu sita`
  - `Usuń: niepotrzebne pliki tymczasowe`

## 🧪 Testowanie

Przed wysłaniem PR upewnij się, że:
- [ ] Kod działa z różnymi rozmiarami danych (n=100, n=10000)
- [ ] Wszystkie funkcje cache działają poprawnie
- [ ] Pliki wyjściowe (PNG/SVG) są generowane
- [ ] Nie ma błędów w konsoli

## 📁 Struktura plików

```
├── ulam_spiral.py              # Główny generator
├── generuj_svg_spirali.py      # Generator SVG
├── generuj_cache_pierwszych.py # Generator cache
├── eksportuj_cache_do_csv.py   # Eksport danych
├── pobierz_i_dopisz_pierwsze.py # Download danych
├── sprawdz_cache_pierwszych.py # Weryfikacja
├── wykres_gestosci_pierwszych.py # Analiza gęstości
├── requirements.txt            # Zależności
├── README.md                  # Dokumentacja
├── CHANGELOG.md               # Historia zmian
└── CONTRIBUTING.md            # Ten plik
```

## 🔧 Rodzaje kontrybucji

### 🐛 Zgłaszanie błędów
- Użyj GitHub Issues
- Opisz kroki reprodukcji
- Podaj wersję Python i OS
- Dołącz logi błędów

### ✨ Nowe funkcjonalności
- Otwórz Issue z opisem funkcjonalności
- Poczekaj na feedback przed implementacją
- Rozważ wpływ na wydajność

### 📖 Dokumentacja
- Poprawki w README.md
- Uzupełnienie docstrings
- Przykłady użycia

### 🎨 Wizualizacje
- Nowe sposoby kolorowania
- Różne formaty eksportu
- Optymalizacje renderowania

## 🚫 Co NIE jest mile widziane

- Zmiany łamiące kompatybilność wstecz
- Kod bez testowania
- Dodawanie dużych plików binarnych
- Zmiany w strukturze cache bez powodu

## 📞 Kontakt

- GitHub Issues dla pytań technicznych
- Pull Requests dla propozycji zmian

Dzięki za wkład w rozwój projektu! 🙏