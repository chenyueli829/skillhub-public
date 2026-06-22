# iwiki-knowledge-organizer 辅助脚本

本目录包含用于Images目录重组和维护的辅助脚本。

## 📁 脚本说明

### 1. convert_to_hierarchical.py ⭐ **推荐使用**

**用途**: 将Images扁平结构转换为层级结构

**功能**:
- 自动解析图片文件名
- 按照{空间名}/{文件夹名}/{文档名}创建目录
- 移动图片到对应位置
- 更新markdown文档引用
- 自动创建备份

**使用**:
```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/convert_to_hierarchical.py
```

**输出**:
- 重组后的Images目录
- 备份: `Images_backup_hierarchical/`
- 更新的markdown文档

---

### 2. update_md_refs.py

**用途**: 单独更新markdown引用

**功能**: 构建路径映射并更新所有markdown文档中的图片引用

**使用场景**: 当已经手动重组Images目录，只需要更新引用时使用

**使用**:
```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/update_md_refs.py
```

---

### 3. fix_md_refs_final.py

**用途**: 最终版引用修复脚本

**功能**: 从备份读取原始文件名，构建准确的路径映射，更新markdown引用

**使用场景**: 当convert_to_hierarchical.py未能正确更新引用时使用

**使用**:
```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/fix_md_refs_final.py
```

**注意**: 需要存在 `Images_backup_final/` 备份目录

---

## 🚀 快速开始

### 场景1: 首次转换Images为层级结构

```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/convert_to_hierarchical.py
```

这个脚本会：
1. 自动备份当前Images目录
2. 将图片重组为层级结构
3. 尝试更新markdown引用
4. 生成详细报告

### 场景2: 只需要更新markdown引用

```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/update_md_refs.py
```

### 场景3: 修复引用失败的情况

```bash
cd /Users/chenyueli/Desktop/work
python3 .cursor/skills/iwiki-knowledge-organizer/scripts/fix_md_refs_final.py
```

---

## 📊 目录结构对比

### 转换前（扁平结构）

```
Images/
├── FiT各主体资金流编排（财务）-【对外】ZX-资金流编排-ZX-一期-image.png
├── FiT各主体资金流编排（财务）-【对外】ZX-资金流编排-ZX-二期-diagram.svg
└── ...
```

### 转换后（层级结构）

```
Images/
└── FiT各主体资金流编排（财务）/
    └── 【对外】ZX/
        └── 资金流编排/
            ├── ZX-一期-image.png
            ├── ZX-二期-diagram.svg
            └── ...
```

---

## ⚠️ 注意事项

1. **备份**: 所有脚本都会自动创建备份，但建议手动再备份一次重要数据
2. **路径**: 脚本假设工作目录为 `/Users/chenyueli/Desktop/work`
3. **依赖**: 只需要Python 3标准库，无需额外安装包
4. **权限**: 确保有读写Images和产品组目录的权限

---

## 🔧 故障排除

### 问题1: 脚本执行后markdown图片不显示

**原因**: 文档中引用的图片名与实际文件名不匹配

**解决**: 使用 `fix_md_refs_final.py` 或手动检查修复

### 问题2: 部分图片未被移动

**原因**: 文件名格式不符合 `段1-段2-段3-...` 的规则

**解决**: 这些文件会保留在Images根目录，可以手动移动

### 问题3: 想要恢复到原始状态

**解决**: 
```bash
cd /Users/chenyueli/Desktop/work
rm -rf Images
mv Images_backup_hierarchical Images
```

---

## 📝 版本历史

- `convert_to_hierarchical.py` - 层级重组（推荐）
- `update_md_refs.py` - 仅更新引用
- `fix_md_refs_final.py` - 引用修复（依赖备份）

---

## 🔗 相关文档

- [../SKILL.md](../SKILL.md) - iwiki-knowledge-organizer skill主文档
- [/Images重组总结报告.md](../../../../Images重组总结报告.md) - 重组操作总结

---

**最后更新**: 2026-02-14
