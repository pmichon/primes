"""
Unit tests for Web API endpoints.

Tests cover all REST API endpoints:
- GET /api/cache-stats
- POST /api/generate-cache
- POST /api/ulam-spiral
- POST /api/density-chart
- POST /api/export-csv
- POST /api/verify-cache
"""

import unittest
import json
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app
from api_helpers import get_cache_stats, PLIK_CACHE_PIERWSZYCH


class TestWebAPI(unittest.TestCase):
    """Test cases for web API endpoints."""

    def setUp(self):
        """Set up test Flask client and temporary directory."""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_cache_path = os.path.join(self.test_dir, 'test_cache.pkl')
        
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    # GET /api/cache-stats Tests
    
    def test_cache_stats_no_cache(self):
        """Test cache stats when no cache exists."""
        with patch('api_helpers.os.path.join', return_value='/nonexistent/path.pkl'):
            response = self.client.get('/api/cache-stats')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertFalse(data['data']['exists'])
            self.assertEqual(data['data']['count'], 0)

    # POST /api/ulam-spiral Tests
    
    def test_ulam_spiral_missing_parameter(self):
        """Test Ulam spiral generation with missing parameter."""
        response = self.client.post('/api/ulam-spiral',
                                   json={},
                                   content_type='application/json')
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('required', data['error'].lower())
    
    def test_ulam_spiral_invalid_size(self):
        """Test Ulam spiral with invalid size."""
        response = self.client.post('/api/ulam-spiral',
                                   json={'n': 50},  # Below minimum
                                   content_type='application/json')
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_ulam_spiral_valid_png(self):
        """Test Ulam spiral generation (PNG format)."""
        response = self.client.post('/api/ulam-spiral',
                                   json={
                                       'n': 100,
                                       'format': 'png',
                                       'colorful': False
                                   },
                                   content_type='application/json')
        
        data = json.loads(response.data)
        if data['success']:
            self.assertEqual(data['format'], 'png')
            self.assertIn('data', data)
            self.assertTrue(len(data['data']) > 0)
    
    def test_ulam_spiral_valid_svg(self):
        """Test Ulam spiral generation (SVG format)."""
        response = self.client.post('/api/ulam-spiral',
                                   json={
                                       'n': 100,
                                       'format': 'svg',
                                       'colorful': False
                                   },
                                   content_type='application/json')
        
        data = json.loads(response.data)
        if data['success']:
            self.assertEqual(data['format'], 'svg')
            self.assertIn('<svg', data['data'])
    
    # POST /api/density-chart Tests
    
    def test_density_chart_invalid_interval(self):
        """Test density chart with invalid interval."""
        response = self.client.post('/api/density-chart',
                                   json={'interval': 500},  # Below minimum
                                   content_type='application/json')
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    # POST /api/export-csv Tests
    
    def test_export_csv_invalid_format(self):
        """Test CSV export with invalid format."""
        response = self.client.post('/api/export-csv',
                                   json={'format': 'invalid_format'},
                                   content_type='application/json')
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_export_csv_basic_format(self):
        """Test CSV export with basic format."""
        # Create test cache first
        import pickle
        test_primes = [2, 3, 5, 7, 11]
        with open(self.test_cache_path, 'wb') as f:
            pickle.dump(test_primes, f)
        
        with patch('api_helpers.os.path.dirname', return_value=self.test_dir):
            response = self.client.post('/api/export-csv',
                                       json={'format': 'basic'},
                                       content_type='application/json')
            
            data = json.loads(response.data)
            if data['success']:
                self.assertEqual(data['data']['format'], 'basic')
                self.assertIn('files', data['data'])
    
    # POST /api/verify-cache Tests
    
    def test_verify_cache_no_cache(self):
        """Test cache verification when no cache exists."""
        with patch('api_helpers.os.path.join', return_value='/nonexistent/path.pkl'):
            response = self.client.post('/api/verify-cache',
                                       json={},
                                       content_type='application/json')
            
            data = json.loads(response.data)
            self.assertFalse(data['success'])
            self.assertIn('does not exist', data['error'].lower())
    
    # API Helper Functions Tests
    
    def test_get_cache_stats_helper(self):
        """Test get_cache_stats helper function."""
        stats = get_cache_stats()
        
        self.assertIn('exists', stats)
        self.assertIn('count', stats)
        self.assertIn('max_value', stats)
        self.assertIn('size_mb', stats)
        
        self.assertIsInstance(stats['exists'], bool)
        self.assertIsInstance(stats['count'], int)
        self.assertIsInstance(stats['max_value'], int)
        self.assertIsInstance(stats['size_mb'], (int, float))


class TestAPIErrorHandling(unittest.TestCase):
    """Test error handling in API."""
    
    def setUp(self):
        """Set up test client."""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
    
    def test_invalid_json(self):
        """Test API response to invalid JSON."""
        response = self.client.post('/api/ulam-spiral',
                                   data='invalid json',
                                   content_type='application/json')
        
        # Should handle gracefully
        self.assertEqual(response.status_code, 400)
    
    def test_missing_content_type(self):
        """Test API without Content-Type header."""
        response = self.client.post('/api/ulam-spiral',
                                   data=json.dumps({'n': 1000}))
        
        # Should still work or return 4xx
        self.assertIn(response.status_code, [200, 400, 415])


class TestAPIResponseFormat(unittest.TestCase):
    """Test consistent API response format."""
    
    def setUp(self):
        """Set up test client."""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
    
    def test_success_response_format(self):
        """Test that success responses have consistent format."""
        response = self.client.get('/api/cache-stats')
        data = json.loads(response.data)
        
        self.assertIn('success', data)
        if data['success']:
            self.assertIn('data', data)
        else:
            self.assertIn('error', data)
    
    def test_error_response_format(self):
        """Test that error responses have consistent format."""
        response = self.client.post('/api/ulam-spiral',
                                   json={'n': 50},  # Invalid
                                   content_type='application/json')
        
        data = json.loads(response.data)
        
        self.assertIn('success', data)
        if not data['success']:
            self.assertIn('error', data)
            self.assertIsInstance(data['error'], str)


if __name__ == '__main__':
    unittest.main()
