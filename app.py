import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})
# model = pickle.load(open('model.pkl', 'rb'))

def multi(rnfll,tmp,ntrgn,phsprs,ptsm,ph):
    model = pickle.load(open('model.pkl','rb'))
    kl=[]
    a=['Bajra', 'Banana', 'Barley', 'Bean', 'Black pepper', 'Blackgram','Bottle Gourd', 'Brinjal', 'Cabbage', 'Cardamom', 'Carrot',
       'Castor seed', 'Cauliflower', 'Chillies', 'Colocosia', 'Coriander','Cotton', 'Cowpea', 'Drum Stick', 'Garlic', 'Ginger', 'Gram',
       'Grapes', 'Groundnut', 'Guar seed', 'Horse-gram', 'Jowar', 'Jute','Khesari', 'Lady Finger', 'Lentil', 'Linseed', 'Maize', 'Mesta',
       'Moong(Green Gram)', 'Moth', 'Onion', 'Orange', 'Papaya','Peas & beans (Pulses)', 'Pineapple', 'Potato', 'Raddish', 'Ragi',
       'Rice', 'Safflower', 'Sannhamp', 'Sesamum', 'Soyabean','Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tomato',
       'Turmeric', 'Urad', 'Varagu', 'Wheat']
    i=0
    k=0
    kl.append(a[int(model.predict([[rnfll,tmp,ntrgn,phsprs,ptsm,ph]]))])
    
    while(True):
        if kl[-1]==a[int(model.predict([[rnfll,tmp,ntrgn,phsprs,ptsm,ph]]))]:
            rnfll=rnfll-10
            tmp=tmp-3
            ntrgn=ntrgn-2
            phsprs=phsprs-1
            ptsm=ptsm-3
            ph=ph-0.2
            k+=1
            
        else:
            kl.append(a[int(model.predict([[rnfll,tmp,ntrgn,phsprs,ptsm,ph]]))])
            i+=1
            
        if i==3 or k==100:
            if len(kl)<4:
                for i in range(len(kl)-1,4):
                    kl.append('')
            return kl


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    data=json.dumps(request.form)
    ko=json.loads(data)
    dicti={}
#     b=int(DT.predict([kl]))
    prediction = multi(float(ko['Rainfall']),float(ko['Temprature']),float(ko['Nitrogen']),float(ko['Phosphorus']),float(ko['Potassium']),float(ko['Ph']))
    print(prediction)
#     output = prediction[0]
    dicti["1"]=prediction[0]    
    dicti["2"]=prediction[1]
    dicti["3"]=prediction[2]
    dicti["4"]=prediction[3]

    return json.dumps(dicti)
#     return render_template('index.html', prediction_text='The predicted value is {}'.format(a[output]))

if __name__ == "__main__":
    app.run()