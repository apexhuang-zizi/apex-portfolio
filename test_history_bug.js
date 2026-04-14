// ==================== 历史得分 BUG 诊断脚本 ====================
// 模拟 english.html 中的核心逻辑，诊断重复和云同步问题

console.log("=== 历史得分系统诊断 ===\n");

// ---- 工具函数 ----
function fbTsToIso(ts) {
    try {
        if (ts && typeof ts.toDate === 'function') return ts.toDate().toISOString();
        if (ts) return new Date(ts).toISOString();
    } catch(e) {}
    return "";
}

function recordKey(r) {
    return (r.user || r.username || "") + "_" + fbTsToIso(r.timestamp) + "_" + (r.score || r.score === 0 ? r.score : "");
}

// ---- 模拟 localStorage（用数组代替） ----
var simulatedLocalStorage = [];

function localGet(key) {
    if (key === "quest_history_all") {
        return JSON.stringify(simulatedLocalStorage);
    }
    return null;
}

function localSet(key, data) {
    if (key === "quest_history_all") {
        simulatedLocalStorage = JSON.parse(data);
        console.log("  [localStorage写入] " + simulatedLocalStorage.length + " 条");
    }
}

// ---- 模拟 Firebase 数据 ----
var firebaseData = [
    // 场景1：手机端存的一条记录（username=apex）
    {
        user: "apex", username: "apex",
        score: 88,
        timestamp: "2026-04-13T10:00:00.000Z",
        correct: 17, total: 20, maxCombo: 5,
        wrongWords: [], type: "word-quest",
        grade: "3", semester: "1"
    },
    // 场景2：另一台设备存的记录（username=yunfeng）
    {
        user: "yunfeng", username: "yunfeng",
        score: 75,
        timestamp: "2026-04-13T15:00:00.000Z",
        correct: 15, total: 20, maxCombo: 3,
        wrongWords: ["apple"], type: "word-quest",
        grade: "3", semester: "1"
    }
];

// ---- BUG 诊断 ----

console.log("【BUG 1】score 类型不一致导致去重失效");
console.log("-------------------------------------------");
// 当前代码：deleteHistoryRecord 中用 (r.score||0) 构建 key
var r1 = { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 88 };  // 数字
var r2 = { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: "88" }; // 字符串（来自Firebase）

var key1 = (r1.user||"")+"_"+r1.timestamp+"_"+(r1.score||0);  // "apex_..._88" (number)
var key2 = (r2.user||"")+"_"+r2.timestamp+"_"+(r2.score||0);  // "apex_..._88" (number 88, 强制转number)

console.log("数字 score=88 → key:", key1);
console.log("字符串 score='88' → key:", key2);
console.log("两者相等:", key1 === key2, "→ 正常情况OK");
console.log();

// 如果 score 是 undefined/null
var r3 = { user: "apex", timestamp: "2026-04-13T10:00:00.000Z" }; // 无score字段
var key3 = (r3.user||"")+"_"+r3.timestamp+"_"+(r3.score||0);
console.log("无score字段 → key:", key3, "→ score=0 的记录会互相冲突!");
console.log();

console.log("【BUG 2】deleteHistoryRecord key 和渲染时 key 不一致");
console.log("-------------------------------------------");
// 当前代码 renderHistoryQuest:  (r.score||0)
// 当前代码 deleteHistoryRecord: (r.score||0)
// 两者一致，没问题。但如果有遗留数据 score 为字符串，则：
var r4 = { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: "88" };
var key4 = (r4.user||"")+"_"+r4.timestamp+"_"+(r4.score||0); // → "apex_..._88"
var key5 = (r4.user||"")+"_"+r4.timestamp+"_"+(r4.score||""); // → "apex_..._88"
console.log("Firebase返回 score='88' (string):");
console.log("  (r.score||0) →", (r4.score||0), "type:", typeof (r4.score||0));
console.log("  (r.score||'') →", (r4.score||""), "type:", typeof (r4.score||""));
console.log("结果都是 88 → 没问题，但逻辑不一致有隐患");
console.log();

console.log("【BUG 3】loadHistoryQuest 被多次调用时的竞态");
console.log("-------------------------------------------");
// 场景：saveRecord → loadHistoryQuest → 立即渲染
//        ↓ Firebase异步返回
//        ↓ 同时：另一设备上传了新记录
//        ↓ 第三台设备也调用了 loadHistoryQuest
// 结果：localStorage 被反复覆盖，最早的 Firebase 数据可能丢失

console.log("假设时序：");
console.log("  T0: 用户A做练习 → saveRecord → 本地写入 → render(local=[A])");
console.log("  T1: Firebase收到A的记录");
console.log("  T2: 用户B做练习 → saveRecord → 本地写入 → render(local=[B,A])");
console.log("  T3: Firebase收到B的记录");
console.log("  T4: T0的Firebase回调返回 → 合并 [A,B] → 写回 → render([A,B])");
console.log("  T5: T2的Firebase回调返回 → 合并 [B,A] → 写回 → render([B,A])");
console.log("结果：顺序可能颠倒，但数据不丢 → 但如果localStorage中间被清空...");
console.log();

console.log("【真实BUG】renderHistoryQuest 重复渲染时 localKeys 不更新");
console.log("-------------------------------------------");
// 当 renderHistoryQuest 被调用两次（第一次本地，第二次合并后），
// 两次用的 records 参数不同，但删除按钮的 key 格式相同 → 实际没问题
// 
// 但如果 records 里有重复（来自不同来源的同一条记录）
var dupRecords = [
    { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 88, correct: 17, total: 20, maxCombo: 5, wrongWords: [], type: "word-quest", grade: "3", semester: "1" },
    { user: "apex", username: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 88, correct: 17, total: 20, maxCombo: 5, wrongWords: [], type: "word-quest", grade: "3", semester: "1" }
];
// 这两条记录去重 key 相同 → renderHistoryQuest 中会显示两次！
console.log("重复记录测试:");
var seen = {};
var unique = [];
for (var i = 0; i < dupRecords.length; i++) {
    var k = recordKey(dupRecords[i]);
    if (!seen[k]) {
        seen[k] = true;
        unique.push(dupRecords[i]);
    } else {
        console.log("  跳过重复:", k);
    }
}
console.log("去重后:", unique.length, "条");
console.log();

// ---- Firebase 查询问题 ----
console.log("【Firebase 查询】.where('type','==','word-quest') 无索引");
console.log("-------------------------------------------");
console.log("Firestore 对无索引字段的复合查询有限制:");
console.log("1. 单字段 .where('type') 不需要索引（可以）");
console.log("2. 但如果有 .orderBy() 组合，需要复合索引");
console.log("3. 免费层 Spark 方案：每天最多 50000 次写入/读取");
console.log("4. .limit(500) 每次查询最多取 500 条");
console.log("");
console.log("手机端数据没上云的可能原因:");
console.log("  - Firestore 安全规则限制写入?");
console.log("  - .where('type') 查询返回空（但有数据）?");
console.log("  - 网络问题导致 add() 静默失败?");
console.log();

// ---- 解决方案测试 ----
console.log("【解决方案】统一去重 key 格式");
console.log("-------------------------------------------");
function safeRecordKey(r) {
    var user = (r.user || r.username || "").trim();
    var ts = fbTsToIso(r.timestamp);
    // score 统一转为字符串
    var score = r.score !== undefined && r.score !== null ? String(r.score) : "";
    return user + "|" + ts + "|" + score;
}

// 测试
var tests = [
    { user: "apex", username: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 88 },
    { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 88 },
    { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: "88" },
    { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: undefined },
    { user: "apex", timestamp: "2026-04-13T10:00:00.000Z", score: 0 },
    { user: null, timestamp: "2026-04-13T10:00:00.000Z", score: 95 },
];
for (var i = 0; i < tests.length; i++) {
    console.log("  key:", safeRecordKey(tests[i]));
}

console.log("\n=== 诊断完成 ===");
console.log("\n结论:");
console.log("1. score类型问题：需要统一用 String(r.score||'')");
console.log("2. 删除key不一致：需要统一用 safeRecordKey()");
console.log("3. Firebase无索引：查询能工作，但建议添加索引");
console.log("4. 去重逻辑：在合并时去重 + 渲染前去重（双重保险）");
