# -*- coding: utf-8 -*-
import subprocess, os
os.chdir(r'C:\Users\15364\Desktop\Apex''s  workspace\个人主页')
print('CWD:', os.getcwd())
for cmd in [['git','add','task.html'],['git','commit','-m','feat(task): 优化手机端按钮可见性 + 多用户数据隔离'],['git','push']]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(cmd, r.stdout, r.stderr)