#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Images扁平结构转换为层级结构
同时更新所有markdown文档引用
"""

from pathlib import Path
import shutil
import re

def parse_and_reorganize():
    """解析并重组Images目录"""
    
    images_path = Path('Images')
    backup_path = Path('Images_backup_hierarchical')
    
    # 备份
    if backup_path.exists():
        shutil.rmtree(backup_path)
    print("📦 创建备份...")
    shutil.copytree(images_path, backup_path)
    
    # 收集所有图片
    image_files = []
    for f in images_path.iterdir():
        if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp']:
            image_files.append(f.name)
    
    print(f"📊 找到 {len(image_files)} 个图片\n")
    
    # 路径映射
    mapping = {}
    moved = 0
    failed = []
    
    for filename in image_files:
        # 解析文件名：段1-段2-段3-剩余部分.扩展名
        ext = Path(filename).suffix
        name = filename[:-len(ext)]
        parts = name.split('-')
        
        if len(parts) < 3:
            failed.append(filename)
            continue
        
        # 提取层级信息
        level1 = parts[0]  # 空间名
        level2 = parts[1]  # 文件夹或"首页"
        level3 = parts[2]  # 子文件夹或文档名
        
        # 剩余部分作为图片名
        if len(parts) > 3:
            img_name = '-'.join(parts[3:])
        else:
            img_name = 'image'
        
        # 创建新目录
        new_dir = images_path / level1 / level2 / level3
        new_dir.mkdir(parents=True, exist_ok=True)
        
        # 移动文件
        src = images_path / filename
        dst = new_dir / f"{img_name}{ext}"
        
        try:
            # 如果目标文件已存在，添加数字后缀
            counter = 1
            final_dst = dst
            while final_dst.exists():
                final_dst = new_dir / f"{img_name}-{counter}{ext}"
                counter += 1
            
            shutil.move(str(src), str(final_dst))
            
            # 记录映射
            new_rel_path = str(final_dst.relative_to(images_path))
            mapping[filename] = new_rel_path
            
            moved += 1
            if moved % 30 == 0:
                print(f"  已处理 {moved}/{len(image_files)}")
        
        except Exception as e:
            print(f"❌ 移动失败: {filename} - {e}")
            failed.append(filename)
    
    print(f"\n✅ 重组完成：")
    print(f"   成功: {moved} 个")
    print(f"   失败: {len(failed)} 个")
    
    return mapping

def update_all_markdown(mapping):
    """更新所有markdown文档的图片引用"""
    
    print(f"\n📝 更新Markdown文档...")
    
    docs_path = Path('产品组')
    md_files = list(docs_path.rglob('*.md'))
    
    updated_files = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # 对每个图片进行替换
            for old_name, new_path in mapping.items():
                # 查找所有可能的引用形式
                for level in range(1, 6):
                    prefix = '../' * level
                    old_ref = f'{prefix}Images/{old_name}'
                    new_ref = f'{prefix}Images/{new_path}'
                    
                    content = content.replace(old_ref, new_ref)
            
            # 写回
            if content != original:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_files.append(md_file)
        
        except Exception as e:
            print(f"❌ {md_file}: {e}")
    
    print(f"✅ 更新了 {len(updated_files)} 个文档")
    
    if updated_files and len(updated_files) <= 20:
        print("\n更新的文档:")
        for f in updated_files:
            print(f"  ✓ {f.relative_to(docs_path)}")

def show_new_structure():
    """显示新的目录结构"""
    print("\n" + "=" * 70)
    print("📁 新的Images目录结构:")
    print("=" * 70)
    
    images = Path('Images')
    
    def show_tree(path, prefix='', max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(path.iterdir())
            dirs = [i for i in items if i.is_dir()]
            files = [i for i in items if i.is_file()]
            
            # 显示目录
            for i, d in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                connector = '└── ' if is_last_dir else '├── '
                print(f"{prefix}{connector}{d.name}/")
                
                new_prefix = prefix + ('    ' if is_last_dir else '│   ')
                show_tree(d, new_prefix, max_depth, current_depth + 1)
            
            # 显示部分文件（只在最后一层）
            if current_depth == max_depth - 1 and files:
                for j, f in enumerate(files[:3]):
                    is_last = j == min(len(files) - 1, 2)
                    connector = '└── ' if is_last else '├── '
                    print(f"{prefix}{connector}{f.name}")
                
                if len(files) > 3:
                    print(f"{prefix}    ... ({len(files)} 个文件)")
        
        except Exception as e:
            print(f"{prefix}[Error: {e}]")
    
    print(f"\n{images.name}/")
    show_tree(images, max_depth=4)

def main():
    print("=" * 70)
    print("🔄 Images目录结构转换：扁平 → 层级")
    print("=" * 70)
    
    print("\n⚠️  本操作将：")
    print("  1. 备份当前Images目录到 Images_backup_hierarchical")
    print("  2. 将图片按层级重组到子目录")
    print("  3. 更新所有markdown文档的图片引用")
    print()
    
    # 1. 重组Images
    mapping = parse_and_reorganize()
    
    if not mapping:
        print("⚠️  没有图片需要处理")
        return
    
    # 2. 更新markdown
    update_all_markdown(mapping)
    
    # 3. 显示结果
    show_new_structure()
    
    print("\n" + "=" * 70)
    print("✅ 转换完成！")
    print("=" * 70)
    print(f"\n💡 提示:")
    print(f"   - 原始文件备份在: Images_backup_hierarchical/")
    print(f"   - 如需还原，运行: mv Images_backup_hierarchical Images")

if __name__ == '__main__':
    main()
