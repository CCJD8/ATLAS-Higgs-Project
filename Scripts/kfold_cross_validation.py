import numpy as np
import pandas as pd
import uproot
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import Dense
from ROOT import *

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
pd_ZH = ZH_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd") #11 elements
pd_Zplus = Zplus_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd")
pd_ttb = ttb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd")
pd_Zbb = Zbb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd")
pd_llvv = llvv_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd")
pd_other = other_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights","mva_random_number"], library="pd")

#Add signal column
pd_ZH["signal"] = 1
pd_Zplus["signal"] = 0
pd_ttb["signal"] = 0
pd_Zbb["signal"] = 0
pd_llvv["signal"] = 0
pd_other["signal"] = 0

#Combine datasets
pd_dataset = pd.concat([pd_ZH, pd_Zplus, pd_ttb, pd_Zbb, pd_llvv, pd_other])

# Create arrays for the features (X), labels (Y), and weights (w)
X = pd_dataset.iloc[:,0:10].values
Y = pd_dataset.iloc[:,12:13].values
w = pd_dataset.iloc[:,10:11].values

mva_random_number = pd_dataset.iloc[:,11:12].values
feature_names = list(pd_dataset.iloc[:,0:10].columns)

# Normalise the data
X = StandardScaler().fit_transform(X)

# Divide and shuffle the data into k folds
kfold = KFold(n_splits=3, shuffle=True, random_state=22)


for i, (train, test) in enumerate(kfold.split(X)):
    kfold.split(Y)
    print("Split ", i)

    # Set model hyperparameters
    model_name = "model8cross"+str(i)
    model = Sequential()
    model.add(Dense(8, input_dim=10, activation='elu'))
    model.add(Dense(6, activation='elu'))
    model.add(Dense(24, activation='elu'))
    model.add(Dense(12, activation='elu'))
    model.add(Dense(6, activation='elu'))
    model.add(Dense(1, activation='sigmoid'))

    # Specify the training configuration (loss function, optimizer, metrics to monitor
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Training with fit() which slices data into batches and iterates over dataset for x epochs. history object stores training metrics (loss, metric values) per epoch
    history = model.fit(X[train], Y[train], validation_data=(X[test], Y[test]), epochs=40, batch_size=64)

    # Save trained model (architecture, weights, optimizer state)
    model.save(model_name)

    # Save the history.history dict for later plotting
    history_dict = pd.DataFrame(history.history)
    history_csv = model_name+"history.csv"
    with open(history_csv, mode='w') as f:
        history_dict.to_csv(f)

    print(model.summary())

    # Check model performance
    Y_pred = model.predict(X[test])
    predicted = list(np.round_(Y_pred, decimals=0))
    test = list(Y[test])
    ascore = accuracy_score(predicted, test)
    print("\nTest dataset accuracy is: ", ascore*100)