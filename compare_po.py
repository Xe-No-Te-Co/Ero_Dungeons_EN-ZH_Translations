import polib
import re

def replace_quotes(s):
	# 找到第一个和最后一个双引号的位置
	first_quote = s.find('"')
	last_quote = s.rfind('"')

	# 如果字符串中没有双引号，或者只有一个双引号，返回原字符串
	if first_quote == -1 or last_quote == -1 or first_quote == last_quote:
		return s

	# 分割字符串成三部分：第一个双引号前，双引号之间，最后一个双引号后
	before_first = s[:first_quote+1]
	middle = s[first_quote+1:last_quote]
	after_last = s[last_quote:]
	
	# 替换中间部分的所有双引号为'\"'
	middle_replaced = middle.replace('"', '\\"')
	
	# 重新组合字符串
	result = before_first + middle_replaced + after_last
	return result

def fix_po(po_path):
	with open(po_path, 'r', encoding='utf8') as f:
		lines = f.readlines()
		new_lines = []
	for line in lines:
		new_line = replace_quotes(line)
		new_lines.append(new_line)
	with open(po_path, 'w', encoding='utf8') as f:
		f.writelines(new_lines)

def compare_po_files(po0_path, po1_path):
	# 读取两个 po 文件
	po0 = polib.pofile(po0_path)
	po1 = polib.pofile(po1_path)

	# 创建字典用于快速查找 po 中的条目
	po0_dict = {entry.tcomment: entry for entry in po0 if entry.tcomment}
	po1_dict = {entry.tcomment: entry for entry in po1 if entry.tcomment}
	# 有三种情况，po0和po1都有，po0有但po1没有，po1有但po0没有

	# 遍历 po0 中的条目，根据 tcomment 替换 msgstr
	for entry in po0:
		if entry.tcomment not in po1_dict:
			print(f'[Entry key]{entry.tcomment} \n[Entry text]{entry.msgid} not in po1')

	for entry in po1:
		if entry.tcomment not in po0_dict:
			# po1有但po0没有
			print(f'[Entry key]{entry.tcomment} \n[Entry text]{entry.msgid} not in po0')


# 示例用法
path = { 
	"base": 'Translations/base.po',
	'zh_hans': 'Translations/zh_HANS.po',
	'de': 'Translations/de.po',
	'zh_hans_merged': 'Translations/zh_HANS.po'
	}

fix_po(path["base"])
compare_po_files(path["base"], path["zh_hans"])