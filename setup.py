from setuptools import setup

setup(
	name='b3irpf',
	version='1.0.1',
	packages=[
		'assetprice',
		'assetprice.migrations',
		'assetprice.management',
		'assetprice.management.commands',
	],
	url='https://github.com/alexsilva/django-assetprice',
	install_requires=["selenium", "selenium-stealth"],
	license='MIT',
	author='alex',
	author_email='',
	description='Pacote que define comandos para cálculo de preço justo'
)
