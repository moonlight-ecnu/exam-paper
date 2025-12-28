const BASE_URL = 'http://127.0.0.1:5000'; // 后端地址
let currentToken = localStorage.getItem('token');
let currentGroup = null;

// Namespace for app functions
const app = {
    // API Request Wrapper
    apiRequest: async (endpoint, method, data, isMultipart = false) => {
        const headers = {};
        if (currentToken) {
            headers['Authorization'] = currentToken;
        }

        let body;
        if (isMultipart) {
            body = data;
        } else {
            headers['Content-Type'] = 'application/json';
            body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${BASE_URL}${endpoint}`, {
                method: method,
                headers: headers,
                body: body
            });

            const result = await response.json();
            
            // Backend returns code=0 for success, and data in 'payload'
            if (result.code === 0 || result.code === 200) {
                return result.payload || result.data;
            } else {
                app.showToast(`错误: ${result.msg || '未知错误'}`);
                return null;
            }
        } catch (error) {
            app.showToast(`请求失败: ${error.message}`);
            console.error(error);
            return null;
        }
    },

    showToast: (message) => {
        const container = document.getElementById('log-container');
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerText = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    },

    // Auth Functions
    switchAuth: (type) => {
        const tabs = document.querySelectorAll('.nav-tab');
        const forms = [document.getElementById('login-form'), document.getElementById('register-form')];
        
        tabs.forEach(t => t.classList.remove('active'));
        forms.forEach(f => f.classList.add('hidden'));

        if (type === 'login') {
            tabs[0].classList.add('active');
            forms[0].classList.remove('hidden');
        } else {
            tabs[1].classList.add('active');
            forms[1].classList.remove('hidden');
        }
    },

    handleLogin: async () => {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        const res = await app.apiRequest('/user/login', 'POST', { email, password });
        if (res) {
            currentToken = res.token;
            localStorage.setItem('token', currentToken);
            app.showToast('登录成功');
            app.showMainPage();
        }
    },

    handleRegister: async () => {
        const username = document.getElementById('reg-username').value;
        const email = document.getElementById('reg-email').value;
        const code = document.getElementById('reg-code').value;
        const password = document.getElementById('reg-password').value;

        const res = await app.apiRequest('/user/register', 'POST', {
            username, email, verify_code: code, password
        });

        if (res) {
            app.showToast('注册成功，请登录');
            app.switchAuth('login');
        }
    },

    sendVerifyCode: async () => {
        const email = document.getElementById('reg-email').value;
        if (!email) return app.showToast('请输入邮箱');
        
        const res = await app.apiRequest('/user/send_verify_code', 'POST', {
            verify_id: email,
            type: 2 
        });
        if (res) app.showToast('验证码已发送');
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        currentToken = null;
        location.reload();
    },

    // UI Navigation
    showMainPage: () => {
        document.getElementById('auth-page').classList.add('hidden');
        document.getElementById('main-page').classList.remove('hidden');
        app.loadMyGroups();
    },

    backToDashboard: () => {
        document.getElementById('group-detail-view').classList.add('hidden');
        document.getElementById('dashboard-view').classList.remove('hidden');
        currentGroup = null;
        app.loadMyGroups(); // Refresh
    },

    // Group Management
    loadMyGroups: async () => {
        const listEl = document.getElementById('group-list');
        listEl.innerHTML = '<div class="loading">加载中...</div>';

        const res = await app.apiRequest('/group/my_groups', 'GET');
        listEl.innerHTML = '';
        
        if (res && res.length > 0) {
            res.forEach(group => {
                const item = document.createElement('div');
                item.className = 'group-item';
                item.onclick = () => app.openGroup(group);
                item.innerHTML = `
                    <div class="group-info">
                        <h4>${group.name}</h4>
                        <p>成员: ${Object.keys(group.members || {}).length} 人</p>
                    </div>
                    <div style="font-size:20px; color:#ccc;">&rsaquo;</div>
                `;
                listEl.appendChild(item);
            });
        } else {
            listEl.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #999;">暂无小组，请创建或加入</div>';
        }
    },

    openGroup: async (group) => {
        currentGroup = group;
        document.getElementById('dashboard-view').classList.add('hidden');
        document.getElementById('group-detail-view').classList.remove('hidden');
        
        document.getElementById('detail-group-name').innerText = group.name;
        document.getElementById('detail-group-id').innerText = group.id || group.group_id;
        
        // Render Members
        const memberListEl = document.getElementById('member-list');
        memberListEl.innerHTML = '';
        if (group.members && group.members.length > 0) {
            group.members.forEach(m => {
                const mDiv = document.createElement('div');
                mDiv.style.padding = '8px 0';
                mDiv.style.borderBottom = '1px solid #eee';
                mDiv.style.display = 'flex';
                mDiv.style.justifyContent = 'space-between';
                mDiv.innerHTML = `
                    <span>${m.user_name || 'Unknown'}</span>
                    <span style="font-size: 12px; color: #888; background: #f0f0f0; padding: 2px 6px; border-radius: 10px;">
                        ${m.role === 'admin' ? '组长' : '成员'}
                    </span>
                `;
                memberListEl.appendChild(mDiv);
            });
        } else {
            memberListEl.innerHTML = '<div style="color:#999; font-size:13px;">暂无详细成员信息</div>';
        }

        app.loadFiles(group.id || group.group_id);
    },

    createGroup: async () => {
        const name = document.getElementById('create-group-name').value;
        const res = await app.apiRequest('/group/create', 'POST', { name });
        if (res) {
            app.showToast('小组创建成功');
            app.closeModal('modal-create-group');
            app.loadMyGroups();
        }
    },

    joinGroup: async () => {
        const gid = document.getElementById('join-group-id').value;
        const res = await app.apiRequest('/group/join', 'POST', { group_id: gid });
        if (res) {
            app.showToast('成功加入小组');
            app.closeModal('modal-join-group');
            app.loadMyGroups();
        }
    },

    inviteUser: async () => {
        if (!currentGroup) return;
        const gid = currentGroup.id || currentGroup.group_id;
        const email = document.getElementById('invite-email').value;
        const res = await app.apiRequest('/group/invite', 'POST', { group_id: gid, user_email: email });
        if (res === null) return; 
        app.showToast('邀请已发送');
        app.closeModal('modal-invite');
    },

    // File Management
    loadFiles: async (groupId) => {
        const listEl = document.getElementById('file-list');
        listEl.innerHTML = '<div class="loading">加载中...</div>';

        const res = await app.apiRequest('/group/list_files', 'POST', { group_id: groupId });
        listEl.innerHTML = '';

        if (res && res.length > 0) {
            res.forEach(file => {
                const item = document.createElement('div');
                item.className = 'file-item';
                
                const meta = file.meta_info || {};
                const tags = [];
                if(meta.subject) tags.push(meta.subject);
                if(meta.year) tags.push(meta.year);
                if(meta.content_type) tags.push(meta.content_type);
                if(meta.exam_type) tags.push(meta.exam_type);
                
                item.innerHTML = `
                    <div class="file-info">
                        <h4>${file.filename}</h4>
                        <p>${tags.join(' • ')}</p>
                        <p style="font-size:12px; color:#999;">${new Date(file.created_at.$date || file.created_at).toLocaleString()}</p>
                    </div>
                    <div class="action-group">
                        <button class="secondary" style="padding: 5px 10px; font-size: 13px;" onclick="app.downloadFile('${file.file_id}', 'origin')">原件</button>
                        <button style="padding: 5px 10px; font-size: 13px;" onclick="app.downloadFile('${file.file_id}', 'gen')">AI解析</button>
                    </div>
                `;
                listEl.appendChild(item);
            });
        } else {
            listEl.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">暂无文件</div>';
        }
    },

    uploadFile: async () => {
        if (!currentGroup) return;
        const fileInput = document.getElementById('file-input');
        if (!fileInput.files[0]) return app.showToast('请选择文件');

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('group_id', currentGroup.group_id || currentGroup.id);
        formData.append('subject', document.getElementById('upload-subject').value);
        formData.append('year', document.getElementById('upload-year').value);
        formData.append('paper_type', document.getElementById('upload-paper-type').value);
        formData.append('description', document.getElementById('upload-desc').value);
        
        if (document.getElementById('upload-paper-type').value === 'exam') {
            formData.append('exam_type', document.getElementById('upload-exam-type').value);
        }

        app.showToast('正在上传并处理，请稍候...');
        const btn = document.getElementById('upload-btn');
        btn.disabled = true;
        btn.innerText = '上传中...';

        const res = await app.apiRequest('/group/upload', 'POST', formData, true);
        
        btn.disabled = false;
        btn.innerText = '上传';

        if (res) {
            app.showToast('上传成功');
            app.closeModal('modal-upload');
            app.loadFiles(currentGroup.group_id || currentGroup.id);
        }
    },

    downloadFile: async (fileId, type) => {
        if (!currentGroup) return;
        
        // Use the ID from the current group object (which might be from my_groups list)
        // Note: my_groups returns group_id, list_files returns file objects.
        const gid = currentGroup.id || currentGroup.group_id;

        const res = await app.apiRequest('/group/download', 'POST', {
            group_id: gid,
            file_id: fileId,
            target_type: type
        });

        if (res && res.url) {
            // For generated HTML files, we want to preview them
            if (type === 'gen' && res.url.includes('.html')) {
                 // Open in new tab which browser renders
                 window.open(res.url, '_blank');
            } else {
                // For others, also open (browser will download or preview depending on type)
                window.open(res.url, '_blank');
            }
        } else {
             if (type === 'gen') {
                 app.showToast('无法找到对应的AI解析文件');
             } else {
                 app.showToast('无法获取文件链接');
             }
        }
    },

    // Modal Helpers
    showCreateGroupModal: () => document.getElementById('modal-create-group').classList.remove('hidden'),
    showJoinGroupModal: () => document.getElementById('modal-join-group').classList.remove('hidden'),
    showInviteModal: () => document.getElementById('modal-invite').classList.remove('hidden'),
    showUploadModal: () => document.getElementById('modal-upload').classList.remove('hidden'),
    
    closeModal: (id) => document.getElementById(id).classList.add('hidden'),

    toggleExamType: () => {
        const type = document.getElementById('upload-paper-type').value;
        const examGroup = document.getElementById('exam-type-group');
        if (type === 'exam') {
            examGroup.classList.remove('hidden');
        } else {
            examGroup.classList.add('hidden');
        }
    },

    handleFileSelect: (input) => {
        const display = document.getElementById('file-name-display');
        const btn = document.getElementById('upload-btn');
        if (input.files && input.files[0]) {
            display.innerText = `已选择: ${input.files[0].name}`;
            btn.disabled = false;
        } else {
            display.innerText = '';
            btn.disabled = true;
        }
    }
};

// Init
window.onload = function() {
    // Expose app to global scope for onclick handlers
    window.app = app;
    
    if (currentToken) {
        app.showMainPage();
    }
};
