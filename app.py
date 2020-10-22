import numpy as np
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import pickle
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = pickle.load(open('RFCovidModel.pkl', 'rb'))
model1 = pickle.load(open('noPlate.pkl', 'rb'))
#model2 = pickle.load(open('noALP.pkl', 'rb'))
#model3 = pickle.load(open('noBothC.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if("text" == "M"):
        text = 1
    else:
        text =0
    int_features = [float(x) for x in request.form.values()]

    int_features1=[]

    int_features = [float(x) for x in request.form.values()]
    for i in int_features:
        #for male, it is zero
        if i != 100:
            int_features1.append(i)
        
    final_features = [np.array(int_features1)]
    
    # if int_features[3]==100 and int_features[12]==100:
        # prediction = model3.predict_proba(final_features)
    # elif int_features[12]==100:
        # prediction = model2.predict_proba(final_features)
    if int_features[3]==100:
        prediction = model1.predict_proba(final_features)
    else:
        prediction = model.predict_proba(final_features)    
    
    
    alpha=0.75
    beta=0.75
   # finalProb=
    for i in prediction:
     # print("list: i is:",i)
      if i[1] > alpha and i[1]> i[0]:
        ele =i[1]
       # print("positive")
        add=1
        finalProb=add
        #finalLabelProb.append(add)
    
      elif i[0]>beta and i[0]>i[1]:
       # print("negative")
        add=0
        finalProb= add
        #finalLabelProb.append(add)
      else:
        #print("abstention incurred")
        add=2
        ##remove prob with target as 2
        finalProb=add
    output=[]

    output.append(finalProb)
    output.append(prediction[0])
    #output = finalProb
    #also display output from 'prediction' variable

    return render_template('index1.html', prediction_text1='Patient is (positive(1) or negative(0)= {}'.format(output[0]),prediction_text2='              Probabilities:{} '.format(output[1]))
    

if __name__ == "__main__":
    app.run(debug=True)
