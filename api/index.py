"""
Vercel Serverless Function Handler
"""
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the Flask app
from app import app

# Wrap with Mangum for ASGI/Serverless compatibility
from mangum import Mangum

# Create handler for Vercel
handler = Mangum(app, lifespan="off")

# Export for Vercel
__all__ = ['handler']
