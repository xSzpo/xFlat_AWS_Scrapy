#!/usr/bin/python
# coding: utf-8

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import json
import random
import os
import re
import logging
import sys
import warnings
import numpy as np
import train


LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="'%(asctime)s - %(name)s - %(levelname)s "
                    "- %(message)s'")

debug = int(os.environ['DEBUG']) > 0
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    if type(request.data) == bytes:
        request_data = request.data.decode("utf-8")
    else:
        request_data = request.data
    json_ = json.loads(request_data)

    np.random.seed(666)
    random.seed(666)
    os.environ['PYTHONHASHSEED'] = str(666)
    try:
        prediction = clf.predict(json_)
        if debug:
            with open("tmp/good/"+json_['_id']+".txt", "w") as f:
                f.write(request_data)

            with open("tmp/good/"+json_['_id']+".json", "w") as f:
                json.dump(json_, f)

        return jsonify({'prediction': list(prediction)})
    except Exception as e:
        LOG.debug(e)
        if debug:
            with open("tmp/bad/"+json_['_id']+".txt", "w") as f:
                f.write(request_data)

            with open("tmp/bad/"+json_['_id']+".json", "w") as f:
                json.dump(json_, f)
        raise


@app.route('/train', methods=['GET'])
def train_model():
    mode = request.args.get('dev')
    score = train.main_train(mode=mode)
    return jsonify({'score': score})


if __name__ == '__main__':
    from waitress import serve

    models = os.listdir("model")
    models = list(filter(lambda x: re.findall("model_[\d]", x), models))
    if bool(models):
        model_path = os.path.join('model', max(models))
    else:
        model_path = 'model/model_default.pkl'

    clf = joblib.load(model_path)
    LOG.info("zaladowano model: %s" % model_path)
    serve(app, host="0.0.0.0", port=8666)
