from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔹 1. 로컬 Flask에서 파일 업로드 받는 API
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get("file")
    job_id = request.form.get("job_id")

    if not file or not job_id:
        return jsonify({"error": "Missing file or job_id"}), 400

    filename = f"result_{job_id}.xlsx"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    return jsonify({"status": "uploaded", "filename": filename}), 200

# 🔹 2. 업로드된 파일을 OutSystems에 serve하는 API
@app.route('/result/<job_id>', methods=['GET'])
def download_excel(job_id):
    file_path = os.path.join(UPLOAD_FOLDER, f"result_{job_id}.xlsx")

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"TEST_{job_id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# 🔹 3. Render에서 필수: PORT 환경변수 받기
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
