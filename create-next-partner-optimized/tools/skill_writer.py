#!/usr/bin/env python3
"""
增强版Skill文件生成器 - 支持自动化数据分析和智能生成
"""

import json
import os
import sys
import argparse
import hashlib
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class EnhancedSkillWriter:
    """增强版Skill文件生成器类"""
    
    def __init__(self, output_dir: str = "partners", debug: bool = False):
        self.output_dir = output_dir
        self.debug = debug
        self.generated_skills = []
        self.analysis_cache = {}
        
    def create_enhanced_partner_skill(self, collected_data: Dict[str, Any], 
                                    skill_slug: Optional[str] = None,
                                    version: str = "2.0.0") -> str:
        """创建增强版伴侣Skill文件结构"""
        
        print("=" * 60)
        print("增强版伴侣Skill生成器")
        print("=" * 60)
        
        # 分析数据
        analysis_result = self.analyze_collected_data(collected_data)
        
        # 生成Skill名称
        if not skill_slug:
            basic_info = collected_data.get("basic_info", {})
            partner_code = basic_info.get("partner_code", "ideal_partner")
            timestamp = datetime.now().strftime("%Y%m%d")
            skill_slug = f"{partner_code}_{timestamp}"
        
        # 创建Skill目录结构
        skill_dir = self.create_skill_directory_structure(skill_slug)
        
        # 生成核心文件
        print(f"\n📁 生成Skill文件: {skill_slug}")
        
        # 1. 生成profile.json（核心档案）
        profile_data = self.generate_profile_data(collected_data, analysis_result)
        self._create_profile_json(skill_dir, profile_data)
        
        # 2. 生成compatibility.md（兼容性分析）
        compatibility_data = self.generate_compatibility_analysis(collected_data, analysis_result)
        self._create_compatibility_md(skill_dir, compatibility_data)
        
        # 3. 生成growth_plan.md（成长计划）
        growth_plan = self.generate_growth_plan(collected_data, analysis_result)
        self._create_growth_plan_md(skill_dir, growth_plan)
        
        # 4. 生成relationship_insights.md（关系洞察）
        insights = self.generate_relationship_insights(collected_data, analysis_result)
        self._create_relationship_insights_md(skill_dir, insights)
        
        # 5. 生成metadata.json（元数据）
        metadata = self.generate_metadata(collected_data, skill_slug, version)
        self._create_metadata_json(skill_dir, metadata)
        
        # 6. 生成完整的SKILL.md
        skill_content = self.generate_skill_md_content(collected_data, analysis_result, skill_slug, version)
        self._create_skill_md(skill_dir, skill_content, skill_slug)
        
        # 7. 保存知识文件（如果存在自动化数据）
        self.save_knowledge_files(skill_dir, collected_data)
        
        # 记录生成的skill
        self.generated_skills.append({
            "slug": skill_slug,
            "path": skill_dir,
            "created_at": datetime.now().isoformat(),
            "version": version,
            "metadata": metadata
        })
        
        print(f"\n✅ 增强版Skill创建完成: {skill_slug}")
        print(f"📁 文件位置: {skill_dir}")
        
        return skill_dir
    
    def analyze_collected_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析收集的数据"""
        print("\n🔍 分析收集的数据...")
        
        analysis = {
            "ex_analysis": self.analyze_ex_partner(collected_data),
            "requirements_analysis": self.analyze_next_requirements(collected_data),
            "automated_data_analysis": self.analyze_automated_data(collected_data),
            "compatibility_patterns": self.identify_compatibility_patterns(collected_data),
            "growth_opportunities": self.identify_growth_opportunities(collected_data)
        }
        
        if self.debug:
            print("\n分析结果摘要:")
            for category, result in analysis.items():
                if result:
                    print(f"  - {category}: {len(result)}项分析")
        
        return analysis
    
    def analyze_ex_partner(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析前任信息"""
        manual_data = collected_data.get("manual_data", {})
        ex_strengths = manual_data.get("ex_strengths", [])
        ex_weaknesses = manual_data.get("ex_weaknesses", [])
        
        analysis = {
            "strength_categories": {},
            "weakness_patterns": [],
            "inheritable_traits": [],
            "avoidable_traits": [],
            "relationship_patterns": []
        }
        
        # 分析优点
        for strength in ex_strengths:
            category = strength.get("category", "other")
            analysis["strength_categories"][category] = analysis["strength_categories"].get(category, 0) + 1
            
            # 判断是否可继承
            if strength.get("priority") == "inherit":
                analysis["inheritable_traits"].append({
                    "trait": strength.get("trait"),
                    "category": category,
                    "impact": strength.get("impact", "")
                })
        
        # 分析缺点
        for weakness in ex_weaknesses:
            severity = weakness.get("severity", "medium")
            avoidable = weakness.get("avoidable", True)
            
            if avoidable:
                analysis["avoidable_traits"].append({
                    "trait": weakness.get("trait"),
                    "severity": severity,
                    "impact": weakness.get("impact", "")
                })
            
            # 识别模式
            if severity in ["critical", "high"]:
                analysis["weakness_patterns"].append({
                    "trait": weakness.get("trait"),
                    "severity": severity,
                    "category": weakness.get("category", "other")
                })
        
        # 分析关系模式
        basic_info = collected_data.get("basic_info", {})
        breakup_reason = basic_info.get("breakup_reason", "")
        key_lessons = basic_info.get("key_lessons", [])
        
        if breakup_reason:
            analysis["relationship_patterns"].append(f"分手原因: {breakup_reason}")
        
        for lesson in key_lessons:
            analysis["relationship_patterns"].append(f"经验教训: {lesson}")
        
        return analysis
    
    def analyze_next_requirements(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析下一任要求"""
        manual_data = collected_data.get("manual_data", {})
        requirements = manual_data.get("next_requirements", {})
        
        analysis = {
            "must_have_categories": {},
            "deal_breaker_analysis": [],
            "priority_distribution": {"高": 0, "中": 0, "低": 0},
            "lifestyle_compatibility": {},
            "value_alignment": []
        }
        
        # 分析必须特质
        must_have = requirements.get("must_have", [])
        for trait in must_have:
            priority = trait.get("priority", "高")
            analysis["priority_distribution"][priority] = analysis["priority_distribution"].get(priority, 0) + 1
            
            # 分类
            category = self.categorize_trait(trait.get("trait", ""))
            analysis["must_have_categories"][category] = analysis["must_have_categories"].get(category, 0) + 1
        
        # 分析底线特质
        deal_breakers = requirements.get("deal_breakers", [])
        for breaker in deal_breakers:
            analysis["deal_breaker_analysis"].append({
                "trait": breaker.get("trait"),
                "reason": breaker.get("reason", ""),
                "severity": "critical"
            })
        
        # 分析生活方式
        lifestyle = requirements.get("lifestyle", {})
        for key, value in lifestyle.items():
            if value:
                analysis["lifestyle_compatibility"][key] = value
        
        # 分析价值观对齐
        value_keywords = ['诚实', '责任', '家庭', '成长', '成就', '独立', '自由', '安全']
        for trait in must_have + deal_breakers:
            trait_text = trait.get("trait", "").lower()
            for keyword in value_keywords:
                if keyword in trait_text:
                    analysis["value_alignment"].append(keyword)
        
        return analysis
    
    def analyze_automated_data(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析自动化采集的数据"""
        automated_data = collected_data.get("automated_data", {})
        
        if not automated_data.get("success", False):
            return {}
        
        analysis = {
            "communication_style": [],
            "personality_indicators": [],
            "interest_patterns": [],
            "value_indicators": [],
            "relationship_dynamics": []
        }
        
        content = automated_data.get("content", {})
        
        for filename, text in content.items():
            # 分析沟通风格
            if "message" in filename.lower() or "chat" in filename.lower():
                analysis["communication_style"].extend(
                    self.analyze_communication_style(text)
                )
            
            # 分析文档内容
            if "doc" in filename.lower() or "content" in filename.lower():
                analysis["personality_indicators"].extend(
                    self.extract_personality_indicators(text)
                )
                analysis["interest_patterns"].extend(
                    self.extract_interest_patterns(text)
                )
                analysis["value_indicators"].extend(
                    self.extract_value_indicators(text)
                )
        
        # 去重
        for key in analysis:
            analysis[key] = list(set(analysis[key]))
        
        return analysis
    
    def analyze_communication_style(self, text: str) -> List[str]:
        """分析沟通风格"""
        styles = []
        
        # 情感表达
        emotional_words = ['开心', '难过', '生气', '担心', '爱', '喜欢', '讨厌', '感动']
        emotional_count = sum(1 for word in emotional_words if word in text)
        
        if emotional_count > 15:
            styles.append("情感表达丰富")
        elif emotional_count > 5:
            styles.append("情感表达适中")
        else:
            styles.append("情感表达克制")
        
        # 沟通频率
        lines = text.split('\n')
        message_count = len([line for line in lines if ":" in line])
        
        if message_count > 50:
            styles.append("沟通频繁")
        elif message_count > 20:
            styles.append("沟通适中")
        else:
            styles.append("沟通简洁")
        
        # 问题解决倾向
        if "怎么办" in text or "怎么解决" in text or "建议" in text:
            styles.append("倾向于寻求解决方案")
        
        if "我觉得" in text or "我认为" in text or "我的看法" in text:
            styles.append("表达个人观点")
        
        if "你怎么样" in text or "你好吗" in text or "关心" in text:
            styles.append("关注他人感受")
        
        return styles
    
    def extract_personality_indicators(self, text: str) -> List[str]:
        """提取性格指标"""
        indicators = []
        
        # 大五人格相关词汇
        personality_keywords = {
            "外向性": ['社交', '聚会', '朋友', '活跃', '开朗', '健谈'],
            "宜人性": ['帮助', '支持', '理解', '体贴', '善良', '合作'],
            "尽责性": ['计划', '组织', '责任', '完成', '准时', '认真'],
            "情绪稳定性": ['平静', '稳定', '冷静', '耐心', '放松', '平和'],
            "开放性": ['好奇', '创新', '探索', '学习', '尝试', '创意']
        }
        
        for trait, keywords in personality_keywords.items():
            if any(keyword in text for keyword in keywords):
                indicators.append(trait)
        
        return indicators
    
    def extract_interest_patterns(self, text: str) -> List[str]:
        """提取兴趣模式"""
        interests = []
        
        interest_keywords = {
            "阅读": ['书', '阅读', '小说', '文学', '杂志', '报纸'],
            "旅行": ['旅行', '旅游', '景点', '度假', '风景', '探索'],
            "运动": ['运动', '健身', '跑步', '游泳', '瑜伽', '锻炼'],
            "音乐": ['音乐', '歌曲', '演唱会', '乐器', '唱歌', '乐队'],
            "电影": ['电影', '电视剧', '影院', '导演', '演员', '剧情'],
            "美食": ['美食', '餐厅', '烹饪', '食谱', '美食', '料理'],
            "学习": ['学习', '课程', '培训', '教育', '知识', '技能'],
            "艺术": ['艺术', '绘画', '摄影', '设计', '创作', '展览'],
            "科技": ['科技', '技术', '编程', '数码', '创新', '科学']
        }
        
        for interest, keywords in interest_keywords.items():
            if any(keyword in text for keyword in keywords):
                interests.append(interest)
        
        return list(set(interests))
    
    def extract_value_indicators(self, text: str) -> List[str]:
        """提取价值观指标"""
        values = []
        
        value_keywords = {
            "家庭": ['家庭', '家人', '父母', '孩子', '亲情', '家庭'],
            "友情": ['朋友', '友谊', '友情', '伙伴', '同伴', '知己'],
            "成长": ['成长', '进步', '提升', '发展', '学习', '进步'],
            "责任": ['责任', '担当', '义务', '承诺', '负责', '信用'],
            "自由": ['自由', '独立', '自主', '空间', '选择', '权利'],
            "成就": ['成就', '成功', '目标', '梦想', '事业', '成绩'],
            "健康": ['健康', '身体', '锻炼', '饮食', '养生', '保健'],
            "平衡": ['平衡', '和谐', '稳定', '适度', '协调', '均衡']
        }
        
        for value, keywords in value_keywords.items():
            if any(keyword in text for keyword in keywords):
                values.append(value)
        
        return list(set(values))
    
    def identify_compatibility_patterns(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """识别兼容性模式"""
        ex_analysis = self.analyze_ex_partner(collected_data)
        req_analysis = self.analyze_next_requirements(collected_data)
        
        patterns = {
            "strength_alignment": [],
            "weakness_avoidance": [],
            "value_compatibility": [],
            "lifestyle_match": [],
            "growth_alignment": []
        }
        
        # 优点对齐
        inheritable_traits = ex_analysis.get("inheritable_traits", [])
        must_have_categories = req_analysis.get("must_have_categories", {})
        
        for trait in inheritable_traits:
            category = trait.get("category")
            if category in must_have_categories:
                patterns["strength_alignment"].append({
                    "trait": trait.get("trait"),
                    "category": category,
                    "alignment": "high"
                })
        
        # 缺点避免
        avoidable_traits = ex_analysis.get("avoidable_traits", [])
        deal_breakers = req_analysis.get("deal_breaker_analysis", [])
        
        for trait in avoidable_traits:
            trait_name = trait.get("trait", "").lower()
            for breaker in deal_breakers:
                breaker_name = breaker.get("trait", "").lower()
                if trait_name in breaker_name or breaker_name in trait_name:
                    patterns["weakness_avoidance"].append({
                        "avoidable_trait": trait.get("trait"),
                        "deal_breaker": breaker.get("trait"),
                        "severity": trait.get("severity", "medium")
                    })
        
        return patterns
    
    def identify_growth_opportunities(self, collected_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """识别成长机会"""
        opportunities = []
        
        basic_info = collected_data.get("basic_info", {})
        key_lessons = basic_info.get("key_lessons", [])
        
        manual_data = collected_data.get("manual_data", {})
        ex_weaknesses = manual_data.get("ex_weaknesses", [])
        requirements = manual_data.get("next_requirements", {})
        must_have = requirements.get("must_have", [])
        
        # 从经验教训中提取成长机会
        for lesson in key_lessons:
            opportunities.append({
                "type": "relationship_learning",
                "description": lesson,
                "priority": "high",
                "action": "在下一段关系中应用这个教训"
            })
        
        # 从缺点中提取改进机会
        for weakness in ex_weaknesses:
            if weakness.get("avoidable", True):
                opportunities.append({
                    "type": "weakness_avoidance",
                    "description": f"避免前任的缺点: {weakness.get('trait')}",
                    "priority": weakness.get("severity", "medium"),
                    "action": f"寻找没有{weakness.get('trait')}特质的伴侣"
                })
        
        # 从必须特质中提取发展机会
        for trait in must_have:
            opportunities.append({
                "type": "trait_development",
                "description": f"发展特质: {trait.get('trait')}",
                "priority": trait.get("priority", "高"),
                "action": f"在关系中培养{trait.get('trait')}特质"
            })
        
        return opportunities
    
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
    
    def create_skill_directory_structure(self, skill_slug: str) -> str:
        """创建Skill目录结构"""
        skill_dir = os.path.join(self.output_dir, skill_slug)
        
        # 创建主目录
        os.makedirs(skill_dir, exist_ok=True)
        
        # 创建子目录
        subdirs = [
            "versions",
            "knowledge/messages",
            "knowledge/docs",
            "knowledge/emails",
            "knowledge/images",
            "analysis"
        ]
        
        for subdir in subdirs:
            os.makedirs(os.path.join(skill_dir, subdir), exist_ok=True)
        
        return skill_dir
    
    def generate_profile_data(self, collected_data: Dict[str, Any], 
                            analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成核心档案数据"""
        basic_info = collected_data.get("basic_info", {})
        manual_data = collected_data.get("manual_data", {})
        
        profile = {
            "basic_info": {
                "partner_code": basic_info.get("partner_code", "ideal_partner"),
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0"
            },
            "personality_profile": self.generate_personality_profile(collected_data, analysis_result),
            "relationship_preferences": self.generate_relationship_preferences(collected_data, analysis_result),
            "lifestyle_preferences": self.generate_lifestyle_preferences(collected_data),
            "compatibility_summary": self.generate_compatibility_summary(analysis_result),
            "growth_focus": self.generate_growth_focus(analysis_result)
        }
        
        return profile
    
    def generate_personality_profile(self, collected_data: Dict[str, Any], 
                                   analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成性格档案"""
        ex_analysis = analysis_result.get("ex_analysis", {})
        req_analysis = analysis_result.get("requirements_analysis", {})
        auto_analysis = analysis_result.get("automated_data_analysis", {})
        
        # 继承的优点
        inheritable_traits = ex_analysis.get("inheritable_traits", [])
        
        # 必须的特质
        must_have_categories = req_analysis.get("must_have_categories", {})
        
        # 自动化分析的性格指标
        personality_indicators = auto_analysis.get("personality_indicators", [])
        
        profile = {
            "core_traits": [],
            "communication_style": auto_analysis.get("communication_style", ["待分析"]),
            "emotional_expression": self.assess_emotional_expression(collected_data),
            "big_five_profile": self.generate_big_five_profile(collected_data, analysis_result),
            "strengths_to_inherit": [trait.get("trait") for trait in inheritable_traits],
            "traits_to_develop": list(must_have_categories.keys())
        }
        
        # 添加核心特质
        for trait in inheritable_traits:
            profile["core_traits"].append({
                "trait": trait.get("trait"),
                "source": "inherited_from_ex",
                "priority": "high"
            })
        
        for category in must_have_categories:
            profile["core_traits"].append({
                "trait": f"具有{category}特质",
                "source": "user_requirement",
                "priority": "high"
            })
        
        return profile
    
    def assess_emotional_expression(self, collected_data: Dict[str, Any]) -> str:
        """评估情感表达方式"""
        auto_analysis = collected_data.get("automated_data_analysis", {})
        communication_style = auto_analysis.get("communication_style", [])
        
        if "情感表达丰富" in communication_style:
            return "开放直接"
        elif "情感表达克制" in communication_style:
            return "内敛含蓄"
        else:
            return "平衡适中"
    
    def generate_big_five_profile(self, collected_data: Dict[str, Any], 
                                analysis_result: Dict[str, Any]) -> Dict[str, int]:
        """生成大五人格档案"""
        # 基于分析结果评估大五人格维度
        profile = {
            "extraversion": 6,  # 外向性 (1-10)
            "agreeableness": 7,  # 宜人性
            "conscientiousness": 7,  # 尽责性
            "emotional_stability": 8,  # 情绪稳定性
            "openness": 6  # 开放性
        }
        
        # 根据自动化分析调整
        auto_analysis = analysis_result.get("automated_data_analysis", {})
        personality_indicators = auto_analysis.get("personality_indicators", [])
        
        if "外向性" in personality_indicators:
            profile["extraversion"] = 8
        
        if "宜人性" in personality_indicators:
            profile["agreeableness"] = 8
        
        if "尽责性" in personality_indicators:
            profile["conscientiousness"] = 8
        
        if "情绪稳定性" in personality_indicators:
            profile["emotional_stability"] = 9
        
        if "开放性" in personality_indicators:
            profile["openness"] = 8
        
        return profile
    
    def generate_relationship_preferences(self, collected_data: Dict[str, Any], 
                                        analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成关系偏好"""
        manual_data = collected_data.get("manual_data", {})
        requirements = manual_data.get("next_requirements", {})
        
        preferences = {
            "communication_needs": self.assess_communication_needs(collected_data),
            "intimacy_level": "平衡",  # 亲密程度
            "independence_need": "适中",  # 独立需求
            "conflict_resolution": "建设性沟通",  # 冲突解决方式
            "support_style": "相互支持"  # 支持方式
        }
        
        # 根据底线特质调整
        deal_breakers = requirements.get("deal_breakers", [])
        for breaker in deal_breakers:
            trait = breaker.get("trait", "").lower()
            if "控制" in trait or "依赖" in trait:
                preferences["independence_need"] = "高"
            elif "冷漠" in trait or "忽视" in trait:
                preferences["communication_needs"] = "高频率"
                preferences["support_style"] = "主动关心"
        
        return preferences
    
    def assess_communication_needs(self, collected_data: Dict[str, Any]) -> str:
        """评估沟通需求"""
        auto_analysis = collected_data.get("automated_data_analysis", {})
        communication_style = auto_analysis.get("communication_style", [])
        
        if "沟通频繁" in communication_style:
            return "高频率"
        elif "沟通简洁" in communication_style:
            return "高质量"
        else:
            return "平衡"
    
    def generate_lifestyle_preferences(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成生活方式偏好"""
        manual_data = collected_data.get("manual_data", {})
        requirements = manual_data.get("next_requirements", {})
        lifestyle = requirements.get("lifestyle", {})
        
        auto_analysis = collected_data.get("automated_data_analysis", {})
        interest_patterns = auto_analysis.get("interest_patterns", [])
        
        preferences = {
            "work_life_balance": lifestyle.get("work_life_balance", "平衡"),
            "social_style": lifestyle.get("social_style", "适中"),
            "hobbies_interests": interest_patterns,
            "future_orientation": lifestyle.get("future_plans", "有规划"),
            "health_habits": ["规律作息", "适度运动"]  # 默认值
        }
        
        return preferences
    
    def generate_compatibility_summary(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成兼容性摘要"""
        compatibility_patterns = analysis_result.get("compatibility_patterns", {})
        
        summary = {
            "strength_alignment_score": len(compatibility_patterns.get("strength_alignment", [])),
            "weakness_avoidance_score": len(compatibility_patterns.get("weakness_avoidance", [])),
            "value_compatibility": compatibility_patterns.get("value_compatibility", []),
            "overall_compatibility": "高",  # 基于分析结果
            "key_alignments": [],
            "potential_challenges": []
        }
        
        # 计算总体兼容性
        total_score = summary["strength_alignment_score"] + summary["weakness_avoidance_score"]
        if total_score >= 5:
            summary["overall_compatibility"] = "非常高"
        elif total_score >= 3:
            summary["overall_compatibility"] = "高"
        elif total_score >= 1:
            summary["overall_compatibility"] = "中等"
        else:
            summary["overall_compatibility"] = "需要进一步评估"
        
        return summary
    
    def generate_growth_focus(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成成长重点"""
        growth_opportunities = analysis_result.get("growth_opportunities", [])
        
        focus_areas = []
        for opportunity in growth_opportunities[:5]:  # 取前5个最重要的
            focus_areas.append({
                "area": opportunity.get("description", ""),
                "priority": opportunity.get("priority", "medium"),
                "action": opportunity.get("action", "")
            })
        
        return focus_areas
    
    def generate_compatibility_analysis(self, collected_data: Dict[str, Any], 
                                      analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成兼容性分析"""
        compatibility_patterns = analysis_result.get("compatibility_patterns", {})
        
        analysis = {
            "emotional_compatibility": self.assess_emotional_compatibility(collected_data),
            "value_compatibility": self.assess_value_compatibility(collected_data),
            "lifestyle_compatibility": self.assess_lifestyle_compatibility(collected_data),
            "communication_compatibility": self.assess_communication_compatibility(collected_data),
            "growth_compatibility": self.assess_growth_compatibility(collected_data),
            "alignment_summary": compatibility_patterns
        }
        
        return analysis
    
    def assess_emotional_compatibility(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估情感兼容性"""
        return {
            "score": 8,
            "strengths": ["情感表达匹配", "情绪稳定性好", "相互理解"],
            "areas_for_attention": ["情感需求沟通", "压力应对协调"],
            "recommendations": ["定期情感交流", "建立情感支持机制"]
        }
    
    def assess_value_compatibility(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估价值观兼容性"""
        analysis_result = collected_data.get("analysis_result", {})
        req_analysis = analysis_result.get("requirements_analysis", {})
        value_alignment = req_analysis.get("value_alignment", [])
        
        return {
            "score": 7,
            "shared_values": value_alignment,
            "potential_differences": [],
            "recommendations": ["明确核心价值观", "尊重差异"]
        }
    
    def assess_lifestyle_compatibility(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估生活方式兼容性"""
        manual_data = collected_data.get("manual_data", {})
        requirements = manual_data.get("next_requirements", {})
        lifestyle = requirements.get("lifestyle", {})
        
        return {
            "score": 7,
            "compatible_areas": list(lifestyle.keys()),
            "adjustment_needed": [],
            "recommendations": ["协调作息时间", "规划共同活动"]
        }
    
    def assess_communication_compatibility(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估沟通兼容性"""
        auto_analysis = collected_data.get("automated_data_analysis", {})
        communication_style = auto_analysis.get("communication_style", [])
        
        return {
            "score": 8,
            "communication_styles": communication_style,
            "potential_challenges": [],
            "recommendations": ["建立沟通规则", "定期关系回顾"]
        }
    
    def assess_growth_compatibility(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估成长兼容性"""
        analysis_result = collected_data.get("analysis_result", {})
        growth_opportunities = analysis_result.get("growth_opportunities", [])
        
        return {
            "score": 8,
            "growth_alignment": len(growth_opportunities),
            "mutual_goals": ["关系成长", "个人发展"],
            "recommendations": ["制定共同成长计划", "定期目标回顾"]
        }
    
    def generate_growth_plan(self, collected_data: Dict[str, Any], 
                           analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成成长计划"""
        growth_opportunities = analysis_result.get("growth_opportunities", [])
        
        plan = {
            "short_term_goals": [],
            "medium_term_goals": [],
            "long_term_vision": [],
            "action_steps": [],
            "success_metrics": []
        }
        
        # 短期目标（1-3个月）
        for opportunity in growth_opportunities[:3]:
            if opportunity.get("priority") in ["high", "critical"]:
                plan["short_term_goals"].append({
                    "goal": opportunity.get("description", ""),
                    "timeline": "1-3个月",
                    "action": opportunity.get("action", "")
                })
        
        # 中期目标（3-12个月）
        plan["medium_term_goals"] = [
            {
                "goal": "建立稳定的沟通模式",
                "timeline": "3-6个月",
                "action": "每周进行关系回顾"
            },
            {
                "goal": "深化情感连接",
                "timeline": "6-12个月",
                "action": "定期进行深度交流"
            }
        ]
        
        # 长期愿景（1-3年）
        plan["long_term_vision"] = [
            "建立相互支持、共同成长的关系",
            "实现个人和关系的平衡发展",
            "培养深厚的信任和理解"
        ]
        
        # 具体行动步骤
        plan["action_steps"] = [
            "每周安排专属的交流时间",
            "每月进行一次关系评估",
            "每季度制定共同目标",
            "每年进行关系回顾和规划"
        ]
        
        # 成功指标
        plan["success_metrics"] = [
            "沟通满意度提升",
            "冲突解决效率提高",
            "相互理解加深",
            "共同目标达成率"
        ]
        
        return plan
    
    def generate_relationship_insights(self, collected_data: Dict[str, Any], 
                                     analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成关系洞察"""
        ex_analysis = analysis_result.get("ex_analysis", {})
        relationship_patterns = ex_analysis.get("relationship_patterns", [])
        
        insights = {
            "key_learnings": relationship_patterns,
            "patterns_to_repeat": [],
            "patterns_to_avoid": [],
            "relationship_principles": [],
            "red_flags": [],
            "green_flags": []
        }
        
        # 从经验教训中提取
        for pattern in relationship_patterns:
            if "经验教训" in pattern:
                insights["key_learnings"].append(pattern)
        
        # 从优点中提取可重复的模式
        inheritable_traits = ex_analysis.get("inheritable_traits", [])
        for trait in inheritable_traits:
            insights["patterns_to_repeat"].append(
                f"保持{trait.get('trait')}的特质"
            )
        
        # 从缺点中提取要避免的模式
        avoidable_traits = ex_analysis.get("avoidable_traits", [])
        for trait in avoidable_traits:
            insights["patterns_to_avoid"].append(
                f"避免{trait.get('trait')}的行为模式"
            )
        
        # 关系原则
        insights["relationship_principles"] = [
            "相互尊重和理解",
            "开放和诚实的沟通",
            "共同成长和支持",
            "保持个人空间和独立性",
            "及时解决冲突"
        ]
        
        # 红色和绿色信号
        insights["red_flags"] = [
            "缺乏基本尊重",
            "沟通障碍持续存在",
            "价值观严重冲突",
            "情感需求长期不被满足"
        ]
        
        insights["green_flags"] = [
            "相互支持和鼓励",
            "有效沟通和解决问题",
            "价值观基本一致",
            "共同成长意愿",
            "相互信任和尊重"
        ]
        
        return insights
    
    def generate_metadata(self, collected_data: Dict[str, Any], skill_slug: str, version: str) -> Dict[str, Any]:
        """生成元数据"""
        basic_info = collected_data.get("basic_info", {})
        manual_data = collected_data.get("manual_data", {})
        automated_data = collected_data.get("automated_data", {})
        
        metadata = {
            "skill_info": {
                "slug": skill_slug,
                "name": basic_info.get("partner_code", "理想伴侣"),
                "description": f"基于前任分析和用户要求生成的理想伴侣档案",
                "version": version,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            "data_sources": {
                "manual_input": bool(manual_data),
                "automated_collection": automated_data.get("success", False),
                "collection_method": collected_data.get("metadata", {}).get("collection_method", "manual"),
                "files_collected": len(automated_data.get("files", [])) if automated_data.get("success") else 0
            },
            "analysis_summary": {
                "ex_strengths_analyzed": len(manual_data.get("ex_strengths", [])),
                "ex_weaknesses_analyzed": len(manual_data.get("ex_weaknesses", [])),
                "must_have_traits": len(manual_data.get("next_requirements", {}).get("must_have", [])),
                "deal_breakers": len(manual_data.get("next_requirements", {}).get("deal_breakers", [])),
                "compatibility_patterns_found": 0  # 将在后续计算
            },
            "generation_info": {
                "generated_by": "EnhancedSkillWriter v2.0",
                "generation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "output_directory": os.path.join(self.output_dir, skill_slug)
            }
        }
        
        return metadata
    
    def generate_skill_md_content(self, collected_data: Dict[str, Any], 
                                analysis_result: Dict[str, Any], 
                                skill_slug: str, version: str) -> str:
        """生成SKILL.md内容"""
        basic_info = collected_data.get("basic_info", {})
        partner_code = basic_info.get("partner_code", "理想伴侣")
        
        # 获取分析结果
        profile_data = self.generate_profile_data(collected_data, analysis_result)
        compatibility_data = self.generate_compatibility_analysis(collected_data, analysis_result)
        growth_plan = self.generate_growth_plan(collected_data, analysis_result)
        insights = self.generate_relationship_insights(collected_data, analysis_result)
        
        # 生成内容
        content = f"""---
name: {skill_slug}
description: {partner_code}的详细档案。基于前任关系分析和下一任要求生成的理想伴侣档案，包含性格特征、价值观体系、生活方式偏好和兼容性分析。
license: CC-BY-NC-4.0
metadata:
  generated_by: create-next-partner-optimized
  version: "{version}"
  generated_at: {datetime.now().isoformat()}
  data_sources: {collected_data.get("metadata", {}).get("collection_method", "manual")}
---

# {partner_code} - 理想伴侣档案（增强版）

## 概述

这是基于您的前任关系分析和下一任要求生成的增强版理想伴侣档案。档案综合了：

1. **值得继承的优点**：从前任关系中提取的积极特质
2. **需要避免的缺点**：从前任关系中识别的问题模式
3. **具体要求**：您对下一任伴侣的具体要求
4. **自动化分析**：基于实际数据的性格和沟通模式分析

## 性格特征

### 核心特质

"""
        
        # 添加核心特质
        personality_profile = profile_data.get("personality_profile", {})
        core_traits = personality_profile.get("core_traits", [])
        
        for trait in core_traits:
            content += f"- **{trait.get('trait')}**（来源：{trait.get('source')}，优先级：{trait.get('priority')}）\n"
        
        content += f"""
### 沟通风格

{', '.join(personality_profile.get('communication_style', ['待分析']))}

### 情感表达方式

{personality_profile.get('emotional_expression', '平衡适中')}

### 大五人格档案

- **外向性**: {personality_profile.get('big_five_profile', {}).get('extraversion', 6)}/10
- **宜人性**: {personality_profile.get('big_five_profile', {}).get('agreeableness', 7)}/10
- **尽责性**: {personality_profile.get('big_five_profile', {}).get('conscientiousness', 7)}/10
- **情绪稳定性**: {personality_profile.get('big_five_profile', {}).get('emotional_stability', 8)}/10
- **开放性**: {personality_profile.get('big_five_profile', {}).get('openness', 6)}/10

## 关系偏好

"""
        
        # 添加关系偏好
        relationship_prefs = profile_data.get("relationship_preferences", {})
        for key, value in relationship_prefs.items():
            content += f"- **{key}**: {value}\n"
        
        content += """
## 生活方式偏好

"""
        
        # 添加生活方式偏好
        lifestyle_prefs = profile_data.get("lifestyle_preferences", {})
        for key, value in lifestyle_prefs.items():
            if isinstance(value, list):
                content += f"- **{key}**: {', '.join(value)}\n"
            else:
                content += f"- **{key}**: {value}\n"
        
        content += """
## 兼容性分析

### 总体兼容性评分

**{compatibility_data.get('alignment_summary', {}).get('overall_compatibility', '高')}**

### 各维度分析

"""
        
        # 添加兼容性分析
        compatibility_keys = ['emotional_compatibility', 'value_compatibility', 
                            'lifestyle_compatibility', 'communication_compatibility', 
                            'growth_compatibility']
        
        for key in compatibility_keys:
            if key in compatibility_data:
                analysis = compatibility_data[key]
                content += f"#### {key.replace('_', ' ').title()}\n"
                content += f"- **评分**: {analysis.get('score', 0)}/10\n"
                content += f"- **优势**: {', '.join(analysis.get('strengths', []))}\n"
                content += f"- **建议**: {', '.join(analysis.get('recommendations', []))}\n\n"
        
        content += """
## 成长发展计划

### 短期目标（1-3个月）

"""
        
        # 添加短期目标
        for goal in growth_plan.get("short_term_goals", []):
            content += f"- **{goal.get('goal', '')}**（时间：{goal.get('timeline', '')}）\n"
            content += f"  行动：{goal.get('action', '')}\n"
        
        content += """
### 中期目标（3-12个月）

"""
        
        # 添加中期目标
        for goal in growth_plan.get("medium_term_goals", []):
            content += f"- **{goal.get('goal', '')}**（时间：{goal.get('timeline', '')}）\n"
            content += f"  行动：{goal.get('action', '')}\n"
        
        content += """
### 长期愿景（1-3年）

"""
        
        # 添加长期愿景
        for vision in growth_plan.get("long_term_vision", []):
            content += f"- {vision}\n"
        
        content += """
### 具体行动步骤

"""
        
        # 添加行动步骤
        for step in growth_plan.get("action_steps", []):
            content += f"- {step}\n"
        
        content += """
## 关系洞察

### 关键经验教训

"""
        
        # 添加经验教训
        for learning in insights.get("key_learnings", []):
            content += f"- {learning}\n"
        
        content += """
### 可重复的模式

"""
        
        # 添加可重复模式
        for pattern in insights.get("patterns_to_repeat", []):
            content += f"- {pattern}\n"
        
        content += """
### 要避免的模式

"""
        
        # 添加要避免的模式
        for pattern in insights.get("patterns_to_avoid", []):
            content += f"- {pattern}\n"
        
        content += """
### 关系健康信号

#### 绿色信号（积极信号）

"""
        
        # 添加绿色信号
        for flag in insights.get("green_flags", []):
            content += f"- ✅ {flag}\n"
        
        content += """
#### 红色信号（警示信号）

"""
        
        # 添加红色信号
        for flag in insights.get("red_flags", []):
            content += f"- ⚠️  {flag}\n"
        
        content += f"""
---

**生成信息**
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 数据来源: {collected_data.get('metadata', {}).get('collection_method', '手动输入')}
- 版本: {version}
- 生成工具: create-next-partner-optimized v2.0

**使用建议**
1. 将此档案作为参考，而非绝对标准
2. 实际关系中保持灵活性和开放性
3. 定期回顾和更新档案内容
4. 关注关系中的实际体验而非理论匹配

**更新说明**
如需更新此档案，请提供新信息或反馈，系统将自动分析并生成更新版本。
"""
        
        return content
    
    def _create_profile_json(self, skill_dir: str, profile_data: Dict[str, Any]):
        """创建profile.json文件"""
        filepath = os.path.join(skill_dir, "profile.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
        print(f"  📄 创建 profile.json")
    
    def _create_compatibility_md(self, skill_dir: str, compatibility_data: Dict[str, Any]):
        """创建compatibility.md文件"""
        filepath = os.path.join(skill_dir, "compatibility.md")
        
        content = f"""# 兼容性分析报告

## 概述

本报告基于您提供的前任关系分析和下一任要求，评估理想伴侣的兼容性。

## 分析维度

"""
        
        # 添加各维度分析
        for key, analysis in compatibility_data.items():
            if key != "alignment_summary" and isinstance(analysis, dict):
                content += f"### {key.replace('_', ' ').title()}\n\n"
                content += f"**评分**: {analysis.get('score', 0)}/10\n\n"
                
                if analysis.get('strengths'):
                    content += "**优势**:\n"
                    for strength in analysis.get('strengths', []):
                        content += f"- {strength}\n"
                    content += "\n"
                
                if analysis.get('areas_for_attention'):
                    content += "**关注点**:\n"
                    for area in analysis.get('areas_for_attention', []):
                        content += f"- {area}\n"
                    content += "\n"
                
                if analysis.get('recommendations'):
                    content += "**建议**:\n"
                    for rec in analysis.get('recommendations', []):
                        content += f"- {rec}\n"
                    content += "\n"
        
        content += "## 总体建议\n\n"
        content += "基于以上分析，建议在关系中重点关注情感沟通和价值观对齐，建立稳定的沟通模式。\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 创建 compatibility.md")
    
    def _create_growth_plan_md(self, skill_dir: str, growth_plan: Dict[str, Any]):
        """创建growth_plan.md文件"""
        filepath = os.path.join(skill_dir, "growth_plan.md")
        
        content = """# 关系成长计划

## 目标设定

### 短期目标（1-3个月）

"""
        
        for goal in growth_plan.get("short_term_goals", []):
            content += f"### {goal.get('goal', '')}\n"
            content += f"- **时间**: {goal.get('timeline', '')}\n"
            content += f"- **行动**: {goal.get('action', '')}\n"
            content += f"- **衡量标准**: 完成相关行动并记录感受\n\n"
        
        content += "### 中期目标（3-12个月）\n\n"
        
        for goal in growth_plan.get("medium_term_goals", []):
            content += f"### {goal.get('goal', '')}\n"
            content += f"- **时间**: {goal.get('timeline', '')}\n"
            content += f"- **行动**: {goal.get('action', '')}\n"
            content += f"- **衡量标准**: 建立稳定的行为模式\n\n"
        
        content += "### 长期愿景（1-3年）\n\n"
        
        for vision in growth_plan.get("long_term_vision", []):
            content += f"- {vision}\n"
        
        content += "\n## 行动步骤\n\n"
        
        for i, step in enumerate(growth_plan.get("action_steps", []), 1):
            content += f"{i}. {step}\n"
        
        content += "\n## 成功指标\n\n"
        
        for metric in growth_plan.get("success_metrics", []):
            content += f"- {metric}\n"
        
        content += "\n## 执行建议\n\n"
        content += "1. 每周回顾进展\n2. 每月评估目标完成情况\n3. 每季度调整计划\n4. 保持灵活性和开放性\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 创建 growth_plan.md")
    
    def _create_relationship_insights_md(self, skill_dir: str, insights: Dict[str, Any]):
        """创建relationship_insights.md文件"""
        filepath = os.path.join(skill_dir, "relationship_insights.md")
        
        content = """# 关系洞察报告

## 从前任关系中学习的经验

"""
        
        for learning in insights.get("key_learnings", []):
            content += f"- {learning}\n"
        
        content += "\n## 可重复的成功模式\n\n"
        
        for pattern in insights.get("patterns_to_repeat", []):
            content += f"- ✅ {pattern}\n"
        
        content += "\n## 要避免的问题模式\n\n"
        
        for pattern in insights.get("patterns_to_avoid", []):
            content += f"- ⚠️  {pattern}\n"
        
        content += "\n## 健康关系原则\n\n"
        
        for principle in insights.get("relationship_principles", []):
            content += f"- {principle}\n"
        
        content += "\n## 关系健康信号\n\n"
        content += "### 绿色信号（积极信号）\n\n"
        
        for flag in insights.get("green_flags", []):
            content += f"- ✅ {flag}\n"
        
        content += "\n### 红色信号（警示信号）\n\n"
        
        for flag in insights.get("red_flags", []):
            content += f"- ⚠️  {flag}\n"
        
        content += "\n## 应用建议\n\n"
        content += "1. 将这些洞察作为关系建设的参考框架\n"
        content += "2. 定期回顾这些原则和信号\n"
        content += "3. 根据实际情况调整和应用\n"
        content += "4. 保持自我反思和关系评估\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 创建 relationship_insights.md")
    
    def _create_metadata_json(self, skill_dir: str, metadata: Dict[str, Any]):
        """创建metadata.json文件"""
        filepath = os.path.join(skill_dir, "metadata.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"  📄 创建 metadata.json")
    
    def _create_skill_md(self, skill_dir: str, content: str, skill_slug: str):
        """创建SKILL.md文件"""
        filepath = os.path.join(skill_dir, "SKILL.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 创建 SKILL.md")
    
    def save_knowledge_files(self, skill_dir: str, collected_data: Dict[str, Any]):
        """保存知识文件"""
        automated_data = collected_data.get("automated_data", {})
        
        if not automated_data.get("success", False):
            return
        
        content = automated_data.get("content", {})
        output_dir = automated_data.get("output_dir", "")
        
        if not content or not output_dir:
            return
        
        knowledge_dir = os.path.join(skill_dir, "knowledge")
        
        # 复制文件
        for filename, text in content.items():
            if filename.endswith(('.txt', '.md', '.json')):
                dest_path = os.path.join(knowledge_dir, filename)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(text)
        
        print(f"  📁 保存知识文件到 knowledge/")
    
    def list_generated_skills(self) -> List[Dict[str, Any]]:
        """列出所有生成的skill"""
        return self.generated_skills
    
    def get_skill_info(self, skill_slug: str) -> Optional[Dict[str, Any]]:
        """获取特定skill的信息"""
        for skill in self.generated_skills:
            if skill.get("slug") == skill_slug:
                return skill
        return None
    
    def update_skill(self, skill_slug: str, new_data: Dict[str, Any], 
                   version: str = "2.0.1") -> Optional[str]:
        """更新现有skill"""
        skill_info = self.get_skill_info(skill_slug)
        if not skill_info:
            print(f"❌ 未找到skill: {skill_slug}")
            return None
        
        skill_dir = skill_info.get("path")
        if not os.path.exists(skill_dir):
            print(f"❌ skill目录不存在: {skill_dir}")
            return None
        
        # 创建版本备份
        versions_dir = os.path.join(skill_dir, "versions")
        os.makedirs(versions_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(versions_dir, f"v{skill_info.get('version', '1.0')}_{timestamp}")
        
        # 备份当前文件
        import shutil
        shutil.copytree(skill_dir, backup_dir, dirs_exist_ok=True)
        print(f"📁 创建版本备份: {backup_dir}")
        
        # 重新生成skill
        print(f"🔄 更新skill: {skill_slug}")
        
        # 合并数据
        collected_data = skill_info.get("metadata", {}).get("original_data", {})
        collected_data.update(new_data)
        
        # 重新分析并生成
        analysis_result = self.analyze_collected_data(collected_data)
        skill_content = self.generate_skill_md_content(collected_data, analysis_result, skill_slug, version)
        
        # 更新文件
        self._create_skill_md(skill_dir, skill_content, skill_slug)
        
        # 更新metadata
        metadata = self.generate_metadata(collected_data, skill_slug, version)
        metadata["previous_version"] = skill_info.get("version")
        metadata["updated_at"] = datetime.now().isoformat()
        self._create_metadata_json(skill_dir, metadata)
        
        # 更新记录
        skill_info.update({
            "version": version,
            "updated_at": datetime.now().isoformat(),
            "metadata": metadata
        })
        
        print(f"✅ skill更新完成: {skill_slug} (v{version})")
        return skill_dir

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="增强版Skill文件生成器")
    parser.add_argument("--input", required=True, help="输入数据文件路径（JSON格式）")
    parser.add_argument("--output-dir", default="partners", help="输出目录")
    parser.add_argument("--skill-name", help="skill名称（可选）")
    parser.add_argument("--version", default="2.0.0", help="版本号")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--list", action="store_true", help="列出所有生成的skill")
    parser.add_argument("--info", help="获取特定skill信息")
    parser.add_argument("--update", help="更新特定skill")
    parser.add_argument("--update-data", help="更新数据文件路径")
    
    args = parser.parse_args()
    
    writer = EnhancedSkillWriter(output_dir=args.output_dir, debug=args.debug)
    
    if args.list:
        # 列出所有skill
        skills = writer.list_generated_skills()
        if skills:
            print("\n📋 生成的Skill列表:")
            for skill in skills:
                print(f"  - {skill.get('slug')} (v{skill.get('version')})")
                print(f"    路径: {skill.get('path')}")
                print(f"    创建时间: {skill.get('created_at')}")
        else:
            print("📭 尚未生成任何skill")
        return
    
    if args.info:
        # 获取skill信息
        skill_info = writer.get_skill_info(args.info)
        if skill_info:
            print(f"\n📋 Skill信息: {args.info}")
            print(f"  版本: {skill_info.get('version')}")
            print(f"  路径: {skill_info.get('path')}")
            print(f"  创建时间: {skill_info.get('created_at')}")
            print(f"  元数据: {json.dumps(skill_info.get('metadata', {}), ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 未找到skill: {args.info}")
        return
    
    if args.update and args.update_data:
        # 更新skill
        try:
            with open(args.update_data, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
            
            result = writer.update_skill(args.update, new_data, version="2.0.1")
            if result:
                print(f"✅ 更新成功: {result}")
            else:
                print("❌ 更新失败")
        except Exception as e:
            print(f"❌ 更新失败: {e}")
        return
    
    # 创建新skill
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            collected_data = json.load(f)
        
        skill_dir = writer.create_enhanced_partner_skill(
            collected_data=collected_data,
            skill_slug=args.skill_name,
            version=args.version
        )
        
        print(f"\n🎉 生成完成!")
        print(f"📁 Skill目录: {skill_dir}")
        print(f"📄 主文件: {os.path.join(skill_dir, 'SKILL.md')}")
        print(f"📊 配置文件: {os.path.join(skill_dir, 'profile.json')}")
        print(f"🤝 兼容性分析: {os.path.join(skill_dir, 'compatibility.md')}")
        print(f"📈 成长计划: {os.path.join(skill_dir, 'growth_plan.md')}")
        print(f"💡 关系洞察: {os.path.join(skill_dir, 'relationship_insights.md')}")
        print(f"📋 元数据: {os.path.join(skill_dir, 'metadata.json')}")
        
    except FileNotFoundError:
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
