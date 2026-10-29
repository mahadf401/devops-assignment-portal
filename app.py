from flask import Flask, render_template_string, request, jsonify, redirect
import re

app = Flask(__name__)
submissions = []

URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Submission Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; }
        .container { max-width: 650px; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #1b365d; margin-top: 0; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input[type="text"] { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
        button { margin-top: 15px; padding: 10px 20px; background: #1b365d; color: white; border: none; border-radius: 4px; cursor: pointer; }
        table { width: 100%; margin-top: 20px; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #1b365d; color: white; }
    </style>
</head>
<body>
<div class="container">
    <h2>Assignment Submission Portal</h2>
    <form method="POST" action="/submit">
        <label>Student Name:</label>
        <input type="text" name="student_name" required>
        
        <label>Registration Number:</label>
        <input type="text" name="reg_num">
        
        <label>Assignment Title:</label>
        <input type="text" name="title" required>
        
        <label>Submission URL:</label>
        <input type="text" name="submission_url" required>
        
        <button type="submit">Submit Assignment</button>
    </form>
    
    <h3>Submitted Assignments</h3>
    <table>
        <tr><th>Name</th><th>Reg #</th><th>Title</th><th>URL</th></tr>
        {% for sub in submissions %}
        <tr>
            <td>{{ sub.student_name }}</td>
            <td>{{ sub.reg_num }}</td>
            <td>{{ sub.title }}</td>
            <td><a href="{{ sub.submission_url }}" target="_blank">{{ sub.submission_url }}</a></td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, submissions=submissions)

@app.route('/submit', methods=['POST'])
def submit():
    is_form = bool(request.form)
    data = request.form.to_dict() if is_form else request.get_json(silent=True) or {}
    
    student_name = data.get('student_name', '').strip()
    reg_num = data.get('reg_num', '').strip()
    title = data.get('title', '').strip()
    submission_url = data.get('submission_url', '').strip()

    # Validation 1: Required Fields
    if not student_name or not reg_num or not title or not submission_url:
        return jsonify({"status": "error", "message": "Missing required fields (including Registration Number)"}), 400

    # Validation 2: URL Format
    if not URL_REGEX.match(submission_url):
        return jsonify({"status": "error", "message": "Invalid submission URL format. Must start with http:// or https://"}), 400

    record = {
        "student_name": student_name,
        "reg_num": reg_num,
        "title": title,
        "submission_url": submission_url
    }
    submissions.append(record)

    if is_form:
        return redirect('/')
    return jsonify({"status": "success", "message": "Submission saved successfully", "data": record}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)