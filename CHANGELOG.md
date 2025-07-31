# 闲鱼智能监控机器人 - 问题修复记录

## 2024年7月31日 - 任务"马里奥网球"卡死问题修复

### 问题描述
任务"马里奥网球"在网页端显示为卡住状态，无法正常运行。

### 根本原因分析
1. **任务被禁用**：在`config.json`中，"马里奥网球"任务的`enabled`字段被设置为`false`
2. **JSON解析错误**：`src/scraper.py`中第339行和344行的`json.loads()`调用报错，因为接收到的数据已经是字典/列表类型，而不是JSON字符串
3. **端口冲突**：Web服务器端口8000被OrbStack占用，导致web_server.py无法启动

### 修复方案

#### 1. 启用任务
**文件**: `config.json`
**修改前**:
```json
{
  "task_id": 7,
  "task_name": "马里奥网球",
  "enabled": false,
  ...
}
```
**修改后**:
```json
{
  "task_id": 7,
  "task_name": "马里奥网球",
  "enabled": true,
  ...
}
```

#### 2. 修复JSON解析错误
**文件**: `src/scraper.py`
**位置**: 第335-370行
**问题**: `json.loads()`被用于已经是字典/列表的数据
**解决方案**: 添加类型检查，只在数据是字符串时才使用`json.loads()`

**修改前**:
```python
item_do_str = safe_get(item_detail, "itemDO", "暂无")
seller_do_str = safe_get(item_detail, "sellerDO", "暂无")
image_infos_str = safe_get(item_detail, "imageInfos", "暂无")

# 可能导致TypeError的代码
item_do = json.loads(item_do_str) if item_do_str != "暂无" else {}
seller_do = json.loads(seller_do_str) if seller_do_str != "暂无" else {}
image_infos = json.loads(image_infos_str) if image_infos_str != "暂无" else []
```

**修改后**:
```python
item_do_raw = safe_get(item_detail, "itemDO", "暂无")
seller_do_raw = safe_get(item_detail, "sellerDO", "暂无")
image_infos_raw = safe_get(item_detail, "imageInfos", "暂无")

# 安全处理不同类型的数据
item_do = item_do_raw if isinstance(item_do_raw, dict) else (
    json.loads(item_do_raw) if isinstance(item_do_raw, str) and item_do_raw != "暂无" else {}
)

seller_do = seller_do_raw if isinstance(seller_do_raw, dict) else (
    json.loads(seller_do_raw) if isinstance(seller_do_raw, str) and seller_do_raw != "暂无" else {}
)

image_infos = image_infos_raw if isinstance(image_infos_raw, list) else (
    json.loads(image_infos_raw) if isinstance(image_infos_raw, str) and image_infos_raw != "暂无" else []
)
```

#### 3. 解决端口冲突
**文件**: `.env`
**修改前**:
```
SERVER_PORT=8000
```
**修改后**:
```
SERVER_PORT=8002
```

### 验证结果
1. **任务状态**: "马里奥网球"任务已启用并可正常运行
2. **JSON解析**: 不再出现"JSON object must be str, bytes or bytearray, not list"错误
3. **Web服务**: 成功运行在 http://127.0.0.1:8002
4. **功能测试**: 任务能够正常爬取商品信息，执行AI分析，并发送通知

### 使用说明
- **网页端访问**: http://127.0.0.1:8002
- **命令行启动**: `python spider_v2.py --task-name "马里奥网球"`
- **调试模式**: 添加 `--debug-limit 2` 参数限制爬取数量

### 注意事项
- 如果再次遇到端口冲突，可以修改.env文件中的SERVER_PORT为其他可用端口
- 任务状态可以在网页端实时查看和管理
- 建议定期检查config.json确保任务保持启用状态