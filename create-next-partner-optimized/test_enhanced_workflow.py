#!/usr/bin/env python3
"""
增强版后任生成器测试工作流程
测试整个系统的集成功能
"""

import json
import os
import sys
import tempfile
from datetime import datetime

def create_test_data():
    """创建测试数据"""
    test_data = {
        "basic_info": {
            "partner_code": "test_ideal_partner",
            "ex_name": "测试前任",
            "relationship_duration": "2年",
            "breakup_reason": "价值观不一致，沟通不畅",
            "key_lessons": [
                "沟通要及时，不要积累问题",
                "需要相互尊重个人空间",
                "价值观一致很重要"
            ]
        },
        "manual_data": {
            "ex_strengths": [
                {
                    "trait": "体贴关心",
                    "example": "生病时会照顾，记得重要日子",
                    "impact": "让人感受到被爱和被重视",
                    "category": "relationship_skill",
                    "priority": "inherit"
                },
                {
                    "trait": "幽默风趣",
                    "example": "能调节气氛，让相处轻松愉快",
                    "impact": "减少关系中的压力",
                    "category": "personality",
                    "priority": "inherit"
                },
                {
                    "trait": "有共同兴趣",
                    "example": "都喜欢音乐和旅行",
                    "impact": "有共同话题和活动",
                    "category": "habit",
                    "priority": "inherit"
                }
            ],
            "ex_weaknesses": [
                {
                    "trait": "情绪不稳定",
                    "impact": "经常因为小事发脾气，难以预测",
                    "avoidable": True,
                    "severity": "high",
                    "category": "personality"
                },
                {
                    "trait": "缺乏安全感",
                    "impact": "需要频繁确认关系，造成压力",
                    "avoidable": True,
                    "severity": "medium",
                    "category": "relationship_skill"
                }
            ],
            "next_requirements": {
                "must_have": [
                    {
                        "trait": "情绪稳定",
                        "reason": "希望关系稳定可预测",
                        "priority": "高",
                        "non_negotiable": True
                    },
                    {
                        "trait": "善于沟通",
                        "reason": "能有效解决问题",
                        "priority": "高",
                        "non_negotiable": True
                    },
                    {
                        "trait": "尊重个人空间",
                        "reason": "需要独立性和信任",
                        "priority": "高",
                        "non_negotiable": True
                    }
                ],
                "nice_to_have": [
                    {
                        "trait": "喜欢旅行",
                        "priority": "低",
                        "non_negotiable": False
                    },
                    {
                        "trait": "有幽默感",
                        "priority": "低",
                        "non_negotiable": False
                    }
                ],
                "deal_breakers": [
                    {
                        "trait": "控制欲强",
                        "reason": "需要自由和尊重",
                        "severity": "critical"
                    },
                    {
                        "trait": "不诚实",
                        "reason": "信任是关系的基础",
                        "severity": "critical"
                    }
                ],
                "lifestyle": {
                    "work_life_balance": "平衡",
                    "social_style": "适中",
                    "future_plans": "有稳定规划",
                    "hobbies_interests": "音乐、旅行、阅读"
                }
            }
        },
        "automated_data": {
            "success": True,
            "method": "paste_text",
            "files": ["pasted_content.txt"],
            "content": {
                "pasted_content.txt": """测试沟通记录：
张三: 今天工作怎么样？
李四: 还不错，完成了项目的第一阶段。
张三: 太好了！晚上一起吃饭庆祝一下？
李四: 好啊，我知道一家新开的餐厅。
张三: 听起来不错，几点见面？
李四: 7点怎么样？我6点下班。
张三: 好的，到时候见！

测试文档内容：
最近在读《非暴力沟通》，觉得沟通真的很重要。
特别是表达感受和需求，而不是指责对方。
希望能在关系中实践这些原则。

兴趣爱好：
喜欢旅行，特别是自然风光。
最近在学吉他，希望能弹几首简单的曲子。
周末喜欢去咖啡馆看书，享受安静时光。"""
            },
            "output_dir": tempfile.mkdtemp()
        },
        "metadata": {
            "collected_at": datetime.now().isoformat(),
            "collection_method": "paste_text",
            "version": "2.0.0"
        }
    }
    
    return test_data

def test_data_collector():
    """测试简化版数据收集器"""
    print("=" * 60)
    print("测试简化版数据收集器")
    print("=" * 60)
    
    # 创建测试数据
    test_data = create_test_data()
    
    # 保存测试数据
    os.makedirs("test_data", exist_ok=True)
    test_file = "test_data/test_collected_data.json"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试数据已创建: {test_file}")
    
    # 测试数据收集器
    try:
        from tools.data_collector import EnhancedDataCollector
        
        collector = EnhancedDataCollector(debug=True)
        
        # 测试保存功能
        saved_file = collector.save_to_file("test_output.json")
        print(f"✅ 数据保存测试通过: {saved_file}")
        
    except Exception as e:
        print(f"❌ 数据收集器测试失败: {e}")
        return False
    
    return True

def test_skill_writer():
    """测试Skill生成器"""
    print("\n" + "=" * 60)
    print("测试增强版Skill生成器")
    print("=" * 60)
    
    # 加载测试数据
    test_file = "test_data/test_collected_data.json"
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
        
        from tools.skill_writer import EnhancedSkillWriter
        
        writer = EnhancedSkillWriter(output_dir="test_partners", debug=True)
        
        # 生成Skill
        skill_dir = writer.create_enhanced_partner_skill(
            collected_data=test_data,
            skill_slug="test_enhanced_partner",
            version="2.0.0"
        )
        
        # 验证生成的文件
        required_files = [
            "SKILL.md",
            "profile.json", 
            "compatibility.md",
            "growth_plan.md",
            "relationship_insights.md",
            "metadata.json"
        ]
        
        print("\n📁 验证生成的文件:")
        for filename in required_files:
            filepath = os.path.join(skill_dir, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"  ✅ {filename}: {file_size} 字节")
            else:
                print(f"  ❌ {filename}: 文件不存在")
                return False
        
        # 测试列表功能
        skills = writer.list_generated_skills()
        if skills:
            print(f"\n📋 生成的Skill数量: {len(skills)}")
            for skill in skills:
                print(f"  - {skill.get('slug')} (v{skill.get('version')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Skill生成器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """测试完整集成工作流程"""
    print("\n" + "=" * 60)
    print("测试完整集成工作流程")
    print("=" * 60)
    
    # 创建测试目录
    test_dir = "test_integration"
    os.makedirs(test_dir, exist_ok=True)
    
    # 模拟完整工作流程
    print("1. 创建测试数据...")
    test_data = create_test_data()
    
    print("2. 保存数据文件...")
    data_file = os.path.join(test_dir, "integration_data.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("3. 生成Skill文件...")
    try:
        # 使用命令行方式测试
        import subprocess
        
        cmd = [
            sys.executable, 
            "tools/skill_writer.py",
            "--input", data_file,
            "--output-dir", os.path.join(test_dir, "partners"),
            "--skill-name", "integration_test_partner",
            "--version", "2.0.0",
            "--debug"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 集成测试通过")
            print(f"输出:\n{result.stdout}")
            return True
        else:
            print(f"❌ 集成测试失败")
            print(f"错误:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 集成测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 增强版后任生成器系统测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        ("数据收集器", test_data_collector),
        ("Skill生成器", test_skill_writer),
        ("集成工作流程", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n▶️  运行测试: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
                
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以正常使用。")
        print("\n使用方法:")
        print("1. 运行数据收集器: python tools/data_collector.py")
        print("2. 生成Skill文件: python tools/skill_writer.py --input collected_data.json")
        print("3. 查看生成的Skill: 在 partners/ 目录下")
    else:
        print("\n⚠️  部分测试失败，请检查相关问题。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)