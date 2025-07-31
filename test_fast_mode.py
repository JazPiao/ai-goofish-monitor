#!/usr/bin/env python3
"""
快速测试脚本 - 用于验证延迟优化效果
运行此脚本可以快速测试爬虫是否正常工作，避免长时间等待
"""

import asyncio
import json
import sys
import os
from datetime import datetime

async def test_single_task():
    """测试单个任务的最小配置"""
    print("🚀 开始快速测试模式...")
    print("=" * 50)
    
    # 创建最小测试配置
    test_config = {
        "task_name": "快速测试",
        "keyword": "测试商品",
        "max_pages": 1,
        "personal_only": False,
        "delay_config": {
            "min_item_delay": 1,
            "max_item_delay": 2,
            "min_page_delay": 3,
            "max_page_delay": 5,
            "filter_click_delay": 0.5,
            "filter_result_delay": 1,
            "detail_access_delay": 0.5
        },
        "ai_prompt_text": "这是一个测试任务，请快速分析商品信息。"
    }
    
    # 检查登录状态
    state_file = "xianyu_state.json"
    if not os.path.exists(state_file):
        print(f"❌ 错误: 登录状态文件 '{state_file}' 不存在")
        print("请先运行: python login.py 或手动创建登录状态")
        return False
    
    try:
        from src.scraper import scrape_xianyu
        
        print("✅ 配置检查通过")
        print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔍 搜索关键词:", test_config["keyword"])
        print("📄 最大页数:", test_config["max_pages"])
        print("⚡ 延迟配置:")
        for key, value in test_config["delay_config"].items():
            print(f"   {key}: {value}s")
        
        print("\n" + "=" * 50)
        print("开始执行测试...")
        
        # 执行测试
        result = await scrape_xianyu(test_config, debug_limit=2)
        
        print("\n" + "=" * 50)
        print(f"✅ 测试完成！处理了 {result} 个商品")
        print("🎉 快速测试成功，爬虫运行正常")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_single_task())
    if success:
        print("\n💡 提示:")
        print("- 现在可以正常运行您的监控任务了")
        print("- 如果遇到卡顿，可以调整 config.json 中的 delay_config")
        print("- 使用 python spider_v2.py --debug-limit 3 进行更多测试")
    else:
        print("\n🔧 请检查错误信息并修复后重试")
        sys.exit(1)