#!/usr/bin/env python3
"""
Flask Web Application for Prime Numbers Toolkit
Provides a web GUI for all prime number generation and visualization features
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import sys
import time
from typing import Dict, Any

# Import API helpers
from api_helpers import (
    get_cache_stats,
    generate_cache_wrapper,
    generate_ulam_spiral_wrapper,
    generate_density_chart_wrapper,
    export_csv_wrapper,
    verify_cache_wrapper
)

# Initialize Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
app.config['SECRET_KEY'] = 'primes-secret-key-change-in-production'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variable for progress tracking
progress_data = {
    'active': False,
    'current': 0,
    'total': 0,
    'message': ''
}


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/cache-stats')
def cache_stats():
    """Get cache statistics."""
    stats = get_cache_stats()
    return jsonify({
        'success': True,
        'data': stats
    })


@app.route('/api/generate-cache', methods=['POST'])
def generate_cache():
    """Generate prime number cache with progress updates."""
    data = request.get_json()
    limit = data.get('limit', 1000000)
    
    def progress_callback(current, total, message):
        """Callback to emit progress via WebSocket."""
        socketio.emit('cache_progress', {
            'current': current,
            'total': total,
            'message': message,
            'percent': int((current / total) * 100) if total > 0 else 0
        })
    
    def generate_async():
        """Run generation in background thread."""
        try:
            socketio.emit('cache_progress', {
                'current': 0,
                'total': limit,
                'message': 'Starting cache generation...',
                'percent': 0
            })
            
            result = generate_cache_wrapper(limit, progress_callback)
            
            socketio.emit('cache_complete', result)
        except Exception as e:
            socketio.emit('cache_error', {'error': str(e)})
    
    # Start generation in background with proper SocketIO context
    socketio.start_background_task(generate_async)
    
    return jsonify({
        'success': True,
        'message': 'Cache generation started',
        'limit': limit
    })


@app.route('/api/ulam-spiral', methods=['POST'])
def ulam_spiral():
    """Generate Ulam spiral."""
    data = request.get_json()
    
    # Validate required parameters
    if 'n' not in data:
        return jsonify({
            'success': False,
            'error': 'Parameter n is required',
            'code': 'MISSING_PARAMETER'
        }), 400
    
    n = data.get('n')
    
    # Validate size range
    if not isinstance(n, int) or n < 100 or n > 100000000:
        return jsonify({
            'success': False,
            'error': 'Spiral size must be between 100 and 100,000,000',
            'code': 'INVALID_SIZE'
        }), 400
    
    colorful = data.get('colorful', False)
    format = data.get('format', 'png')
    
    result = generate_ulam_spiral_wrapper(n, colorful, format)
    return jsonify(result)


@app.route('/api/density-chart', methods=['POST'])
def density_chart():
    """Generate density chart."""
    data = request.get_json()
    interval = data.get('interval', 10000)
    
    # Validate interval
    if not isinstance(interval, int) or interval < 1000:
        return jsonify({
            'success': False,
            'error': 'Interval must be at least 1000',
            'code': 'INVALID_INTERVAL'
        }), 400
    
    max_range = data.get('max_range', None)
    
    result = generate_density_chart_wrapper(interval, max_range)
    return jsonify(result)


@app.route('/api/export-csv', methods=['POST'])
def export_csv():
    """Export cache to CSV format."""
    data = request.get_json()
    format_type = data.get('format', 'basic')
    chunk_size = data.get('chunk_size', 1000000)
    
    result = export_csv_wrapper(format_type, chunk_size)
    return jsonify(result)


@app.route('/api/verify-cache', methods=['POST'])
def verify_cache():
    """Verify cache integrity."""
    result = verify_cache_wrapper()
    return jsonify(result)


@app.route('/api/download-csv/<filename>')
def download_csv(filename):
    """Download generated CSV file."""
    try:
        # Navigate to parent directory where CSV files are saved
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            filename
        )
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print('Client disconnected')


@socketio.on('request_cache_stats')
def handle_cache_stats_request():
    """Handle real-time cache stats request."""
    stats = get_cache_stats()
    emit('cache_stats_update', stats)


if __name__ == '__main__':
    print("=" * 60)
    print("🔢 Prime Numbers Web Application")
    print("=" * 60)
    print(f"Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
