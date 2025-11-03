import math
import ctypes
import numpy as np
from ROOT import *

gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasStyle.C')
gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasUtils.C')
gROOT.SetBatch(kTRUE)
SetAtlasStyle()

PI = math.pi


canv = TCanvas('c', 'c', 800, 800)
canv.cd()

newpad = TPad("newpad", "Transparent pad", 0, 0, 1, 1, -1, 300, 1)
newpad.SetFillStyle(4000)
newpad.Draw()
newpad.cd()
newpad.GetFrame().SetBorderSize(200)

color_list = [kBlack, kRed, kBlue, kGreen, kViolet, kMagenta, kAzure, kViolet, kOrange, kYellow, kMagenta+3, kCyan, kYellow+2]

# Data files split into groups based on the physical process modelled (Z+jets, llvv, ttb/Wt, diboson, ZH, other)
samples = [
    ("Z+jets", ["364100.Sh221_PDF30_Zmumu_MV0_70_CVBV.root","364101.Sh221_PDF30_Zmumu_MV0_70_CFBV.root","364102.Sh221_PDF30_Zmumu_MV0_70_BF.root","364103.Sh221_PDF30_Zmumu_MV70_140_CVBV.root","364104.Sh221_PDF30_Zmumu_MV70_140_CFBV.root","364105.Sh221_PDF30_Zmumu_MV70_140_BF.root","364106.Sh221_PDF30_Zmumu_MV140_280_CVBV.root","364107.Sh221_PDF30_Zmumu_MV140_280_CFBV.root","364108.Sh221_PDF30_Zmumu_MV140_280_BF.root","364109.Sh221_PDF30_Zmumu_MV280_500_CVBV.root","364110.Sh221_PDF30_Zmumu_MV280_500_CFBV.root","364111.Sh221_PDF30_Zmumu_MV280_500_BF.root","364112.Sh221_PDF30_Zmumu_MV500_1000.root","364113.Sh221_PDF30_Zmumu_MV1000_E_CMS.root","364114.Sh221_PDF30_Zee_MV0_70_CVBV.root","364115.Sh221_PDF30_Zee_MV0_70_CFBV.root","364116.Sh221_PDF30_Zee_MV0_70_BF.root","364117.Sh221_PDF30_Zee_MV70_140_CVBV.root","364118.Sh221_PDF30_Zee_MV70_140_CFBV.root","364119.Sh221_PDF30_Zee_MV70_140_BF.root","364120.Sh221_PDF30_Zee_MV140_280_CVBV.root","364121.Sh221_PDF30_Zee_MV140_280_CFBV.root","364122.Sh221_PDF30_Zee_MV140_280_BF.root","364123.Sh221_PDF30_Zee_MV280_500_CVBV.root","364124.Sh221_PDF30_Zee_MV280_500_CFBV.root","364125.Sh221_PDF30_Zee_MV280_500_BF.root","364126.Sh221_PDF30_Zee_MV500_1000.root","364127.Sh221_PDF30_Zee_MV1000_E_CMS.root","364128.Sh221_PDF30_Ztt_MV0_70_CVBV.root","364129.Sh221_PDF30_Ztt_MV0_70_CFBV.root","364130.Sh221_PDF30_Ztt_MV0_70_BF.root","364131.Sh221_PDF30_Ztt_MV70_140_CVBV.root","364132.Sh221_PDF30_Ztt_MV70_140_CFBV.root","364133.Sh221_PDF30_Ztt_MV70_140_BF.root","364134.Sh221_PDF30_Ztt_MV140_280_CVBV.root","364135.Sh221_PDF30_Ztt_MV140_280_CFBV.root","364136.Sh221_PDF30_Ztt_MV140_280_BF.root","364137.Sh221_PDF30_Ztt_MV280_500_CVBV.root","364138.Sh221_PDF30_Ztt_MV280_500_CFBV.root","364139.Sh221_PDF30_Ztt_MV280_500_BF.root","364140.Sh221_PDF30_Ztt_MV500_1000.root","364141.Sh221_PDF30_Ztt_MV1000_E_CMS.root","364216.Sh221_PDF30_Zmumu_PTV500_1000.root","364217.Sh221_PDF30_Zmumu_PTV1000_E_CMS.root","364218.Sh221_PDF30_Zee_PTV500_1000.root","364219.Sh221_PDF30_Zee_PTV1000_E_CMS.root","364220.Sh221_PDF30_Ztt_PTV500_1000.root","364221.Sh221_PDF30_Ztt_PTV1000_E_CMS.root"], kYellow),
    ("llvv", ["364254.Sh222_PDF30_llvv.root","364285.Sh222_PDF30_llvvjj_EW6.root","364286.Sh222_PDF30_llvvjj_ss_EW4.root","366088.Sh_222__llvvjj_ss_Min_N_TChannel.root"], kOrange+1),
    ("other", ["410218.aMcNloPy8_MEN30NLO_ttee.root","410219.aMcNloPy8_MEN30NLO_ttmumu.root","364244.Sh222_PDF30_WWZ_2l4v_EW6.root","364249.Sh222_PDF30_ZZZ_2l4v_EW6.root"], kRed),
    ("ttb/Wt", ["410472.PhPy8_A14_ttb_dil.root","410648.PoPy8_A14_Wt_DR_dilepton_top.root","410649.PoPy8_A14_Wt_DR_dilepton_atop.root"], kBlue-1), 
    ("diboson", ["700492.Sh_2211_WqqZll.root","700493.Sh_2211_ZqqZll.root","700494.Sh_2211_ZbbZll.root","364302.Sh222_PDF30_ggZllZqq.root"], kRed+2),
    ("ZH", ["345055.PoPy8_NNPDF3__ZH125J_MINLO_llbb_VpT.root","345057.PoPy8_NNPDF3__ggZH125_llbb.root"], kBlack)]

# Data files split into two groups for either signal or background process (signal: ZH || background: Z+jets, llvv, ttb/Wt, diboson, other)
samples_sig_back = [
    ("Signal", ["345055.PoPy8_NNPDF3__ZH125J_MINLO_llbb_VpT.root","345057.PoPy8_NNPDF3__ggZH125_llbb.root"], kRed), 
    ("Background", ["364100.Sh221_PDF30_Zmumu_MV0_70_CVBV.root","364101.Sh221_PDF30_Zmumu_MV0_70_CFBV.root","364102.Sh221_PDF30_Zmumu_MV0_70_BF.root","364103.Sh221_PDF30_Zmumu_MV70_140_CVBV.root","364104.Sh221_PDF30_Zmumu_MV70_140_CFBV.root","364105.Sh221_PDF30_Zmumu_MV70_140_BF.root","364106.Sh221_PDF30_Zmumu_MV140_280_CVBV.root","364107.Sh221_PDF30_Zmumu_MV140_280_CFBV.root","364108.Sh221_PDF30_Zmumu_MV140_280_BF.root","364109.Sh221_PDF30_Zmumu_MV280_500_CVBV.root","364110.Sh221_PDF30_Zmumu_MV280_500_CFBV.root","364111.Sh221_PDF30_Zmumu_MV280_500_BF.root","364112.Sh221_PDF30_Zmumu_MV500_1000.root","364113.Sh221_PDF30_Zmumu_MV1000_E_CMS.root","364114.Sh221_PDF30_Zee_MV0_70_CVBV.root","364115.Sh221_PDF30_Zee_MV0_70_CFBV.root","364116.Sh221_PDF30_Zee_MV0_70_BF.root","364117.Sh221_PDF30_Zee_MV70_140_CVBV.root","364118.Sh221_PDF30_Zee_MV70_140_CFBV.root","364119.Sh221_PDF30_Zee_MV70_140_BF.root","364120.Sh221_PDF30_Zee_MV140_280_CVBV.root","364121.Sh221_PDF30_Zee_MV140_280_CFBV.root","364122.Sh221_PDF30_Zee_MV140_280_BF.root","364123.Sh221_PDF30_Zee_MV280_500_CVBV.root","364124.Sh221_PDF30_Zee_MV280_500_CFBV.root","364125.Sh221_PDF30_Zee_MV280_500_BF.root","364126.Sh221_PDF30_Zee_MV500_1000.root","364127.Sh221_PDF30_Zee_MV1000_E_CMS.root","364128.Sh221_PDF30_Ztt_MV0_70_CVBV.root","364129.Sh221_PDF30_Ztt_MV0_70_CFBV.root","364130.Sh221_PDF30_Ztt_MV0_70_BF.root","364131.Sh221_PDF30_Ztt_MV70_140_CVBV.root","364132.Sh221_PDF30_Ztt_MV70_140_CFBV.root","364133.Sh221_PDF30_Ztt_MV70_140_BF.root","364134.Sh221_PDF30_Ztt_MV140_280_CVBV.root","364135.Sh221_PDF30_Ztt_MV140_280_CFBV.root","364136.Sh221_PDF30_Ztt_MV140_280_BF.root","364137.Sh221_PDF30_Ztt_MV280_500_CVBV.root","364138.Sh221_PDF30_Ztt_MV280_500_CFBV.root","364139.Sh221_PDF30_Ztt_MV280_500_BF.root","364140.Sh221_PDF30_Ztt_MV500_1000.root","364141.Sh221_PDF30_Ztt_MV1000_E_CMS.root","364216.Sh221_PDF30_Zmumu_PTV500_1000.root","364217.Sh221_PDF30_Zmumu_PTV1000_E_CMS.root","364218.Sh221_PDF30_Zee_PTV500_1000.root","364219.Sh221_PDF30_Zee_PTV1000_E_CMS.root","364220.Sh221_PDF30_Ztt_PTV500_1000.root","364221.Sh221_PDF30_Ztt_PTV1000_E_CMS.root","364254.Sh222_PDF30_llvv.root","364285.Sh222_PDF30_llvvjj_EW6.root","364286.Sh222_PDF30_llvvjj_ss_EW4.root","366088.Sh_222__llvvjj_ss_Min_N_TChannel.root","410218.aMcNloPy8_MEN30NLO_ttee.root","410219.aMcNloPy8_MEN30NLO_ttmumu.root","364244.Sh222_PDF30_WWZ_2l4v_EW6.root","364249.Sh222_PDF30_ZZZ_2l4v_EW6.root","410472.PhPy8_A14_ttb_dil.root","410648.PoPy8_A14_Wt_DR_dilepton_top.root","410649.PoPy8_A14_Wt_DR_dilepton_atop.root","700492.Sh_2211_WqqZll.root","700493.Sh_2211_ZqqZll.root","700494.Sh_2211_ZbbZll.root","364302.Sh222_PDF30_ggZllZqq.root"], kBlack)]

integral_yields = ['c1lep0_pt', 'c2lep0_pt', 'c3lep0_pt', 'c4lep0_pt', 'c5lep0_pt']

feature_list = ['lep0_pt', 'lep1_pt', 'jet0_pt', 'jet1_pt', 'mll', 'mbb', 'pTdilep', 'deltaRjets', 'etabb', 'etall', 'n_jets', 'phibb', 'phill', 'metpt', 'cosll', 'coslminus', 'signedphi']

stack_pTl0 = THStack("stack_pTl0", "Stack plot; Transverse momentum [GeV]; Counts")
stack_pTl1 = THStack("stack_pTl1", "Stack plot; Transverse momentum [GeV]; Counts")
stack_pTj0 = THStack("stack_pTj0", "Stack plot; Transverse momentum [GeV]; Counts")
stack_pTj1 = THStack("stack_pTj1", "Stack plot; Transverse momentum [GeV]; Counts")
stack_mll = THStack("stack_mll", "Stack plot; Mass [GeV]; Counts")
stack_mbb = THStack("stack_mbb", "Stack plot; Mass [GeV]; Counts")
stack_pTdilep = THStack("stack_pTdilep", "Stack plot; Transverse momentum [GeV]; Counts")
stack_deltaRjets = THStack("stack_deltaRjets", "Angle between jets; Angular distance between jets (#Delta R); Counts")
stack_etabb = THStack("stack_etabb", "#Delta#eta between b jets; Angle #Delta#eta; Counts")
stack_etall = THStack("stack_etall", "#Delta#eta between leptons; Angle #Delta#eta; Counts")
stack_n_jets = THStack("stack_n_jets", "Number of jets; Number of jets; Counts")
stack_phibb = THStack("stack_phibb", "#Delta#phi between b jets; Angle #Delta#phi [Rads]; Counts")
stack_phill = THStack("stack_phill", "#Delta#phi between leptons; Angle #Delta#phi [Rads]; Counts")
stack_metpt = THStack("stack_metpt", "Missing transverse energy; Missing transverse energy [GeV]; Counts")
stack_cosll = THStack("stack_cosll", "Cosine of angle between leptons; Cos(#Delta#phi); Counts")
stack_coslminus = THStack("stack_coslminus", "Cosine of angle from negative lepton; Cos(#Delta#phi); Counts")
stack_signedphi = THStack("signedphi", "Signed #phi; Signed #phi; Counts")

phiB = TH1D("phiB", "phiB; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiB.Sumw2()
phiS = TH1D("phiS", "phiS; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiS.Sumw2()
phiratio = TH1D("phiratio", "phiratio; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiratio.Sumw2()

stack_histograms = [stack_pTl0, stack_pTl1, stack_pTj0, stack_pTj1, stack_mll, stack_mbb, stack_pTdilep, stack_deltaRjets, stack_etabb, stack_etall, stack_n_jets, stack_phibb, stack_phill, stack_metpt, stack_cosll, stack_coslminus, stack_signedphi]
 
cutcounter = 0

# Creating signal/background ratio plots
for var in feature_list:
    legend = TLegend(0.42, 0.8, 0.72, 0.9)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
    legend.SetEntrySeparation(0.3)
    legend.SetTextFont(20)
    maximum = -999.0

    # Iterate over each tuple where each sample is (label, list_of_files, color)
    for sample in samples_sig_back:
        no_of_root_files = len(sample[1])
        
        # Signal histogram
        if sample[0] == "Signal":
            for i in range(0, len(sample[1])):
                infile = TFile.Open(sample[1][i], "READ")
                
                if (i == 0):
                    signal_histo = infile.Get(var)
                    signal_histo.SetDirectory(0)
                    if var == "signedphi":
                        phiS.Add(signal_histo)
                else:
                    signal_histo.Add(infile.Get(var))
                    if var == "signedphi":
                        phiS.Add(signal_histo)
            
            infile.Close()
            #signal_histo.Scale(1/signal_histo.Integral())

        # Background histogram
        else: 
            for i in range(0, len(sample[1])):
                infile = TFile.Open(sample[1][i], "READ")
                
                if (i == 0):
                    background_histo = infile.Get(var)
                    background_histo.SetDirectory(0)
                    if var == "signedphi":
                        phiB.Add(background_histo)
                else:
                    background_histo.Add(infile.Get(var))
                    if var == "signedphi":
                        phiB.Add(background_histo)
            
            infile.Close()
            #background_histo.Scale(1/background_histo.Integral())
        
        
    ratiohistoup = signal_histo.Clone()
    ratiohistodown = signal_histo.Clone()
    maxx = signal_histo.GetNbinsX()+1

    for x in range(0, maxx):
        signalintup = signal_histo.Integral(0, x)
        backgroundintup = background_histo.Integral(0, x)
        signalintdown = signal_histo.Integral(x, maxx)
        backgroundintdown = background_histo.Integral(x, maxx)
        
        if ((signalintup + backgroundintup) != 0):
            ratioup = signalintup / np.sqrt(signalintup + backgroundintup)
        else:
            ratioup = 0
        if ((signalintdown + backgroundintdown) != 0):
            ratiodown = signalintdown / np.sqrt(signalintdown + backgroundintdown)
        else:
            ratiodown = 0

        ratiohistoup.SetBinContent(x, ratioup)
        ratiohistodown.SetBinContent(x, ratiodown)
        
    
    maxratioatup = str(round(ratiohistoup.GetBinLowEdge(ratiohistoup.FindFirstBinAbove(ratiohistoup.GetMaximum()-1e-9)), 2)) 
    maxratioatdown = str(round(ratiohistodown.GetBinLowEdge(ratiohistodown.FindFirstBinAbove(ratiohistodown.GetMaximum()-1e-9)), 2)) 
    ratiohistoup.SetMaximum(ratiohistoup.GetMaximum() * 1.3)
    ratiohistodown.SetMaximum(ratiohistodown.GetMaximum() * 1.3)
    ratiohistoup.SetYTitle("S/sqrt(S+B)")
    ratiohistodown.SetYTitle("S/sqrt(S+B)")
    

    ratiohistoup.Draw('hist')
    ratiohistodown.Draw('histSAME')
    legend.AddEntry(ratiohistoup, ("Upper cut point: " + maxratioatup), 'l')
    legend.AddEntry(ratiohistodown, ("Lower cut point: " + maxratioatdown), 'l')
    legend.Draw('SAME')
    canv.SaveAs('ratio_ShapePlot_' + var + '.pdf')
    canv.Clear()



# Calculating yields after successive selection cuts
for var in integral_yields:
    cuthistos = []
    cutintegrals = []
    cutintegralserror = []

    for sample in samples:
        for i in range(0, len(sample[1])):
            infile = TFile.Open(sample[1][i], "READ")
            if (i == 0):
                histo = infile.Get(var)
                histo.SetDirectory(0)
            else:
                histo.Add(infile.Get(var))
        infile.Close()

        cutintegrals.append(histo.Integral(0, histo.GetNbinsX()+1))

        ####################################################################################################
        error = ctypes.c_double()
        integral = histo.IntegralAndError(0, histo.GetNbinsX()+1, error)
        cutintegralserror.append(error.value)
    
    cutcounter += 1
    
    totalbackground = cutintegrals[0] + cutintegrals[1] + cutintegrals[2] + cutintegrals[3] + cutintegrals[4]
    totalbackgrounderror = np.sqrt(cutintegralserror[0]**2 + cutintegralserror[2]**2 + cutintegralserror[2]**2 + cutintegralserror[3]**2 + cutintegralserror[4]**2)
    SB = cutintegrals[5] / np.sqrt(cutintegrals[5] + totalbackground)
    SBerror = np.sqrt(((cutintegrals[5] + cutintegralserror[5]) / np.sqrt(cutintegrals[5] + cutintegralserror[5] + totalbackground) - SB)**2 + (cutintegrals[5] / np.sqrt(cutintegrals[5] + totalbackground + totalbackgrounderror) - SB)**2)
    
    print("==========================================================\nAfter cut", cutcounter, "the yields are:\n")
    print("Z+jets =", cutintegrals[0], "+-", cutintegralserror[0])
    print("llvv =", cutintegrals[1], "+-", cutintegralserror[1])
    print("other =", cutintegrals[2], "+-", cutintegralserror[2])
    print("ttb/Wt =", cutintegrals[3], "+-", cutintegralserror[3])
    print("diboson =", cutintegrals[4], "+-", cutintegralserror[4])
    print("Total Background =", totalbackground, "+-", totalbackgrounderror)
    print("ZH =", cutintegrals[5], "+-", cutintegralserror[5])
    print("\nS/B =", cutintegrals[5] / totalbackground)
    print("S/sqrt(S+B) = ", SB, "+-", SBerror)
    print("==========================================================")


counter = 0

for var in feature_list:
    legend = TLegend(0.58, 0.7, 0.68, 0.9)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.04)
    legend.SetEntrySeparation(0.3)
    legend.SetTextFont(20)
    NNhistos = []
    histos = []
    legnames = []
    integrals = []
    maximum = -999.0

    #read through signal and background files
    for sample in samples:

        for i in range(0, len(sample[1])):
            infile = TFile.Open(sample[1][i], "READ")
            
            if (i == 0):
                histo = infile.Get(var)
                histo.SetDirectory(0)
            else:
                histo.Add(infile.Get(var))
                
        
        infile.Close()
        
        NNhisto = histo.Clone()
        NNhisto.SetDirectory(0)
        

        legName = sample[0]
        if (histo.Integral() > 0):
            integrals.append(histo.Integral(0, histo.GetNbinsX()+1))
            histo.Scale(1 / histo.Integral())

        if histo.GetMaximum() > maximum:
            maximum = histo.GetMaximum()

        histo.SetMarkerColor(sample[2])
        histo.SetLineColor(sample[2])
        histo.SetLineWidth(3)
        histos.append(histo)

        NNhisto.SetMarkerColor(sample[2])
        NNhisto.SetLineColor(sample[2]) #original sample[2]
        NNhisto.SetLineWidth(3)
        NNhisto.SetFillColor(sample[2])
        NNhistos.append(NNhisto)

        legnames.append(legName)

    #draw histograms
    for i in range(0, len(histos)):
        if i == 0:
            histos[i].SetMaximum(maximum * 1.3)
            histos[i].Draw('hist')
            stack_histograms[counter].Add(NNhistos[i])
        else:
            histos[i].Draw('histSAME')
            stack_histograms[counter].Add(NNhistos[i])

        histos[i].GetYaxis().SetTitleOffset(1.6)
        #histos[i].GetXaxis().SetLabelSize(0.04)
        #histos[i].GetYaxis().SetLabelSize(0.04)
        #histos[i].GetXaxis().SetTitleSize(0.04)
        #histos[i].GetYaxis().SetTitleSize(0.04)

        legend.AddEntry(histos[i], legnames[i], 'l')

    legend.Draw('SAME')
    canv.SaveAs('ShapePlot_' + var + '.pdf')
    canv.Clear()

    
    stack_histograms[counter].Draw('hist')
    stack_histograms[counter].GetYaxis().SetTitleOffset(1.81)
    #stack_histograms[counter].GetXaxis().SetLabelSize(0.04)
    #stack_histograms[counter].GetYaxis().SetLabelSize(0.04)
    #stack_histograms[counter].GetXaxis().SetTitleSize(0.04)
    #stack_histograms[counter].GetYaxis().SetTitleSize(0.04)
    legend.Draw('SAME')
    canv.SaveAs('ShapePlot_stack' + var + '.pdf')
    canv.Clear()

    counter += 1

# SIGNED PHI SIGNIFICANCE SCAN

phiB.SetLineColor(kBlack)
phiS.SetLineColor(kRed)

for i in range(0, phiS.GetNbinsX()+1):
    if (phiS.GetBinContent(i) + phiB.GetBinContent(i)) != 0:
        ratio = phiS.GetBinContent(i) / np.sqrt(phiS.GetBinContent(i) + phiB.GetBinContent(i))
    else:
        ratio = 0
    phiratio.SetBinContent(i, ratio)

phiratio.Draw("HIST")
canv.SaveAs('ratio_perbin_signedphi.pdf')
canv.Clear()

print()