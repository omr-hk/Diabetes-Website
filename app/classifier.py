import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,TransformerMixin

class data_input:
    def __init__(self):
        self.gender=""
        self.age=0
        self.hypertension=0
        self.heart_disease=0
        self.smoking_history=""
        self.bmi=0
        self.HbA1c_level=0
        self.blood_glucose_level=0
    def set_data(self,gender:str,age:int,hypertension:int,heart_disease:int,smoking_history:str,bmi:float,HbA1c_level:float,
               blood_glucose_level:int):
        self.gender=gender
        self.age=age
        self.hypertension=hypertension
        self.heart_disease=heart_disease
        self.smoking_history=smoking_history
        self.bmi=bmi
        self.HbA1c_level=HbA1c_level
        self.blood_glucose_level=blood_glucose_level
    def get_data(self):
        dictionary={
        'gender':self.gender,
        'age':self.age,
        'hypertension':self.hypertension,
        'heart_disease':self.heart_disease,
        'smoking_history':self.smoking_history,
        'bmi':self.bmi,
        'HbA1c_level':self.HbA1c_level,
        'blood_glucose_level':self.blood_glucose_level
        }
        return pd.DataFrame(dictionary,index=[0])
    def clear_data(self):
        self.gender=""
        self.age=0
        self.hypertension=0
        self.heart_disease=0
        self.smoking_history=""
        self.bmi=0
        self.HbA1c_level=0
        self.blood_glucose_level=0

class DataStandardizer(BaseEstimator,TransformerMixin):
    def __init__(self):
        self.cat=['gender', 'smoking_history']
        self.metric=['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        self.dummy=['gender_Male', 'smoking_history_current', 'smoking_history_ever', 'smoking_history_former', 'smoking_history_never', 'smoking_history_not current']
        with open('./tools/Scaler.pickle','rb') as g:
            self.scaler=pickle.load(g)
    def fit(self,x,y=None):
        return self
    def transform(self,x):
        return pd.concat([pd.DataFrame(self.scaler.transform(x[self.metric]),columns=self.metric,index=x[self.metric].index),x[self.dummy]],axis=1)
    
class DummyVariables(BaseEstimator,TransformerMixin):
    def __init__(self):
        self.cat=['gender', 'smoking_history']
        self.metric=['age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        self.dummy=['gender_Male', 'smoking_history_current', 'smoking_history_ever', 'smoking_history_former', 'smoking_history_never', 'smoking_history_not current']
        self.dummy_location={
            'current':self.dummy[1],
            'ever':self.dummy[2],
            'former':self.dummy[3],
            'never':self.dummy[4],
            'not current':self.dummy[5]
        }
    def fit(self,x,y=None):
        return self
    def transform(self,x):
        gender=x['gender'][0]
        smoking_history=self.dummy_location[x['smoking_history'][0]]
        x.drop(self.cat,inplace=True,axis=1)
        for i in self.dummy:
            if(i=='gender_Male'):
                if(gender=='Male'):
                    x.loc[0,i]=1
                else:
                    x.loc[0,i]=0
            elif(i==smoking_history):
                  x.loc[0,i]=1
            else:
                  x.loc[0,i]=0
        x[i].astype(int)
        return x

class classify:
    def __init__(self,params:dict):
        with open('./tools/DiabetesClassifier.pickle','rb') as f:
            self.classifier=pickle.load(f)
        self.pipe=Pipeline([
            ('DummyVariables',DummyVariables()),
            ('DataStandardizer',DataStandardizer()),
            ('Classifier',self.classifier)
        ])
        self.formatter=data_input()
        self.params=params
    
    def predictResult(self):
        self.formatter.set_data(gender=self.params['gen'],age=self.params['ag'],hypertension=self.params['hyp'],heart_disease=self.params['heart'],smoking_history=self.params['smk'],bmi=self.params['bmi'],HbA1c_level=self.params['hba'],
                 blood_glucose_level=self.params['bcl'])
        data=self.formatter.get_data()
        result=self.pipe.predict(data)
        if(result[0]==0):
            return 'Absent'
        return 'Present'