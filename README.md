# Augment 设备指纹清理工具

> 遵循"除非必要勿增实体"原则设计的彻底清理工具

## 🎯 功能特点

- **彻底清理**: 递归清除所有 Augment 设备指纹和缓存
- **跨平台支持**: Windows、macOS、Linux 全平台兼容
- **安全可靠**: 只清理 Augment 相关数据，保留 VS Code 设置
- **零依赖设计**: 单文件应用，仅使用 Python 标准库
- **智能日志**: 详细的操作反馈和错误处理

## 📁 文件说明

```
├── clean_augment.py                    # 跨平台清理脚本（核心工具）
├── README.md                          # 项目说明（当前文件）
├── 使用说明.md                         # 简单易懂的使用教程（推荐先看这个）
└── Augment设备指纹清除技术文档.md        # 详细技术实现文档
```

> 💡 **新手建议**：如果你不是程序员，建议先看 `使用说明.md`，里面用大白话解释了怎么用。

## 🚀 使用方法

```bash
# 交互式清理（推荐）
python3 clean_augment.py

# 详细输出模式
python3 clean_augment.py -v

# 强制清理（无确认提示）
python3 clean_augment.py -f

# 组合使用
python3 clean_augment.py -vf
```

## 🔧 清理范围

工具会彻底清理以下 Augment 相关数据：

### 数据库清理
- `state.vscdb` 中所有包含 `augment` 的记录
- 使用 SQL 精确删除：`DELETE FROM ItemTable WHERE key LIKE '%augment%'`

### 文件系统清理
- `storage.json` 中的 Augment 相关键值对
- `globalStorage` 目录中所有 `augment` 相关文件和目录（递归）
- 系统临时目录中的 Augment 缓存文件（递归）

### VS Code 缓存清理
- `Cache` 目录 - 通用缓存
- `CachedData` 目录 - 扩展缓存数据
- `GPUCache` 目录 - GPU 渲染缓存

### 设备标识符重新生成
- `telemetry.machineId`: 使用 `secrets.token_hex(32)` 生成新的 64 位十六进制 ID
- `devDeviceId`: 使用 `uuid.uuid4()` 生成新的标准 UUID

## ⚠️ 使用注意

1. **清理前必须完全关闭 VS Code**（工具会自动尝试停止进程）
2. 清理过程不可逆，请确认后操作
3. 清理完成后需重新登录 Augment
4. 建议在测试环境先验证效果
5. 清理过程中如遇权限问题，请以管理员身份运行

## 🎨 设计原则

本工具严格遵循"除非必要勿增实体"原则：

- **零外部依赖**: 仅使用 Python 3 标准库
- **单一职责**: 专注于彻底清理 Augment 指纹
- **跨平台兼容**: 一套代码支持三大操作系统
- **安全优先**: 精确定位，避免误删其他数据
- **用户友好**: 详细日志输出和操作确认

## 🔍 验证效果

清理完成后验证步骤：

1. 重启 VS Code
2. 重新安装/登录 Augment 扩展
3. 检查是否被识别为新设备
4. 确认免费额度是否重置
5. 验证 VS Code 其他功能正常

## 📝 技术实现

### 核心技术栈
- **Python 3** - 跨平台脚本语言
- **SQLite3** - VS Code 数据库操作
- **pathlib** - 现代化路径处理
- **subprocess** - 进程管理（停止 VS Code）
- **secrets** - 加密级随机数生成
- **uuid** - 标准 UUID 生成

### 关键算法
- **递归搜索**: 使用 `rglob("*augment*")` 深度清理
- **SQL 精确删除**: `LIKE '%augment%'` 模式匹配
- **安全随机**: `secrets.token_hex(32)` 生成新设备 ID
- **跨平台路径**: 自动适配不同操作系统的 VS Code 路径

## 🛡️ 安全保障

- **精确定位**: 只删除包含 `augment` 的文件和记录
- **数据隔离**: 不影响 VS Code 其他扩展和设置
- **本地操作**: 所有操作在本地执行，无网络传输
- **错误处理**: 完善的异常捕获和用户反馈
- **操作确认**: 默认需要用户确认才执行清理

## 🚀 更新日志

### v2.0 - 彻底清理版
- ✅ 新增递归清理算法，彻底清除所有 Augment 痕迹
- ✅ 新增 VS Code 缓存目录清理（Cache/CachedData/GPUCache）
- ✅ 改进设备 ID 生成，使用加密级随机数
- ✅ 优化日志系统，支持详细输出模式
- ✅ 增强错误处理和用户反馈
- ✅ 完善跨平台兼容性

### v1.0 - 基础版本
- ✅ 基本的数据库和文件清理功能
- ✅ 跨平台支持

---

**当前版本**: v2.0 - 彻底清理版
**设计原则**: 除非必要勿增实体
**兼容性**: VS Code + Augment 扩展
**技术栈**: Python 3 + 标准库

## 💝 支持项目

如果这个工具对您有帮助，欢迎支持：

<img src="https://github.com/user-attachments/assets/0175c0f7-4929-4132-bb1a-24149429e699" width="300" alt="支付宝赞赏码">
<img src="https://github.com/user-attachments/assets/dc1c65a4-c221-4811-8f2e-d65dda5cc8f5" width="300" alt="微信赞赏码">

**感谢您的支持！** 🙏
