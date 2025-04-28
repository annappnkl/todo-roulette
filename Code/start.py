import threading
import time
import subprocess
from pyngrok import ngrok

# Function to start Streamlit in the background
def run_streamlit():
    subprocess.run(["streamlit", "run", "main.py"])

# Start Streamlit in a separate thread
thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()

# Wait until Streamlit is ready
time.sleep(5)

# Open ngrok tunnel
public_url = ngrok.connect(8501)
print(f"🚀 Streamlit is running! Click here: {public_url}")