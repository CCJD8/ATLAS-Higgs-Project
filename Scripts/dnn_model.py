import numpy as np
import pandas as pd
import uproot
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ROOT import *
import copy, os, re, sys
import argparse
gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasStyle.C')
gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasUtils.C')
gROOT.SetBatch(kTRUE)
SetAtlasStyle()


# Import datasets
ZH_tree = uproot.open('Ntuple_ZH.root:nominal')
Zplus_tree = uproot.open('Ntuple_Zplus.root:nominal')
ttb_tree = uproot.open('Ntuple_ttb.root:nominal')
Zbb_tree = uproot.open('Ntuple_Zbb.root:nominal')
llvv_tree = uproot.open('Ntuple_llvv.root:nominal')
other_tree = uproot.open('Ntuple_other.root:nominal')

# Convert to pandas
pdZH = ZH_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd") #11 elements
pdZplus = Zplus_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pdttb = ttb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pdZbb = Zbb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pdllvv = llvv_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pdother = other_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")

#Add signal column
pdZH["signal"] = 1
pdZplus["signal"] = 0
pdttb["signal"] = 0
pdZbb["signal"] = 0
pdllvv["signal"] = 0
pdother["signal"] = 0

#Combine datasets
pddataset = pd.concat([pdZH, pdZplus, pdttb, pdZbb, pdllvv, pdother])

# Change pandas dataframe to array with input variables (X), output variable (Y) and weights (w)
X = pddataset.iloc[:,0:10].values
Y = pddataset.iloc[:,11:12].values
w = pddataset.iloc[:,10:11].values

# Normalise the data
X = StandardScaler().fit_transform(X)
X = X

# One hot encode (convert integer class to binary)
#Y = OneHotEncoder().fit_transform(Y).toarray()

sinYtrain = 0
sinYtest = 0
backYtrain = 0
backYtest = 0

# Split the data into train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=22)

for i in range(len(Y_train)):
    if (Y_train[i] == 1):
        sinYtrain += 1
    else:
        backYtrain += 1

for i in range(len(Y_test)):
    if (Y_test[i] == 1):
        sinYtest += 1
    else:
        backYtest += 1


print("Signal proportion in training set ", 100*sinYtrain/backYtrain, "%")
print("Signal proportion in test set ", 100*sinYtest/backYtest, "%\n")


# Create the neural network
import keras
from keras.models import Sequential
from keras.layers import Dense

modelname = "model8"
model = Sequential()
model.add(Dense(8, input_dim=10, activation='elu'))
model.add(Dense(6, activation='elu'))
model.add(Dense(24, activation='elu'))
model.add(Dense(12, activation='elu'))
model.add(Dense(6, activation='elu'))
model.add(Dense(1, activation='sigmoid'))                                                              #sigmoid/softmax
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])                      #binary_crossentropy / categorical_crossentropy

# Train the neural network
history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=50, batch_size=64)

# Save the network
model.save(modelname)

# Save the history.history dict for later plotting
historydict = pd.DataFrame(history.history)
historycsv = modelname+"history.csv"
with open(historycsv, mode='w') as f:
    historydict.to_csv(f)

print(model.summary())

# Check model performance
Y_pred = model.predict(X_test)

predicted = list(np.round_(Y_pred, decimals=0))
test = list(Y_test)

ascore = accuracy_score(predicted, test)
print("\nTest dataset accuracy is: ", ascore*100)