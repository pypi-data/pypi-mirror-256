from ..runtime import as_sophie_list, Message
from ..scheduler import NativeObjectProxy

class FileSystem:
	@staticmethod
	def read_lines(path, target:Message):
		with open(path, "r") as fh: lines = list(fh)
		target.dispatch_with(as_sophie_list(lines))
	
	@staticmethod
	def read_file(path, target:Message):
		with open(path, "r") as fh: text = fh.read()
		target.dispatch_with(text)

filesystem = NativeObjectProxy(FileSystem(), pin=False)

