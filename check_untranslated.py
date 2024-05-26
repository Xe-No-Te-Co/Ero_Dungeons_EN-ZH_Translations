import polib

# 读取原始 po 文件
path0 = './Translations/zh_HANS.po'
path1 = './Translations/zh_HANS.untrans.po'

po = polib.pofile(path0,wrapwidth=9999)
po.wrapwidth = 9999
# 创建一个新的 po 文件对象
# untranslated_po = polib.POFile(wrapwidth=0)

# 过滤出 msgstr 与 msgid 相同的条目
for entry in po:
    if entry.msgstr == entry.msgid:  # 检查 msgstr 是否与 msgid 相同
        entry.msgstr = ""
        # untranslated_po.append(entry)

po.save(path0)

# 保存新的 po 文件
# untranslated_po.save(path1)

# print(f"找到 {len(untranslated_po)} 个未翻译的条目，并已导出到 {path1}")