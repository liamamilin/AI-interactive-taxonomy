# AI-Interactive-Taxonomy · 围绕“人”的交互式知识图谱

一个以 **“人”为圆心、覆盖 10 大核心领域** 的 2 分钟可交互科普知识图谱（Explorable Explanations Taxonomy）。  
不用公式、不依赖后端 API，通过亲手拨动滑块、切换开关和观察可视化反馈，把复杂学科的底层原理变成一眼悟懂的互动玩具。

## 10 大核心领域（3 个同心圈层）

- **第一圈：内在与表达（人自己）**：🧬 身体与健康 · 🧠 心智与认知 · 🎨 设计与审美
- **第二圈：协作与价值（人与人）**：🏛️ 社会与法律 · 📈 商业与博弈 · 💰 金融与财富
- **第三圈：科学与构建（人与世界）**：🌌 数学与自然 · 💻 软件与开发 · ⚙️ 工程与系统 · 🤖 AI 与智能

## 本地使用

直接双击根目录的 `index.html` 即可在浏览器中打开完整双视图应用（支持**全景知识图谱** / **分类探索**切换、搜索、亮暗色模式、应用内沉浸试玩与进度保存）。

## 持续扩展与自动同步

新增任何领域的主题玩具只需遵循 `TOY_SPEC.md` 放入 `domains/<domain>/<topic>/`，然后运行：

```bash
python3 scripts/validate_toys.py
python3 scripts/sync_catalog.py
```

推送到 GitHub `main` 分支后，GitHub Actions 会自动执行校验、同步目录并部署到 GitHub Pages。
