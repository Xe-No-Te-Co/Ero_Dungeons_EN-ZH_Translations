import polib
import re
from zhconv import convert

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
		
def normalize_po_file(po_file_path):
	# Reopen the merged file and manually merge multiline msgids into single lines
	with open(po_file_path, 'r', encoding='utf-8') as file:
		lines = file.readlines()

	with open(po_file_path, 'w', encoding='utf-8') as file:
		for line in lines:
			if line.startswith('msgctxt'):
				msgid = line.strip()
				while True:
					next_line = lines.pop(0)
					if next_line.startswith('"'):
						msgid += next_line.strip()
					else:
						lines.insert(0, next_line)
						break
				file.write(msgid + '\n')
			else:
				file.write(line)

def merge_po_files(po0_path, po1_path, merged_po_path):
	# 读取两个 po 文件
	po0 = polib.pofile(po0_path)
	po1 = polib.pofile(po1_path)

	# 创建字典用于快速查找 po 中的条目
	po0_dict = {entry.tcomment: entry for entry in po0 if entry.tcomment}
	po1_dict = {entry.tcomment: entry for entry in po1 if entry.tcomment}
	# 有三种情况，po0和po1都有，po0有但po1没有，po1有但po0没有

	# 遍历 po0 中的条目，根据 tcomment 替换 msgstr
	for entry in po0:
		print(f'[Entry key]{entry.tcomment} \n[Entry text]{entry.msgid}')
		if entry.tcomment in po1_dict:
			# po0和po1都有，用po1的msgstr覆盖po0的
			po1_entry = po1_dict[entry.tcomment]
			if (po1_entry.msgid == entry.msgid) and (po1_entry.msgstr != entry.msgstr):
				print(f'Translation updated: {entry.msgstr} -> {po1_entry.msgstr}')
				entry.msgstr = po1_entry.msgstr
			else:
				print(f'Translation unchanged.')
		else:
			# po0有但po1没有，不用动
			print(f'Translation lost.')
		print('')

	# for entry in po1:
		
	# 	if entry.tcomment not in po0_dict:
	# 		# po1有但po0没有
	# 		print(f'[Entry key]{entry.tcomment} \n[Entry text]{entry.msgid}')
	# 		print(f'Translation added.')
	# 		po0.append(entry)
	# 		print('')

	

	# 将合并后的 po 文件保存
	# export_po(merged_po_path, po0)
	po0.save(merged_po_path)
	
	# Normalize the saved .po file
	# normalize_po_file(merged_po_path)

def export_po(fp, po):
	def to_string(pre, string):
		return f'{pre} \"{string}\"\n'

	header = '''msgid ""
msgstr ""
"Project-Id-Version: zh_HANS\\n"
"POT-Creation-Date: \\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: \\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"X-Generator: Poedit 3.4.2\\n"
	\n'''
	with open(fp, 'w', encoding='utf8') as f:
		f.write(header)
		for entry in po:
			f.write(f'# {entry.tcomment}\n')
			if entry.msgctxt:
				f.write(to_string('msgctxt', entry.msgctxt))
			f.write(to_string('msgid', entry.msgid))
			f.write(to_string('msgstr', entry.msgstr))
			f.write('\n')

# 示例用法
path = { 
	"base": 'Translations/zh_HANS.untrans.po',
	'zh_hans_merged': 'Translations/zh_HANS_11.po',
	'zh_TW': 'Translations/zh_TW.po'
	}
# fix_po(path["base"])
merge_po_files(path["base"], path["zh_TW"], path["zh_hans_merged"])