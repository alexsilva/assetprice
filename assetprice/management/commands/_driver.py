import argparse
import json

from django.core.management import BaseCommand
from django.utils.module_loading import import_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from assetprice import settings


class Ticker:
	def __call__(self, value):
		try:
			if isinstance(settings.TICKER_VALIDATOR, str):
				validator = import_string(settings.TICKER_VALIDATOR)
				value = validator(value and value.upper()).lower()
			return value
		except ValueError as exc:
			raise argparse.ArgumentTypeError(str(exc))


class ResponseResult:
	def __init__(self, url, data=None):
		self.url = url
		self.data = data

	def __str__(self):
		return f"{self.url}:\n{self.data}"


class BaseWebDriverCommand(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('-t', '--ticker', type=Ticker())

	@staticmethod
	def get_json(url, **cmd_options) -> ResponseResult:
		options = webdriver.ChromeOptions()
		options.add_argument("start-maximized")
		options.add_argument("--headless")
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
		options.add_experimental_option('useAutomationExtension', False)

		driver = webdriver.Chrome(options=options)
		stealth(driver,
		        languages=["pt-BR", "pt", "en-US", "en"],
		        vendor="Google Inc.",
		        platform="Win32",
		        webgl_vendor="Intel Inc.",
		        renderer="Intel Iris OpenGL Engine",
		        fix_hairline=True
		        )
		result = ResponseResult(url)
		try:
			driver.get(url)
		finally:
			text = driver.find_element(By.TAG_NAME, "pre").text
			result.data = json.loads(text)
			driver.close()
		return result
