#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复markdown文档图片引用 - 最终版"""

from pathlib import Path
import os

def build_correct_mapping():
    """构建正确的路径映射"""
    backup_path = Path('Images_backup_final')
    images_path = Path('Images')
    
    if not backup_path.exists():
        print("❌ 备份目录不存在")
        return {}
    
    mapping = {}
    
    # 从备份读取原始文件名
    for orig_file in backup_path.iterdir():
        if not orig_file.is_file():
            continue
        
        if orig_file.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']:
            continue
        
        orig_name = orig_file.name
        
        # 解析原始文件名，找到新位置
        # 原始：段1-段2-段3-剩余.扩展名
        # 新的：段1/段2/段3/剩余.扩展名
        
        ext = orig_file.suffix
        name_no_ext = orig_name[:-len(ext)]
        parts = name_no_ext.split('-')
        
        if len(parts) >= 3:
            level1 = parts[0]
            level2 = parts[1]
            level3 = parts[2]
            remaining = '-'.join(parts[3:]) if len(parts) > 3 else 'image'
            
            # 构建新路径
            new_path = f"{level1}/{level2}/{level3}/{remaining}{ext}"
            
            # 检查新文件是否存在
            new_file = images_path / level1 / level2 / level3 / f"{remaining}{ext}"
            
            if new_file.exists():
                mapping[orig_name] = new_path
            else:
                # 可能文件名有差异，尝试在该目录下查找
                new_dir = images_path / level1 / level2 / level3
                if new_dir.exists():
                    files = list(new_dir.iterdir())
                    if len(files) == 1:  # 如果目录里只有一个文件，就用它
                        actual_file = files[0].relative_to(images_path)
                        mapping[orig_name] = str(actual_file)
    
    return mapping

def update_docs(docs_root='产品组'):
    """更新文档"""
    print("📊 构建映射...")
    mapping = build_correct_mapping()
    print(f"   映射数量: {len(mapping)}")
    
    if len(mapping) == 0:
        print("⚠️  没有映射，无法更新")
        return
    
    # 显示前3个映射
    print("\n映射示例:")
    for i, (old, new) in enumerate(list(mapping.items())[:3]):
        print(f"  {old}")
        print(f"  → {new}\n")
    
    # 更新markdown
    docs_path = Path(docs_root)
    md_files = list(docs_path.rglob('*.md'))
    
    print(f"📝 更新 {len(md_files)} 个文档...")
    
    updated = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            for old_name, new_path in mapping.items():
                # 替换各种层级的相对路径
                for level in range(1, 6):
                    old_ref = '../' * level + f'Images/{old_name}'
                    new_ref = '../' * level + f'Images/{new_path}'
                    
                    if old_ref in content:
                        content = content.replace(old_ref, new_ref)
            
            if content != original:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
        
        except Exception as e:
            print(f"❌ {md_file}: {e}")
    
    print(f"\n✅ 成功更新 {updated} 个文档！")

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 修复Markdown图片引用 - 最终版")
    print("=" * 70)
    update_docs()
    print("=" * 70)
