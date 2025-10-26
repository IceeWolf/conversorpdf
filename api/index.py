"""
Vercel Serverless Function Handler
Uses Mangum to adapt Flask app for serverless
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app
from app import app

# Use Mangum to wrap Flask app for serverless
from mangum import Mangum

# Create ASGI handler
handler = Mangum(app)
