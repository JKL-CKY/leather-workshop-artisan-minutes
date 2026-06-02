const API_BASE = 'http://localhost:5000/api';

const patternsData = [
    {
        name: '短款钱包',
        file: 'wallet_short.svg',
        description: '经典短款对折钱包，包含卡位和钞位设计',
        difficulty: '入门',
        leather: '植鞣革 1.5mm',
        materials: ['蜡线 2米', '菱斩 2.5mm', '床面处理剂']
    },
    {
        name: '长款钱包',
        file: 'wallet_long.svg',
        description: '商务长款西装夹，多卡位设计，适合正装搭配',
        difficulty: '进阶',
        leather: '植鞣革 1.2mm',
        materials: ['蜡线 3米', '菱斩 2.5mm', '封边液', '五金按扣']
    },
    {
        name: '卡包',
        file: 'card_holder.svg',
        description: '简约卡包，4个卡位，轻薄便携',
        difficulty: '入门',
        leather: '植鞣革 1.2mm',
        materials: ['蜡线 1.5米', '菱斩 2.0mm']
    },
    {
        name: '托特包',
        file: 'tote_bag.svg',
        description: '经典托特包，大容量，日常通勤必备',
        difficulty: '进阶',
        leather: '植鞣革 2.0mm',
        materials: ['蜡线 5米', '菱斩 3.0mm', '提手带', '铆钉']
    },
    {
        name: '笔袋',
        file: 'pencil_case.svg',
        description: '复古笔袋，保护书写工具，文艺气息十足',
        difficulty: '入门',
        leather: '植鞣革 1.5mm',
        materials: ['蜡线 2米', '菱斩 2.5mm', '拉链']
    },
    {
        name: '钥匙包',
        file: 'key_case.svg',
        description: '实用钥匙包，可收纳多把钥匙，防止刮花物品',
        difficulty: '入门',
        leather: '植鞣革 1.5mm',
        materials: ['蜡线 1.5米', '菱斩 2.5mm', '钥匙排', '按扣']
    }
];

let currentFilepath = null;
let currentMarkdown = '';

document.addEventListener('DOMContentLoaded', function() {
    renderPatterns();
    setupUploadHandlers();
    setupNavigation();
    setupModal();
    loadPatternsFromServer();
});

function renderPatterns() {
    const grid = document.getElementById('patternsGrid');
    grid.innerHTML = patternsData.map((pattern, index) => `
        <div class="pattern-card" onclick="showPatternDetail(${index})">
            <div class="pattern-preview">
                <div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#f5e6d3,#e8d4bc);border-radius:8px;">
                    <span style="font-size:3rem;">📐</span>
                </div>
            </div>
            <div class="pattern-info">
                <h3>${pattern.name}</h3>
                <p>${pattern.description}</p>
                <p style="margin-top:0.5rem;color:#d2691e;font-size:0.85rem;">难度：${pattern.difficulty}</p>
            </div>
        </div>
    `).join('');
}

function loadPatternsFromServer() {
    fetch(`${API_BASE}/patterns`)
        .then(res => res.json())
        .then(patterns => {
            console.log('Available patterns from server:', patterns);
        })
        .catch(err => {
            console.log('Could not load patterns from server:', err);
        });
}

function showPatternDetail(index) {
    const pattern = patternsData[index];
    const modal = document.getElementById('patternModal');
    const modalBody = document.getElementById('modalBody');

    modalBody.innerHTML = `
        <h2>${pattern.name}</h2>
        <div class="modal-pattern-svg">
            <div style="width:100%;height:300px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#f5e6d3,#e8d4bc);border-radius:8px;">
                <span style="font-size:8rem;">📐</span>
            </div>
        </div>
        <div class="modal-info">
            <h3>📝 图纸说明</h3>
            <p>${pattern.description}</p>
            
            <h3>📊 难度等级</h3>
            <p>${pattern.difficulty}</p>
            
            <h3>🧵 推荐皮革</h3>
            <p>${pattern.leather}</p>
            
            <h3>📦 所需材料</h3>
            <ul>
                ${pattern.materials.map(m => `<li>${m}</li>`).join('')}
            </ul>
            
            <h3>💡 制作建议</h3>
            <ul>
                <li>先在废皮上练习缝合，掌握手感</li>
                <li>裁皮时刀刃要保持锋利，切口才会整齐</li>
                <li>打孔时菱斩一定要垂直，否则缝线会歪斜</li>
                <li>缝线张力要均匀，不要过紧或过松</li>
                <li>边缘打磨需要耐心，反复多次才能光滑</li>
            </ul>
        </div>
    `;

    modal.style.display = 'block';
}

function setupModal() {
    const modal = document.getElementById('patternModal');
    const closeBtn = document.querySelector('.close');

    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }

            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function setupUploadHandlers() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const processBtn = document.getElementById('processBtn');

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    processBtn.addEventListener('click', processAudio);
}

function handleFile(file) {
    const fileInfo = document.getElementById('fileInfo');
    const processBtn = document.getElementById('processBtn');

    fileInfo.style.display = 'block';
    fileInfo.innerHTML = `✅ 已选择文件：<strong>${file.name}</strong> (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    
    processBtn.disabled = false;

    const formData = new FormData();
    formData.append('file', file);

    fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        currentFilepath = data.filepath;
        console.log('File uploaded:', data);
    })
    .catch(err => {
        console.error('Upload error:', err);
        fileInfo.innerHTML = `❌ 上传失败：${err.message}`;
    });
}

function processAudio() {
    if (!currentFilepath) return;

    const processBtn = document.getElementById('processBtn');
    const processText = document.getElementById('processText');
    const processSpinner = document.getElementById('processSpinner');
    const progressBar = document.getElementById('progressBar');
    const teacherName = document.getElementById('teacherName').value;

    processBtn.disabled = true;
    processText.textContent = '处理中...';
    processSpinner.style.display = 'inline-block';
    progressBar.style.display = 'block';

    fetch(`${API_BASE}/process`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filepath: currentFilepath,
            teacher_name: teacherName || '老师'
        })
    })
    .then(res => res.json())
    .then(data => {
        displayResults(data);
        processText.textContent = '处理完成';
        processSpinner.style.display = 'none';
        progressBar.style.display = 'none';
    })
    .catch(err => {
        console.error('Processing error:', err);
        processText.textContent = '开始处理';
        processSpinner.style.display = 'none';
        progressBar.style.display = 'none';
        processBtn.disabled = false;
        alert('处理失败：' + err.message);
    });
}

function displayResults(data) {
    const resultsContainer = document.getElementById('results');
    const summaryResult = document.getElementById('summaryResult');
    const materialsResult = document.getElementById('materialsResult');
    const markdownResult = document.getElementById('markdownResult');

    currentMarkdown = data.markdown_email;

    let summaryHtml = '';
    if (data.summary && typeof data.summary === 'object') {
        if (data.summary.main_points && data.summary.main_points.length > 0) {
            summaryHtml += '<h4 style="color:#8b4513;margin:1rem 0 0.5rem;">📌 主要知识点</h4>';
            summaryHtml += '<ul>' + data.summary.main_points.map(p => `<li>${p}</li>`).join('') + '</ul>';
        }
        if (data.summary.key_tips && data.summary.key_tips.length > 0) {
            summaryHtml += '<h4 style="color:#8b4513;margin:1rem 0 0.5rem;">💡 关键技巧</h4>';
            summaryHtml += '<ul>' + data.summary.key_tips.map(t => `<li>${t}</li>`).join('') + '</ul>';
        }
        if (data.summary.leather_knowledge && data.summary.leather_knowledge.length > 0) {
            summaryHtml += '<h4 style="color:#8b4513;margin:1rem 0 0.5rem;">📚 皮革知识</h4>';
            summaryHtml += '<ul>' + data.summary.leather_knowledge.map(k => `<li>${k}</li>`).join('') + '</ul>';
        }
        if (data.summary.stitching_techniques && data.summary.stitching_techniques.length > 0) {
            summaryHtml += '<h4 style="color:#8b4513;margin:1rem 0 0.5rem;">🪡 缝线技巧</h4>';
            summaryHtml += '<ul>' + data.summary.stitching_techniques.map(s => `<li>${s}</li>`).join('') + '</ul>';
        }
        if (data.summary.tools_mentioned && data.summary.tools_mentioned.length > 0) {
            summaryHtml += '<h4 style="color:#8b4513;margin:1rem 0 0.5rem;">🛠️ 涉及工具</h4>';
            summaryHtml += '<p>' + data.summary.tools_mentioned.join('、') + '</p>';
        }
    }
    summaryResult.innerHTML = summaryHtml || '<p>暂无摘要数据</p>';

    let materialsHtml = '';
    if (data.materials && data.materials.length > 0) {
        materialsHtml = '<table><thead><tr><th>材料/工具</th><th>数量</th><th>备注</th></tr></thead><tbody>';
        materialsHtml += data.materials.map(m => `
            <tr>
                <td>${m.name || ''}</td>
                <td>${m.quantity || ''}</td>
                <td>${m.notes || ''}</td>
            </tr>
        `).join('');
        materialsHtml += '</tbody></table>';
    }
    materialsResult.innerHTML = materialsHtml || '<p>暂无材料清单</p>';

    markdownResult.value = data.markdown_email || '';

    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function copyMarkdown() {
    const textarea = document.getElementById('markdownResult');
    textarea.select();
    document.execCommand('copy');
    
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '已复制 ✓';
    setTimeout(() => {
        btn.textContent = originalText;
    }, 2000);
}

function downloadMarkdown() {
    if (!currentMarkdown) return;

    const blob = new Blob([currentMarkdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `匠人纪要_课程笔记_${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
