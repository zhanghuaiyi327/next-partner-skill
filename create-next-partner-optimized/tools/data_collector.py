#!/usr/bin/env python3
"""
增强版数据收集器 - 支持自动化数据采集和手动输入混合模式
结合create-next-partner的关系分析核心和colleague-skill-main的自动化工具
"""

import json
import sys
import os
import argparse
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
from pathlib import Path

class EnhancedDataCollector:
    """增强版数据收集器类"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.validation_errors = []
        self.collected_data = {
            "ex_partner": {},
            "next_partner_requirements": {},
            "automated_data": {},
            "metadata": {}
        }
        self.skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def collect_hybrid_data(self) -> Dict[str, Any]:
        """混合模式数据收集：自动化采集 + 手动输入"""
        print("=" * 60)
        print("后任生成器 - 增强版数据收集")
        print("=" * 60)
        
        # 收集基本信息
        basic_info = self.collect_basic_info()
        
        # 选择数据采集方式
        collection_method = self.select_collection_method()
        
        # 执行数据采集
        automated_data = {}
        if collection_method != "skip":
            automated_data = self.execute_automated_collection(collection_method, basic_info.get("ex_name", ""))
        
        # 收集手动信息
        manual_data = self.collect_manual_info()
        
        # 合并数据
        self.collected_data.update({
            "basic_info": basic_info,
            "automated_data": automated_data,
            "manual_data": manual_data,
            "metadata": {
                "collected_at": datetime.now().isoformat(),
                "collection_method": collection_method,
                "version": "2.0.0"
            }
        })
        
        # 验证数据
        self.validate_collected_data()
        
        if self.validation_errors:
            print("\n⚠️  验证警告：")
            for error in self.validation_errors:
                print(f"  - {error}")
        
        return self.collected_data
    
    def collect_basic_info(self) -> Dict[str, Any]:
        """收集基本信息"""
        print("\n1. 基本信息收集")
        print("-" * 40)
        
        basic_info = {}
        
        # 伴侣代号
        partner_code = input("\n理想伴侣代号（用于文件命名）：").strip()
        while not partner_code:
            print("⚠️  代号不能为空")
            partner_code = input("理想伴侣代号：").strip()
        basic_info["partner_code"] = partner_code
        
        # 前任姓名（用于自动化采集）
        ex_name = input("\n前任姓名（用于自动化采集，可选）：").strip()
        if ex_name:
            basic_info["ex_name"] = ex_name
        
        # 关系基本信息
        print("\n关系基本信息：")
        basic_info["relationship_duration"] = input("关系持续时间（如：2年、6个月）：").strip()
        basic_info["breakup_reason"] = input("分手主要原因：").strip()
        
        # 关键经验教训
        print("\n从这段关系中学到的重要教训（输入'完成'结束）：")
        lessons = []
        count = 1
        while True:
            lesson = input(f"经验教训 {count}：").strip()
            if lesson.lower() == '完成':
                if len(lessons) < 1:
                    print("⚠️  至少需要1个经验教训")
                    continue
                break
            if lesson:
                lessons.append(lesson)
                count += 1
        basic_info["key_lessons"] = lessons
        
        return basic_info
    
    def select_collection_method(self) -> str:
        """选择数据采集方式（简化版）"""
        print("\n2. 数据采集方式选择")
        print("-" * 40)
        
        print("""
请选择数据采集方式：

  [A] 上传文件
      PDF / 图片 / TXT / JSON / 聊天记录导出

  [B] 直接粘贴内容
      把文字复制进来进行分析

  [C] 跳过（仅凭手动信息生成）
""")
        
        while True:
            choice = input("\n选择 [A/B/C]：").strip().upper()
            if choice in ["A", "B", "C"]:
                method_map = {
                    "A": "file_upload",
                    "B": "paste_text",
                    "C": "skip"
                }
                return method_map[choice]
            print("⚠️  请选择有效的选项")
    
    def execute_automated_collection(self, method: str, target_name: str) -> Dict[str, Any]:
        """执行数据采集（简化版）"""
        print(f"\n执行 {method} 数据采集...")
        
        automated_data = {
            "method": method,
            "collected_at": datetime.now().isoformat(),
            "files": [],
            "content": {}
        }
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix="partner_collect_")
        
        try:
            if method == "file_upload":
                result = self.handle_file_upload(temp_dir)
            elif method == "paste_text":
                result = self.handle_paste_text(temp_dir)
            else:
                result = {"success": False, "error": f"未知方法: {method}"}
            
            if result.get("success", False):
                automated_data.update(result)
                print(f"✅ {method} 数据采集成功")
            else:
                print(f"❌ {method} 数据采集失败: {result.get('error', '未知错误')}")
                automated_data["error"] = result.get("error", "未知错误")
                
        except Exception as e:
            print(f"❌ 数据采集异常: {e}")
            automated_data["error"] = str(e)
        
        return automated_data
    
    def handle_file_upload(self, temp_dir: str) -> Dict[str, Any]:
        """处理文件上传"""
        print("\n请将文件复制到以下目录：")
        print(f"  {temp_dir}")
        print("\n完成后按回车键继续...")
        input()
        
        # 检查文件
        collected_files = []
        content = {}
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.txt', '.json', '.md', '.pdf')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content[file] = f.read()
                        collected_files.append(file)
                    except:
                        pass
        
        if collected_files:
            return {
                "success": True,
                "files": collected_files,
                "content": content,
                "output_dir": temp_dir
            }
        else:
            return {
                "success": False,
                "error": "未找到有效文件"
            }
    
    def handle_paste_text(self, temp_dir: str) -> Dict[str, Any]:
        """处理粘贴文本"""
        print("\n请粘贴文本内容（输入'END'单独一行结束）：")
        print("-" * 40)
        
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        
        content_text = "\n".join(lines)
        
        if not content_text.strip():
            return {"success": False, "error": "文本内容为空"}
        
        output_file = os.path.join(temp_dir, "pasted_content.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content_text)
        
        return {
            "success": True,
            "files": ["pasted_content.txt"],
            "content": {"pasted_content.txt": content_text},
            "output_dir": temp_dir
        }
    
    def collect_manual_info(self) -> Dict[str, Any]:
        """收集手动信息（前任优点、缺点、下一任要求）"""
        print("\n3. 手动信息收集")
        print("-" * 40)
        
        manual_data = {
            "ex_strengths": self.collect_ex_strengths(),
            "ex_weaknesses": self.collect_ex_weaknesses(),
            "next_requirements": self.collect_next_requirements()
        }
        
        return manual_data
    
    def collect_ex_strengths(self) -> List[Dict[str, Any]]:
        """收集前任优点"""
        print("\n前任的优点和长处：")
        print("（请输入至少3个优点，每个优点用具体例子说明）")
        print("输入'完成'结束输入")
        
        strengths = []
        count = 1
        while True:
            print(f"\n优点 {count}:")
            trait = input("  特质：").strip()
            if trait.lower() == '完成':
                if len(strengths) < 3:
                    print(f"⚠️  至少需要3个优点，当前只有{len(strengths)}个")
                    continue
                break
            
            example = input("  具体例子：").strip()
            impact = input("  对关系的影响：").strip()
            
            if trait and example:
                strengths.append({
                    "trait": trait,
                    "example": example,
                    "impact": impact,
                    "category": self.categorize_trait(trait),
                    "priority": "inherit"  # 需要继承的特质
                })
                count += 1
            else:
                print("⚠️  特质和例子都不能为空")
        
        return strengths
    
    def collect_ex_weaknesses(self) -> List[Dict[str, Any]]:
        """收集前任缺点"""
        print("\n前任的缺点和问题：")
        print("（请输入至少2个缺点，描述具体影响）")
        print("输入'完成'结束输入")
        
        weaknesses = []
        count = 1
        while True:
            print(f"\n缺点 {count}:")
            trait = input("  问题：").strip()
            if trait.lower() == '完成':
                if len(weaknesses) < 2:
                    print(f"⚠️  至少需要2个缺点，当前只有{len(weaknesses)}个")
                    continue
                break
            
            impact = input("  具体影响：").strip()
            avoidable = input("  是否必须避免？（是/否）：").strip().lower() == '是'
            
            if trait and impact:
                weaknesses.append({
                    "trait": trait,
                    "impact": impact,
                    "avoidable": avoidable,
                    "severity": self.assess_severity(trait, impact),
                    "category": self.categorize_trait(trait)
                })
                count += 1
            else:
                print("⚠️  问题和影响都不能为空")
        
        return weaknesses
    
    def collect_next_requirements(self) -> Dict[str, Any]:
        """收集下一任要求"""
        print("\n对下一任的要求：")
        
        requirements = {
            "must_have": self.collect_must_have_traits(),
            "nice_to_have": self.collect_nice_to_have_traits(),
            "deal_breakers": self.collect_deal_breakers(),
            "lifestyle": self.collect_lifestyle_preferences()
        }
        
        return requirements
    
    def collect_must_have_traits(self) -> List[Dict[str, Any]]:
        """收集必须拥有的特质"""
        print("\n必须拥有的特质（非妥协项）：")
        print("（请输入至少3个必须特质）")
        print("输入'完成'结束输入")
        
        must_have = []
        count = 1
        while True:
            print(f"\n必须特质 {count}:")
            trait = input("  特质：").strip()
            if trait.lower() == '完成':
                if len(must_have) < 3:
                    print(f"⚠️  至少需要3个必须特质，当前只有{len(must_have)}个")
                    continue
                break
            
            reason = input("  为什么这个特质很重要：").strip()
            priority = input("  优先级（高/中/低）：").strip().lower()
            
            if trait and reason:
                must_have.append({
                    "trait": trait,
                    "reason": reason,
                    "priority": priority if priority in ['高', '中', '低'] else '高',
                    "non_negotiable": True
                })
                count += 1
            else:
                print("⚠️  特质和原因都不能为空")
        
        return must_have
    
    def collect_nice_to_have_traits(self) -> List[Dict[str, Any]]:
        """收集希望拥有的特质"""
        print("\n希望拥有的特质（加分项，可选）：")
        print("输入'完成'结束输入")
        
        nice_to_have = []
        while True:
            trait = input("\n希望特质：").strip()
            if trait.lower() == '完成':
                break
            
            if trait:
                nice_to_have.append({
                    "trait": trait,
                    "priority": "低",
                    "non_negotiable": False
                })
        
        return nice_to_have
    
    def collect_deal_breakers(self) -> List[Dict[str, Any]]:
        """收集绝对不能接受的特质"""
        print("\n绝对不能接受的特质（底线）：")
        print("输入'完成'结束输入")
        
        deal_breakers = []
        while True:
            trait = input("\n底线特质：").strip()
            if trait.lower() == '完成':
                break
            
            reason = input("  为什么不能接受：").strip()
            
            if trait and reason:
                deal_breakers.append({
                    "trait": trait,
                    "reason": reason,
                    "severity": "critical"
                })
        
        return deal_breakers
    
    def collect_lifestyle_preferences(self) -> Dict[str, Any]:
        """收集生活方式偏好"""
        print("\n生活方式偏好：")
        
        return {
            "work_life_balance": input("工作生活平衡偏好：").strip(),
            "social_style": input("社交风格偏好：").strip(),
            "future_plans": input("未来3-5年生活规划：").strip(),
            "hobbies_interests": input("兴趣爱好偏好：").strip()
        }
    
    def categorize_trait(self, trait: str) -> str:
        """对特质进行分类"""
        trait_lower = trait.lower()
        
        # 性格特质
        personality_keywords = ['外向', '内向', '乐观', '悲观', '开朗', '沉稳', '幽默', '情绪']
        if any(keyword in trait_lower for keyword in personality_keywords):
            return "personality"
        
        # 关系技能
        relationship_keywords = ['沟通', '倾听', '支持', '体贴', '关心', '尊重', '信任', '忠诚']
        if any(keyword in trait_lower for keyword in relationship_keywords):
            return "relationship_skill"
        
        # 价值观
        value_keywords = ['诚实', '责任', '家庭', '成长', '成就', '独立', '自由', '安全']
        if any(keyword in trait_lower for keyword in value_keywords):
            return "value"
        
        # 生活习惯
        habit_keywords = ['整洁', '守时', '健康', '运动', '阅读', '旅行', '作息', '饮食']
        if any(keyword in trait_lower for keyword in habit_keywords):
            return "habit"
        
        return "other"
    
    def assess_severity(self, trait: str, impact: str) -> str:
        """评估缺点的严重程度"""
        severity_keywords = {
            "critical": ['暴力', '虐待', '欺骗', '背叛', '成瘾', '控制', '嫉妒'],
            "high": ['冷漠', '忽视', '不忠', '自私', '固执', '挑剔'],
            "medium": ['拖延', '健忘', '情绪化', '犹豫', '被动', '依赖'],
            "low": ['邋遢', '迟到', '话多', '节省', '谨慎', '内向']
        }
        
        combined = (trait + impact).lower()
        
        for severity, keywords in severity_keywords.items():
            if any(keyword in combined for keyword in keywords):
                return severity
        
        return "medium"
    
    def validate_collected_data(self):
        """验证收集的数据"""
        # 检查基本信息
        if "basic_info" not in self.collected_data:
            self.validation_errors.append("缺少基本信息")
        
        # 检查手动信息
        if "manual_data" in self.collected_data:
            manual_data = self.collected_data["manual_data"]
            
            # 检查前任优点
            if len(manual_data.get("ex_strengths", [])) < 3:
                self.validation_errors.append("前任优点至少需要3个")
            
            # 检查前任缺点
            if len(manual_data.get("ex_weaknesses", [])) < 2:
                self.validation_errors.append("前任缺点至少需要2个")
            
            # 检查必须特质
            if len(manual_data.get("next_requirements", {}).get("must_have", [])) < 3:
                self.validation_errors.append("必须特质至少需要3个")
    
    def save_to_file(self, filename: Optional[str] = None) -> str:
        """保存收集的数据到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"collected_data_{timestamp}.json"
        
        # 确保目录存在
        os.makedirs("collected_data", exist_ok=True)
        filepath = os.path.join("collected_data", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 数据已保存到：{filepath}")
        return filepath
    
    def load_from_file(self, filepath: str) -> Dict[str, Any]:
        """从文件加载数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.collected_data = data
            print(f"✅ 数据已从 {filepath} 加载")
            return data
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ 加载文件失败：{e}")
            return {}
    
    def analyze_automated_data(self) -> Dict[str, Any]:
        """分析自动化采集的数据"""
        if "automated_data" not in self.collected_data:
            return {}
        
        automated_data = self.collected_data["automated_data"]
        if not automated_data.get("success", False):
            return {}
        
        analysis = {
            "communication_patterns": [],
            "personality_traits": [],
            "values_interests": [],
            "relationship_patterns": []
        }
        
        # 分析消息内容（如果存在）
        content = automated_data.get("content", {})
        for filename, text in content.items():
            if "message" in filename.lower() or "chat" in filename.lower():
                # 分析沟通模式
                analysis["communication_patterns"].extend(
                    self.analyze_communication_patterns(text)
                )
            
            if "doc" in filename.lower() or "content" in filename.lower():
                # 分析价值观和兴趣
                analysis["values_interests"].extend(
                    self.analyze_values_interests(text)
                )
        
        return analysis
    
    def analyze_communication_patterns(self, text: str) -> List[str]:
        """分析沟通模式"""
        patterns = []
        
        # 简单的模式识别
        lines = text.split('\n')
        
        # 检查回复速度
        reply_counts = {}
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) > 1:
                    speaker = parts[0].strip()
                    reply_counts[speaker] = reply_counts.get(speaker, 0) + 1
        
        # 检查情感词汇
        emotional_words = ['开心', '难过', '生气', '担心', '爱', '喜欢', '讨厌']
        emotional_count = sum(1 for word in emotional_words if word in text)
        
        if emotional_count > 10:
            patterns.append("情感表达丰富")
        elif emotional_count < 3:
            patterns.append("情感表达克制")
        
        # 检查问题解决方式
        if "怎么办" in text or "怎么解决" in text:
            patterns.append("倾向于寻求解决方案")
        
        if "我觉得" in text or "我认为" in text:
            patterns.append("表达个人观点")
        
        return patterns
    
    def analyze_values_interests(self, text: str) -> List[str]:
        """分析价值观和兴趣"""
        interests = []
        
        # 兴趣关键词
        interest_keywords = {
            "阅读": ['书', '阅读', '小说', '文学'],
            "旅行": ['旅行', '旅游', '景点', '度假'],
            "运动": ['运动', '健身', '跑步', '游泳', '瑜伽'],
            "音乐": ['音乐', '歌曲', '演唱会', '乐器'],
            "电影": ['电影', '电视剧', '影院', '导演'],
            "美食": ['美食', '餐厅', '烹饪', '食谱'],
            "学习": ['学习', '课程', '培训', '教育'],
            "工作": ['工作', '项目', '职业', '事业']
        }
        
        for interest, keywords in interest_keywords.items():
            if any(keyword in text for keyword in keywords):
                interests.append(interest)
        
        # 价值观关键词
        value_keywords = {
            "家庭": ['家庭', '家人', '父母', '孩子'],
            "友情": ['朋友', '友谊', '友情', '伙伴'],
            "成长": ['成长', '进步', '提升', '发展'],
            "责任": ['责任', '担当', '义务', '承诺'],
            "自由": ['自由', '独立', '自主', '空间'],
            "成就": ['成就', '成功', '目标', '梦想']
        }
        
        for value, keywords in value_keywords.items():
            if any(keyword in text for keyword in keywords):
                interests.append(value)
        
        return list(set(interests))  # 去重

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="增强版数据收集器 - 支持自动化采集和手动输入")
    parser.add_argument("--input", help="输入文件路径（JSON格式）")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--analyze", action="store_true", help="分析自动化数据")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    collector = EnhancedDataCollector(debug=args.debug)
    
    if args.input:
        # 从文件加载
        data = collector.load_from_file(args.input)
        if not data:
            sys.exit(1)
    else:
        # 交互式收集
        data = collector.collect_hybrid_data()
    
    # 分析自动化数据
    if args.analyze and "automated_data" in data:
        analysis = collector.analyze_automated_data()
        if analysis:
            print("\n" + "=" * 60)
            print("自动化数据分析结果")
            print("=" * 60)
            for category, items in analysis.items():
                if items:
                    print(f"\n{category}:")
                    for item in items:
                        print(f"  - {item}")
    
    # 保存数据
    if args.output or not args.input:
        output_file = args.output or None
        saved_path = collector.save_to_file(output_file)
        
        print("\n" + "=" * 60)
        print("数据收集完成")
        print("=" * 60)
        print(f"收集的数据：")
        print(f"- 基本信息：{data.get('basic_info', {}).get('partner_code', '未知')}")
        
        manual_data = data.get("manual_data", {})
        print(f"- 前任优点：{len(manual_data.get('ex_strengths', []))}个")
        print(f"- 前任缺点：{len(manual_data.get('ex_weaknesses', []))}个")
        
        next_req = manual_data.get("next_requirements", {})
        print(f"- 必须特质：{len(next_req.get('must_have', []))}个")
        print(f"- 底线特质：{len(next_req.get('deal_breakers', []))}个")
        
        automated_data = data.get("automated_data", {})
        if automated_data.get("success", False):
            print(f"- 自动化采集文件：{len(automated_data.get('files', []))}个")
        
        print(f"\n保存位置：{saved_path}")

if __name__ == "__main__":
    main()
