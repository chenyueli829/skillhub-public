#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新markdown文档中的图片引用"""

import re
from pathlib import Path

def build_path_mapping():
    """构建路径映射表"""
    images_path = Path('Images')
    mapping = {}
    
    # 遍历新的目录结构
    for img_file in images_path.rglob('*'):
        if not img_file.is_file():
            continue
        
        if not img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']:
            continue
        
        # 获取相对于Images的新路径
        new_rel_path = img_file.relative_to(images_path)
        
        # 构建旧的文件名（平铺格式）
        # 新路径如: FiT各主体资金流编排（财务）/【对外】ZX/资金流编排/ZX-一期-image.png
        # 旧路径应该是: FiT各主体资金流编排（财务）-【对外】ZX-资金流编排-ZX-一期-image.png
        parts = list(new_rel_path.parts)
        
        if len(parts) >= 2:
            # 前几部分用-连接，最后一部分是文件名
            old_name = '-'.join(parts[:-1]) + '-' + parts[-1]
            
            mapping[old_name] = str(new_rel_path)
    
    return mapping

def update_markdown_files(docs_root='产品组'):
    """更新markdown文档"""
    docs_path = Path(docs_root)
    
    # 构建映射
    print("📊 构建路径映射...")
    mapping = build_path_mapping()
    print(f"   找到 {len(mapping)} 个图片路径映射")
    
    if len(mapping) > 0:
        print("\n映射示例（前3个）:")
        for i, (old, new) in enumerate(list(mapping.items())[:3]):
            print(f"  {old}")
            print(f"  → {new}")
            print()
    
    # 查找所有markdown文件
    md_files = list(docs_path.rglob('*.md'))
    print(f"\n📝 找到 {len(md_files)} 个Markdown文件")
    
    updated_count = 0
    update_details = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_updated = False
            
            # 对每个映射进行替换
            for old_path, new_path in mapping.items():
                # 匹配各种相对路径层级
                for level in range(1, 6):
                    prefix = '../' * level
                    old_ref = f'{prefix}Images/{old_path}'
                    new_ref = f'{prefix}Images/{new_path}'
                    
                    if old_ref in content:
                        content = content.replace(old_ref, new_ref)
                        file_updated = True
            
            # 如果有更新，写回文件
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
                update_details.append(md_file.relative_to(docs_root))
        
        except Exception as e:
            print(f"❌ 更新失败: {md_file} - {e}")
    
    print(f"\n✅ 更新了 {updated_count} 个文档")
    
    if update_details and updated_count <= 15:
        print("\n更新的文档:")
        for f in update_details:
            print(f"  ✓ {f}")

if __name__ == '__main__':
    print("=" * 70)
    print("🔄 更新Markdown文档图片引用")
    print("=" * 70)
    update_markdown_files()
    print("\n" + "=" * 70)
    print("✅ 完成！")
    print("=" * 70)
