# -*- coding: utf-8 -*-
#
# Jame Yu
#

## usage example:
#
# This api interface runs as stand-alone process.
# 

import os
import sys
import logging
import json

from flask import Flask, request, send_file, abort
from flask_restful import Resource, Api
from flask.json import jsonify
from flask_cors import CORS

from helper import ConnStrDBSession
from db_models import *

from conf import username, password

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
format='%(asctime)s - %(name)s - %(filename)s:%(lineno)d: %(levelname)s:%(funcName)s() - %(message)s')

dbConnStr = "mysql+pymysql://"+username+":"+password+"@127.0.0.1:3306/measure?charset=utf8" 

app = Flask(__name__)
CORS(app)
api = Api(app)

class saveVal(Resource):

    def get(self, voltage, current):
        vol  = int(voltage)
        curr = int(current)

        measure_data = dataVal(voltage=vol,
                              current=curr)

        #save user info into mysqldb
        with ConnStrDBSession(dbConnStr) as session:
            session.add(measure_data)
            session.commit()

        return jsonify({'result':'ok'})


class getData(Resource):
    def get(self):

        #get measure data from mysqldb
        with ConnStrDBSession(dbConnStr) as session:
            dataList= []
            data = session.query(dataVal).order_by(dataVal.ts.desc()).limit(5).all()
            if data:
                for item in data:
                    dataList.append({'v': item.voltage, 'a': item.current, 'ts': item.ts})
                return jsonify({'result':'ok', 'data': dataList})

        return jsonify({'result':'failed'})


api.add_resource(saveVal, '/saveval/<voltage>/<current>')
api.add_resource(getData, '/get')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
