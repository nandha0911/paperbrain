#!/bin/bash
# Start the FastAPI backend in the background
python api.py &

# Wait a moment for the API to start
sleep 5

# Start Streamlit frontend (foreground so Docker keeps running)
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
