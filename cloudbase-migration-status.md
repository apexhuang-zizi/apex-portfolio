# CloudBase 云端同步配置说明

**更新时间:** 2026-04-16 08:20 GMT+7

---

## ✅ 已完成的配置

### 1. task.html（任务清单模块）

| 项目 | 状态 | 值 |
|------|------|-----|
| CloudBase SDK | ✅ 已修复 | @cloudbase/js-sdk@1.7.1 |
| 环境ID | ✅ 已配置 | apex-english-4ga1ck7148c9e3 |
| 匿名登录 | ✅ 已启用 | anonymousAuthProvider |
| Collection | ✅ 已配置 | task_list |
| 本地回退 | ✅ 已保留 | makeLocalDB() |

### 2. english.html（英语星球模块）

| 项目 | 状态 | 值 |
|------|------|-----|
| CloudBase SDK | ✅ 已配置 | @cloudbase/js-sdk@1.7.1 |
| 环境ID | ✅ 已配置 | apex-english-4ga1ck7148c9e3 |
| 匿名登录 | ✅ 已启用 | anonymousAuthProvider |
| Collections | ✅ 已配置 | english_vocabulary, english_records |
| 本地回退 | ✅ 已保留 | makeLocalDB() |
| Firebase | ✅ 已移除 | 无残留代码 |

---

## 🔧 需要手动完成的步骤

### 步骤 1: 启用 CloudBase 匿名登录

1. 打开 [腾讯云控制台](https://cloud.tencent.com/login/subAccount/100045731974?type=subAccount&username=1536424073@qq.com)
2. 进入 **云开发 CloudBase** → 选择环境 **apex-english-4ga1ck7148c9e3**
3. 左侧菜单 → **用户管理** → **登录授权**
4. 找到 **匿名登录**，点击启用

### 步骤 2: 确认集合已配置

CloudBase 会自动创建集合（当数据第一次写入时）。确保以下集合已创建：

| 集合名 | 用途 | 数据示例 |
|--------|------|----------|
| task_list | 任务清单 | {"task":"买牛奶","date":"2026-04-16"} |
| english_records | 英语学习记录 | {"score":85,"unit":"U1","time":"3min"} |

### 步骤 3: 提交代码到 GitHub

```bash
cd "C:\Users\15364\Desktop\Apex's  workspace\个人主页"
git add task.html english.html
git commit -m "CloudBase: 修复SDK URL并配置云端同步"
git push origin main
```

### 步骤 4: 测试云端同步

1. 打开 https://apexhuang-zizi.github.io/apex-portfolio/task.html
2. 打开浏览器开发者工具 (F12) → Console
3. 确认看到 "CloudBase 匿名登录成功"
4. 添加一条测试任务
5. 在另一台设备打开同一页面，确认数据同步

---

## 📱 多设备同步说明

### 数据存储位置

| 模块 | CloudBase Collection | localStorage Key |
|------|---------------------|------------------|
| 任务清单 | task_list | task_list_data |
| 英语星球 | english_records | tcb_english_records |

### 同步逻辑

1. 页面加载时 → 从 CloudBase 读取数据
2. 数据变更时 → 自动写入 CloudBase
3. CloudBase 离线/失败时 → 自动回退到 localStorage

---

## 🔐 安全说明

当前使用**匿名登录**，这意味着：
- ✅ 任何人都可以读取/写入数据
- ⚠️ 数据安全性较低
- 建议后续：启用登录验证，用户需登录才能操作

如需增强安全性：
1. 关闭匿名登录
2. 实现用户名密码登录
3. 添加用户权限验证

---

## 📞 技术支持

如有 CloudBase 连接问题，请检查：
1. 匿名登录是否已启用
2. 环境ID是否正确
3. SDK URL 是否可访问

常用测试URL：
- CloudBase SDK: https://cdn.jsdelivr.net/npm/@cloudbase/js-sdk@1.7.1/cloudbase.full.js
- GitHub Pages: https://apexhuang-zizi.github.io/apex-portfolio/
