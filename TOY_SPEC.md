# AI-Interactive-Taxonomy 玩具生成规范（TOY_SPEC v2.0）

本仓库采用 **“稳固架子 + 批量生成”** 架构。未来在任意 10 大领域下新增 2 分钟互动玩具，请严格遵循本规范：

## 1. 目录位置与命名

```text
domains/<domain_id>/<topic-slug>/
├── meta.json               # 必填：主题元数据（slug 须与 taxonomy.json 蓝图一致以便自动点亮！）
├── index.html              # 可选：单主题独立导览页
├── 01-<toy-slug>.html      # 玩具 1（按编号排序）
├── 02-<toy-slug>.html      # 玩具 2
└── 03-<toy-slug>.html      # 玩具 3
```

`<domain_id>` 必须为 `taxonomy.json` 中定义的 10 个领域之一：
`health` | `mind` | `design` | `society` | `business` | `finance` | `science` | `software` | `engineering` | `ai`

## 2. `meta.json` 标准格式

```json
{
  "domain": "health",
  "branch": "metabolism",
  "order": 1,
  "title": "血糖与胰岛素过山车",
  "icon": "🩸",
  "subtitle": "吃一碗白米饭 vs 一份蔬菜鸡胸肉，你的血糖曲线如何剧烈震荡？",
  "difficulty": "入门",
  "related": ["mind/motivation-habits", "engineering/control-feedback"],
  "toys": {
    "01-gi-rollercoaster.html": {
      "title": "血糖过山车",
      "icon": "🎢",
      "archetype": "simulation",
      "concept": "升糖指数 GI · 胰岛素过冲 · 饭困真相",
      "summary": "搭配不同餐盘点击进食，实时观察血糖飙升与胰岛素滞后导致的餐后犯困低谷。"
    }
  }
}
```

## 3. 防同质化：6 大互动原型池（Interaction Archetypes）

为避免批量生成后所有玩具都变成“左滑块 + 右文字框”，**同一主题的 3 个玩具必须至少覆盖 2–3 种不同原型**：

| 原型 ID (`archetype`) | 原型名称 | 典型代表 |
| :--- | :--- | :--- |
| `simulation` | **曲线 / 物理沙盘** | 血糖过山车、双摆混沌、幽灵堵车波、PID 无人机 |
| `race` | **双栏实时竞速** | 静态 vs 连续批处理、快思考 vs 慢思考、算法赛跑 |
| `builder` | **拖拽 / 装配台** | 手脚装配台、LoRA 贴纸店、切块手术台、电路拼接 |
| `scenario` | **红蓝攻防 / 情景抉择** | 提示词注入、囚徒困境、三选一诊疗室、无知之幕 |
| `spatial` | **空间星图 / 拓扑连线** | 语义星座图、谢林隔离棋盘、M×N 连线、A* 寻路 |
| `blind-lab` | **盲测 / A-B 对照实验** | 盲测竞技场 Elo、双盲临床试验、A/B 偷看样本陷阱 |

## 4. 2 分钟好玩具的“黄金 4 要素”

1. **打破 1 个具体误区**：开篇一句话直击大众最常见错觉。
2. **不超过 3 个核心控件**：滑块、开关、点击或拖拽，保证 3 秒内无需说明直接开玩。
3. **实时可视化反馈**：用 SVG/Canvas 曲线、状态动画或对比图呈现机理，拒绝纯文字问答。
4. **明确的一句话顿悟（Aha! Moment）**：用户动手后动态给出本质总结。

## 5. 统一使用共享母版（零构建、原生亮暗模式）

所有新玩具请基于 `shared/toy-template.html` 编写，并在 `<head>` 引入：

```html
<link rel="stylesheet" href="../../../shared/toy-base.css" />
<script src="../../../shared/toy-sdk.js"></script>
```

## 6. 生成后的标准上线命令

```bash
python3 scripts/validate_toys.py
python3 scripts/sync_catalog.py
git add . && git commit -m "feat(<domain>): add <topic-slug>" && git push
```
