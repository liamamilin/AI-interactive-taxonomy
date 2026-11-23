# AI-Interactive-Taxonomy 玩具生成规范（TOY_SPEC）

本仓库采用 **“稳固架子 + 批量生成”** 架构。未来在任意 10 大领域下新增 2 分钟互动玩具，请严格遵循本规范：

## 1. 目录位置与命名

```text
domains/<domain_id>/<topic-slug>/
├── meta.json               # 必填：主题元数据与跨领域关联
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
  "related": ["mind/dopamine-loop", "engineering/pid-control"],
  "toys": {
    "01-gi-rollercoaster.html": {
      "title": "血糖过山车",
      "icon": "🎢",
      "concept": "升糖指数 GI · 胰岛素过冲 · 饭困真相",
      "summary": "搭配不同餐盘点击进食，实时观察血糖飙升与胰岛素滞后导致的餐后犯困低谷。"
    }
  }
}
```

## 3. 2 分钟好玩具的“黄金 4 要素”

1. **打破 1 个具体误区**：开篇一句话点出大众最常误解的点。
2. **不超过 3 个核心交互控件**：滑块、开关、点击或拖拽，保证用户 3 秒内无需看说明书就会玩。
3. **实时可视化反馈**：用 SVG 曲线、Canvas 动画、状态卡片或对比条把抽象机制具象化，拒绝纯静态文字问答。
4. **明确的一句话顿悟（Aha! Moment）**：用户动手操作后，底部动态给出直击本质的结论。

## 4. 引入共享底座（推荐用于所有新玩具）

新玩具建议在 `<head>` 中引入共享样式与 SDK（零构建、纯静态）：

```html
<link rel="stylesheet" href="../../../shared/toy-base.css" />
<script src="../../../shared/toy-sdk.js"></script>
```

## 5. 生成后的标准上线命令

```bash
python3 scripts/validate_toys.py
python3 scripts/sync_catalog.py
git add . && git commit -m "feat(<domain>): add <topic-slug>" && git push
```
