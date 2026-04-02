# 增强版后任生成器 (create-next-partner-optimized)

基于前任分析和下一任要求生成理想伴侣Skill的增强版系统。支持自动化数据采集、智能性格分析、兼容性评估和持续进化。

## 🎯 核心功能

### 1. **混合数据采集模式**
- **自动化采集**: 支持飞书、钉钉自动采集消息和文档
- **文件上传**: 支持PDF、图片、JSON、邮件等多种格式
- **链接解析**: 支持飞书文档链接直接解析
- **手动输入**: 交互式数据收集界面

### 2. **智能分析引擎**
- **前任分析**: 自动识别优点、缺点和关系模式
- **要求分析**: 分析下一任的具体要求和优先级
- **自动化数据分析**: 从实际数据中提取性格特征和沟通模式
- **兼容性分析**: 多维度评估关系兼容性

### 3. **增强版Skill生成**
- **完整档案**: 包含性格特征、价值观、生活方式等
- **兼容性报告**: 详细的兼容性分析和建议
- **成长计划**: 具体的关系发展行动计划
- **关系洞察**: 从前任关系中提取的经验教训

### 4. **持续进化能力**
- **版本管理**: 完整的版本控制和备份
- **增量更新**: 支持基于新信息的Skill更新
- **纠正机制**: 支持用户反馈和纠正

## 📁 项目结构

```
create-next-partner-optimized/
├── SKILL.md                    # 主Skill文件
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── test_enhanced_workflow.py   # 系统测试
├── prompts/                    # 提示词模板
├── tools/                      # 工具脚本
│   ├── data_collector.py       # 增强版数据收集器
│   ├── skill_writer.py         # 增强版Skill生成器
│   ├── version_manager.py      # 版本管理工具
│   ├── feishu_auto_collector.py # 飞书自动采集
│   ├── dingtalk_auto_collector.py # 钉钉自动采集
│   ├── feishu_parser.py        # 飞书解析器
│   ├── feishu_browser.py       # 飞书浏览器方案
│   ├── feishu_mcp_client.py    # 飞书MCP方案
│   └── email_parser.py         # 邮件解析器
├── docs/                       # 文档
├── assets/                     # 资源文件
└── test_data/                  # 测试数据
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据收集

```bash
# 交互式数据收集
python tools/data_collector.py

# 或使用现有数据文件
python tools/data_collector.py --input your_data.json --output collected_data.json
```

### 3. 生成Skill

```bash
# 生成增强版Skill
python tools/skill_writer.py --input collected_data.json --skill-name ideal_partner

# 带调试信息
python tools/skill_writer.py --input collected_data.json --skill-name ideal_partner --debug
```

### 4. 查看结果

生成的Skill文件位于 `partners/{skill_name}/` 目录，包含：
- `SKILL.md` - 主档案文件
- `profile.json` - 核心档案数据
- `compatibility.md` - 兼容性分析
- `growth_plan.md` - 成长计划
- `relationship_insights.md` - 关系洞察
- `metadata.json` - 元数据

## 🔧 高级功能

### 自动化数据采集

#### 飞书自动采集
```bash
# 首次配置
python tools/feishu_auto_collector.py --setup

# 采集数据
python tools/feishu_auto_collector.py --name "张三" --output-dir ./knowledge/zhangsan
```

#### 钉钉自动采集
```bash
# 首次配置
python tools/dingtalk_auto_collector.py --setup

# 采集数据
python tools/dingtalk_auto_collector.py --name "李四" --output-dir ./knowledge/lisi
```

### Skill管理

#### 列出所有Skill
```bash
python tools/skill_writer.py --list
```

#### 获取Skill信息
```bash
python tools/skill_writer.py --info skill_name
```

#### 更新Skill
```bash
python tools/skill_writer.py --update skill_name --update-data new_data.json
```

## 📊 数据分析维度

### 性格特征分析
- **大五人格模型**: 外向性、宜人性、尽责性、情绪稳定性、开放性
- **沟通风格**: 情感表达、沟通频率、问题解决倾向
- **情感表达**: 开放直接、内敛含蓄、平衡适中

### 兼容性分析
- **情感兼容性**: 情感表达匹配、情绪稳定性
- **价值观兼容性**: 核心价值观对齐
- **生活方式兼容性**: 作息、兴趣、社交风格
- **沟通兼容性**: 沟通频率和方式匹配
- **成长兼容性**: 个人发展和关系成长目标

### 关系洞察
- **可重复的成功模式**: 从前任关系中提取的积极模式
- **要避免的问题模式**: 需要避免的负面模式
- **关系健康信号**: 绿色信号和红色信号识别

## 🧪 测试系统

运行完整测试：

```bash
python test_enhanced_workflow.py
```

测试内容包括：
1. 数据收集器功能测试
2. Skill生成器功能测试
3. 完整集成工作流程测试

## 📈 输出示例

### 生成的Skill档案结构

```
理想伴侣 - 增强版档案
├── 性格特征
│   ├── 核心特质（继承的优点 + 具体要求）
│   ├── 沟通风格（基于实际数据分析）
│   ├── 情感表达方式
│   └── 大五人格档案
├── 关系偏好
│   ├── 沟通需求
│   ├── 亲密程度
│   ├── 独立需求
│   └── 冲突解决方式
├── 生活方式偏好
│   ├── 工作生活平衡
│   ├── 社交风格
│   ├── 兴趣爱好
│   └── 未来规划
├── 兼容性分析
│   ├── 各维度评分（0-10）
│   ├── 优势分析
│   └── 改进建议
├── 成长发展计划
│   ├── 短期目标（1-3个月）
│   ├── 中期目标（3-12个月）
│   ├── 长期愿景（1-3年）
│   └── 具体行动步骤
└── 关系洞察
    ├── 关键经验教训
    ├── 可重复的成功模式
    ├── 要避免的问题模式
    └── 关系健康信号
```

## 🔄 持续进化

### 版本控制
- 每次更新自动创建版本备份
- 支持版本回滚
- 完整的更新历史记录

### 增量学习
- 基于新信息自动更新档案
- 用户反馈整合
- 持续优化分析模型

## 📝 使用建议

### 最佳实践
1. **数据质量**: 提供详细的前任信息和具体的要求
2. **自动化采集**: 尽可能使用自动化工具获取真实数据
3. **定期更新**: 随着认知变化更新伴侣档案
4. **实际验证**: 将生成的档案与实际关系体验对比

### 注意事项
- 此档案为理想模型，实际关系需要灵活调整
- 每个人都是独特的，避免刻板印象
- 健康关系需要双方共同努力
- 定期回顾和更新档案内容

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

### 开发流程
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

### 代码规范
- 遵循PEP 8编码规范
- 添加适当的注释和文档
- 编写单元测试
- 确保向后兼容性

## 📄 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 🙏 致谢

感谢所有贡献者和用户的支持，特别感谢：
- 原版create-next-partner项目的启发
- colleague-skill-main项目的自动化工具
- 所有提供反馈和建议的用户

---

**开始使用**: 运行 `python tools/data_collector.py` 开始创建你的理想伴侣档案！