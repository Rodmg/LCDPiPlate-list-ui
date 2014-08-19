#!/usr/bin/python
# coding: utf-8

#Autor: Rodrigo Méndez Gamboa

import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

class MenuEntry:
	def __init__(self, name ,action):
		self.name = name
		self.action = action

class UI(Adafruit_CharLCDPlate):

	LOADINGMSG = "Loading..."

	def __init__(self):
		Adafruit_CharLCDPlate.__init__(self)
		self.backlight(self.GREEN)
		self.lastTime = time.time()
		self.timeout = 0
		self.DEFAULTIMEOUT = 5

		self.lastButton = self.LEFT
		self.lastBounce = 0
		self.DEBOUNCETIME = 0.4
		self.FASTDEBOUNCETIME = 0.2
		self.timeDebounce = self.DEBOUNCETIME
		self.CANCEL = self.RIGHT

		self.screenContent = self.LOADINGMSG
		self.menuEntries = []
		self.currentEntry = 0

		self.roll = False
		self.currentShift = 0
		self.shiftTimeout = 0.8
		self.lastShiftTime = time.time()

	def addMenuEntry(self, entry):
		self.menuEntries.append(entry)
		self._updateEntryDisplay()

	def clrMenu(self):
		self.menuEntries = []
		self.currentEntry = 0
		self.screenContent = self.LOADINGMSG

	#Shows a message for <timeout> seconds, 5 by default.
	def alert(self, message, timeout = -1):
		self.clear()
		self.message(message)
		if timeout < 0:
			self.timeout = self.DEFAULTIMEOUT
		else:
			self.timeout = timeout
		self.lastTime = time.time()

	def _updateEntryDisplay(self):
		self.clear()

		topEntry = self.menuEntries[self.currentEntry].name
		##Character shifting managment, for messages longer than the screen.
		lenTEntry = len(topEntry)

		if lenTEntry > 14:
			self.roll = True
			if self.currentShift > lenTEntry - 14:
				self.currentShift = 0
				self.roll = False
			topEntry = topEntry[ self.currentShift : self.currentShift + 14 ]
			self.lastShiftTime = time.time()
			self.currentShift = self.currentShift + 1
		else:
			self.roll = False
		##

		msg = chr(126) + topEntry
		if self.currentEntry != 0:
			if len(msg) < 16:
				msg = msg + '                '
			msg = msg[:15] + chr(94)			#Up arrow indicatong that there are more options over.
		if (self.currentEntry < len(self.menuEntries) - 1):
			msg = msg + '\n ' + self.menuEntries[self.currentEntry + 1].name
		self.screenContent = msg
		self.message(msg)

	def _debounce(self, button):
		if self.lastButton == button:
			if self.lastBounce + self.timeDebounce <= time.time():
				if self.buttonPressed(button):			#If the button is still pressed after timeout, start fast scroll.
					self.lastBounce = time.time()
					self.timeDebounce = self.FASTDEBOUNCETIME
				return True
		else:
			self.lastBounce = time.time()
			self.lastButton = button
			self.timeDebounce = self.DEBOUNCETIME
			return True
		return False

	def update(self):
		#Update the screen after an alert
		if self.timeout >= 0 and ((self.lastTime + self.timeout) <= time.time()):
			self.clear()
			self.message(self.screenContent)
			self.lastTime = time.time()
			self.timeout = -1

		#Character shifting for long messages:
		if self.timeout == -1 and self.roll and ((self.lastShiftTime + self.shiftTimeout) <= time.time()):
			self._updateEntryDisplay()

		#Check the buttons:
		if self.buttonPressed(self.UP) and self._debounce(self.UP):
			if (self.currentEntry > 0):
				self.currentEntry = self.currentEntry - 1
				self.currentShift = 0
				self._updateEntryDisplay()

		elif self.buttonPressed(self.DOWN) and self._debounce(self.DOWN):
			if (self.currentEntry < len(self.menuEntries) - 1):
				self.currentEntry = self.currentEntry + 1
				self.currentShift = 0
				self._updateEntryDisplay()

		elif self.buttonPressed(self.SELECT) and self._debounce(self.SELECT):
			self.menuEntries[self.currentEntry].action()

		elif self.buttonPressed(self.CANCEL) and self._debounce(self.CANCEL):
			self.timeout = 0


if __name__ == '__main__':
	ui = UI()
	ui.addMenuEntry(MenuEntry('Red', lambda: {ui.backlight(ui.RED)}))
	ui.addMenuEntry(MenuEntry('Alert', lambda: ui.alert('Test Alert')))
	ui.addMenuEntry(MenuEntry('Blue', lambda: {ui.backlight(ui.BLUE)}))

	while True:
		ui.update()