#!/usr/bin/env python3
"""
快速测试脚本：验证爬虫能否正常运行
"""
import asyncio
import json
import sys
import os

# 添加src目录到路径
sys.path.append('src')

from src.scraper import scrape_xianyu

async def quick_test():
    """快速测试爬虫"""
    print("=== 快速测试爬虫运行 ===")
    
    # 测试任务
    test_task = {
        "keyword": "马里奥网球",
        "task_name": "快速测试",
        "max_pages": 1,
        "personal_only": False,
        "min_price": 50,
        "max_price": 500,
        "ai_prompt_text": "测试",
        "delay_config": {
            "page_navigation_delay": 3,
            "detail_access_delay": 1,
            "min_item_delay": 3,
            "max_item_delay": 5,
            "min_page_delay": 5,
            "max_page_delay": 10
        }
    }
    
    print("开始测试任务...")
    print(f"关键词: {test_task['keyword']}")
    print(f"最大页数: {test_task['max_pages']}")
    
    try:
        processed = await scrape_xianyu(test_task, debug_limit=2)
        print(f"测试完成，处理了 {processed} 个商品")
    except KeyboardInterrupt:
        print("用户中断测试")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())