"""
Vercel Serverless Function - Flask App Export
This exports the Flask application for Vercel to execute
"""

# Import required modules
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import Flask app from app.py
from app import app

# Export for Vercel Python runtime
# The app variable is what Vercel will execute
__all__ = ['app']
