## ATLAS-Higgs-Project
This repository hosts the programs used in the project "background reduction for the Higgs' associated ZH production and subsequent b-quark decay channel using deep neural networks trained on Standard Model generated data for the ATLAS detector".

<p align="center">
  <img src="https://github.com/user-attachments/assets/d00bd5cd-8cf7-44ec-9184-932aa99f61e6" alt="Tree-level-Feynman-diagram-of-the-associated-production-of-Higgs-boson" width="383" height="211"/>
  <br>
  <em>Figure 1: Tree level Feynman diagram for the associated production of the Higgs boson decaying hadronically to b-quarks.</em>
</p>

The signal isolation was achieved by the supervised training of deep neural network models in Python with TensorFlow. The large labelled dataset was created with event generators of Standard Model events. A label with numerical value of 1 indicated a ZH event. The trained models were then used to predict on unlabelled data and a signal-to-background isolation metric was established. The physics motivations for this project are largely set out by *Brehmer et al* in their paper on "Better Higgs-CP tests through information geometry" [1]. 

### Data Pre-Preparation






<br><br><br>

### References
[1] - Brehmer, J., Kling, F., Plehn, T., & Tait, T. M. (2018). Better Higgs-CP tests through information geometry. *Physical Review D*, 97(9), 095017.
