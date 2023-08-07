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
		parser.add_argument('-exp', '--executable-path', type=str,
		                    default=settings.SELENIUM_CHROME_EXECUTABLE_PATH)

	@staticmethod
	def get_json(url, **options) -> ResponseResult:
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("start-maximized")
		chrome_options.add_argument("--headless")
		chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		chrome_options.add_experimental_option('useAutomationExtension', False)

		service = Service(options['executable_path'])
		driver = webdriver.Chrome(service=service, options=chrome_options)
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
