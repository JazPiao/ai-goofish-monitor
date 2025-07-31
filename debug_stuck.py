#!/usr/bin/env python3
"""
调试脚本：检查程序卡住的原因
"""
import asyncio
import json
import sys
import os

# 添加src目录到路径
sys.path.append('src')

async def debug_scraper():
    """调试爬虫卡住的问题"""
    print("=== 调试爬虫卡住问题 ===")
    
    # 检查配置文件
    from src.config import STATE_FILE, RUN_HEADLESS, LOGIN_IS_EDGE, RUNNING_IN_DOCKER
    
    print(f"检查配置:")
    print(f"  STATE_FILE: {STATE_FILE}")
    print(f"  RUN_HEADLESS: {RUN_HEADLESS}")
    print(f"  LOGIN_IS_EDGE: {LOGIN_IS_EDGE}")
    print(f"  RUNNING_IN_DOCKER: {RUNNING_IN_DOCKER}")
    
    # 检查状态文件
    if os.path.exists(STATE_FILE):
        print(f"  状态文件存在: {STATE_FILE}")
        with open(STATE_FILE, 'r') as f:
            state_content = f.read()
            print(f"  状态文件内容长度: {len(state_content)} 字符")
    else:
        print(f"  状态文件不存在: {STATE_FILE}")
    
    # 检查网络连接
    import requests
    try:
        response = requests.get("https://www.goofish.com", timeout=10)
        print(f"  网络连接测试: 成功 (状态码 {response.status_code})")
    except Exception as e:
        print(f"  网络连接测试: 失败 - {e}")
    
    print("\n=== 检查任务配置 ===")
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                print(f"  找到 {len(tasks)} 个任务")
                for i, task in enumerate(tasks):
                    print(f"  任务 {i+1}: {task.get('keyword', '未知')} - {task.get('task_name', '未命名')}")
        except Exception as e:
            print(f"  读取配置文件失败: {e}")
    else:
        print("  配置文件不存在")

if __name__ == "__main__":
    asyncio.run(debug_scraper())