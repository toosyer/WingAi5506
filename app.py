from flask import Flask, request, render_template_string
import requests
import time
import json
from datetime import datetime
import pytz
import os  # 添加這行

app = Flask(__name__)

# API配置
API_KEY = "sk-5702c61a17fa4f888c1871a4dcf1625c"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def call_api(prompt):
    """調用AI API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4000
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API錯誤: 狀態碼 {response.status_code}"
            
    except Exception as e:
        return f"連接錯誤: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ""
    ai_response = ""
    thinking_steps = []
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        if user_input:
            # 模擬思考過程
            thinking_steps = [
                "🔍 正在分析問題內容...",
                "📚 檢索相關知識庫...", 
                "🤔 深入思考問題核心...",
                "💡 組織回答內容...",
                "✍️ 生成最終回答..."
            ]
            
            # 調用API
            ai_response = call_api(user_input)

    # 獲取香港當前時間
    hongkong_time = get_hongkong_time()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WingAI問答系統</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
                font-family: "Microsoft JhengHei", Arial, sans-serif; 
            }
            
            body { 
                background: #f8f9fa;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container { 
                max-width: 1200px; 
                margin: 0 auto;
                display: flex;
                gap: 20px;
            }
            
            /* 左側聊天區 */
            .chat-panel { 
                flex: 2; 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            
            .header { 
                text-align: center; 
                margin-bottom: 30px; 
            }
            
            .header h1 { 
                color: #2c3e50; 
                font-size: 2.2em;
                margin-bottom: 10px;
            }
            
            .header .subtitle {
                color: #7f8c8d;
                font-size: 1.1em;
            }
            
            .input-area {
                margin-bottom: 25px;
            }
            
            textarea {
                width: 100%;
                padding: 18px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
                min-height: 100px;
                margin-bottom: 15px;
                transition: border-color 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #3498db;
            }
            
            button {
                width: 100%;
                padding: 16px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s;
            }
            
            button:hover {
                background: #2980b9;
            }
            
            .thinking-process {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                min-height: 120px;
            }
            
            .thinking-step {
                margin-bottom: 8px;
                padding: 8px 12px;
                background: white;
                border-radius: 6px;
                border-left: 4px solid #f39c12;
                animation: fadeIn 0.5s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .result {
                padding: 25px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                background: #f8f9fa;
                white-space: pre-wrap;
                line-height: 1.7;
                min-height: 250px;
                font-size: 15px;
            }
            
            .result.error {
                border-color: #e74c3c;
                background: #fdf2f2;
            }
            
            .result.success {
                border-color: #27ae60;
                background: #f2fdf2;
            }
            
            /* 右側信息區 */
            .info-panel { 
                flex: 1; 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
            }
            
            .clock {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .time {
                font-size: 2em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 8px;
                font-family: 'Courier New', monospace;
            }
            
            .date {
                color: #7f8c8d;
                margin-bottom: 8px;
                font-size: 1.1em;
            }
            
            .location {
                color: #95a5a6;
                font-size: 0.9em;
            }
            
            .tips {
                background: #e8f4fd;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }
            
            .tips h3 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            .copyright {
                text-align: center;
                color: #7f8c8d;
                margin-top: auto;
                padding-top: 25px;
                border-top: 1px solid #ecf0f1;
                font-size: 0.9em;
            }
            
            .loading {
                text-align: center;
                color: #7f8c8d;
                padding: 20px;
            }
            
            @media (max-width: 768px) {
                .container {
                    flex-direction: column;
                }
                
                .chat-panel, .info-panel {
                    padding: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- 左側：聊天區 -->
            <div class="chat-panel">
                <div class="header">
                    <h1>WingAI系統</h1>
                    <div class="subtitle">AI問答服務</div>
                </div>
                
                <form method="POST" id="chatForm">
                    <div class="input-area">
                        <textarea name="user_input" placeholder="請輸入您的問題..." required>{{ user_input }}</textarea>
                        <button type="submit" id="submitBtn">🚀 發出問題</button>
                    </div>
                </form>
                
                {% if thinking_steps and not ai_response %}
                <div class="thinking-process" id="thinkingProcess">
                    <div style="color: #e67e22; font-weight: bold; margin-bottom: 15px;">💭 思考過程中...</div>
                    {% for step in thinking_steps %}
                    <div class="thinking-step">{{ step }}</div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="result {{ 'error' if '錯誤' in ai_response else 'success' if ai_response else '' }}" id="resultArea">
                    {% if ai_response %}
                        {{ ai_response }}
                    {% elif not thinking_steps %}
                        <div class="loading">
                            <div>💡 歡迎使用WingAI系統</div>
                            <div style="margin-top: 15px; font-size: 14px; color: #7f8c8d;">
                                請在左側輸入您的問題，系統將為您提供專業回答
                            </div>
                        </div>
                    {% endif %}
                </div>
            </div>

            <!-- 右側：信息區 -->
            <div class="info-panel">
                <div class="clock">
                    <div class="time" id="currentTime">00:00:00</div>
                    <div class="date" id="currentDate">載入中...</div>
                    <div class="location">🕒 香港時間</div>
                </div>
                
                <div class="tips">
                    <h3>💡 使用提示</h3>
                    <div style="line-height: 1.6; font-size: 14px;">
                        • 可詢問各類專業問題<br>
                        • 支援複雜問題分析<br>
                        • 即時資訊查詢<br>
                        • 技術問題解答<br>
                        • 創意內容生成
                    </div>
                </div>
                
                <div class="copyright">
                    <div>© 2025-2030 WingAI系統</div>
                    <div>專業AI技術驅動</div>
                </div>
            </div>
        </div>

        <script>
            // 時鐘功能
            function updateClock() {
                const now = new Date();
                const timeString = now.toLocaleTimeString('zh-HK', { 
                    hour12: false,
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
                const dateString = now.toLocaleDateString('zh-HK', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    weekday: 'long'
                });
                
                document.getElementById('currentTime').textContent = timeString;
                document.getElementById('currentDate').textContent = dateString;
            }
            
            updateClock();
            setInterval(updateClock, 1000);
            
            // 自動聚焦到輸入框
            document.addEventListener('DOMContentLoaded', function() {
                const textarea = document.querySelector('textarea[name="user_input"]');
                if (textarea) {
                    textarea.focus();
                }
            });
            
            // 表單提交處理
            document.getElementById('chatForm').addEventListener('submit', function() {
                const submitBtn = document.getElementById('submitBtn');
                const resultArea = document.getElementById('resultArea');
                
                submitBtn.textContent = '⏳ 處理中...';
                submitBtn.disabled = true;
                
                if (resultArea) {
                    resultArea.innerHTML = '<div class="loading">💭 AI正在思考中，請稍候...</div>';
                }
            });
            
            // 模擬思考過程動畫
            {% if thinking_steps and not ai_response %}
            let stepIndex = 0;
            const thinkingContainer = document.getElementById('thinkingProcess');
            const steps = {{ thinking_steps | tojson }};
            
            function animateThinking() {
                if (stepIndex < steps.length) {
                    const stepElement = thinkingContainer.querySelectorAll('.thinking-step')[stepIndex];
                    stepElement.style.animation = 'none';
                    setTimeout(() => {
                        stepElement.style.animation = 'fadeIn 0.5s ease-in';
                    }, 10);
                    stepIndex++;
                    setTimeout(animateThinking, 800);
                }
            }
            
            setTimeout(animateThinking, 500);
            {% endif %}
        </script>
    </body>
    </html>
    """
    return render_template_string(html, 
                                user_input=user_input, 
                                ai_response=ai_response,
                                thinking_steps=thinking_steps,
                                hongkong_time=hongkong_time)

def get_hongkong_time():
    """獲取香港當前時間"""
    try:
        hongkong_tz = pytz.timezone('Asia/Hong_Kong')
        hongkong_time = datetime.now(hongkong_tz)
        return hongkong_time.strftime("%Y年%m月%d日 %H:%M:%S")
    except:
        return "時間獲取中..."

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))