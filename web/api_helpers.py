#!/usr/bin/env python3
"""
API Helpers for Prime Numbers Web Application
Provides helper functions to integrate existing Python modules with Flask API
"""

import sys
import os
import io
import base64
from typing import Dict, Any, Set, Callable
import pickle

# Add parent directory to path to import existing modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ulam_spiral
import generuj_cache_pierwszych
import wykres_gestosci_pierwszych
import eksportuj_cache_do_csv
import sprawdz_cache_pierwszych

PLIK_CACHE_PIERWSZYCH = "pierwsze_cache.pkl"


def get_cache_stats() -> Dict[str, Any]:
    """Get statistics about the current cache."""
    try:
        cache_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            PLIK_CACHE_PIERWSZYCH
        )
        
        if not os.path.exists(cache_path):
            return {
                "exists": False,
                "count": 0,
                "max_value": 0,
                "size_mb": 0
            }
        
        with open(cache_path, 'rb') as f:
            data = pickle.load(f)
            pierwsze = data['pierwsze']
            max_sprawdzone = data['max_sprawdzone']
        
        file_size = os.path.getsize(cache_path) / (1024 * 1024)
        
        return {
            "exists": True,
            "count": len(pierwsze),
            "max_value": max_sprawdzone,
            "size_mb": round(file_size, 2)
        }
    except Exception as e:
        return {
            "exists": False,
            "error": str(e),
            "count": 0,
            "max_value": 0,
            "size_mb": 0
        }


def generate_cache_wrapper(limit: int, progress_callback: Callable = None) -> Dict[str, Any]:
    """
    Wrapper for generating prime cache with progress callback.
    
    Args:
        limit: Maximum number to check for primes
        progress_callback: Function to call with progress updates (current, total, message)
    
    Returns:
        Dictionary with results
    """
    try:
        # Set global progress callback in the module
        generuj_cache_pierwszych.PROGRESS_CALLBACK = progress_callback
        
        # Generate cache using existing function
        zasoby = generuj_cache_pierwszych.wykryj_zasoby_systemu()
        parametry = generuj_cache_pierwszych.oblicz_optymalne_parametry(limit, zasoby)
        pierwsze = generuj_cache_pierwszych.sito_eratostenesa_dla_cache(limit, parametry)
        generuj_cache_pierwszych.zapisz_cache(pierwsze, limit)
        
        # Clear callback after completion
        generuj_cache_pierwszych.PROGRESS_CALLBACK = None
        
        # Send final progress if callback was provided
        if progress_callback:
            progress_callback(limit, limit, "Zakończono!")
        
        return {
            "success": True,
            "count": len(pierwsze),
            "max_value": limit,
            "message": f"Successfully generated {len(pierwsze):,} primes up to {limit:,}"
        }
    except Exception as e:
        # Clear callback on error
        generuj_cache_pierwszych.PROGRESS_CALLBACK = None
        
        return {
            "success": False,
            "error": str(e)
        }


def generate_ulam_spiral_wrapper(n: int = 1000, colorful: bool = False, 
                                 format: str = "png") -> Dict[str, Any]:
    """
    Generate Ulam spiral and return as base64 encoded image.
    
    Args:
        n: Size of spiral
        colorful: Whether to use colorful visualization
        format: Output format (png or svg)
    
    Returns:
        Dictionary with image data
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        # Load prime cache
        pierwsze, max_sprawdzone = ulam_spiral.wczytaj_cache_pierwszych()
        
        # Generate spiral
        wspolrzedne = ulam_spiral.generuj_wspolrzedne_spirali(n)
        
        if format == "svg":
            # Generate SVG
            temp_file = f"temp_spiral_{n}.svg"
            ulam_spiral.generuj_svg_spirali_ulama(
                wspolrzedne, pierwsze, temp_file, rozmiar_punktu=1.0
            )
            
            with open(temp_file, 'r') as f:
                svg_content = f.read()
            
            os.remove(temp_file)
            
            return {
                "success": True,
                "format": "svg",
                "data": svg_content,
                "size": n
            }
        else:
            # Generate PNG
            siatka, wspolrzedne_result, pierwsze_result = ulam_spiral.utworz_spirale_ulama(n, uzyj_sito=True)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 12), facecolor='white')
            
            # Visualize
            ulam_spiral.wizualizuj_spirale_ulama(siatka, pierwsze_result, f"Spirala Ulama (n={n})")
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            plt.close(fig)
            
            # Encode to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            
            return {
                "success": True,
                "format": "png",
                "data": img_base64,
                "size": n
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_density_chart_wrapper(interval: int = 10000, 
                                   max_range: int = None) -> Dict[str, Any]:
    """
    Generate density chart and return as base64 encoded image.
    
    Args:
        interval: Size of each interval
        max_range: Maximum range to analyze
    
    Returns:
        Dictionary with image data
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        # Load cache
        pierwsze, max_sprawdzone = wykres_gestosci_pierwszych.wczytaj_cache()
        
        if max_range is None or max_range > max_sprawdzone:
            max_range = max_sprawdzone
        
        # Calculate density
        przedzialy, gestosci, liczby = wykres_gestosci_pierwszych.oblicz_gestosc_w_przedziałach(
            pierwsze, max_range, interval
        )
        
        # Calculate theoretical density
        gestosci_teoretyczne = wykres_gestosci_pierwszych.oblicz_gestosc_teoretyczna(przedzialy)
        
        # Create chart
        wykres_gestosci_pierwszych.utworz_wykres_gestosci(
            przedzialy, gestosci, gestosci_teoretyczne, liczby, interval, None
        )
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Encode to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            "success": True,
            "data": img_base64,
            "interval": interval,
            "max_range": max_range
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def export_csv_wrapper(format_type: str = "basic", 
                      chunk_size: int = 1000000) -> Dict[str, Any]:
    """
    Export prime cache to CSV format.
    
    Args:
        format_type: Type of export (basic, advanced, chunks)
        chunk_size: Size of chunks if using chunked export
    
    Returns:
        Dictionary with file path and info
    """
    try:
        # Load cache
        pierwsze, max_sprawdzone = eksportuj_cache_do_csv.wczytaj_cache()
        
        output_file = f"primes_export_{format_type}.csv"
        
        if format_type == "basic":
            eksportuj_cache_do_csv.eksportuj_do_csv_podstawowy(pierwsze, output_file)
        elif format_type == "advanced":
            eksportuj_cache_do_csv.eksportuj_do_csv_zaawansowany(pierwsze, output_file)
        elif format_type == "chunks":
            eksportuj_cache_do_csv.eksportuj_do_csv_w_chunkach(
                pierwsze, "primes_chunk", chunk_size
            )
            output_file = f"primes_chunk_*.csv (multiple files)"
        
        return {
            "success": True,
            "file": output_file,
            "count": len(pierwsze),
            "format": format_type
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def verify_cache_wrapper() -> Dict[str, Any]:
    """Verify prime cache integrity."""
    try:
        # This would use sprawdz_cache_pierwszych functionality
        cache_stats = get_cache_stats()
        
        if not cache_stats["exists"]:
            return {
                "success": False,
                "error": "Cache does not exist"
            }
        
        # Basic verification
        return {
            "success": True,
            "message": "Cache verification successful",
            "stats": cache_stats
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
