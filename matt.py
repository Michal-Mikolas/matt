import time
import pyautogui
import json
import os
from pathlib import Path
from datetime import datetime
import pytesseract
import re
import pyperclip

class Matt(object):
	def __init__(self, cache_file:str, logger:callable=None, timeout:int=20, grayscale:bool=False):
		self.cache_file = cache_file
		self.logger = logger if logger else (lambda msg: print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}"))
		self.timeout = timeout
		self.grayscale = grayscale

		self.size = pyautogui.size()
		self._cache = self.reload_cache()
		self.ui = {}

	def set_ui(self, ui):
		"""
		Sets the UI elements dictionary.

		:param ui: A dictionary where keys are element names and values are file paths to images (or lists of paths).
		"""
		self.ui = ui

	def wait(self, ui, timeout=None, step=0.1):
		"""
		Waits for a UI element to appear on the screen.

		:param ui: The name of the UI element (defined in set_ui) or a list of image paths.
		:param timeout: Maximum time to wait in seconds (defaults to self.timeout).
		:param step: Interval between checks in seconds.
		:return: The center coordinates (x, y) of the found element.
		:raises TimeoutError: If the element is not found within the timeout.
		"""
		# Default params
		ui = self.get_ui(ui)
		timeout = timeout or self.timeout
		step = step or 0.1

		# Elements lookup with performance optimisation
		pos = None
		start = time.time()
		end_time = start + timeout
		while not pos and (time.time() <= end_time):
			for img in ui:
				pos = self.locate_on_screen(img, region_optimisation=True)
				if pos:
					break

			time.sleep(step)

		# If performance optimisation failed, try the last time
		if not pos:
			for img in ui:
				pos = self.locate_on_screen(img, region_optimisation=False)
				if pos:
					break

		# Finish & serve what we've got
		if not pos:
			self.logger("Waiting for %s timed out after %f seconds" % (img, time.time() - start))
			raise TimeoutError(str(ui))

		return self.get_center(pos)

	def which(self, *args, timeout=None, step=0.1):
		"""
		Waits for any one of the specified UI elements to appear.

		:param args: Names of UI elements to look for.
		:param timeout: Maximum time to wait in seconds.
		:param step: Interval between checks in seconds.
		:return: A tuple (element_name, (x, y)) of the first found element.
		:raises TimeoutError: If none of the elements are found.
		"""
		# Default params
		timeout = timeout or self.timeout
		step = step or 0.1

		# Perform lookup
		result = None
		start = time.time()
		end_time = start + timeout
		while not result and (time.time() <= end_time):
			for _ui in args:
				ui = self.get_ui(_ui)
				for img in ui:
					pos = self.locate_on_screen(img, region_optimisation=True, only_optimised=True)

					if pos:
						result = (_ui, self.get_center(pos))
						""""""
						print("[{:s}] Which: Found {:s} after {:f} sec".format(datetime.now().strftime("%H:%M:%S"), _ui, time.time()-start))
						break
				if result:
					break

			if not result:
				time.sleep(step)

		# If performance optimisation failed, try the last time
		if not result:
			for _ui in args:
				ui = self.get_ui(_ui)
				for img in ui:
					pos = self.locate_on_screen(img, region_optimisation=False)

					if pos:
						result = (_ui, self.get_center(pos))
						""""""
						#print("")
						#print("[{:s}] Which*: Found {:s} after {:f} sec".format(datetime.now().strftime("%H:%M:%S"), _ui, time.time()-start))
						#print("[{:s}] - pos: {:s}".format(datetime.now().strftime("%H:%M:%S"), str(pos)))
						break
				if result:
					break

		# Finish & serve what we've got
		if not result:
			self.logger("Waiting for %s timed out after %f seconds" % (str(args), time.time() - start))
			raise TimeoutError(str(args))

		return result

	def click(self, ui=None, x=0, y=0, timeout=None):
		"""
		Clicks on a UI element or the current mouse position.

		:param ui: The name of the UI element to click. If None, clicks at current position.
		:param x: Horizontal offset from the center of the element.
		:param y: Vertical offset from the center of the element.
		:param timeout: Maximum time to wait for the element to appear.
		"""
		if not ui:
			return pyautogui.click()

		pos = self.wait(ui, timeout=timeout)
		pyautogui.click(pos[0] + x, pos[1] + y)

	def double_click(self, ui=None, x=0, y=0, timeout=None):
		"""
		Double-clicks on a UI element or the current mouse position.

		:param ui: The name of the UI element to double-click. If None, clicks at current position.
		:param x: Horizontal offset from the center of the element.
		:param y: Vertical offset from the center of the element.
		:param timeout: Maximum time to wait for the element to appear.
		"""
		if not ui:
			return pyautogui.doubleClick()

		pos = self.wait(ui, timeout=timeout)
		pyautogui.doubleClick(pos[0] + x, pos[1] + y)

	def right_click(self, ui=None, x=0, y=0, timeout=None):
		"""
		Right-clicks on a UI element or the current mouse position.

		:param ui: The name of the UI element to right-click. If None, clicks at current position.
		:param x: Horizontal offset from the center of the element.
		:param y: Vertical offset from the center of the element.
		:param timeout: Maximum time to wait for the element to appear.
		"""
		if not ui:
			return pyautogui.click(button='right')

		pos = self.wait(ui, timeout=timeout)
		pyautogui.click(pos[0] + x, pos[1] + y, button='right')

	def move_to(self, ui, x=0, y=0, timeout=None):
		"""
		Moves the mouse cursor to a UI element.

		:param ui: The name of the UI element to move to.
		:param x: Horizontal offset from the center of the element.
		:param y: Vertical offset from the center of the element.
		:param timeout: Maximum time to wait for the element to appear.
		"""
		pos = self.wait(ui, timeout=timeout)
		pyautogui.moveTo(pos[0] + x, pos[1] + y)

	def hotkey(self, *args, **kwargs):
		"""
		Presses a hotkey combination (e.g., 'ctrl', 'c').

		:param args: The keys to press in order.
		"""
		'''Example: matt.hotkey('alt', 'tab')'''
		pyautogui.hotkey(*args, **kwargs)

	def typewrite(self, message, interval=0.0):
		"""
		Types a message.

		:param message: The string to type.
		:param interval: Delay between each character.
		"""
		pyautogui.typewrite(message, interval)

	def mouse_down(self):
		"""
		Presses the mouse button down (without releasing).
		"""
		pyautogui.mouseDown()

	def mouse_up(self):
		"""
		Releases the mouse button.
		"""
		pyautogui.mouseUp()

	def screenshot(self, filename = None, region = None):
		"""
		Takes a screenshot.

		:param filename: File path to save the screenshot. If None, returns the image object.
		:param region: A tuple (left, top, width, height) of the region to capture.
		:return: The PIL image object.
		"""
		if filename:
			directory = os.path.dirname(filename)
			Path(directory).mkdir(parents=True, exist_ok=True)

		return pyautogui.screenshot(filename, region=region)

	def ocr(self, region = None):
		"""
		Performs Optical Character Recognition (OCR) on a region of the screen or the whole screen.

		:param region: A tuple (left, top, width, height) to capture.
		:return: The recognized text with non-digit characters removed.
		"""
		# img = pyautogui.screenshot('screenshots\\ps.png', region=region)
		img = pyautogui.screenshot(region=region)
		result = pytesseract.image_to_string(img)
		result = re.sub(r'[^\d]', '', result)

		return result

	def select(self, region):
		"""
		Selects a region by dragging the mouse.

		:param region: A tuple (start_x, start_y, width, height). The mouse drags from (start_x, start_y) by (width, height).
		"""
		pyautogui.moveTo(region[0], region[1])
		pyautogui.mouseDown()
		pyautogui.move(region[2], region[3])
		pyautogui.mouseUp()

	def copy(self):
		"""
		Performs a copy operation (Ctrl+C) and returns the clipboard content.

		:return: The content of the clipboard.
		"""
		pyautogui.hotkey('ctrl', 'c')
		time.sleep(0.2)
		result = pyperclip.paste()

		return result

	def get_ui(self, ui):
		if (type(ui).__name__ == 'str') and (ui in self.ui):
			ui = self.ui[ui]

		if type(ui).__name__ == 'str':
			ui = [ui]

		return ui

	def get_center(self, pos):
		return (
			int(pos[0] + pos[2] / 2),  # x + (width / 2)
			int(pos[1] + pos[3] / 2),  # y + (height / 2)
		)

	def locate_on_screen(self, img, region_optimisation=False, only_optimised=False):
		region = self.get_region(img) if region_optimisation else None
		if only_optimised and not region:
			return None

		pos = pyautogui.locateOnScreen(img, grayscale=self.grayscale, region=region)

		if pos:
			self.update_region(img, pos)

		return pos


	######
	#     # ######  ####  #  ####  #    #  ####
	#     # #      #    # # #    # ##   # #
	######  #####  #      # #    # # #  #  ####
	#   #   #      #  ### # #    # #  # #      #
	#    #  #      #    # # #    # #   ## #    #
	#     # ######  ####  #  ####  #    #  ####

	def get_region(self, img):
		regions = self.cache('regions') or {}

		if img not in regions:
			# self.logger('get_region("%s"): %s' % (img, 'None'))  ###
			return None

		region = regions[img]

		if region['success_counter'] >= 3:
			return (region['start_x'], region['start_y'], region['width'], region['height'])
		else:
			return None

	def update_region(self, img, pos):
		# Prepare
		regions = self.cache('regions') or {}

		# Process
		if img not in regions:
			""""""
			#print("[{:s}] - UpdateRegion: Creating '{:s}' cache entry".format(datetime.now().strftime("%H:%M:%S"), img))

			# Region doesn't exist, create
			regions[img] = {
				'start_x': int(pos[0]),
				'start_y': int(pos[1]),
				'width': int(pos[2]),
				'height': int(pos[3]),
				'success_counter': 1,
			}

			self.cache('regions', regions)

		elif (pos[0] >= regions[img]['start_x']
			and pos[1] >= regions[img]['start_y']
			and (pos[0] + pos[2]) <= (regions[img]['start_x'] + regions[img]['width'])
			and (pos[1] + pos[3]) <= (regions[img]['start_y'] + regions[img]['height'])
		):
			""""""
			#print("[{:s}] - UpdateRegion: No need to update '{:s}'".format(datetime.now().strftime("%H:%M:%S"), img))

			# No need to update region
			regions[img]['success_counter'] += 1

			# Only update counter if necesary
			if regions[img]['success_counter'] <= 3:
				self.cache('regions', regions)

		else:
			""""""
			#print("[{:s}] - UpdateRegion: Updating '{:s}' entry".format(datetime.now().strftime("%H:%M:%S"), img))
			#print("({:d} + {:d}) <= ({:d} + {:d})".format(
			#	pos[1],
			#	pos[3],
			#	regions[img]['start_y'],
			#	regions[img]['height']
			#))
			#print(str((pos[1] + pos[3]) <= (regions[img]['start_y'] + regions[img]['height'])))
			#print("[{:s}] - old data: {:s}".format(datetime.now().strftime("%H:%M:%S"), str(regions[img])))

			# Update region
			if pos[0] < regions[img]['start_x']:
				regions[img]['start_x'] = min(regions[img]['start_x'], pos[0])
				regions[img]['width'] += max(regions[img]['start_x'], pos[0]) - min(regions[img]['start_x'], pos[0])

			if pos[1] < regions[img]['start_y']:
				regions[img]['start_y'] = min(regions[img]['start_y'], pos[1])
				regions[img]['height'] += max(regions[img]['start_y'], pos[1]) - min(regions[img]['start_y'], pos[1])

			old_end_x = regions[img]['start_x'] + regions[img]['width']
			new_end_x = pos[0] + pos[2]
			if new_end_x > old_end_x:
				regions[img]['width'] += new_end_x - old_end_x
				regions[img]['height'] += max(regions[img]['start_y'], pos[1]) - min(regions[img]['start_y'], pos[1])

			old_end_y = regions[img]['start_y'] + regions[img]['height']
			new_end_y = pos[1] + pos[3]
			if new_end_y > old_end_y:
				regions[img]['height'] += new_end_y - old_end_y

			regions[img]['success_counter'] = 0

			#print("[{:s}] - new data: {:s}".format(datetime.now().strftime("%H:%M:%S"), str(regions[img])))
			regions[img]['start_x'] = int(regions[img]['start_x'])
			regions[img]['start_y'] = int(regions[img]['start_y'])
			regions[img]['width'] = int(regions[img]['width'])
			regions[img]['height'] = int(regions[img]['height'])
			self.cache('regions', regions)


	 #####
	#     #   ##    ####  #    # ######
	#        #  #  #    # #    # #
	#       #    # #      ###### #####
	#       ###### #      #    # #
	#     # #    # #    # #    # #
	 #####  #    #  ####  #    # ######

	def cache(self, key, value=None):
		if value is not None:
			self._cache[key] = value
			self.resave_cache()

		return self._cache[key] if key in self._cache else None

	def reload_cache(self):
		# Prepare directory
		directory = os.path.dirname(self.cache_file)
		Path(directory).mkdir(parents=True, exist_ok=True)

		with open(self.cache_file, 'a+') as file:
			file.seek(0)  # a+ creates file if not exist and move the cursor to the file end
			try:
				self._cache = json.load(file)
			except json.JSONDecodeError:  # empty file
				self._cache = {}

			return self._cache

	def resave_cache(self):
		# Prepare directory
		directory = os.path.dirname(self.cache_file)
		Path(directory).mkdir(parents=True, exist_ok=True)

		with open(self.cache_file, 'w') as file:
			json.dump(self._cache, file, indent=4)
