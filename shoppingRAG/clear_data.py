#!/usr/bin/env python3
"""
RAG系统数据清除脚本
用于完全清除知识库、上传记录和重置向量索引
"""

import os
import json
import shutil

def clear_all_data():
    """清除所有RAG系统数据"""
    
    # 1. 清除知识库文件
    kb_path = "rag/data/knowledge_base.json"
    if os.path.exists(kb_path):
        # 清空知识库内容，保留文件结构
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"✓ 已清空知识库: {kb_path}")
    else:
        print(f"⚠ 知识库文件不存在: {kb_path}")
    
    # 2. 清除上传日志
    log_path = "rag/upload_log.json"
    if os.path.exists(log_path):
        # 清空上传记录
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"✓ 已清空上传记录: {log_path}")
    else:
        print(f"⚠ 上传日志文件不存在: {log_path}")
    
    # 3. 删除整个data目录（可选）
    data_dir = "rag/data"
    if os.path.exists(data_dir):
        try:
            shutil.rmtree(data_dir)
            os.makedirs(data_dir)  # 重新创建空目录
            print(f"✓ 已删除并重建data目录: {data_dir}")
        except Exception as e:
            print(f"✗ 删除data目录失败: {e}")
    
    print("\n🎉 数据清除完成！")
    print("💡 提示：重启后端服务以重置内存中的向量索引")

def clear_knowledge_base_only():
    """仅清除知识库内容，保留上传记录"""
    
    kb_path = "rag/data/knowledge_base.json"
    if os.path.exists(kb_path):
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"✓ 已清空知识库: {kb_path}")
    else:
        print(f"⚠ 知识库文件不存在: {kb_path}")
    
    print("\n🎉 知识库清除完成！")
    print("💡 提示：重启后端服务以重置内存中的向量索引")

def clear_upload_log_only():
    """仅清除上传记录，保留知识库"""
    
    log_path = "rag/upload_log.json"
    if os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        print(f"✓ 已清空上传记录: {log_path}")
    else:
        print(f"⚠ 上传日志文件不存在: {log_path}")

if __name__ == "__main__":
    print("🧹 RAG系统数据清除工具")
    print("=" * 40)
    print("1. 清除所有数据（知识库 + 上传记录）")
    print("2. 仅清除知识库内容")
    print("3. 仅清除上传记录")
    print("4. 退出")
    
    choice = input("\n请选择操作 (1-4): ").strip()
    
    if choice == "1":
        clear_all_data()
    elif choice == "2":
        clear_knowledge_base_only()
    elif choice == "3":
        clear_upload_log_only()
    elif choice == "4":
        print("退出程序")
    else:
        print("无效选择，退出程序") 