from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400
    
    file_path = "test-report.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"\n[SUCCESS] Received test report for commit {data.get('commit_sha')}. Saved to {file_path}")
    return jsonify({"status": "received", "saved_to": file_path}), 200

if __name__ == '__main__':
    print("Local HTTP Receiver running at http://localhost:5000/report...")
    app.run(host='0.0.0.0', port=5000)