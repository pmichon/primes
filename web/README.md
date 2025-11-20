# Aplikacja Webowa dla Liczb Pierwszych

## 🌐 Szybki Start

Aplikacja webowa zapewnia przyjazny interfejs GUI do wszystkich funkcjonalności generatora liczb pierwszych.

### Instalacja i Uruchomienie

1. **Zainstaluj zależności:**
   ```bash
   cd web
   pip3 install -r requirements-web.txt
   ```

2. **Uruchom serwer:**
   ```bash
   python3 app.py
   ```

3. **Otwórz przeglądarkę:**
   ```
   http://localhost:5000
   ```

## ✨ Funkcjonalności

### 🗄️ Generowanie Cache
- **Interaktywne generowanie** liczb pierwszych do określonego limitu
- **Real-time progress bar** z WebSocket
- **Automatyczne statystyki** po zakończeniu
- **Optymalizacja wydajności** dla różnych rozmiarów

### 🌀 Spirala Ulama
- **Wizualizacja** liczb pierwszych w układzie spiralnym
- **Format PNG lub SVG** do wyboru
- **Wersja kolorowa** dla lepszej widoczności
- **Podgląd w przeglądarce** i możliwość pobrania

### 📊 Wykres Gęstości
- **Analiza rozkładu** liczb pierwszych
- **Porównanie z teorią** (1/ln(x))
- **Konfigurowalne przedziały**
- **Wysokiej jakości wykresy**

### 💾 Eksport CSV
- **Format podstawowy** - tylko liczby pierwsze
- **Format zaawansowany** - z metadanymi
- **Eksport w chunkach** - dla dużych zbiorów

### ✅ Weryfikacja Cache
- **Sprawdzanie integralności** cache
- **Statystyki w czasie rzeczywistym**
- **Automatyczna walidacja**

## 🎨 Cechy Interfejsu

- **🌓 Dark Mode** - przełączanie między jasnym i ciemnym motywem
- **📱 Responsive Design** - działa na wszystkich urządzeniach
- **⚡ Real-time Updates** - WebSocket dla live progress
- **🎯 Modern UI** - glassmorphism, gradienty, animacje
- **♿ Accessibility** - przyjazny dla użytkownika interfejs

## 🔧 Architektura

### Backend (Flask)
- **REST API** - standardowe endpointy HTTP
- **WebSocket** - real-time komunikacja przez Socket.IO
- **API Helpers** - wrappery dla istniejących modułów Python
- **CORS enabled** - bezpieczna komunikacja cross-origin

### Frontend (Vanilla JS)
- **Modularny kod** - każda funkcjonalność w osobnym pliku
- **No framework** - czysta JavaScript dla szybkości
- **Modern CSS** - custom properties, grid, flexbox
- **Progressive Enhancement** - działa bez JavaScript (podstawowo)

## 📁 Struktura Plików

```
web/
├── app.py                          # Flask server + Socket.IO
├── api_helpers.py                  # Wrappery dla Python modules
├── requirements-web.txt            # Zależności
├── static/
│   ├── css/
│   │   └── style.css              # Design system
│   └── js/
│       ├── app.js                 # Main app logic
│       ├── cache-generator.js     # Cache generation
│       ├── ulam-spiral.js         # Spiral visualization
│       ├── density-chart.js       # Density charts
│       └── csv-exporter.js        # CSV export
└── templates/
    └── index.html                 # Main page
```

## 🚀 API Endpoints

### Cache Management
- `GET /api/cache-stats` - Pobierz statystyki cache
- `POST /api/generate-cache` - Generuj cache (body: `{limit: number}`)
- `GET /api/verify-cache` - Weryfikuj cache

### Visualizations
- `POST /api/ulam-spiral` - Generuj spiralę (body: `{n, colorful, format}`)
- `POST /api/density-chart` - Generuj wykres (body: `{interval, max_range}`)

### Export
- `POST /api/export-csv` - Eksport CSV (body: `{format, chunk_size}`)
- `GET /api/download-csv/<filename>` - Pobierz plik CSV

### WebSocket Events
- `cache_progress` - Progress update (client receives)
- `cache_complete` - Generation complete (client receives)
- `cache_error` - Error occurred (client receives)

## 💡 Wskazówki Użytkowania

1. **Dla małych testów**: Użyj limitu 100,000 - 1,000,000
2. **Dla poważnej analizy**: 10,000,000 - 100,000,000
3. **Spirala Ulama**: Rozmiar 1000-2000 dla dobrego balansu jakość/wydajność
4. **Wykres gęstości**: Przedział 10,000 dla szczegółowej analizy

## 🔒 Bezpieczeństwo

- **Production**: Zmień `SECRET_KEY` w `app.py`
- **Firewall**: Ogranicz dostęp do portu 5000
- **HTTPS**: Użyj reverse proxy (nginx) dla HTTPS
- **Rate limiting**: Dodaj dla API w produkcji

## 🐛 Troubleshooting

**Problem**: Server nie startuje
- **Rozwiązanie**: Sprawdź czy port 5000 jest wolny: `lsof -i :5000`

**Problem**: WebSocket nie działa
- **Rozwiązanie**: Upewnij się że eventlet jest zainstalowany

**Problem**: Brak cache
- **Rozwiązanie**: Wygeneruj cache używając zakładki "Generuj Cache"

## 📝 Development

### Local Development
```bash
# Install dependencies
pip3 install -r requirements-web.txt

# Run in debug mode (auto-reload)
python3 app.py
```

### Adding New Features
1. Dodaj endpoint w `app.py`
2. Dodaj helper function w `api_helpers.py`
3. Dodaj UI w `templates/index.html`
4. Dodaj logikę w nowym pliku JS w `static/js/`

---

**Created with ❤️ for Prime Numbers Enthusiasts**
