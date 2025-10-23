import ROOT
import copy, os, re, sys
import argparse
import math

pi = math.pi

#COPY FROM test_ZHbb.py u

## Method to resolve regular expressions in file names.
#  TChain::Add only supports wildcards in the last items, i.e. on file level.
#  This method can resolve all wildcards at any directory level,
#  e.g. /my/directory/a*test*/pattern/*.root
#  @param pattern      the file name pattern using python regular expressions
#  @return list of all files matching the pattern
def findAllFilesInPath( pattern ,path ):
    files = []
    items = pattern.split( '/' )
    
    def checkPath( path, items ):
        # nested method to deal with the recursion
        import ROOT
        if not items:
            return
        myItems = copy.copy( items )
        item = myItems.pop(0)
        if '*' in item:
            directory = ROOT.gSystem.OpenDirectory( path )
            # beg and end of line control so that *truc does not match bla_truc_xyz
            item = "^"+item.replace( '*', '.*' )+"$"
            p = re.compile( item )
            entry = True
            while entry:
                entry = ROOT.gSystem.GetDirEntry( directory )
                if p.match( entry ):
                    if not myItems:
                        files.append( path + entry )
                    else:
                        checkPath( path + entry + '/', myItems)
            ROOT.gSystem.FreeDirectory( directory )
        elif item and not myItems:
            files.append( path + item )
        else:
            checkPath( path + item + '/', myItems )
    checkPath( path, items )
    return files





def main(args):
    directory = "/home/connor/"+args.inputsample
    pattern = "*.root"

    luminosity = 140000
    sumofweights = 0

    tree = ROOT.TChain( "NOMINAL" )
    nFiles = 0
    for fileName in findAllFilesInPath( pattern, directory ):
        nFiles += tree.Add( fileName )
        cFile = ROOT.TFile.Open(fileName, "READ")
        h = cFile.Get("h_metadata")
        sumofweights += h.GetBinContent(8)
    
    splitsec = args.inputsample.split(".")
    outputsample = splitsec[4]+"."+splitsec[5]+".root"

    print()
    print(outputsample)


    ####      define histograms  

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

    signedphi = ROOT.TH1D("signedphi", "Signed #phi; Signed #phi; Normalised counts", 8, -pi, pi)
    signedphi.SetLineWidth(2)
    signedphi.Sumw2()

    #event loop
    for i in range(0,tree.GetEntries()):
        tree.GetEntry(i)
        p4_leptons = []
        p4_jets = []
        cut_twoLeptons = False
        cut_twoJets = False
        cut_deltaR = False
        cut_mbb = False
        cut_metpt = False

        #cut for same flavour opposite charge leptons
        if ( (getattr(tree, "lep_0") == getattr(tree, "lep_1")) and (getattr(tree, "lep_0_q") != getattr(tree, "lep_1_q")) ):

            cut_twoLeptons = True

            #calculate weights
            cross_section = getattr(tree, "cross_section")
            weight_mc = getattr(tree, "weight_mc")
            weight_pile = getattr(tree, "NOMINAL_pileup_combined_weight")
            wtotal = weight_mc*weight_pile*cross_section*luminosity/(sumofweights)

            #cuts for b-tagging
            if ( (getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_1_p4"))
                cut_twoJets = True

            if ( (getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_2_p4"))
                cut_twoJets = True

            if ( (getattr(tree, "jet_0_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_0_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True

            if ( (getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_1_p4"))
                p4_jets.append(getattr(tree, "jet_2_p4"))
                cut_twoJets = True
            
            if ( (getattr(tree, "jet_1_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_1_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True

            if ( (getattr(tree, "jet_2_b_tagged_DL1r_FixedCutBEff_70")) == 1 and (getattr(tree, "jet_3_b_tagged_DL1r_FixedCutBEff_70")) == 1 ):
                p4_jets.append(getattr(tree, "jet_2_p4"))
                p4_jets.append(getattr(tree, "jet_3_p4"))
                cut_twoJets = True


            #cut for delta R between b-jets
            if ( (cut_twoJets == True) and  (p4_jets[0].DeltaR(p4_jets[1]) > 0.5) and (p4_jets[0].DeltaR(p4_jets[1]) < 3.5) ):
                cut_deltaR = True

            #cut for mbb
            if ( (cut_twoJets == True) and ((p4_jets[0]+p4_jets[1]).M() > 75) and ((p4_jets[0]+p4_jets[1]).M() < 145)  ):
                cut_mbb = True

            #cut for metpt
            if (  getattr(tree, "met_p4").Pt() < 52 ):
                cut_metpt = True


        #fill histograms
            
        #filling histograms after lepton flavour/charge cut
        if cut_twoLeptons == True:
            c1pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

            #filling histograms after b-tagged jet cut
            if cut_twoJets == True:
                c2pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

                #filling histograms after deltaR cut
                if cut_deltaR == True:
                    c3pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

                    #filling histograms after mbb cut
                    if cut_mbb == True:
                        c4pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

                        #filling histograms after metpt
                        if cut_metpt == True:
                            c5pTl0.Fill(getattr(tree, "lep_0_p4").Pt(), wtotal)

                            p4_leptons.append(getattr(tree, "lep_0_p4"))
                            p4_leptons.append(getattr(tree, "lep_1_p4"))
                            pTj0.Fill(p4_jets[0].Pt(), wtotal)
                            pTj1.Fill(p4_jets[1].Pt(), wtotal)
                            mbb.Fill((p4_jets[0]+p4_jets[1]).M(), wtotal)
                            Rjets.Fill(p4_jets[0].DeltaR(p4_jets[1]), wtotal)
                            phibb.Fill(p4_jets[0].DeltaPhi(p4_jets[1]), wtotal)
                            etabb.Fill(abs(p4_jets[0].Eta()-p4_jets[1].Eta()), wtotal)
                            cosll.Fill(ROOT.TMath.Cos(p4_jets[0].Phi()-p4_jets[1].Phi()), wtotal)
                            
                            pTl0.Fill(p4_leptons[0].Pt(), wtotal)
                            pTl1.Fill(p4_leptons[1].Pt(), wtotal)
                            njets.Fill(getattr(tree, "n_jets"), wtotal)
                            mll.Fill((p4_leptons[0]+p4_leptons[1]).M(), wtotal)
                            pTdilep.Fill(getattr(tree, "dilep_p4").Pt(), wtotal)
                            phill.Fill(p4_leptons[0].DeltaPhi(p4_leptons[1]), wtotal)
                            etall.Fill(abs(p4_leptons[0].Eta()-p4_leptons[1].Eta()), wtotal)
                            metpt.Fill(getattr(tree, "met_p4").Pt(), wtotal)

                            if (getattr(tree, "lep_0_q") == -1):
                                coslminus.Fill(ROOT.TMath.Cos(p4_leptons[0].Phi()-(p4_leptons[0]+p4_leptons[1]).Phi()), wtotal)
                            elif (getattr(tree, "lep_1_q") == -1):
                                coslminus.Fill(ROOT.TMath.Cos(p4_leptons[1].Phi()-(p4_leptons[0]+p4_leptons[1]).Phi()), wtotal)

                            if (p4_leptons[0].Eta() > p4_leptons[1].Eta()):
                                signedphi.Fill(p4_leptons[0].DeltaPhi(p4_leptons[1]), wtotal)
                            else:
                                signedphi.Fill(p4_leptons[1].DeltaPhi(p4_leptons[0]), wtotal)

    #integrate the histograms
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
    # parse the CLI arguments
    parser = argparse.ArgumentParser(description='script to run over ntuple dataset')
    parser.add_argument('--inputsample', '-i', metavar='INPUT', type=str, dest="inputsample", default="ZH_llbb_345055/", help='directory for input root files')
    parser.add_argument('--outputfile', '-o', metavar='OUTPUT', type=str, dest="outputfile", default="llbbhistograms.root", help='outputfile for process')
    args = parser.parse_args()

    # call the main function
    main(args);