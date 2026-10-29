# DevOps Assignment Submission Portal

## How to Run Application
`pip install flask pytest pytest-json-report requests`  
`python app.py` (Access at http://localhost:5000)

## How to Execute Tests
`pytest -v`

## How to Start Receiver & Tunnel
`python local_receiver.py`  
`ngrok http 5000`