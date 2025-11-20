# API Reference - Web Application

Complete API documentation for the Prime Numbers Web Application.

## Base URL

```
http://localhost:5000
```

## Response Format

All API responses follow this JSON structure:

```json
{
  "success": true|false,
  "data": { ... },        // Present on success
  "error": "message",     // Present on failure
  "code": "ERROR_CODE"    // Present on failure
}
```

---

## Endpoints

### GET /api/cache-stats

Get current cache statistics.

**Request:**
```http
GET /api/cache-stats HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "exists": true,
    "count": 78498,
    "max_value": 1000000,
    "size_mb": 1.42
  }
}
```

**Response Fields:**
- `exists` (boolean): Whether cache file exists
- `count` (integer): Number of primes in cache
- `max_value` (integer): Largest prime in cache
- `size_mb` (float): Cache file size in megabytes

**Errors:**
- None (always returns 200 with exists=false if no cache)

---

### POST /api/generate-cache

Generate prime numbers cache up to specified limit. Uses WebSocket for progress updates.

**Request:**
```http
POST /api/generate-cache HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "limit": 1000000
}
```

**Request Body:**
- `limit` (integer, required): Maximum number to check for primality
  - Min: 100
  - Max: Not enforced (but recommend < 100M for reasonable time)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "count": 78498,
    "max_value": 1000000,
    "time_seconds": 2.45,
    "primes_per_second": 32038.37
  }
}
```

**Response Fields:**
- `count` (integer): Number of primes generated
- `max_value` (integer): Largest prime generated
- `time_seconds` (float): Generation time in seconds
- `primes_per_second` (float): Generation rate

**WebSocket Progress Events:**

Client receives `progress` events during generation:

```json
{
  "percent": 45.2,
  "message": "Generating primes...",
  "current": 452000,
  "total": 1000000
}
```

**Errors:**

```json
// Invalid limit
{
  "success": false,
  "error": "Invalid limit parameter",
  "code": "INVALID_LIMIT"
}

// Generation failed
{
  "success": false,
  "error": "Cache generation failed: <reason>",
  "code": "GENERATION_ERROR"
}
```

---

### POST /api/ulam-spiral

Generate Ulam Spiral visualization.

**Request:**
```http
POST /api/ulam-spiral HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "n": 1000,
  "colorful": true,
  "format": "png"
}
```

**Request Body:**
- `n` (integer, required): Spiral size (number of points)
  - Min: 100
  - Max: 100,000,000
- `colorful` (boolean, optional): Use colorful visualization
  - Default: false
- `format` (string, optional): Output format
  - Values: "png" | "svg"
  - Default: "png"

**Response (200 OK) - PNG:**
```json
{
  "success": true,
  "data": "base64_encoded_image_data...",
  "format": "png",
  "size": 1000
}
```

**Response (200 OK) - SVG:**
```json
{
  "success": true,
  "data": "<svg>...</svg>",
  "format": "svg",
  "size": 1000
}
```

**Response Fields:**
- `data` (string): Base64-encoded PNG or raw SVG markup
- `format` (string): Format of returned data
- `size` (integer): Spiral size (n value)

**Errors:**

```json
// Missing required parameter
{
  "success": false,
  "error": "Parameter 'n' is required",
  "code": "MISSING_PARAMETER"
}

// Invalid size
{
  "success": false,
  "error": "Spiral size must be between 100 and 100000000",
  "code": "INVALID_SIZE"
}

// Generation failed
{
  "success": false,
  "error": "Spiral generation failed: <reason>",
  "code": "GENERATION_ERROR"
}
```

---

### POST /api/density-chart

Generate prime density analysis chart.

**Request:**
```http
POST /api/density-chart HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "interval": 10000,
  "max_range": 1000000
}
```

**Request Body:**
- `interval` (integer, required): Interval size for density calculation
  - Min: 1000
  - Recommended: 10,000 - 100,000
- `max_range` (integer, optional): Maximum range for analysis
  - Default: Uses max value from cache

**Response (200 OK):**
```json
{
  "success": true,
  "data": "base64_encoded_chart_image...",
  "interval": 10000,
  "max_range": 1000000,
  "num_intervals": 100
}
```

**Response Fields:**
- `data` (string): Base64-encoded PNG image
- `interval` (integer): Interval size used
- `max_range` (integer): Maximum range analyzed
- `num_intervals` (integer): Number of intervals in chart

**Errors:**

```json
// Invalid interval
{
  "success": false,
  "error": "Interval must be at least 1000",
  "code": "INVALID_INTERVAL"
}

// No cache available
{
  "success": false,
  "error": "No cache available. Generate cache first.",
  "code": "NO_CACHE"
}

// Chart generation failed
{
  "success": false,
  "error": "Chart generation failed: <reason>",
  "code": "GENERATION_ERROR"
}
```

---

### POST /api/export-csv

Export cache to CSV file(s).

**Request:**
```http
POST /api/export-csv HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "format": "advanced",
  "chunk_size": 1000000
}
```

**Request Body:**
- `format` (string, required): Export format
  - Values: "basic" | "advanced" | "chunks"
  - "basic": Single column with primes
  - "advanced": Multiple columns with metadata
  - "chunks": Multiple files split by chunk_size
- `chunk_size` (integer, optional): Size of each chunk (only for "chunks" format)
  - Default: 1,000,000
  - Min: 100,000

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "files": ["pierwsze_basic.csv"],
    "total_primes": 78498,
    "format": "basic"
  }
}
```

**Response (200 OK) - Chunks:**
```json
{
  "success": true,
  "data": {
    "files": [
      "pierwsze_chunk_1.csv",
      "pierwsze_chunk_2.csv"
    ],
    "total_primes": 1500000,
    "format": "chunks",
    "chunk_size": 1000000,
    "num_chunks": 2
  }
}
```

**Response Fields:**
- `files` (array): List of generated CSV file paths
- `total_primes` (integer): Total number of primes exported
- `format` (string): Export format used
- `chunk_size` (integer, optional): Chunk size (if chunks format)
- `num_chunks` (integer, optional): Number of chunks (if chunks format)

**CSV Formats:**

**Basic:**
```csv
liczba_pierwsza
2
3
5
7
...
```

**Advanced:**
```csv
indeks,liczba_pierwsza,roznica_od_poprzedniej,czy_pierwsza_blizniacz,chunk_id
1,2,0,False,1
2,3,1,True,1
3,5,2,True,1
4,7,2,False,1
...
```

**Errors:**

```json
// No cache available
{
  "success": false,
  "error": "No cache available. Generate cache first.",
  "code": "NO_CACHE"
}

// Invalid format
{
  "success": false,
  "error": "Invalid format. Must be 'basic', 'advanced', or 'chunks'",
  "code": "INVALID_FORMAT"
}

// Export failed
{
  "success": false,
  "error": "CSV export failed: <reason>",
  "code": "EXPORT_ERROR"
}
```

---

### POST /api/verify-cache

Verify cache integrity and correctness.

**Request:**
```http
POST /api/verify-cache HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{}
```

**Request Body:**
Empty object or omitted.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "valid": true,
    "errors": [],
    "stats": {
      "total_primes": 78498,
      "max_value": 1000000,
      "verified_count": 78498
    }
  }
}
```

**Response (200 OK) - With Errors:**
```json
{
  "success": true,
  "data": {
    "valid": false,
    "errors": [
      "Number 4 is not prime",
      "Missing prime: 7"
    ],
    "stats": {
      "total_primes": 78500,
      "max_value": 1000000,
      "verified_count": 78498,
      "error_count": 2
    }
  }
}
```

**Response Fields:**
- `valid` (boolean): Whether cache is valid
- `errors` (array): List of error messages (empty if valid)
- `stats` (object): Verification statistics

**Errors:**

```json
// No cache available
{
  "success": false,
  "error": "No cache available. Generate cache first.",
  "code": "NO_CACHE"
}

// Verification failed
{
  "success": false,
  "error": "Verification process failed: <reason>",
  "code": "VERIFICATION_ERROR"
}
```

---

## WebSocket Events

The application uses Socket.IO for real-time communication.

### Client → Server

**connect**
```javascript
socket.on('connect', () => {
  console.log('Connected to server');
});
```

**disconnect**
```javascript
socket.on('disconnect', () => {
  console.log('Disconnected from server');
});
```

### Server → Client

**progress**

Sent during cache generation to update progress.

```javascript
socket.on('progress', (data) => {
  // data structure:
  {
    percent: 45.2,          // Percentage complete (0-100)
    message: "Processing...", // Status message
    current: 452000,        // Current value
    total: 1000000          // Total to process
  }
});
```

**error**

Sent when an error occurs during async operations.

```javascript
socket.on('error', (data) => {
  // data structure:
  {
    message: "Error description",
    code: "ERROR_CODE",
    details: { ... }        // Optional additional context
  }
});
```

**Example Usage:**

```javascript
const socket = io();

socket.on('connect', () => {
  console.log('WebSocket connected');
});

socket.on('progress', (data) => {
  updateProgressBar(data.percent);
  console.log(`${data.message}: ${data.percent}%`);
});

socket.on('error', (data) => {
  console.error(`Error: ${data.message}`);
  showAlert(data.message, 'error');
});
```

---

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_LIMIT` | Limit parameter invalid or out of range | 400 |
| `INVALID_SIZE` | Size parameter invalid or out of range | 400 |
| `INVALID_INTERVAL` | Interval parameter invalid | 400 |
| `INVALID_FORMAT` | Format parameter invalid | 400 |
| `MISSING_PARAMETER` | Required parameter missing | 400 |
| `NO_CACHE` | Cache file doesn't exist | 404 |
| `GENERATION_ERROR` | Error during generation | 500 |
| `EXPORT_ERROR` | Error during CSV export | 500 |
| `VERIFICATION_ERROR` | Error during verification | 500 |

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests/minute per IP for GET endpoints
- 10 requests/minute per IP for POST endpoints
- WebSocket connections: 5 per IP

---

## CORS

CORS is configured to allow all origins in development. For production, configure specific origins in `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

---

## Examples

### JavaScript (Fetch API)

```javascript
// Get cache stats
const stats = await fetch('/api/cache-stats')
  .then(res => res.json());

console.log(stats.data);

// Generate cache
const result = await fetch('/api/generate-cache', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ limit: 100000 })
}).then(res => res.json());

console.log(`Generated ${result.data.count} primes`);

// Generate Ulam Spiral
const spiral = await fetch('/api/ulam-spiral', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ n: 1000, colorful: true, format: 'png' })
}).then(res => res.json());

// Display image
const img = document.createElement('img');
img.src = `data:image/png;base64,${spiral.data}`;
document.body.appendChild(img);
```

### Python (requests)

```python
import requests

# Get cache stats
response = requests.get('http://localhost:5000/api/cache-stats')
stats = response.json()
print(f"Primes in cache: {stats['data']['count']}")

# Generate cache
response = requests.post('http://localhost:5000/api/generate-cache', 
                        json={'limit': 100000})
result = response.json()
print(f"Generated {result['data']['count']} primes in {result['data']['time_seconds']}s")

# Generate spiral
response = requests.post('http://localhost:5000/api/ulam-spiral',
                        json={'n': 1000, 'format': 'svg'})
svg_data = response.json()['data']

# Save SVG
with open('spiral.svg', 'w') as f:
    f.write(svg_data)
```

### cURL

```bash
# Get cache stats
curl http://localhost:5000/api/cache-stats

# Generate cache
curl -X POST http://localhost:5000/api/generate-cache \
  -H "Content-Type: application/json" \
  -d '{"limit": 100000}'

# Generate Ulam Spiral (PNG)
curl -X POST http://localhost:5000/api/ulam-spiral \
  -H "Content-Type: application/json" \
  -d '{"n": 1000, "colorful": true, "format": "png"}' \
  | jq -r '.data' | base64 -d > spiral.png

# Export CSV
curl -X POST http://localhost:5000/api/export-csv \
  -H "Content-Type: application/json" \
  -d '{"format": "basic"}'
```

---

**Questions or issues?** Open an issue on GitHub!
