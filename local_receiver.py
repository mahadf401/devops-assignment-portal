from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def receive_report():
    try:
        data = request.get_json(force=True)
        # Write the incoming JSON report directly to disk as required by Task 4
        with open('test-report.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("\n[+] Webhook received and saved to test-report.json successfully!")
        return jsonify({"status": "success", "message": "Report saved to test-report.json"}), 200
    except Exception as e:
        print(f"[-] Error saving report: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)