import os
import sys
import math
import copy
import re
import argparse
import ROOT

def find_all_files_in_path(pattern, path):
    """
    Recursively finds all files in a directory tree that match the pattern. There can be wildcards in
    the path which can be resolved at any directory level (not just file level like in ROOT.TChain()).
    
    Args:
        pattern (str) - The pattern to be matched with optional wildcards (e.g. "dir/*/my_file.txt").
        path (str) - The starting directory path.
        
    Returns:
        list [str] - list of all files which match the pattern.
    """
    
    files = []
    items = pattern.split('/')
    
    def check_path(current_path, remaining_items):
        """Recursive helper function to traverse directories."""
        
        # End recursion if the end of the path is reached
        if not remaining_items:
            return
        
        my_items = copy.copy(remaining_items)
        item = my_items.pop(0)
        
        # Deal with wildcards
        if '*' in item:
            directory = ROOT.gSystem.OpenDirectory(current_path)
            regex_item = "^"+item.replace('*', '.*')+"$" # Create string regex version of item
            regex_pattern = re.compile(regex_item) # Create regex pattern object of item
            
            entry = True
            while entry:
                entry = ROOT.gSystem.GetDirEntry(directory)
                if regex_pattern.match(entry):
                    if not my_items:
                        files.append(current_path + entry)
                    else:
                        check_path(current_path + entry + '/', my_items)
                        
            ROOT.gSystem.FreeDirectory(directory)
            
        elif item and not my_items:
            files.append(current_path + item)
        else:
            check_path(current_path + item + '/', my_items)
            
    check_path(path, items)
    return files


def main(args):
    """
    Read all *.root files to create and fill ROOT histograms for each detector observable (feature).
    The five selection cuts are made on the data as prepreparation. Yields are also calculated
    following each of the five selection cuts.
    """
    
    directory = "/home/connor/" + args.inputsample
    pattern = "*.root"

    luminosity = 140000
    sum_of_weights = 0.0

    # Create TChain() object to chain together *.root files that contain "NOMINAL" tree ie. treat the separate files as one large dataset.
    tree = ROOT.TChain("NOMINAL")
    n_files = 0
    
    for file_name in find_all_files_in_path(pattern, directory):
        n_files += tree.Add(file_name)
        current_file = ROOT.TFile.Open(file_name, "READ")
        hist_metadata = current_file.Get("h_metadata")
        sum_of_weights += hist_metadata.GetBinContent(8)
    
    split_parts = args.inputsample.split(".")
    outputsample = split_parts[4] + "." + split_parts[5] + ".root"

    print()
    print(outputsample)

    # Define histograms
    pTl0 = ROOT.TH1D("lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    pTl0.SetLineWidth(2)
    pTl0.Sumw2()

    c1pTl0 = ROOT.TH1D("c1lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    c1pTl0.SetLineWidth(2)
    c1pTl0.Sumw2()

    c2pTl0 = ROOT.TH1D("c2lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    c2pTl0.SetLineWidth(2)
    c2pTl0.Sumw2()

    c3pTl0 = ROOT.TH1D("c3lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    c3pTl0.SetLineWidth(2)
    c3pTl0.Sumw2()

    c4pTl0 = ROOT.TH1D("c4lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    c4pTl0.SetLineWidth(2)
    c4pTl0.Sumw2()

    c5pTl0 = ROOT.TH1D("c5lep0_pt","p_{T}^{l_0}; Transverse Momentum [GeV]; Normalised counts" ,70,0 ,250)
    c5pTl0.SetLineWidth(2)
    c5pTl0.Sumw2()

    pTl1 = ROOT.TH1D("lep1_pt", "p_{T}^{l_1}; Transverse Momentum [GeV]; Normalised counts", 70, 0, 150)
    pTl1.SetLineWidth(2)
    pTl1.Sumw2()

    pTj0 = ROOT.TH1D("jet0_pt", "p_{T}^{jet_0}; Transverse momentum [GeV]; Normalised counts", 70, 0, 300)
    pTj0.SetLineWidth(2)
    pTj0.Sumw2()
    
    pTj1 = ROOT.TH1D("jet1_pt", "p_{T}^{jet_1}; Transverse momentum [GeV]; Normalised counts", 70, 0, 300)
    pTj1.SetLineWidth(2)
    pTj1.Sumw2()
    
    njets = ROOT.TH1D("n_jets", "Number of jets; Number of jets; Normalised counts", 20, 0, 20)
    njets.SetLineWidth(2)
    njets.Sumw2()

    Rjets = ROOT.TH1D("deltaRjets", "Angle between jets; Angular distance between jets (#Delta R); Normalised counts", 25, 0, 5)
    Rjets.SetLineWidth(2)
    Rjets.Sumw2()

    mll = ROOT.TH1D("mll", "Invariant mass of two leptons; Invariant mass [GeV]; Normalised counts", 50, 70, 110)
    mll.SetLineWidth(2)
    mll.Sumw2()

    pTdilep = ROOT.TH1D("pTdilep", "p_{T} of the dilepton system; Transverse momentum [GeV]; Normalised counts", 70, 0, 300)
    pTdilep.SetLineWidth(2)
    pTdilep.Sumw2()

    mbb = ROOT.TH1D("mbb", "Invariant mass of b-jets; Invariant mass [GeV]; Normalised counts", 70, 0, 250)
    mbb.SetLineWidth(2)
    mbb.Sumw2()

    phill = ROOT.TH1D("phill", "#Delta#phi between leptons; Angle #Delta#phi [Rads]; Normalised counts", 40, -4, 4)
    phill.SetLineWidth(2)
    phill.Sumw2()

    phibb = ROOT.TH1D("phibb", "#Delta#phi between b jets; Angle #Delta#phi [Rads]; Normalised counts", 40, -4, 4)
    phibb.SetLineWidth(2)
    phibb.Sumw2()

    etall = ROOT.TH1D("etall", "#Delta#eta between leptons; Angle #Delta#eta; Normalised counts", 20, 0, 4)
    etall.SetLineWidth(2)
    etall.Sumw2()

    etabb = ROOT.TH1D("etabb", "#Delta#eta between b jets; Angle #Delta#eta; Normalised counts", 20, 0, 4)
    etabb.SetLineWidth(2)
    etabb.Sumw2()

    metpt = ROOT.TH1D("metpt", "Missing transverse momentum; Missing transverse momentum [GeV]; Normalised counts", 50, 0, 100)
    metpt.SetLineWidth(2)
    metpt.Sumw2()

    cosll = ROOT.TH1D("cosll", "Cosine of angle between leptons; Cos(#Delta#phi); Normalised counts", 10, 0, 1)
    cosll.SetLineWidth(2)
    cosll.Sumw2()

    coslminus = ROOT.TH1D("coslminus", "Cosine of angle from negative lepton; Cos(#Delta#phi); Normalised counts", 10, 0, 1)
    coslminus.SetLineWidth(2)
    coslminus.Sumw2()

    signedphi = ROOT.TH1D("signedphi", "Signed #phi; Signed #phi; Normalised counts", 8, -math.pi, math.pi)
    signedphi.SetLineWidth(2)
    signedphi.Sumw2()

    # Loop over events
    for i in range(0, tree.GetEntries()):
        tree.GetEntry(i)
        p4_leptons = []
        p4_jets = []
        cut_twoLeptons = False
        cut_twoJets = False
        cut_deltaR = False
        cut_mbb = False
        cut_metpt = False

        # Cut on same flavour opposite charge leptons
        if ((getattr(tree, "lep_0") == getattr(tree, "lep_1")) and (getattr(tree, "lep_0_q") != getattr(tree, "lep_1_q"))):

            cut_twoLeptons = True

            # Calculate weights
            cross_section = getattr(tree, "cross_section")
            weight_mc = getattr(tree, "weight_mc")
            weight_pile = getattr(tree, "NOMINAL_pileup_combined_weight")
            wtotal = (weight_mc * weight_pile * cross_section * luminosity) / sum_of_weights

            # Cuts on b-tagging
            if ((getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_1_p4"))
                cut_twoJets = True

            if ((getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_2_p4"))
                cut_twoJets = True

            if ((getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True

            if ((getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_1_p4"))
                p4_jets.append(getattr(tree, "jet_2_p4"))
                cut_twoJets = True
            
            if ((getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_1_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True

            if ((getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1):
                p4_jets.append(getattr(tree, "jet_2_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True


            # Cut on delta R between b-jets
            if ((cut_twoJets == True) and (p4_jets[0].DeltaR(p4_jets[1]) > 0.5) and (p4_jets[0].DeltaR(p4_jets[1]) < 3.5)):
                cut_deltaR = True

            # Cut on mbb
            if ((cut_twoJets == True) and ((p4_jets[0]+p4_jets[1]).M() > 75) and ((p4_jets[0]+p4_jets[1]).M() < 145)):
                cut_mbb = True

            # Cut on metpt
            if (getattr(tree, "met_p4").Pt() < 52):
                cut_metpt = True


        # Fill histograms
            
        # Filling histograms after lepton flavour/charge cut
        if cut_twoLeptons:
            c1pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

        # Filling histograms after b-tagged jet cut
        if cut_twoLeptons and cut_twoJets:
            c2pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

        # Filling histograms after deltaR cut
        if cut_twoLeptons and cut_twoJets and cut_deltaR:
            c3pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

        # Filling histograms after mbb cut
        if cut_twoLeptons and cut_twoJets and cut_deltaR and cut_mbb:
            c4pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

        # Filling histograms after metpt
        if cut_twoLeptons and cut_twoJets and cut_deltaR and cut_mbb and cut_metpt:
            c5pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

            p4_leptons.append(getattr(tree, "lep_0_p4"))
            p4_leptons.append(getattr(tree, "lep_1_p4"))
            pTj0.Fill(p4_jets[0].Pt(), wtotal)
            pTj1.Fill(p4_jets[1].Pt(), wtotal)
            mbb.Fill((p4_jets[0]+p4_jets[1]).M(), wtotal)
            Rjets.Fill(p4_jets[0].DeltaR(p4_jets[1]), wtotal)
            phibb.Fill(p4_jets[0].DeltaPhi(p4_jets[1]), wtotal)
            etabb.Fill(abs(p4_jets[0].Eta() - p4_jets[1].Eta()), wtotal)
            cosll.Fill(ROOT.TMath.Cos(p4_jets[0].Phi() - p4_jets[1].Phi()), wtotal)
            
            pTl0.Fill(p4_leptons[0].Pt(), wtotal)
            pTl1.Fill(p4_leptons[1].Pt(), wtotal)
            njets.Fill(getattr(tree, "n_jets"), wtotal)
            mll.Fill((p4_leptons[0]+p4_leptons[1]).M(), wtotal)
            pTdilep.Fill(getattr(tree, "dilep_p4").Pt(), wtotal)
            phill.Fill(p4_leptons[0].DeltaPhi(p4_leptons[1]), wtotal)
            etall.Fill(abs(p4_leptons[0].Eta() - p4_leptons[1].Eta()), wtotal)
            metpt.Fill(getattr(tree, "met_p4").Pt(), wtotal)

            if (getattr(tree, "lep_0_q") == -1):
                coslminus.Fill(ROOT.TMath.Cos(p4_leptons[0].Phi() - (p4_leptons[0]+p4_leptons[1]).Phi()), wtotal)
            elif (getattr(tree, "lep_1_q") == -1):
                coslminus.Fill(ROOT.TMath.Cos(p4_leptons[1].Phi() - (p4_leptons[0]+p4_leptons[1]).Phi()), wtotal)

            if (p4_leptons[0].Eta() > p4_leptons[1].Eta()):
                signedphi.Fill(p4_leptons[0].DeltaPhi(p4_leptons[1]), wtotal)
            else:
                signedphi.Fill(p4_leptons[1].DeltaPhi(p4_leptons[0]), wtotal)

    # Integrate histograms
    intc1 = c1pTl0.Integral(0, c1pTl0.GetNbinsX()+1)
    intc2 = c2pTl0.Integral(0, c2pTl0.GetNbinsX()+1)
    intc3 = c3pTl0.Integral(0, c3pTl0.GetNbinsX()+1)
    intc4 = c4pTl0.Integral(0, c4pTl0.GetNbinsX()+1)
    intc5 = c5pTl0.Integral(0, c5pTl0.GetNbinsX()+1)
    print("The yield after cut 1 (lepton same flavour and different charge cut) is ",intc1)
    print("The yield after cut 2 (exactly two b-tagged jets) is                    ",intc2)
    print("The yield after cut 3 (delta R bounds) is                               ",intc3)
    print("The yield after cut 4 (mbb cut) is                                      ",intc4)
    print("The yield after cut 5 (metpt cut) is                                    ",intc5)


    outHistFile = ROOT.TFile.Open(outputsample ,"RECREATE") #args.outputfile
    outHistFile.cd()

    pTl0.Write()
    pTl1.Write()
    pTj0.Write()
    pTj1.Write()
    njets.Write()
    Rjets.Write()
    mll.Write()
    mbb.Write()
    pTdilep.Write()
    phill.Write()
    phibb.Write()
    etall.Write()
    etabb.Write()
    metpt.Write()
    cosll.Write()
    coslminus.Write()
    signedphi.Write()
    c1pTl0.Write()
    c2pTl0.Write()
    c3pTl0.Write()
    c4pTl0.Write()
    c5pTl0.Write()

    outHistFile.Close()

    del tree

if __name__ == "__main__":
    # Parse command line input arguments
    parser = argparse.ArgumentParser(description='script to run over ntuple dataset')
    parser.add_argument('--inputsample', '-i', metavar='INPUT', type=str, dest="inputsample", default="ZH_llbb_345055/", help='directory for input root files')
    parser.add_argument('--outputfile', '-o', metavar='OUTPUT', type=str, dest="outputfile", default="llbbhistograms.root", help='outputfile for process')
    args = parser.parse_args()

    # Call main function
    main(args)