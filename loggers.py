from datetime import datetime
import logging
import traceback


class Logger():
	def log(self, msg:str):
		raise NotImplementedError

	def now_str(self) -> str:
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class FakeLogger(Logger):
	def log(self, msg:str):
		pass


class ConsoleLogger(Logger):
	def log(self, msg:str):
		print("[{:s}] {:s}".format(self.now_str(), msg))
