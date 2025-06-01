# Augment设备指纹清除技术文档

## 📋 技术原理

Augment通过以下方式识别设备：

1. **存储位置**
   - VS Code SQLite数据库：`state.vscdb`
   - 设备标识符文件：`storage.json`
   - 扩展全局存储：`globalStorage/augment.*`
   - 系统临时缓存：临时目录中的augment文件

2. **关键标识符**
   - `telemetry.machineId`: 64位十六进制字符串
   - `devDeviceId`: UUID格式字符串

## 🔧 清理策略

### 核心文件位置

#### Windows
```
%APPDATA%\Code\User\storage.json
%APPDATA%\Code\User\globalStorage\state.vscdb
%APPDATA%\Code\User\globalStorage\augment.*\
%TEMP%\augment*
```

#### macOS
```
~/Library/Application Support/Code/User/storage.json
~/Library/Application Support/Code/User/globalStorage/state.vscdb
~/Library/Application Support/Code/User/globalStorage/augment.*/
/tmp/augment*
```

#### Linux
```
~/.config/Code/User/storage.json
~/.config/Code/User/globalStorage/state.vscdb
~/.config/Code/User/globalStorage/augment.*/
/tmp/augment*
```

### 清理步骤

1. **停止VS Code进程**
2. **清理数据库**: `DELETE FROM ItemTable WHERE key LIKE '%augment%'`
3. **更新设备ID**: 生成新的machineId和devDeviceId
4. **清理全局存储**: 删除augment相关目录
5. **清理临时文件**: 删除临时目录中的augment文件

## 🔍 验证效果

清理完成后：
1. 重启VS Code
2. 重新登录Augment
3. 检查是否被识别为新设备
4. 验证免费额度是否重置

## ⚠️ 注意事项

- 操作前完全关闭VS Code
- 只清除Augment相关数据，保留VS Code设置
- 建议先在测试环境验证

---

**版本**: v3.0 - 精简版
**设计原则**: 除非必要勿增实体
