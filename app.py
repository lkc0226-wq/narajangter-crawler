from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=30000)
            
            content = page.content()
            
            licenses = []
            if '전기공사업' in content:
                licenses.append('전기공사업')
            if '정보통신공사업' in content:
                licenses.append('정보통신공사업')
            if '전문건설업' in content:
                licenses.append('전문건설업')
            
            browser.close()
            
            return jsonify({
                'success': True,
                'licenses': licenses
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
