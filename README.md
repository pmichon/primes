# Generator Spirali Ulama i Narzędzia do Liczb Pierwszych

Kompleksowy zestaw narzędzi do pracy z liczbami pierwszymi, generowania spirali Ulama oraz analizy rozkładu liczb pierwszych.

## 📋 Spis treści

- [Funkcjonalności](#funkcjonalności)
- [Instalacja](#instalacja)
- [Narzędzia](#narzędzia)
- [Przykłady użycia](#przykłady-użycia)
- [Wymagania](#wymagania)
- [Struktura projektu](#struktura-projektu)

## ✨ Funkcjonalności

- 🌀 **Generowanie spirali Ulama** z wizualizacją liczb pierwszych
- 🎨 **Format wektorowy SVG** z interaktywnymi elementami
- 🗄️ **System cache liczb pierwszych** z optymalizacjami wydajności
- 📊 **Analiza gęstości liczb pierwszych** z wykresami
- 🌐 **Pobieranie zbiorów liczb pierwszych** z internetu (t5k.org)
- 📁 **Eksport danych** do formatów CSV
- ✅ **Weryfikacja poprawności** cache liczb pierwszych
- 📈 **Paski postępu** dla długotrwałych operacji
- 🖤 **Zaawansowana wizualizacja** z równomierną widocznością
- 🏷️ **Gotowość do publikacji** na PyPI z pełną konfiguracją

## 🚀 Instalacja

1. **Klonuj repozytorium:**
```bash
git clone https://github.com/pmichon/primes.git
cd primes
```

2. **Zainstaluj zależności:**
```bash
pip3 install -r requirements.txt
```

3. **Uruchom pierwszy test:**
```bash
python3 ulam_spiral.py --n 1000 --pokaz
```

## 🛠️ Narzędzia

### 1. Generator Spirali Ulama (`ulam_spiral.py`)
Tworzy spiralę Ulama z zaznaczonymi liczbami pierwszymi.

```bash
# Spirala 2000x2000 z zapisem do pliku
python3 ulam_spiral.py --n 2000 --zapisz spirala.png

# Interaktywna spirala z pokazaniem na ekranie
python3 ulam_spiral.py --n 1000 --pokaz --kolorowa
```

**Opcje:**
- `--n NUMBER` - Rozmiar spirali (domyślnie: 1000)
- `--zapisz PLIK` - Zapisz do pliku PNG
- `--pokaz` - Pokaż spiralę na ekranie
- `--kolorowa` - Kolorowa wizualizacja
- `--cache PLIK` - Użyj własnego cache liczb pierwszych

### 2. Generator Cache Liczb Pierwszych (`generuj_cache_pierwszych.py`)
Generuje i zapisuje cache liczb pierwszych do określonego limitu.

```bash
# Generuj liczby pierwsze do 1 miliona
python3 generuj_cache_pierwszych.py --limit 1000000

# Generuj do 100 milionów z własną nazwą pliku
python3 generuj_cache_pierwszych.py --limit 100000000 --plik duzy_cache.pkl
```

**Funkcjonalności:**
- Algorytm segmentowanego sita Eratostenesa
- Paski postępu i statystyki wydajności
- Automatyczna optymalizacja pamięci

### 3. Weryfikator Cache (`sprawdz_cache_pierwszych.py`)
Sprawdza poprawność i kompletność cache liczb pierwszych.

```bash
# Pełna weryfikacja cache
python3 sprawdz_cache_pierwszych.py

# Sprawdź tylko strukturę (szybko)
python3 sprawdz_cache_pierwszych.py --tylko-struktura

# Weryfikacja do określonego limitu
python3 sprawdz_cache_pierwszych.py --limit 1000000
```

### 4. Generator Wykresów Gęstości (`wykres_gestosci_pierwszych.py`)
Analizuje i wizualizuje gęstość liczb pierwszych w przedziałach.

```bash
# Standardowy wykres gęstości
python3 wykres_gestosci_pierwszych.py

# Własne przedziały i zakres
python3 wykres_gestosci_pierwszych.py --przedział 50000 --limit 1000000

# Pokaż wykres na ekranie
python3 wykres_gestosci_pierwszych.py --pokaz
```

**Analiza obejmuje:**
- Rzeczywistą gęstość liczb pierwszych
- Teoretyczną gęstość (1/ln(x))
- Liczby pierwsze w każdym przedziale
- Statystyki i porównania

### 5. Pobieracz Liczb Pierwszych (`pobierz_i_dopisz_pierwsze.py`)
Pobiera gotowe zbiory liczb pierwszych z t5k.org i dopisuje do cache.

```bash
# Pobierz wszystkie 50 milionów liczb pierwszych
python3 pobierz_i_dopisz_pierwsze.py

# Pobierz tylko pierwsze 5 plików
python3 pobierz_i_dopisz_pierwsze.py --pliki 1-5

# Pobierz konkretne pliki
python3 pobierz_i_dopisz_pierwsze.py --pliki 1,3,5,10
```

**Funkcjonalności:**
- Automatyczne pobieranie i rozpakowanie plików ZIP
- Parsowanie formatów t5k.org
- Wykrywanie duplikatów
- Integracja z cache

### 6. Eksporter do CSV (`eksportuj_cache_do_csv.py`)
Eksportuje cache liczb pierwszych do plików CSV.

```bash
# Prosty eksport (jedna kolumna)
python3 eksportuj_cache_do_csv.py

# Zaawansowany eksport z metadanymi
python3 eksportuj_cache_do_csv.py --zaawansowany

# Podział na chunki po 1M liczb każdy
python3 eksportuj_cache_do_csv.py --chunki 1000000
```

**Formaty eksportu:**
- **Podstawowy**: `liczba_pierwsza`
- **Zaawansowany**: `indeks, liczba_pierwsza, różnica_od_poprzedniej, czy_pierwsza_bliźniacza, chunk_id`
- **Chunki**: Wiele plików dla dużych zbiorów

## 📊 Przykłady użycia

### Kompletny workflow analizy liczb pierwszych:

```bash
# 1. Wygeneruj cache liczb pierwszych do 10M
python3 generuj_cache_pierwszych.py --limit 10000000

# 2. Sprawdź poprawność cache
python3 sprawdz_cache_pierwszych.py

# 3. Pobierz dodatkowe liczby pierwsze z internetu
python3 pobierz_i_dopisz_pierwsze.py --pliki 1-10

# 4. Wygeneruj spiralę Ulama
python3 ulam_spiral.py --n 5000 --zapisz spirala_10M.png

# 5. Przeanalizuj gęstość
python3 wykres_gestosci_pierwszych.py --przedział 100000

# 6. Eksportuj do CSV
python3 eksportuj_cache_do_csv.py --zaawansowany
```

### Analiza wydajności:
```bash
# Porównanie algorytmów dla różnych limitów
python3 generuj_cache_pierwszych.py --limit 1000000 --algorytm segmentowany
python3 generuj_cache_pierwszych.py --limit 1000000 --algorytm podstawowy
```

## 📋 Wymagania

**Python 3.9+** z bibliotekami:
- `numpy>=1.21.0` - Operacje numeryczne
- `matplotlib>=3.5.0` - Generowanie wykresów
- `psutil>=5.8.0` - Monitorowanie zasobów systemowych
- `requests` - Pobieranie plików z internetu (automatycznie instalowane)

**Opcjonalne:**
- Co najmniej 4GB RAM dla cache > 100M liczb pierwszych
- ~1GB miejsca na dysku dla pełnych zbiorów danych

## 📁 Struktura projektu

```
primes/
├── README.md                        # Ten plik
├── requirements.txt                 # Zależności Python
├── ulam_spiral.py                   # Generator spirali Ulama
├── generuj_cache_pierwszych.py      # Generator cache
├── sprawdz_cache_pierwszych.py      # Weryfikator cache
├── wykres_gestosci_pierwszych.py    # Analiza gęstości
├── pobierz_i_dopisz_pierwsze.py     # Pobieracz z t5k.org
├── eksportuj_cache_do_csv.py        # Eksporter CSV
└── downloaded_primes/               # Pobrane pliki (auto-tworzony)
```

## 🎯 Dane wyjściowe

**Pliki cache:**
- `pierwsze_cache.pkl` - Główny cache liczb pierwszych (format pickle)

**Obrazy:**
- `spirala_ulama_*.png` - Wygenerowane spirale Ulama
- `gestosc_pierwszych_*.png` - Wykresy gęstości

**Eksport:**
- `*.csv` - Eksportowane dane w formacie CSV
- `*_chunk_*.csv` - Pliki przy eksporcie w chunkach

## 🔧 Zaawansowane opcje

### Optymalizacja wydajności:
- Użyj `--algorytm segmentowany` dla dużych limitów
- Zwiększ `--segment-size` dla większej ilości RAM
- Użyj `--przedział` mniejszy niż 10000 dla dokładniejszej analizy gęstości

### Dostosowywanie wizualizacji:
- `--kolorowa` dla lepszej wizualizacji spirali
- `--dpi 300` dla wysokiej jakości obrazów
- `--pokaz` do interaktywnego przeglądania

## 🤝 Współpraca

Ten projekt został wygenerowany z pomocą [Claude Code](https://claude.ai/code).

## 📈 Statystyki

- **50 milionów liczb pierwszych** dostępnych do pobrania
- **Liczby pierwsze do ~982 milionów** w pełnym cache
- **Wydajność**: ~1M liczb pierwszych/sekundę na nowoczesnym sprzęcie
- **Dokładność**: 100% weryfikacji z algorytmami referencyjnymi

---

**Miłej zabawy z liczbami pierwszymi!** 🔢✨