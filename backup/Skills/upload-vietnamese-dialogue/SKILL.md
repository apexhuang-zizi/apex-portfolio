# 越南语对话上传器

## 功能描述
将当前对话中最近生成的越南语情景对话自动上传到个人网站的越南语对话模块，保存后自动翻译、支持TTS播放。

## 触发方式
用户说以下内容时触发：
- "帮我上传最近的情景对话"
- "上传越南语对话"
- "保存对话到网站"
- "上传对话"

## 关键信息
- Firebase 项目: `vietnames-data`
- Collection: `dialogues`
- Firebase REST API 端点: `https://firestore.googleapis.com/v1/projects/vietnames-data/databases/(default)/documents/dialogues`
- Firebase Auth 匿名登录: `https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyCMPFTNEBWXA_EnkF7Yk__F1gdHYfPg8kM`
- 网站: `https://apexhuang-zizi.github.io/apex-portfolio/vietnamese.html`

## ⚠️ 人称代词规范（最高优先级）

**严格禁止使用 "anh/chị" 斜杠模板写法！**

越南语的人称代词（anh, chị, em, ông, bà, bạn, mình 等）应根据**场景和人物关系**自然选择使用，这是越南语的核心社交语言特征，必须真实体现。

❌ **错误做法**——斜杠模板，不自然：
```
A: Xin chào, tôi có thể giúp gì cho anh/chị?
B: Chào anh/chị, tôi muốn hỏi...
```

✅ **正确做法**——根据场景选一个，自然使用：
```
A: Xin chào, tôi có thể giúp gì cho anh?        （对方是男性）
B: Chào chị, em muốn hỏi...                      （对方是女性，自称 em）
```

✅ **更多示例**：
- 男对男："Anh cần mua gì ạ?" → 对方用 anh
- 女对女："Chị muốn xem mẫu nào?" → 对方用 chị  
- 年轻人对长辈："Dạ, em nghe ạ" → 自称 em
- 同龄朋友："Bạn ơi, mình muốn hỏi..." → bạn/mình

**核心原则**：
1. 每个角色有明确的性别/年龄/身份设定
2. 根据角色关系自然选择代词（anh, chị, em, bạn, mình 等）
3. ❌ 绝不出现 "anh/chị" 斜杠写法
4. 说话人标识用 `A:` / `B:` / `C:` 角色标签

## ⚠️ 编码规范（最高优先级）

**越南语音调符号（如 ầ, ờ, ệ, ưởng）是越南语的核心组成部分，上传时必须完整保留，不得丢失。**

所有文件读写和 HTTP 请求必须显式声明 UTF-8 编码：
- Python 脚本文件顶部必须写 `# -*- coding: utf-8 -*-`（或 `encoding='utf-8'`）
- 脚本中的中英文字符串统一写成 Python unicode 字符串（直接写 UTF-8 字符，无需转义）
- JSON 序列化时必须指定 `ensure_ascii=False`
- `urllib.request.Request` 需加 `encoding='utf-8'` header

❌ **错误做法**（会导致音调符号丢失）：
```python
data = json.dumps(doc).encode()  # 不指定 ensure_ascii，音调符号会变乱码
```

✅ **正确做法**：
```python
data = json.dumps(doc, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    'Content-Type': 'application/json; charset=utf-8'
})
```

## 对话数据结构
上传到 Firebase 的每条对话格式：
```json
{
  "fields": {
    "date": {"stringValue": "2026-04-14"},
    "topic": {"stringValue": "mua sắm tại cửa hàng"},
    "content": {"stringValue": "A: Chào bạn, bạn cần mua gì ạ?\n\nA: 你好，请问你要买什么？\n\n..."},
    "created": {"timestampValue": "2026-04-14T..."}
  }
}
```

## 执行步骤

### Step 1: 从对话历史提取最近的越南语对话

使用 `lcm_grep` 搜索当前对话中包含越南语场景标记的内容：

```
搜索模式: 【场景】
```

找到最近的完整对话（包含 `【场景】` 开头，越南语角色名+对话内容，至少8句）。

如果当前对话没有找到，使用 `lcm_expand` 扩展搜索范围。

### Step 2: 解析对话并转换为网站格式

对话生成 Skill 的输出格式：
```
【场景】中文场景描述

越南文标题（第二行，如 "Mua sắm online"）

A: Chào bạn, bạn cần mua gì ạ?
A: 你好，请问你要买什么？

B: Tôi muốn mua một cái áo.
B: 我想买一件衣服。
```

**转换规则**：
1. 跳过 `【场景】...` 行
2. 第二行（越南文标题）→ 这是 `topic`
3. 后续行每两行一组：越南语行 + 中文翻译行
4. **说话人统一用 A / B 替代具体人名**，格式：`A: 越南语句子\n\nA: 中文翻译`（双换行分隔，同一说话人的句子之间空一行）
5. **每条完整对话行之间用 `\n\n` 分隔**（两个换行符）
6. `date` 用当前日期（越南时区 UTC+7）
7. `created` 用 ISO 8601 时间戳

**转换示例**：
```
输入：
  A: Chào bạn, bạn cần mua gì ạ?
  A: 你好，请问你要买什么？

输出：
  A: Chào bạn, bạn cần mua gì ạ?

A: 你好，请问你要买什么？
```

（每条回复之间用双换行 `\n\n` 分隔，同一说话人的越南文和中文翻译之间也用 `\n\n` 分隔）

### Step 3: 通过 Python 脚本上传（主要方案）

⚠️ **必须使用 Python 脚本**，不得用 PowerShell（PowerShell 中文/越南语编码会丢失音调）。

```python
# -*- coding: utf-8 -*-
import urllib.request, json, time

API_KEY = 'AIzaSyCMPFTNEBWXA_EnkF7Yk__F1gdHYfPg8kM'
PROJECT = 'vietnames-data'
DATE = '2026-04-16'  # 替换为实际日期
TOPIC = 'Mua thuốc tại nhà thuốc'  # 越南文标题，含音调符号
CONTENT = '...'  # 完整对话内容，含音调符号

# Step 3a: Firebase 匿名登录，拿 idToken
sign_up_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}'
sign_up_req = urllib.request.Request(
    sign_up_url,
    data=json.dumps({}).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
sign_up_resp = json.loads(urllib.request.urlopen(sign_up_req, timeout=10).read())
id_token = sign_up_resp['idToken']

# Step 3b: 写入 Firestore（注意 ensure_ascii=False，保持音调符号）
doc = {
    'fields': {
        'date': {'stringValue': DATE},
        'topic': {'stringValue': TOPIC},
        'content': {'stringValue': CONTENT},
        'created': {'timestampValue': time.strftime('%Y-%m-%dT%H:%M:%SZ')}
    }
}

fs_url = f'https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/dialogues?key={API_KEY}'
fs_req = urllib.request.Request(
    fs_url,
    data=json.dumps(doc, ensure_ascii=False).encode('utf-8'),
    headers={
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {id_token}'
    }
)
fs_resp = json.loads(urllib.request.urlopen(fs_req, timeout=10).read())
doc_id = fs_resp['name'].split('/')[-1]
print(f'Upload OK: {doc_id}')
```

### Step 4: 验证上传成功

检查返回的 doc_id 是否为非空字符串（格式如 `6HVTOQbqwS5v2Dvq2c9E`）。如果返回错误码，检查 Firebase 安全规则或网络连接。

打开网站 https://apexhuang-zizi.github.io/apex-portfolio/vietnamese.html 确认新对话出现在列表中。

### Step 5: 清理测试数据（可选）

如需删除测试数据，用以下脚本：
```python
# -*- coding: utf-8 -*-
import urllib.request, json

API_KEY = 'AIzaSyCMPFTNEBWXA_EnkF7Yk__F1gdHYfPg8kM'
PROJECT = 'vietnames-data'

# 匿名登录
sign_up_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}'
sign_up_req = urllib.request.Request(
    sign_up_url,
    data=json.dumps({}).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
id_token = json.loads(urllib.request.urlopen(sign_up_req, timeout=10).read())['idToken']

# 查询含 "test" 的对话
query_url = f'https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents:runQuery?key={API_KEY}'
query_body = {
    'structuredQuery': {
        'where': {'fieldFilter': {'field': {'fieldPath': 'topic'}, 'op': 'CONTAINS', 'value': {'stringValue': 'test'}}}
    }
}
query_req = urllib.request.Request(
    query_url,
    data=json.dumps(query_body, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'Bearer {id_token}'}
)
results = json.loads(urllib.request.urlopen(query_req, timeout=10).read())

for r in results:
    doc = r.get('document', {})
    doc_id = doc.get('name', '').split('/')[-1]
    if doc_id:
        del_url = f'https://firestore.googleapis.com/v1/{doc["name"]}?key={API_KEY}'
        del_req = urllib.request.Request(del_url, data=b'', headers={'Authorization': f'Bearer {id_token}'})
        del_req.get_method = lambda: 'DELETE'
        urllib.request.urlopen(del_req, timeout=10)
        print(f'Deleted: {doc_id}')
```

## 错误处理
- **Firebase 403/权限错误**: 检查匿名登录是否在 Firebase Console 中开启（Authentication → 登录方式 → 匿名）
- **上传后音调符号丢失**: 确认脚本使用 `ensure_ascii=False` + `charset=utf-8` header
- **对话内容不完整**: 确认对话至少有8句（4轮来回），不完整则提示用户重新生成
- **重复检测**: 上传前检查 Firebase 中是否已有相同 topic 的对话

## 注意事项
- ⚠️ **不要修改 vietnamese.html 的代码**
- ⚠️ **不要影响其他模块**（英语星球、问题追踪表、index.html）
- ⚠️ **不要推送任何代码变更**到 GitHub，等待用户确认
- 上传前确认对话内容完整且格式正确
- 测试完成后删除测试数据
- **越南语音调符号是越南语的核心，丢失后越南人无法正确理解语义，必须完整保留**
