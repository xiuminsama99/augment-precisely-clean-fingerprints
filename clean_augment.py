#!/usr/bin/env python3
"""
Augment 设备指纹清理工具
遵循"除非必要勿增实体"原则
"""

import os
import sys
import json
import sqlite3
import platform
import subprocess
import tempfile
import shutil
import uuid
import secrets
from pathlib import Path

class AugmentCleaner:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.system = platform.system()
        
    def log(self, message: str, level: str = "INFO"):
        """简单日志输出"""
        if self.verbose or level in ["ERROR", "SUCCESS"]:
            prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
            print(f"{prefix.get(level, 'ℹ️')} {message}")
    
    def get_vscode_paths(self):
        """获取 VS Code 相关路径"""
        paths = {}
        
        if self.system == "Windows":
            appdata = Path(os.environ["APPDATA"])
            base_path = appdata / "Code" / "User"
        elif self.system == "Darwin":  # macOS
            home = Path.home()
            base_path = home / "Library" / "Application Support" / "Code" / "User"
        else:  # Linux
            home = Path.home()
            base_path = home / ".config" / "Code" / "User"
        
        paths["storage_json"] = base_path / "storage.json"
        paths["state_db"] = base_path / "globalStorage" / "state.vscdb"
        paths["global_storage"] = base_path / "globalStorage"
        paths["temp_dir"] = Path(tempfile.gettempdir())
        
        return paths
    
    def stop_vscode(self):
        """停止 VS Code 进程"""
        self.log("停止 VS Code 进程...")
        
        try:
            if self.system == "Windows":
                subprocess.run(["taskkill", "/F", "/IM", "Code.exe"], 
                             capture_output=True, check=False)
            else:
                subprocess.run(["pkill", "-f", "Visual Studio Code"], 
                             capture_output=True, check=False)
            
            self.log("VS Code 进程已停止", "SUCCESS")
        except Exception as e:
            self.log(f"停止进程时出错: {e}", "WARNING")
    
    def clean_database(self, db_path: Path):
        """清理 SQLite 数据库"""
        if not db_path.exists():
            self.log(f"数据库文件不存在: {db_path}", "WARNING")
            return
        
        self.log(f"清理数据库: {db_path}")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 删除所有包含 augment 的键
            cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%augment%'")
            conn.commit()
            conn.close()
            
            self.log("数据库清理完成", "SUCCESS")
        except Exception as e:
            self.log(f"数据库清理失败: {e}", "ERROR")
    
    def clean_storage_json(self, json_path: Path):
        """清理存储 JSON 文件"""
        if not json_path.exists():
            self.log(f"存储文件不存在: {json_path}", "WARNING")
            return
        
        self.log(f"清理存储文件: {json_path}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 生成新的设备标识符
            new_machine_id = secrets.token_hex(32)  # 64位十六进制
            new_device_id = str(uuid.uuid4())
            
            # 更新设备ID
            if "telemetry.machineId" in data:
                data["telemetry.machineId"] = new_machine_id
            if "devDeviceId" in data:
                data["devDeviceId"] = new_device_id
            
            # 移除所有 augment 相关的键
            keys_to_remove = [key for key in data.keys() if "augment" in key.lower()]
            for key in keys_to_remove:
                del data[key]
            
            # 写回文件
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.log("存储文件清理完成", "SUCCESS")
        except Exception as e:
            self.log(f"存储文件清理失败: {e}", "ERROR")
    
    def clean_augment_files(self, path: Path, name: str):
        """清理包含augment的文件和目录"""
        if not path.exists():
            self.log(f"{name}不存在: {path}", "WARNING")
            return

        self.log(f"清理{name}...")

        try:
            if path.is_dir():
                # 清理目录中的augment相关项
                for item in path.iterdir():
                    if "augment" in item.name.lower():
                        self.log(f"删除: {item}")
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                # 清理临时目录的glob模式
                for item in path.glob("*augment*"):
                    self.log(f"删除: {item}")
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)

            self.log(f"{name}清理完成", "SUCCESS")
        except Exception as e:
            self.log(f"{name}清理失败: {e}", "ERROR")
    
    def clean(self, force: bool = False):
        """执行完整清理流程"""
        self.log("开始 Augment 设备指纹清理")
        self.log("遵循原则: 除非必要勿增实体")
        
        if not force:
            confirm = input("确认开始清理？这将删除所有 Augment 相关数据 (y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                self.log("用户取消操作", "WARNING")
                return False
        
        # 获取路径
        paths = self.get_vscode_paths()
        
        # 执行清理步骤
        self.stop_vscode()
        self.clean_database(paths["state_db"])
        self.clean_storage_json(paths["storage_json"])
        self.clean_augment_files(paths["global_storage"], "全局存储")
        self.clean_augment_files(paths["temp_dir"], "临时文件")
        
        self.log("清理完成！请重启 VS Code 并重新登录 Augment", "SUCCESS")
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Augment 设备指纹清理工具")
    parser.add_argument("-f", "--force", action="store_true", help="强制清理，不询问确认")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    cleaner = AugmentCleaner(verbose=args.verbose)
    success = cleaner.clean(force=args.force)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
