"""
使用Flask框架实现的流式API演示
展示多种流式响应的实现方式
"""

from flask import Flask, Response, request, render_template_string
import json
import time
import random
import threading
from datetime import datetime

app = Flask(__name__)

# 1. 基础文本流式响应
@app.route('/stream/text')
def stream_text():
    """流式返回文本数据"""
    
    def generate_text():
        messages = [
            "欢迎使用Flask流式API！",
            "这是第一条消息...",
            "正在处理您的请求...",
            "数据正在生成中...",
            "即将完成...",
            "流式传输完成！"
        ]
        
        for i, message in enumerate(messages):
            yield f"[{i+1}/{len(messages)}] {message}\n"
            time.sleep(1)  # 模拟处理时间
    
    return Response(
        generate_text(),
        mimetype='text/plain',
        headers={'Cache-Control': 'no-cache'}
    )

# 2. JSON流式响应
@app.route('/stream/json')
def stream_json():
    """流式返回JSON数据"""
    
    def generate_json():
        for i in range(10):
            data = {
                "id": i + 1,
                "timestamp": time.time(),
                "message": f"这是第 {i+1} 条JSON消息",
                "random_value": random.randint(1, 100),
                "status": "processing" if i < 9 else "completed"
            }
            yield f"{json.dumps(data, ensure_ascii=False)}\n"
            time.sleep(0.5)
    
    return Response(
        generate_json(),
        mimetype='application/json',
        headers={'Cache-Control': 'no-cache'}
    )

# 3. Server-Sent Events (SSE) 流式响应
@app.route('/stream/sse')
def stream_sse():
    """Server-Sent Events 流式响应"""
    
    def generate_sse():
        yield "data: 连接已建立\n\n"
        
        for i in range(20):
            # 发送不同类型的事件
            if i % 5 == 0:
                event_type = "status"
                data = {"type": "status", "message": f"进度: {i*5}%"}
            else:
                event_type = "data"
                data = {
                    "type": "data",
                    "id": i,
                    "content": f"实时数据 #{i}",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
            
            yield f"event: {event_type}\n"
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            time.sleep(0.8)
        
        # 发送结束事件
        yield "event: end\n"
        yield f"data: {json.dumps({'message': '流式传输结束'}, ensure_ascii=False)}\n\n"
    
    return Response(
        generate_sse(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Cache-Control'
        }
    )

# 4. 模拟聊天机器人流式响应
@app.route('/stream/chat')
def stream_chat():
    """模拟聊天机器人的流式响应"""
    message = request.args.get('message', '你好')
    
    def generate_chat_response():
        # 模拟AI思考过程
        thinking_steps = [
            "正在理解您的问题...",
            "搜索相关信息...",
            "组织回答内容...",
            "生成回复..."
        ]
        
        for step in thinking_steps:
            yield f"data: {json.dumps({'type': 'thinking', 'content': step}, ensure_ascii=False)}\n\n"
            time.sleep(0.5)
        
        # 模拟逐字输出回复
        response_text = f"您好！您刚才说的是：'{message}'。这是一个Flask流式API演示，我正在逐字为您生成回复。流式响应可以让用户实时看到内容生成过程，提供更好的用户体验。"
        
        current_text = ""
        for char in response_text:
            current_text += char
            yield f"data: {json.dumps({'type': 'response', 'content': current_text}, ensure_ascii=False)}\n\n"
            time.sleep(0.05)  # 模拟打字效果
        
        # 发送完成信号
        yield f"data: {json.dumps({'type': 'done', 'content': '回复完成'}, ensure_ascii=False)}\n\n"
    
    return Response(
        generate_chat_response(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

# 5. 文件流式下载
@app.route('/stream/download')
def stream_download():
    """流式下载大文件（模拟）"""
    
    def generate_file_content():
        # 模拟大文件内容
        total_chunks = 50
        
        for i in range(total_chunks):
            chunk_data = f"这是文件的第 {i+1} 块数据，包含一些示例内容...\n" * 10
            yield chunk_data.encode('utf-8')
            time.sleep(0.1)  # 模拟网络延迟
    
    return Response(
        generate_file_content(),
        mimetype='application/octet-stream',
        headers={
            'Content-Disposition': 'attachment; filename=demo_file.txt'
        }
    )

# 6. 实时日志流
@app.route('/stream/logs')
def stream_logs():
    """模拟实时日志流"""
    
    def generate_logs():
        log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        services = ["API", "Database", "Cache", "Queue", "Auth"]
        
        for i in range(100):
            level = random.choice(log_levels)
            service = random.choice(services)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            log_entry = {
                "timestamp": timestamp,
                "level": level,
                "service": service,
                "message": f"这是来自 {service} 服务的 {level} 级别日志消息 #{i+1}",
                "request_id": f"req_{random.randint(1000, 9999)}"
            }
            
            yield f"data: {json.dumps(log_entry, ensure_ascii=False)}\n\n"
            time.sleep(random.uniform(0.2, 1.0))  # 随机间隔
    
    return Response(
        generate_logs(),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache'}
    )

# 7. 数据处理进度流
@app.route('/stream/progress')
def stream_progress():
    """模拟数据处理进度"""
    
    def generate_progress():
        total_items = 100
        
        for i in range(total_items + 1):
            progress = {
                "current": i,
                "total": total_items,
                "percentage": round((i / total_items) * 100, 2),
                "status": "processing" if i < total_items else "completed",
                "message": f"正在处理第 {i} 项，共 {total_items} 项"
            }
            
            yield f"data: {json.dumps(progress, ensure_ascii=False)}\n\n"
            time.sleep(0.1)
    
    return Response(
        generate_progress(),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache'}
    )

# 8. 演示页面
@app.route('/')
def demo_page():
    """演示页面"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 流式 API 演示</title>
        <meta charset="utf-8">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { margin: 0; font-size: 2.5em; }
            .header p { margin: 10px 0 0 0; opacity: 0.9; }
            .content { padding: 30px; }
            .endpoint { 
                margin: 25px 0; 
                padding: 20px; 
                border: 2px solid #e1e5e9; 
                border-radius: 10px; 
                transition: all 0.3s ease;
            }
            .endpoint:hover { 
                border-color: #667eea; 
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
            }
            .endpoint h3 { 
                margin-top: 0; 
                color: #333; 
                font-size: 1.3em;
            }
            .endpoint p { 
                color: #666; 
                margin: 10px 0;
            }
            .test-area { 
                margin: 15px 0; 
                padding: 15px; 
                background: #f8f9fa; 
                border-radius: 8px; 
                border-left: 4px solid #667eea;
            }
            button { 
                padding: 10px 20px; 
                margin: 5px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                border: none; 
                border-radius: 25px; 
                cursor: pointer; 
                font-weight: bold;
                transition: all 0.3s ease;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }
            button:active { transform: translateY(0); }
            input[type="text"] {
                padding: 10px;
                border: 2px solid #e1e5e9;
                border-radius: 5px;
                margin: 5px;
                width: 300px;
                font-size: 14px;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            #output { 
                margin: 20px 0; 
                padding: 20px; 
                background: #1a1a1a; 
                color: #00ff00; 
                font-family: 'Courier New', monospace; 
                height: 400px; 
                overflow-y: auto; 
                border-radius: 8px;
                border: 2px solid #333;
                font-size: 13px;
                line-height: 1.4;
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            .stat-item {
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                color: #666;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Flask 流式 API 演示</h1>
                <p>体验实时数据流的强大功能</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">7</div>
                        <div class="stat-label">API端点</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">∞</div>
                        <div class="stat-label">实时数据</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">0ms</div>
                        <div class="stat-label">延迟感知</div>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>📝 1. 文本流式响应</h3>
                    <p>演示基础的文本流式传输，逐步返回文本内容</p>
                    <div class="test-area">
                        <button onclick="testEndpoint('/stream/text')">🚀 测试文本流</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>📊 2. JSON流式响应</h3>
                    <p>演示JSON数据的流式传输，实时返回结构化数据</p>
                    <div class="test-area">
                        <button onclick="testEndpoint('/stream/json')">📊 测试JSON流</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>⚡ 3. Server-Sent Events</h3>
                    <p>演示SSE事件流，支持不同类型的实时事件推送</p>
                    <div class="test-area">
                        <button onclick="testSSE('/stream/sse')">⚡ 测试SSE</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>🤖 4. 聊天机器人流式响应</h3>
                    <p>模拟AI聊天的流式回复，展现打字机效果</p>
                    <div class="test-area">
                        <input type="text" id="chatInput" placeholder="输入您的消息..." value="你好，请介绍一下Flask流式API">
                        <button onclick="testChat()">💬 发送消息</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>📋 5. 实时日志流</h3>
                    <p>模拟实时日志数据流，展示系统监控场景</p>
                    <div class="test-area">
                        <button onclick="testSSE('/stream/logs')">📋 查看日志流</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>📈 6. 进度流</h3>
                    <p>模拟数据处理进度，实时显示任务完成状态</p>
                    <div class="test-area">
                        <button onclick="testSSE('/stream/progress')">📈 查看进度</button>
                    </div>
                </div>
                
                <div class="endpoint">
                    <h3>💾 7. 文件流式下载</h3>
                    <p>演示大文件的流式下载</p>
                    <div class="test-area">
                        <button onclick="window.open('/stream/download')">💾 下载文件</button>
                    </div>
                </div>
                
                <div class="test-area">
                    <h3>🖥️ 输出控制台</h3>
                    <button onclick="clearOutput()">🗑️ 清空输出</button>
                    <button onclick="toggleOutput()">👁️ 切换显示</button>
                    <div id="output"></div>
                </div>
            </div>
        </div>
        
        <script>
            const output = document.getElementById('output');
            let outputVisible = true;
            
            function clearOutput() {
                output.innerHTML = '';
            }
            
            function toggleOutput() {
                outputVisible = !outputVisible;
                output.style.display = outputVisible ? 'block' : 'none';
            }
            
            function appendOutput(text, type = 'normal') {
                const timestamp = new Date().toLocaleTimeString();
                const colors = {
                    normal: '#00ff00',
                    info: '#00bfff',
                    warning: '#ffa500',
                    error: '#ff4444',
                    success: '#00ff88'
                };
                
                const color = colors[type] || colors.normal;
                output.innerHTML += `<span style="color: #888">[${timestamp}]</span> <span style="color: ${color}">${text}</span>\\n`;
                output.scrollTop = output.scrollHeight;
            }
            
            async function testEndpoint(url) {
                clearOutput();
                appendOutput(`🚀 开始测试: ${url}`, 'info');
                
                try {
                    const response = await fetch(url);
                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    
                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) {
                            appendOutput('✅ 流式传输完成', 'success');
                            break;
                        }
                        
                        const text = decoder.decode(value);
                        appendOutput(text.trim());
                    }
                } catch (error) {
                    appendOutput(`❌ 错误: ${error.message}`, 'error');
                }
            }
            
            function testSSE(url) {
                clearOutput();
                appendOutput(`⚡ 开始SSE连接: ${url}`, 'info');
                
                const eventSource = new EventSource(url);
                let messageCount = 0;
                
                eventSource.onmessage = function(event) {
                    messageCount++;
                    appendOutput(`📨 消息 #${messageCount}: ${event.data}`);
                };
                
                eventSource.addEventListener('status', function(event) {
                    appendOutput(`📊 状态更新: ${event.data}`, 'info');
                });
                
                eventSource.addEventListener('data', function(event) {
                    appendOutput(`📦 数据: ${event.data}`, 'info');
                });
                
                eventSource.addEventListener('end', function(event) {
                    appendOutput(`🏁 结束: ${event.data}`, 'success');
                    eventSource.close();
                });
                
                eventSource.onerror = function(event) {
                    appendOutput('❌ SSE连接错误', 'error');
                    eventSource.close();
                };
                
                // 30秒后自动关闭连接
                setTimeout(() => {
                    if (eventSource.readyState !== EventSource.CLOSED) {
                        eventSource.close();
                        appendOutput('⏰ 连接超时，已自动关闭', 'warning');
                    }
                }, 30000);
            }
            
            function testChat() {
                const message = document.getElementById('chatInput').value;
                const url = `/stream/chat?message=${encodeURIComponent(message)}`;
                
                clearOutput();
                appendOutput(`💬 发送消息: ${message}`, 'info');
                
                const eventSource = new EventSource(url);
                let currentResponse = '';
                
                eventSource.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'thinking') {
                        appendOutput(`🤔 ${data.content}`, 'warning');
                    } else if (data.type === 'response') {
                        // 更新当前回复
                        currentResponse = data.content;
                        // 清除之前的回复行，显示最新的完整回复
                        const lines = output.innerHTML.split('\\n');
                        const filteredLines = lines.filter(line => !line.includes('🤖'));
                        output.innerHTML = filteredLines.join('\\n');
                        appendOutput(`🤖 ${currentResponse}`);
                    } else if (data.type === 'done') {
                        appendOutput(`✅ ${data.content}`, 'success');
                        eventSource.close();
                    }
                };
                
                eventSource.onerror = function() {
                    appendOutput('❌ 聊天连接错误', 'error');
                    eventSource.close();
                };
            }
            
            // 页面加载完成后的欢迎信息
            window.onload = function() {
                appendOutput('🎉 欢迎使用Flask流式API演示！', 'success');
                appendOutput('💡 点击上方按钮开始体验各种流式API功能', 'info');
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

# 健康检查端点
@app.route('/health')
def health_check():
    """健康检查"""
    return {
        "status": "healthy", 
        "timestamp": time.time(),
        "server": "Flask",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    print("🚀 启动Flask流式API演示服务器...")
    print("📱 访问 http://localhost:5000 查看演示页面")
    print("🔧 健康检查: http://localhost:5000/health")
    print("⚡ 服务器支持热重载，修改代码后自动重启")
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )