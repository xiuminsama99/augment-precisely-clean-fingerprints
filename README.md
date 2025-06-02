# Augment 设备指纹清理工具

> 遵循"除非必要勿增实体"原则设计的简洁清理工具

## 🎯 功能特点

- **一键清理**: 清除所有 Augment 设备指纹
- **跨平台支持**: Windows、macOS、Linux 全平台兼容
- **安全可靠**: 只清理 Augment 相关数据，保留 VS Code 设置
- **最小化设计**: 单文件应用，无额外依赖

## 📁 文件说明

```
├── clean_augment.py        # 跨平台清理脚本（唯一工具）
├── README.md              # 使用说明
└── Augment设备指纹清除技术文档.md  # 技术文档
```

## 🚀 使用方法

```bash
# 运行清理工具
python3 clean_augment.py

# 详细输出模式
python3 clean_augment.py -v

# 强制清理（无确认提示）
python3 clean_augment.py -f
```

## 🔧 清理内容

工具会清理以下 Augment 相关数据：

### 数据库清理
- `state.vscdb` 中的 Augment 相关记录
- 设备标识符重新生成

### 文件清理
- `storage.json` 中的设备 ID
- `globalStorage/augment.*` 目录
- 临时目录中的 Augment 文件

### 标识符更新
- `telemetry.machineId`: 生成新的 64 位十六进制 ID
- `devDeviceId`: 生成新的 UUID

## ⚠️ 使用注意

1. **清理前必须完全关闭 VS Code**
2. 清理过程不可逆，请确认后操作
3. 清理完成后需重新登录 Augment
4. 建议在测试环境先验证效果

## 🎨 设计原则

本工具严格遵循"除非必要勿增实体"原则：

- **最小化依赖**: 只使用必要的系统工具
- **单一职责**: 专注于指纹清理功能
- **简洁实现**: 命令行工具，无多余界面
- **高效执行**: 直接操作目标文件，无冗余步骤

## 🔍 验证效果

清理完成后验证步骤：

1. 重启 VS Code
2. 重新安装/登录 Augment 扩展
3. 检查是否被识别为新设备
4. 确认免费额度是否重置

## 📝 技术实现

- **语言**: Python 3 (跨平台)
- **数据库**: SQLite3 操作
- **文件操作**: 系统原生 API

## 🛡️ 安全说明

- 只删除 Augment 相关数据
- 不影响 VS Code 其他设置
- 不收集或上传任何用户数据
- 所有操作在本地执行

---

**版本**: v1.0  
**设计原则**: 除非必要勿增实体  
**兼容性**: VS Code + Augment 扩展
支持项目
如果您觉得这个项目对您有帮助，可以请我喝杯奶茶或者吃个小饼干：![image](https://github.com/user-attachments/assets/64b380a2-b4e7-4c0b-ac4e-43bf17ab1963)![image](https://github.com/user-attachments/assets/7f3c9578-7607-4614-83ab-8c1f4358498d)

