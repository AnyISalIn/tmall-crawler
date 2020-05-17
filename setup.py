from setuptools import setup

setup(name='tmall_crawler',
      version='0.1',
      description='tmall crawler',
      author='AnyISalIn',
      author_email='anyisalin@gmail.com',
      packages=['tmall_crawler'],
      install_requires=[
          'selenium==3.4.3',
          'celery==4.0.2',
          'bs4==0.0.1',
          'requests==2.12.4'
      ],
      entry_points={
          'console_scripts': [
              'tmall-crawler=tmall_crawler.run:main'
          ]},
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ])
