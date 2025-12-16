# run_api_local.py

import os
import threading
from pyngrok import ngrok
from app import app # Import your running Flask application

def run_flask_app():
    """Runs the Flask app in a background thread."""
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    print("Starting Flask API...")
    
    # Run Flask in a separate thread so the main thread can handle ngrok
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    
    # 1. Start ngrok tunnel
    # Note: If running this in a new terminal, you might need to install: pip install pyngrok
    # For a stable connection, consider setting an ngrok auth token.
    public_url = ngrok.connect(5000).public_url
    
    print(f"\n==========================================================")
    print(f"🚀 PUBLIC API URL: {public_url}")
    print(f"==========================================================")
    print(f"   API Health Check: {public_url}/health")
    print(f"   Recommendation Endpoint: {public_url}/recommend")
    print("\nAPI is running. Press CTRL+C to stop both Flask and ngrok.")
    
    # Keep the main thread alive until CTRL+C is pressed
    # This loop is necessary to maintain the ngrok tunnel connection
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.kill() # Ensure ngrok process is stopped