import setuptools

setuptools.setup(
	name='FruceAPI',
	version='1.0.0',
	author='kotvpalto',
	author_email='kotvpaltoof@ya.ru',
	description='FruceAPI is a simple tool for managing your server on FruitSpace hosting',
	packages=['FruceAPI'],
	install_requires=["urllib", "aiohttp", "zlib", "base64"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)