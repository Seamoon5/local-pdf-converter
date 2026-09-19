import io
import os
import shutil
import subprocess
import tempfile
import threading
import traceback
import webbrowser
import mimetypes
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  

OUTPUT_EXTENSIONS = {'.pdf': 'docx', '.docx': 'pdf', '.doc': 'pdf'}
MAX_SIZE_MB = 60


def convert_pdf_to_docx(src_path, dst_path):
    from pdf2docx import Converter
    cv = Converter(src_path)
    cv.convert(dst_path)
    cv.close()


def convert_docx_to_pdf(src_path, dst_path):
    try:
        from docx2pdf import convert as word_convert
        word_convert(src_path, dst_path)
        if os.path.exists(dst_path) and os.path.getsize(dst_path) > 0:
            return
    except Exception:
        pass

    soffice = shutil.which('soffice') or shutil.which('libreoffice')
    if not soffice:
        raise RuntimeError(
            'No converter found for Word to PDF. '
            'Install Microsoft Word (recommended on Windows) or LibreOffice '
            '(recommended on Linux/Mac).'
        )
    result = subprocess.run(
        [soffice, '--headless', '--convert-to', 'pdf',
         '--outdir', os.path.dirname(dst_path), src_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError('LibreOffice failed: ' + result.stderr.strip())


def perform_conversion(src_path, target_ext):
    stem = os.path.splitext(os.path.basename(src_path))[0]
    dst_path = os.path.join(os.path.dirname(src_path), stem + '.' + target_ext)

    if target_ext == 'docx':
        convert_pdf_to_docx(src_path, dst_path)
    else:
        convert_docx_to_pdf(src_path, dst_path)

    if not os.path.exists(dst_path) or os.path.getsize(dst_path) == 0:
        raise RuntimeError('Conversion produced an empty or missing file.')
    return dst_path


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': f'File is larger than {MAX_SIZE_MB} MB.'}), 413


@app.route('/api/health')
def api_health():
    return jsonify({'status': 'ok'}), 200


@app.route('/api/convert', methods=['POST'])
def api_convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    uploaded = request.files['file']
    if not uploaded.filename:
        return jsonify({'error': 'No file selected.'}), 400

    original_name = secure_filename(uploaded.filename)
    ext = os.path.splitext(original_name)[1].lower()

    if ext not in OUTPUT_EXTENSIONS:
        return jsonify({'error': 'Unsupported file type. Use .pdf, .docx or .doc.'}), 400

    tmp_dir = tempfile.mkdtemp(prefix='pdfconv_')
    try:
        src_path = os.path.join(tmp_dir, original_name)
        uploaded.save(src_path)

        if os.path.getsize(src_path) > MAX_SIZE_MB * 1024 * 1024:
            return jsonify({'error': f'File is larger than {MAX_SIZE_MB} MB.'}), 400

        target_ext = OUTPUT_EXTENSIONS[ext]
        dst_path = perform_conversion(src_path, target_ext)

        # Read the converted file into memory BEFORE deleting anything.
        # Deleting an open file fails on Windows and kills the request
        # with "Failed to fetch".
        with open(dst_path, 'rb') as fh:
            data = fh.read()

        download_name = os.path.splitext(original_name)[0] + '.' + target_ext
        mime = mimetypes.guess_type(download_name)[0] or 'application/octet-stream'
        return send_file(
            io.BytesIO(data),
            as_attachment=True,
            download_name=download_name,
            mimetype=mime
        )
    except IndexError:
        return jsonify({'error': 'The PDF contains no extractable text or pages.'}), 500
    except Exception as exc:
        print('CONVERSION ERROR:', traceback.format_exc())
        return jsonify({'error': str(exc) or 'Unknown error.'}), 500
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == '__main__':
    threading.Timer(1.0, lambda: webbrowser.open('http://127.0.0.1:8000')).start()
    print('Local PDF & Word Converter running at http://127.0.0.1:8000')
    print('Close this window to stop the server.')
    app.run(host='127.0.0.1', port=8000, debug=False)