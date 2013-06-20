#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import jsonlib

# SQLAlchemy
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
データ取得先のURL
データベースパス
"""
url		= "http://matsuura.naist.jp/naist_weather/"
database	= "sqlite:///weather"

"""
SQLAlchemyのデータ構造定義
"""
Base = declarative_base()
Base.metadata = MetaData()
class Weather(Base):
	__tablename__ = 'weather'

	id		= Column(Integer, primary_key=True)
	temperature	= Column(Float)
	humidity	= Column(Float)
	wind_speed	= Column(Float)
	wind_dir	= Column(Float)
	pressure	= Column(Float)
	rainfall	= Column(Float)

	def __init__(self, temperature, humidity, wind_speed, wind_dir, pressure, rainfall):
		self.temperature	= temperature
		self.humidity		= humidity
		self.wind_speed		= wind_speed
		self.wind_dir		= wind_dir
		self.pressure		= pressure
		self.rainfall		= rainfall

	def __repr__(self):
		return u"<weather t = %s, h = %s, ws = %s, wd = %s, p = %s, r = %s>" %(
			self.temperature,
			self.humidity,
			self.wind_speed,
			self.wind_dir,
			self.pressure,
			self.rainfall
		)

"""
データベースにテーブル等の作成(存在する場合は接続のみ)
"""
engine = create_engine('sqlite:///weather', echo=False)
Base.metadata.create_all(engine)

"""
セッションの作成
"""
Session = sessionmaker(bind=engine)

"""
URLからJSONデータの取得
"""
sensordata = None
try:
	"""
	各BBSのURLを取得するためのhtmlを取得
	"""
	json = urllib2.urlopen(url).read()

	"""
	JSONを解析しセンサデータを取得
	"""
	sensordata = jsonlib.read (json)
except:
	pass

"""
センサーデータが正しく入力されているかの確認
"""
if sensordata:
	"""
	センサデータの要素
	"""
	elements = ["Temperature", "Humidity", "WindSpeed", "WindDir", "Pressure", "Rainfall"]
	for element in elements:
		"""
		正しくデータが入っているかの確認
		"""
		if not (sensordata.has_key(element) and sensordata[element].has_key("value")):
			sensordata = None
			break

"""
センサーデータが正しく入力されている場合には、データベースに書き込み
"""
if sensordata:
	"""
	各値の取得
	"""
	temperature	= sensordata["Temperature"]["value"]
	humidity	= sensordata["Humidity"]["value"]
	wind_speed	= sensordata["WindSpeed"]["value"]
	wind_dir	= sensordata["WindDir"]["value"]
	pressure	= sensordata["Pressure"]["value"]
	rainfall	= sensordata["Rainfall"]["value"]

	"""
	Weatherモデルのインスタンス化
	"""
	weather = Weather(temperature, humidity, wind_speed, wind_dir, pressure, rainfall)

	"""
	データベースへ登録
	"""
	session = Session()
	session.add(weather)
	session.commit()	

	print weather
