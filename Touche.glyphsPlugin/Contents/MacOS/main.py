# -*- coding: utf-8 -*-
def _run(script):
	global __file__
	import os, sys
	reload(sys)
	sys.setdefaultencoding('utf8')
	sys.frozen = 'macosx_plugin'
	if not __file__ or __file__.find("Contents/Resources/") < 0:
	base = os.environ['RESOURCEPATH']
		__file__ = path = os.path.join(base, script)
	else:
		__file__ = path = __file__.replace("../MacOS/main.py", script)
	
	if sys.version_info[0] == 2:
		with open(path, 'rU') as fp:
			source = fp.read() + "\n"
	else:
		with open(path, 'r', encoding='utf-8') as fp:
			source = fp.read() + '\n'

	exec(compile(source, path, 'exec'), globals(), globals())

_run('plugin.py')
