import polib
import re
from tqdm import tqdm
from collections import OrderedDict

class Translation():
	"""docstring for Translation"""
	def __init__(self, filepath):
		self.po = polib.pofile(filepath)
		self.pod = self.get_pod()

	def get_pod(self):
		pod = {}
		for entry in self.po:
			key = (entry.msgid, entry.msgctxt)
			pod[key] = entry.msgstr
		self.pod = pod
		return pod


def merge_trans(trans0, trans1, output):
	po0 = trans0.po
	po1 = trans1.po
	pod0 = trans0.pod
	pod1 = trans1.pod	
	for key, msgstr in tqdm(pod0.items()):
		print(key)
		msgid, msgctxt = key
		if (msgstr == "") and (msgid != ""):
			entry = po0.find(msgid, msgctxt=msgctxt)
			if entry:
				entry.msgstr = pod1.get(key, '')
	po0.save(output)


# 示例用法
path = { 
	"base": 'Translations/base.po',
	'zh_hans': 'Translations/zh_HANS_pre.po',
	'zh_hans_merged': 'Translations/zh_HANS.po'
	}
# fix_po(path["base"])
# merge_po_files(, path["zh_hans"], path["zh_hans_merged"])

trans0 = Translation(path["zh_hans"])
trans1 = Translation('Translations/zh_TW2CN.po')
output = 'Translations/zh_HANS.po'
merge_trans(trans0, trans1, output)