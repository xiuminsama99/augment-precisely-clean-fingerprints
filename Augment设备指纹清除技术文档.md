# Augment 设备指纹清除技术文档

## 📋 技术原理

### Augment 设备识别机制

Augment 通过多层指纹技术识别设备：

1. **数据库存储**
   - VS Code SQLite 数据库：`state.vscdb`
   - 存储扩展状态、用户偏好、设备标识符

2. **配置文件存储**
   - 设备标识符文件：`storage.json`
   - 包含机器 ID、设备 ID 等关键标识符

3. **全局存储目录**
   - 扩展全局存储：`globalStorage/augment.*`
   - 缓存用户数据、会话信息、本地设置

4. **系统缓存**
   - 临时目录中的 Augment 文件
   - VS Code 各级缓存目录

5. **关键标识符**
   - `telemetry.machineId`: 64 位十六进制字符串（设备唯一标识）
   - `devDeviceId`: UUID 格式字符串（开发设备标识）

## 🔧 清理策略 v2.0

### 跨平台文件路径映射

#### Windows 平台
```
数据存储根目录: %APPDATA%\Code\User\
├── storage.json                    # 设备标识符配置
├── globalStorage\
│   ├── state.vscdb                # SQLite 数据库
│   └── augment.*\                 # Augment 全局存储（递归清理）
└── ..\Cache\                      # VS Code 缓存目录
    ├── Cache\                     # 通用缓存
    ├── CachedData\               # 扩展缓存数据
    └── GPUCache\                 # GPU 渲染缓存

临时文件: %TEMP%\augment*          # 系统临时目录（递归清理）
```

#### macOS 平台
```
数据存储根目录: ~/Library/Application Support/Code/User/
├── storage.json                    # 设备标识符配置
├── globalStorage/
│   ├── state.vscdb                # SQLite 数据库
│   └── augment.*/                 # Augment 全局存储（递归清理）
└── ../Cache/                      # VS Code 缓存目录
    ├── Cache/                     # 通用缓存
    ├── CachedData/               # 扩展缓存数据
    └── GPUCache/                 # GPU 渲染缓存

临时文件: /tmp/augment*            # 系统临时目录（递归清理）
```

#### Linux 平台
```
数据存储根目录: ~/.config/Code/User/
├── storage.json                    # 设备标识符配置
├── globalStorage/
│   ├── state.vscdb                # SQLite 数据库
│   └── augment.*/                 # Augment 全局存储（递归清理）
└── ../Cache/                      # VS Code 缓存目录
    ├── Cache/                     # 通用缓存
    ├── CachedData/               # 扩展缓存数据
    └── GPUCache/                 # GPU 渲染缓存

临时文件: /tmp/augment*            # 系统临时目录（递归清理）
```

### 彻底清理执行流程

#### 第一阶段：进程管理
```python
# 跨平台进程停止
if system == "Windows":
    subprocess.run(["taskkill", "/F", "/IM", "Code.exe"])
else:
    subprocess.run(["pkill", "-f", "Visual Studio Code"])
```

#### 第二阶段：数据库清理
```sql
-- 精确 SQL 删除操作
DELETE FROM ItemTable WHERE key LIKE '%augment%';
```
- 目标：`state.vscdb` SQLite 数据库
- 方法：模式匹配删除所有包含 `augment` 的键值对
- 结果：彻底清除扩展在数据库中的所有痕迹

#### 第三阶段：配置文件更新
```python
# 安全随机数生成新设备标识符
new_machine_id = secrets.token_hex(32)  # 64位十六进制
new_device_id = str(uuid.uuid4())       # 标准UUID

# 更新 storage.json
data["telemetry.machineId"] = new_machine_id
data["devDeviceId"] = new_device_id

# 清理所有 augment 相关键
keys_to_remove = [key for key in data.keys() if "augment" in key.lower()]
```

#### 第四阶段：递归文件清理
```python
# 深度递归搜索和删除
for item in path.rglob("*augment*"):
    if item.is_file():
        item.unlink()           # 删除文件
    elif item.is_dir():
        shutil.rmtree(item)     # 删除目录树
```
- 目标：全局存储目录、临时文件目录
- 方法：使用 `rglob("*augment*")` 递归搜索
- 范围：所有包含 `augment` 的文件和目录

#### 第五阶段：缓存清理
```python
# VS Code 缓存目录完全清理
cache_directories = ["Cache", "CachedData", "GPUCache"]
for cache_dir in cache_directories:
    shutil.rmtree(cache_path)
```

## 🔬 技术实现细节

### 核心算法

#### 1. 跨平台路径解析
```python
def get_vscode_paths(self):
    if self.system == "Windows":
        base_path = Path(os.environ["APPDATA"]) / "Code" / "User"
    elif self.system == "Darwin":  # macOS
        base_path = Path.home() / "Library" / "Application Support" / "Code" / "User"
    else:  # Linux
        base_path = Path.home() / ".config" / "Code" / "User"
```

#### 2. 安全随机数生成
```python
# 使用 secrets 模块确保加密级安全性
new_machine_id = secrets.token_hex(32)  # 比 random 更安全
new_device_id = str(uuid.uuid4())       # 标准 UUID v4
```

#### 3. 递归清理算法
```python
# 两层清理确保彻底性
for item in path.rglob("*augment*"):     # 递归搜索
    # 处理匹配项
for item in path.iterdir():              # 顶级目录再次检查
    if "augment" in item.name.lower():
        # 处理遗漏项
```

### 错误处理机制

#### 分层异常处理
```python
try:
    # 主要操作
except PermissionError:
    self.log("权限不足，请以管理员身份运行", "ERROR")
except FileNotFoundError:
    self.log("目标文件不存在，跳过", "WARNING")
except Exception as e:
    self.log(f"未知错误: {e}", "ERROR")
```

#### 操作状态跟踪
```python
items_deleted_count = 0
# 每次成功删除后计数
items_deleted_count += 1
# 最终报告删除统计
```

## 🔍 验证与测试

### 清理效果验证步骤

1. **进程验证**
   ```bash
   # Windows
   tasklist | findstr Code.exe

   # macOS/Linux
   ps aux | grep "Visual Studio Code"
   ```

2. **数据库验证**
   ```sql
   SELECT key FROM ItemTable WHERE key LIKE '%augment%';
   -- 应该返回空结果
   ```

3. **文件系统验证**
   ```bash
   # 检查全局存储目录
   find globalStorage -name "*augment*" -type f

   # 检查临时目录
   find /tmp -name "*augment*" 2>/dev/null
   ```

4. **设备标识符验证**
   ```bash
   # 检查新生成的设备ID
   grep -E "(machineId|devDeviceId)" storage.json
   ```

### 功能测试流程

1. **重启 VS Code**
2. **重新安装 Augment 扩展**
3. **检查是否被识别为新设备**
4. **验证免费额度是否重置**
5. **确认 VS Code 其他功能正常**

## ⚠️ 安全注意事项

### 操作前检查清单
- [ ] 完全关闭 VS Code（包括后台进程）
- [ ] 备份重要的 VS Code 配置（可选）
- [ ] 确认当前用户有足够的文件操作权限
- [ ] 在测试环境先验证效果

### 数据安全保障
- **精确定位**：只删除包含 `augment` 的特定数据
- **范围限制**：不影响 VS Code 核心设置和其他扩展
- **本地操作**：所有操作在本地执行，无网络传输
- **可逆性**：虽然清理不可逆，但不影响系统稳定性

---

**版本**: v2.0 - 彻底清理版
**设计原则**: 除非必要勿增实体
**技术栈**: Python 3 + 标准库
**兼容性**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
