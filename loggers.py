
class Logger():
	def log(msg):
		raise NotImplementedError


class FakeLogger(Logger):
	def log(msg):
		pass


class ConsoleLogger(Logger):
	def log(msg):
		pass
