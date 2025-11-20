# Web GUI Application - Generator Liczb Pierwszych

Nowoczesna aplikacja webowa z interfejsem GUI dla generatora liczb pierwszych, spirali Ulama i analizy gęstości.

## 📋 Spis Treści

- [Przegląd](#przegląd)
- [Funkcjonalności](#funkcjonalności)
- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [API Reference](#api-reference)
- [Architektura](#architektura)
- [Development](#development)
- [Deployment](#deployment)

## 🌐 Przegląd

Aplikacja webowa dostarcza kompletny interfejs graficzny dla wszystkich funkcjonalności projektu liczb pierwszych. Zbudowana z Flask backend i vanilla JavaScript frontend, oferuje real-time updates, interaktywne wizualizacje i intuicyjny UX.

**Tech Stack:**
- **Backend**: Flask 2.3+ z Flask-SocketIO
- **Frontend**: Vanilla JavaScript (ES6+), Modern CSS
- **Communication**: RESTful API + WebSockets
- **Visualizations**: Matplotlib (backend), Canvas/SVG (frontend)

## ✨ Funkcjonalności

### 1. 🗄️ Generator Cache Liczb Pierwszych
- Generowanie cache do dowolnego limitu (max 100,000,000)
- Real-time progress tracking via WebSocket
- Optymalizowany algorytm segmentowanego sita Eratostenesa
- Automatyczne zapisywanie i wczytywanie cache

### 2. 🌀 Spirala Ulama
- Generowanie spiral do 100,000,000 punktów
- Formaty: PNG (raster) i SVG (wektor)
- Opcja kolorowej wizualizacji
- Download wygenerowanych obrazów
- Podgląd inline w przeglądarce

### 3. 📊 Wykres Gęstości Liczb Pierwszych
- Analiza gęstości w konfigurowalnych przedziałach
- Porównanie z teoretyczną gęstością (1/ln(x))
- Interaktywne wykresy PNG
- Automatyczne skalowanie osi

### 4. 💾 Eksport CSV
- 3 formaty eksportu:
  - **Podstawowy**: pojedyncza kolumna liczb pierwszych
  - **Zaawansowany**: z metadanymi (indeks, różnice, bliźniacze)
  - **Chunki**: podział na mniejsze pliki
- Automatyczne generowanie i download

### 5. ✅ Weryfikacja Cache
- Sprawdzanie integralności cache
- Weryfikacja pierwszości liczb
- Raportowanie błędów i statystyk

### 6. 📡 Dashboard Status
- Real-time cache statistics
- Liczba wygenerowanych liczb pierwszych
- Maksymalna wartość w cache
- Rozmiar pliku cache w MB

### 7. 🎨 Modern UI/UX
- Responsive design (desktop, tablet, mobile)
- Dark/Light theme toggle
- Smooth animations i transitions
- Glassmorphism design
- Accessible (keyboard navigation, ARIA labels)

## 🚀 Instalacja

### Requirements

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Nowoczesna przeglądarka (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

### Installation Steps

**Option A: Using uv (Recommended)**

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to web directory
cd primes/web

# Install dependencies from lockfile (ensures reproducible builds)
uv pip sync requirements-web.lock
```

**Option B: Using pip**

```bash
cd primes/web
pip3 install -r requirements-web.txt
```

2. **Weryfikuj instalację:**

```bash
python3 -c "import flask, flask_socketio; print('OK')"
```

## 📖 Użycie

### Uruchomienie serwera

```bash
cd primes/web
python3 app.py
```

Server wystartuje na `http://localhost:5000`

### Pierwsze kroki

1. **Otwórz przeglądarkę** → `http://localhost:5000`
2. **Wygeneruj cache** (zakładka "Generuj Cache"):
   - Ustaw limit np. 100,000 dla szybkiego testu
   - Kliknij "Generuj Cache"
   - Obserwuj postęp w real-time
3. **Wygeneruj spiralę Ulama** (zakładka "Spirala Ulama"):
   - Rozmiar: 1000 (dla szybkiego renderowania)
   - Format: PNG lub SVG
   - Opcjonalnie: zaznacz "Wersja kolorowa"
   - Kliknij "Generuj Spiralę"
4. **Eksploruj inne funkcje** w kolejnych zakładkach

### Zmienne środowiskowe

```bash
# Port serwera (domyślnie: 5000)
export FLASK_PORT=8080

# Tryb debug (domyślnie: False)
export FLASK_DEBUG=True

# Host (domyślnie: 127.0.0.1)
export FLASK_HOST=0.0.0.0
```

## 🔌 API Reference

Zobacz [API.md](API.md) dla kompletnej dokumentacji API.

### Quick Reference

**GET Endpoints:**
- `GET /api/cache-stats` - Pobierz statystyki cache
- `GET /static/*` - Pliki statyczne (CSS, JS, images)

**POST Endpoints:**
- `POST /api/generate-cache` - Generuj cache liczb pierwszych
- `POST /api/ulam-spiral` - Generuj spiralę Ulama
- `POST /api/density-chart` - Generuj wykres gęstości
- `POST /api/export-csv` - Eksportuj do CSV
- `POST /api/verify-cache` - Weryfikuj cache

**WebSocket Events:**
- `connect` - Połączenie nawiązane
- `disconnect` - Połączenie zamknięte
- `progress` - Progress update (cache generation)
- `error` - Błąd operacji

## 🏗️ Architektura

```
web/
├── app.py                     # Flask application entry point
├── api_helpers.py             # API helper functions
├── requirements-web.txt       # Python dependencies
├── templates/
│   └── index.html            # Main SPA template
└── static/
    ├── css/
    │   └── style.css         # Global styles + design system
    └── js/
        ├── app.js            # Main app logic, theme, utilities
        ├── cache-generator.js  # Cache generation module
        ├── ulam-spiral.js      # Ulam spiral module
        ├── density-chart.js    # Density chart module
        └── csv-exporter.js     # CSV export module
```

### Design Patterns

**Frontend:**
- Module pattern (każda funkcja w osobnym pliku)
- Event-driven architecture (addEventListener)
- Utility-first CSS z design tokens
- Progressive enhancement

**Backend:**
- RESTful API design
- Function-based views
- Stateless endpoints (oprócz cache)
- Error handling middleware

### Data Flow

```
User Action (Browser)
    ↓
JavaScript Event Handler
    ↓
Fetch API / Socket.IO
    ↓
Flask Route Handler
    ↓
Helper Function (api_helpers.py)
    ↓
Core Python Module (../generuj_cache_pierwszych.py etc.)
    ↓
Response (JSON/Binary)
    ↓
JavaScript Callback
    ↓
DOM Update / File Download
```

## 💻 Development

### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/pmichon/primes.git
cd primes/web

# Install dependencies
pip3 install -r requirements-web.txt

# Run in debug mode
export FLASK_DEBUG=True
python3 app.py
```

### Code Style

- **Python**: PEP 8 compliant (via autopep8)
- **JavaScript**: ES6+, airbnb style guide
- **CSS**: BEM methodology dla klas

### Testing

```bash
# Unit tests
python3 -m unittest test_api.py

# Integration tests
python3 -m unittest test_integration.py

# All tests
python3 ../run_tests.py
```

### Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

**IE 11**: ❌ Not supported (ES6+ features)

## 🚀 Deployment

### Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use production WSGI server (gunicorn, uWSGI)
- [ ] Configure reverse proxy (nginx, Apache)
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Configure CORS properly
- [ ] Set up monitoring/logging

### Example: Gunicorn + Nginx

**Install gunicorn:**
```bash
pip3 install gunicorn
```

**Run with gunicorn:**
```bash
gunicorn -w 4 -b 127.0.0.1:5000 --worker-class eventlet app:app
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--worker-class", "eventlet", "app:app"]
```

## 🐛 Troubleshooting

### Common Issues

**Port już używany:**
```bash
# Zmień port
export FLASK_PORT=8080
python3 app.py
```

**Brak modułu flask:**
```bash
pip3 install flask flask-socketio flask-cors
```

**Cache nie działa:**
- Sprawdź czy `pierwsze_cache.pkl` istnieje w `web/`
- Wygeneruj nowy cache przez GUI
- Upewnij się że masz uprawnienia do zapisu

**WebSocket nie łączy:**
- Sprawdź console przeglądarki
- Upewnij się że socket.io.js jest załadowany
- Sprawdź czy port nie jest blokowany przez firewall

## 📝 License

MIT License - zobacz główny [LICENSE](../LICENSE)

## 🤝 Contributing

Contributions welcome! Zobacz główny [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Miłej zabawy z aplikacją webową!** 🎉
