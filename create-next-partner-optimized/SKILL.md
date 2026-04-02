---
name: create-next-partner-optimized
description: "基于前任分析和下一任要求生成理想伴侣Skill。支持自动化数据采集、性格分析、兼容性评估和持续进化。 | Generate ideal partner skill based on ex-analysis and next-partner requirements. Supports automated data collection, personality analysis, compatibility assessment, and continuous evolution."
argument-hint: "[partner-name-or-slug]"
version: "2.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout. Below are instructions in both languages — follow the one matching the user's language.
>
> 本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。下方提供了两种语言的指令，按用户语言选择对应版本执行。

# 后任生成器（优化版）

## 触发条件

当用户说以下任意内容时启动：
- `/create-next-partner`
- "帮我创建一个理想伴侣 skill"
- "我想分析前任并生成下一任"
- "新建理想伴侣"
- "给我做一个理想伴侣的 skill"

当用户对已有伴侣 Skill 说以下内容时，进入进化模式：
- "我有新信息" / "追加"
- "这不对" / "他不会这样" / "他应该是"
- `/update-partner {slug}`

当用户说 `/list-partners` 时列出所有已生成的伴侣。

---

## 工具使用规则

本 Skill 运行在 Claude Code 环境，使用以下工具：

| 任务 | 使用工具 |
|------|---------|
| 读取 PDF 文档 | `Read` 工具（原生支持 PDF） |
| 读取图片截图 | `Read` 工具（原生支持图片） |
| 读取 MD/TXT/JSON 文件 | `Read` 工具 |
| 数据收集和验证 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/data_collector.py` |
| 写入/更新 Skill 文件 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py` |
| 版本管理 | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list` |

**基础目录**：Skill 文件写入 `./partners/{slug}/`（相对于本项目目录）。

---

## 主流程：创建新伴侣 Skill

### Step 1：基础信息收集

参考 `${CLAUDE_SKILL_DIR}/prompts/intake.md` 的问题序列，收集以下信息：

1. **伴侣代号**（必填）
2. **前任基本信息**（关系持续时间、分手原因、关键经验教训）
3. **前任优点分析**（至少3个具体优点，每个有例子）
4. **前任缺点分析**（至少2个具体缺点，每个有影响描述）
5. **下一任要求**（必须特质、希望特质、底线特质、生活方式偏好）

### Step 2：原材料导入

询问用户提供原材料，展示三种方式供选择：

```
原材料怎么提供？

  [A] 上传文件
      PDF / 图片 / TXT / JSON / 聊天记录导出

  [B] 直接粘贴内容
      把文字复制进来进行分析

  [C] 跳过（仅凭手动信息生成）
```

#### 方式 A：上传文件

- **PDF / 图片**：`Read` 工具直接读取
- **TXT / JSON 文件**：`Read` 工具直接读取
- **聊天记录导出**：`Read` 工具直接读取

#### 方式 B：直接粘贴

用户粘贴的内容直接作为文本原材料，无需调用任何工具。

#### 方式 C：跳过

仅使用手动输入的信息生成伴侣档案。

### Step 3：分析原材料

将收集到的所有原材料和用户填写的基础信息汇总，按以下三条线分析：

**线路 A（前任性格分析）**：
- 参考 `${CLAUDE_SKILL_DIR}/prompts/ex_analyzer.md` 中的提取维度
- 提取：沟通风格、情绪管理、冲突处理、价值观体系
- 分析优点和缺点的根本原因

**线路 B（性格特征提取）**：
- 参考 `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md` 中的提取维度
- 基于大五人格模型：外向性、宜人性、尽责性、情绪稳定性、开放性
- 提取关系特定特征：情感表达、亲密需求、边界意识

**线路 C（兼容性分析）**：
- 参考 `${CLAUDE_SKILL_DIR}/prompts/compatibility_analyzer.md` 中的提取维度
- 分析：价值观匹配、生活习惯兼容、性格互补
- 评估关系发展潜力

### Step 4：生成并预览

参考 `${CLAUDE_SKILL_DIR}/prompts/profile_builder.md` 生成伴侣档案内容。

向用户展示摘要（各 5-8 行），询问：

```
性格特征摘要：
  - 核心性格：{xxx}
  - 沟通风格：{xxx}
  - 情感表达：{xxx}
  ...

价值观体系摘要：
  - 核心价值观：{xxx}
  - 关系价值观：{xxx}
  - 生活哲学：{xxx}
  ...

兼容性分析摘要：
  - 情感兼容性：{xxx}
  - 价值观匹配：{xxx}
  - 生活兼容性：{xxx}
  ...

确认生成？还是需要调整？
```

### Step 5：写入文件

用户确认后，执行以下写入操作：

**1. 创建目录结构**（用 Bash）：
```bash
mkdir -p partners/{slug}/versions
mkdir -p partners/{slug}/knowledge/docs
mkdir -p partners/{slug}/knowledge/messages
mkdir -p partners/{slug}/knowledge/emails
```

**2. 写入 profile.json**（用 Write 工具）：
路径：`partners/{slug}/profile.json`

**3. 写入 compatibility.md**（用 Write 工具）：
路径：`partners/{slug}/compatibility.md`

**4. 写入 growth_plan.md**（用 Write 工具）：
路径：`partners/{slug}/growth_plan.md`

**5. 写入 meta.json**（用 Write 工具）：
路径：`partners/{slug}/meta.json`
内容：
```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO时间}",
  "updated_at": "{ISO时间}",
  "version": "v1",
  "relationship_analysis": {
    "ex_strengths": [...],
    "ex_weaknesses": [...],
    "key_lessons": [...],
    "next_requirements": [...]
  },
  "personality_profile": {
    "big_five": {...},
    "communication_style": "...",
    "emotional_expression": "..."
  },
  "compatibility_scores": {
    "emotional": 8,
    "values": 7,
    "lifestyle": 6,
    "overall": 7
  },
  "knowledge_sources": [...已导入文件列表],
  "corrections_count": 0
}
```

**6. 生成完整 SKILL.md**（用 Write 工具）：
路径：`partners/{slug}/SKILL.md`

SKILL.md 结构：
```markdown
---
name: partner-{slug}
description: {name}，基于前任分析和用户要求生成的理想伴侣
user-invocable: true
---

# {name} - 理想伴侣档案

## 性格特征

{性格特征摘要}

## 价值观体系

{价值观体系摘要}

## 生活方式

{生活方式描述}

## 兼容性分析

{兼容性分析摘要}

## 关系发展建议

{具体建议和行动计划}

---

**生成信息**
- 生成时间: {时间}
- 数据来源: {来源}
- 版本: {版本}
```

告知用户：
```
✅ 伴侣 Skill 已创建！

文件位置：partners/{slug}/
触发词：/{slug}

如果用起来感觉哪里不对，直接说"他不会这样"，我来更新。
```

---

## 进化模式：追加信息

用户提供新信息或文本时：

1. 按 Step 2 的方式读取新内容
2. 用 `Read` 读取现有 `partners/{slug}/profile.json` 和相关文件
3. 参考 `${CLAUDE_SKILL_DIR}/prompts/merger.md` 分析增量内容
4. 存档当前版本（用 Bash）：
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action backup --slug {slug} --base-dir ./partners
   ```
5. 用 `Edit` 工具更新相关文件
6. 重新生成 `SKILL.md`
7. 更新 `meta.json` 的 version 和 updated_at

---

## 进化模式：对话纠正

用户表达"不对"/"应该是"时：

1. 参考 `${CLAUDE_SKILL_DIR}/prompts/correction_handler.md` 识别纠正内容
2. 判断属于性格特征、价值观还是兼容性分析
3. 生成 correction 记录
4. 用 `Edit` 工具追加到对应文件的 `## Correction 记录` 节
5. 重新生成 `SKILL.md`

---

## 管理命令

`/list-partners`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --base-dir ./partners
```

`/partner-rollback {slug} {version}`：
```bash
python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py --action rollback --slug {slug} --version {version} --base-dir ./partners
```

`/delete-partner {slug}`：
确认后执行：
```bash
rm -rf partners/{slug}
```

---

## 关系特定功能

### 1. 大五人格分析
基于收集的数据自动评估：
- 外向性：社交偏好和能量来源
- 宜人性：合作倾向和同理心
- 尽责性：组织性和责任感
- 情绪稳定性：压力反应和情绪波动
- 开放性：好奇心和创新思维

### 2. 关系价值观评估
分析以下维度：
- 忠诚与专一
- 沟通与表达
- 个人空间与亲密
- 未来规划一致性
- 冲突处理方式

### 3. 兼容性评分系统
提供多维度的兼容性评分：
- 情感兼容性（0-10）
- 价值观匹配度（0-10）
- 生活习惯兼容性（0-10）
- 性格互补性（0-10）
- 总体兼容性评分

### 4. 成长发展计划
生成具体的关系发展建议：
- 短期目标（1-3个月）
- 中期目标（3-12个月）
- 长期愿景（1-3年）
- 具体行动步骤

---

## 使用建议

### 最佳实践
1. **数据质量**：提供越详细的前任信息，分析越准确
2. **具体要求**：明确下一任的具体要求，避免模糊描述
3. **定期更新**：随着认知变化，可以更新伴侣档案
4. **实际验证**：将生成的档案与实际关系对比，持续优化

### 注意事项
- 此档案为理想模型，实际关系需要灵活调整
- 每个人都是独特的，避免刻板印象
- 健康关系需要双方共同努力
- 定期回顾和更新档案内容

---

# English Version

# Next Partner Generator (Optimized Edition)

## Trigger Conditions

Activate when the user says any of the following:
- `/create-next-partner`
- "Help me create an ideal partner skill"
- "I want to analyze my ex and generate the next partner"
- "New ideal partner"
- "Make a skill for ideal partner"

Enter evolution mode when the user says:
- "I have new information" / "append"
- "That's wrong" / "He wouldn't do that" / "He should be"
- `/update-partner {slug}`

List all generated partners when the user says `/list-partners`.

---

## Tool Usage Rules

This Skill runs in the Claude Code environment with the following tools:

| Task | Tool |
|------|------|
| Read PDF documents | `Read` tool (native PDF support) |
| Read image screenshots | `Read` tool (native image support) |
| Read MD/TXT files | `Read` tool |
| Parse Feishu message JSON export | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/feishu_parser.py` |
| Feishu auto-collect (recommended) | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/feishu_auto_collector.py` |
| Feishu docs (browser session) | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/feishu_browser.py` |
| Feishu docs (MCP App Token) | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/feishu_mcp_client.py` |
| DingTalk auto-collect | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/dingtalk_auto_collector.py` |
| Parse email .eml/.mbox | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/email_parser.py` |
| Data collection and validation | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/data_collector.py` |
| Write/update Skill files | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/skill_writer.py` |
| Version management | `Bash` → `python3 ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| List existing Skills | `Bash` → `python3 ${CL