# coding: utf-8
from app import app
from flask import render_template
from .data import PTList,targetList,imglist,bonelist
from flask_assets import Environment,Bundle
import os

APIkey=app.config.get("APIKEY")

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html",PTList=PTList,APIkey=APIkey,imglist=imglist, metacontent=u"汪骨外科診所為大北門地區第一間骨外科診所，旨在提供病患最有效的骨外科治療．")

@app.route("/target")
def target():
  return render_template("targetpage.html",targetList=targetList, metacontent=u"汪骨外科診所的主治項目．") 

@app.route("/boneMassMeasurement")
def boneMassMeasurement():
  return render_template("boneMassMeasurement.html",bonelist=bonelist, metacontent=u"汪骨外科診所提供的骨質密度檢測．")

@app.route("/google8029c7599236ab79.html")
def comfirm():
  return render_template("google8029c7599236ab79.html")

@app.route("/sitemap.xml")
def sitemap():
  return render_template("sitemap.xml")