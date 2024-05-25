import polib
from zhconv import convert

# 读取 PO 文件
po0_path = './Translations/zh_TW.po'
po1_path = './Translations/zh_TW2CN.po'
# zh-cn 大陆简体
# zh-tw 台灣正體
# zh-hk 香港繁體
# zh-sg 马新简体
# zh-hans 简体
# zh-hant 繁體
target_lang = 'zh-cn'


def simple_convert(po0_path, po1_path):
    with open(po0_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(po1_path, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if line.startswith('msgstr'):
                # 提取 msgstr 的内容并转换
                original_msgstr = line.split('"', 1)[1].rsplit('"', 1)[0]
                converted_msgstr = convert(original_msgstr, 'zh-hans')
                # 重新构造 msgstr 行
                line = f'msgstr "{converted_msgstr}"\n'
            outfile.write(line)

    print("转换完成并保存到新的 PO 文件。")

def polib_convert(po0_path, po1_path):
    po = polib.pofile(po0_path)

    # 遍历每一个 entry 并转换 msgstr
    for entry in po:
        if entry.msgstr:
            entry.msgstr = convert(entry.msgstr, 'zh-hans')

    # 保存修改后的 PO 文件
    po.save(po1_path)

    print("转换完成并保存到新的 PO 文件。")

polib_convert(po0_path, po1_path)