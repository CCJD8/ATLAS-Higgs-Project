import numpy as np
import pandas as pd
import uproot
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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
pd_ZH = ZH_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd") #11 elements
pd_Zplus = Zplus_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pd_ttb = ttb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pd_Zbb = Zbb_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pd_llvv = llvv_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")
pd_other = other_tree.arrays(["lep0_pt", "lep1_pt", "jet0_pt", "jet1_pt", "n_jets", "deltaRjets", "mbb", "mll", "metpt", "pTdilep","weights"], library="pd")

# Add signal column
pd_ZH["signal"] = 1
pd_Zplus["signal"] = 0
pd_ttb["signal"] = 0
pd_Zbb["signal"] = 0
pd_llvv["signal"] = 0
pd_other["signal"] = 0

# Combine datasets
pd_full_dataset = pd.concat([pd_ZH, pd_Zplus, pd_ttb, pd_Zbb, pd_llvv, pd_other])

# Create arrays for the features (X), labels (Y), and weights (w)
X = pd_full_dataset.iloc[:,0:10].values
Y = pd_full_dataset.iloc[:,11:12].values
w = pd_full_dataset.iloc[:,10:11].values

# Normalise the data
X = StandardScaler().fit_transform(X)

# One hot encode (convert integer class to binary)
#Y = OneHotEncoder().fit_transform(Y).toarray()

Y_train_signal = 0
Y_test_signal = 0
Y_train_background = 0
Y_test_background = 0

# Divide the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=22)

# Count number of signal and background events in training and testing sets
for i in range(len(Y_train)):
    if (Y_train[i] == 1):
        Y_train_signal += 1
    else:
        Y_train_background += 1

for i in range(len(Y_test)):
    if (Y_test[i] == 1):
        Y_test_signal += 1
    else:
        Y_test_background += 1

print("Signal proportion in training set ", 100*Y_train_signal/Y_train_background, "%")
print("Signal proportion in test set ", 100*Y_test_signal/Y_test_background, "%\n")


# Set hyperparameters for network
model_name = "my_model"
model = Sequential()
model.add(Dense(8, input_dim=10, activation='elu'))
model.add(Dense(6, activation='elu'))
model.add(Dense(24, activation='elu'))
model.add(Dense(12, activation='elu'))
model.add(Dense(6, activation='elu'))
model.add(Dense(1, activation='sigmoid')) #sigmoid/softmax

# Specify the training configuration (loss function, optimizer, metrics to monitor)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) 

# Training with fit() which slices data into batches and iterates over dataset for x epochs. history object stores training metrics (loss, metric values) per epoch
history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=50, batch_size=64)

# Save trained model (architecture, weights, optimizer state) to a file with name model_name
model.save(model_name)

# Save the history.history dict for later plotting
history_dict = pd.DataFrame(history.history)
history_csv = model_name + "history.csv"
with open(history_csv, mode='w') as f:
    history_dict.to_csv(f)

print(model.summary())

# Check model performance
Y_pred = model.predict(X_test)

predicted = list(np.round_(Y_pred, decimals=0)) 
test = list(Y_test)

ascore = accuracy_score(predicted, test)
print("\nTest dataset accuracy is: ", ascore*100)