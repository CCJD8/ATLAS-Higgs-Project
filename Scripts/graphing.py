import math
import ctypes
import numpy as np
from ROOT import *

# ===== Style and batch mode =====
gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasStyle.C')
gROOT.LoadMacro('/home/connor/atlasrootstyle/atlasrootstyle/AtlasUtils.C')
gROOT.SetBatch(kTRUE)
SetAtlasStyle()

PI = math.pi

# ===== ROOT canvas and pad setup =====
canv = TCanvas('c', 'c', 800, 800)
canv.cd()

overlay = TPad("overlay", "Transparent pad", 0, 0, 1, 1, -1, 300, 1)
overlay.SetFillStyle(4000)
overlay.Draw()
overlay.cd()
overlay.GetFrame().SetBorderSize(200)

# ===== Samples =====
# Grouped on the physical process modelled (Z+jets, llvv, other, ttb/Wt, diboson, ZH)
samples_group_by_process = [
    ("Z+jets", ["364100.Sh221_PDF30_Zmumu_MV0_70_CVBV.root","364101.Sh221_PDF30_Zmumu_MV0_70_CFBV.root","364102.Sh221_PDF30_Zmumu_MV0_70_BF.root","364103.Sh221_PDF30_Zmumu_MV70_140_CVBV.root","364104.Sh221_PDF30_Zmumu_MV70_140_CFBV.root","364105.Sh221_PDF30_Zmumu_MV70_140_BF.root","364106.Sh221_PDF30_Zmumu_MV140_280_CVBV.root","364107.Sh221_PDF30_Zmumu_MV140_280_CFBV.root","364108.Sh221_PDF30_Zmumu_MV140_280_BF.root","364109.Sh221_PDF30_Zmumu_MV280_500_CVBV.root","364110.Sh221_PDF30_Zmumu_MV280_500_CFBV.root","364111.Sh221_PDF30_Zmumu_MV280_500_BF.root","364112.Sh221_PDF30_Zmumu_MV500_1000.root","364113.Sh221_PDF30_Zmumu_MV1000_E_CMS.root","364114.Sh221_PDF30_Zee_MV0_70_CVBV.root","364115.Sh221_PDF30_Zee_MV0_70_CFBV.root","364116.Sh221_PDF30_Zee_MV0_70_BF.root","364117.Sh221_PDF30_Zee_MV70_140_CVBV.root","364118.Sh221_PDF30_Zee_MV70_140_CFBV.root","364119.Sh221_PDF30_Zee_MV70_140_BF.root","364120.Sh221_PDF30_Zee_MV140_280_CVBV.root","364121.Sh221_PDF30_Zee_MV140_280_CFBV.root","364122.Sh221_PDF30_Zee_MV140_280_BF.root","364123.Sh221_PDF30_Zee_MV280_500_CVBV.root","364124.Sh221_PDF30_Zee_MV280_500_CFBV.root","364125.Sh221_PDF30_Zee_MV280_500_BF.root","364126.Sh221_PDF30_Zee_MV500_1000.root","364127.Sh221_PDF30_Zee_MV1000_E_CMS.root","364128.Sh221_PDF30_Ztt_MV0_70_CVBV.root","364129.Sh221_PDF30_Ztt_MV0_70_CFBV.root","364130.Sh221_PDF30_Ztt_MV0_70_BF.root","364131.Sh221_PDF30_Ztt_MV70_140_CVBV.root","364132.Sh221_PDF30_Ztt_MV70_140_CFBV.root","364133.Sh221_PDF30_Ztt_MV70_140_BF.root","364134.Sh221_PDF30_Ztt_MV140_280_CVBV.root","364135.Sh221_PDF30_Ztt_MV140_280_CFBV.root","364136.Sh221_PDF30_Ztt_MV140_280_BF.root","364137.Sh221_PDF30_Ztt_MV280_500_CVBV.root","364138.Sh221_PDF30_Ztt_MV280_500_CFBV.root","364139.Sh221_PDF30_Ztt_MV280_500_BF.root","364140.Sh221_PDF30_Ztt_MV500_1000.root","364141.Sh221_PDF30_Ztt_MV1000_E_CMS.root","364216.Sh221_PDF30_Zmumu_PTV500_1000.root","364217.Sh221_PDF30_Zmumu_PTV1000_E_CMS.root","364218.Sh221_PDF30_Zee_PTV500_1000.root","364219.Sh221_PDF30_Zee_PTV1000_E_CMS.root","364220.Sh221_PDF30_Ztt_PTV500_1000.root","364221.Sh221_PDF30_Ztt_PTV1000_E_CMS.root"], kYellow),
    ("llvv", ["364254.Sh222_PDF30_llvv.root","364285.Sh222_PDF30_llvvjj_EW6.root","364286.Sh222_PDF30_llvvjj_ss_EW4.root","366088.Sh_222__llvvjj_ss_Min_N_TChannel.root"], kOrange+1),
    ("other", ["410218.aMcNloPy8_MEN30NLO_ttee.root","410219.aMcNloPy8_MEN30NLO_ttmumu.root","364244.Sh222_PDF30_WWZ_2l4v_EW6.root","364249.Sh222_PDF30_ZZZ_2l4v_EW6.root"], kRed),
    ("ttb/Wt", ["410472.PhPy8_A14_ttb_dil.root","410648.PoPy8_A14_Wt_DR_dilepton_top.root","410649.PoPy8_A14_Wt_DR_dilepton_atop.root"], kBlue-1), 
    ("diboson", ["700492.Sh_2211_WqqZll.root","700493.Sh_2211_ZqqZll.root","700494.Sh_2211_ZbbZll.root","364302.Sh222_PDF30_ggZllZqq.root"], kRed+2),
    ("ZH", ["345055.PoPy8_NNPDF3__ZH125J_MINLO_llbb_VpT.root","345057.PoPy8_NNPDF3__ggZH125_llbb.root"], kBlack)]

# Grouped signal or background process (Signal, Background)
samples_group_by_sb = [
    ("Signal", ["345055.PoPy8_NNPDF3__ZH125J_MINLO_llbb_VpT.root","345057.PoPy8_NNPDF3__ggZH125_llbb.root"], kRed), 
    ("Background", ["364100.Sh221_PDF30_Zmumu_MV0_70_CVBV.root","364101.Sh221_PDF30_Zmumu_MV0_70_CFBV.root","364102.Sh221_PDF30_Zmumu_MV0_70_BF.root","364103.Sh221_PDF30_Zmumu_MV70_140_CVBV.root","364104.Sh221_PDF30_Zmumu_MV70_140_CFBV.root","364105.Sh221_PDF30_Zmumu_MV70_140_BF.root","364106.Sh221_PDF30_Zmumu_MV140_280_CVBV.root","364107.Sh221_PDF30_Zmumu_MV140_280_CFBV.root","364108.Sh221_PDF30_Zmumu_MV140_280_BF.root","364109.Sh221_PDF30_Zmumu_MV280_500_CVBV.root","364110.Sh221_PDF30_Zmumu_MV280_500_CFBV.root","364111.Sh221_PDF30_Zmumu_MV280_500_BF.root","364112.Sh221_PDF30_Zmumu_MV500_1000.root","364113.Sh221_PDF30_Zmumu_MV1000_E_CMS.root","364114.Sh221_PDF30_Zee_MV0_70_CVBV.root","364115.Sh221_PDF30_Zee_MV0_70_CFBV.root","364116.Sh221_PDF30_Zee_MV0_70_BF.root","364117.Sh221_PDF30_Zee_MV70_140_CVBV.root","364118.Sh221_PDF30_Zee_MV70_140_CFBV.root","364119.Sh221_PDF30_Zee_MV70_140_BF.root","364120.Sh221_PDF30_Zee_MV140_280_CVBV.root","364121.Sh221_PDF30_Zee_MV140_280_CFBV.root","364122.Sh221_PDF30_Zee_MV140_280_BF.root","364123.Sh221_PDF30_Zee_MV280_500_CVBV.root","364124.Sh221_PDF30_Zee_MV280_500_CFBV.root","364125.Sh221_PDF30_Zee_MV280_500_BF.root","364126.Sh221_PDF30_Zee_MV500_1000.root","364127.Sh221_PDF30_Zee_MV1000_E_CMS.root","364128.Sh221_PDF30_Ztt_MV0_70_CVBV.root","364129.Sh221_PDF30_Ztt_MV0_70_CFBV.root","364130.Sh221_PDF30_Ztt_MV0_70_BF.root","364131.Sh221_PDF30_Ztt_MV70_140_CVBV.root","364132.Sh221_PDF30_Ztt_MV70_140_CFBV.root","364133.Sh221_PDF30_Ztt_MV70_140_BF.root","364134.Sh221_PDF30_Ztt_MV140_280_CVBV.root","364135.Sh221_PDF30_Ztt_MV140_280_CFBV.root","364136.Sh221_PDF30_Ztt_MV140_280_BF.root","364137.Sh221_PDF30_Ztt_MV280_500_CVBV.root","364138.Sh221_PDF30_Ztt_MV280_500_CFBV.root","364139.Sh221_PDF30_Ztt_MV280_500_BF.root","364140.Sh221_PDF30_Ztt_MV500_1000.root","364141.Sh221_PDF30_Ztt_MV1000_E_CMS.root","364216.Sh221_PDF30_Zmumu_PTV500_1000.root","364217.Sh221_PDF30_Zmumu_PTV1000_E_CMS.root","364218.Sh221_PDF30_Zee_PTV500_1000.root","364219.Sh221_PDF30_Zee_PTV1000_E_CMS.root","364220.Sh221_PDF30_Ztt_PTV500_1000.root","364221.Sh221_PDF30_Ztt_PTV1000_E_CMS.root","364254.Sh222_PDF30_llvv.root","364285.Sh222_PDF30_llvvjj_EW6.root","364286.Sh222_PDF30_llvvjj_ss_EW4.root","366088.Sh_222__llvvjj_ss_Min_N_TChannel.root","410218.aMcNloPy8_MEN30NLO_ttee.root","410219.aMcNloPy8_MEN30NLO_ttmumu.root","364244.Sh222_PDF30_WWZ_2l4v_EW6.root","364249.Sh222_PDF30_ZZZ_2l4v_EW6.root","410472.PhPy8_A14_ttb_dil.root","410648.PoPy8_A14_Wt_DR_dilepton_top.root","410649.PoPy8_A14_Wt_DR_dilepton_atop.root","700492.Sh_2211_WqqZll.root","700493.Sh_2211_ZqqZll.root","700494.Sh_2211_ZbbZll.root","364302.Sh222_PDF30_ggZllZqq.root"], kBlack)]

# ===== Features =====
feature_list = ['lep0_pt', 'lep1_pt', 'jet0_pt', 'jet1_pt', 'mll', 'mbb', 'pTdilep', 'deltaRjets', 'etabb', 'etall', 'n_jets', 'phibb', 'phill', 'metpt', 'cosll', 'coslminus', 'signedphi']
yield_feature_list = ['c1lep0_pt', 'c2lep0_pt', 'c3lep0_pt', 'c4lep0_pt', 'c5lep0_pt']

# ===== Helper Functions =====
def load_hist(files, var):
    """
    Get histogram for a particular feature (e.g. pTl0) with data from the files given in the files list.
    
    Args:
        files [str] - list of *.root files to be read (e.g. ["file_1.root","file_2.root"])
        var (str) - name of feature to be read from *.root file (e.g. "mbb")
        
    Returns:
        h_sum - TH1D histogram object of a particular feature (e.g. mbb) filled with data from the *.root files in files.
    """
    h_sum = None
    for path in files:
        f = TFile.Open(path, "READ")
        h. f.Get(var)
        if h_sum is None:
            h_sum = h.Clone()
            h_sum.SetDirectory(0)
        else:
            h_sum.Add(h)
        f.Close()
    return h_sum


# Set up histogram objects
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
stack_histograms = [stack_pTl0, stack_pTl1, stack_pTj0, stack_pTj1, stack_mll, stack_mbb, stack_pTdilep, stack_deltaRjets, stack_etabb, stack_etall, stack_n_jets, stack_phibb, stack_phill, stack_metpt, stack_cosll, stack_coslminus, stack_signedphi]

phiB = TH1D("phiB", "phiB; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiB.Sumw2()
phiS = TH1D("phiS", "phiS; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiS.Sumw2()
phiratio = TH1D("phiratio", "phiratio; Signed #Delta#phi (ll); S/sqrt(S+B)", 8, -PI, PI)
phiratio.Sumw2()

legend = TLegend(0.42, 0.8, 0.72, 0.9)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.SetEntrySeparation(0.3)
legend.SetTextFont(20)

# Iterate over each feature to create shape and stack plots 
for var in feature_list:
    nn_histos = []
    histos = []
    leg_names = []
    integrals = []
    
    # Iterate over each sample group
    # sample is a tuple of form: (label, list_of_files, color)
    #                              [0]        [1]        [2]
    for sample in samples_group_by_process:        
        histo = load_hist(sample[1], var)
        histo.SetMarkerColor(sample[2])
        histo.SetLineColor(sample[2])
        histo.SetLineWidth(3)
        
        nn_histo = histo.Clone()
        nn_histo.SetDirectory(0)
    
        if (histo.Integral() > 0):
            integrals.append(histo.Integral(0, histo.GetNbinsX()+1))
            histo.Scale(1 / histo.Integral())

        if histo.GetMaximum() > maximum:
            maximum = histo.GetMaximum()
        
        histos.append(histo)
        nn_histos.append(nn_histo)
        leg_names.append(sample[0])

    # Draw histograms    
    for i, _ in enumerate(histos):
        if i == 0:
            histos[i].SetMaximum(maximum * 1.3)
            histos[i].Draw('hist')
            stack_histograms[counter].Add(nn_histos[i])
        else:
            histos[i].Draw('histSAME')
            stack_histograms[counter].Add(nn_histos[i])

        histos[i].GetYaxis().SetTitleOffset(1.6)
        legend.AddEntry(histos[i], leg_names[i], 'l')
        
        
    legend.Draw('SAME')
    canv.SaveAs('ShapePlot_' + var + '.pdf')
    canv.Clear()

    stack_histograms[counter].Draw('hist')
    stack_histograms[counter].GetYaxis().SetTitleOffset(1.81)
    legend.Draw('SAME')
    canv.SaveAs('ShapePlot_stack' + var + '.pdf')
    canv.Clear()

    counter += 1


# Iterate over each feature to create signal/background ratio plots
for var in feature_list:
    maximum = -999.0
    
    # Iterate over each sample group
    # sample is a tuple of form: (label, list_of_files, color)
    #                              [0]        [1]        [2]
    for sample in samples_group_by_sb:
        
        # Signal histogram
        if sample[0] == "Signal":
            for i, _ in enumerate(sample[1]):
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


# Iterate over each feature to caluculate yields after successive selection cuts
for i, var in enumerate(yield_feature_list):
    cut_integrals = []
    cut_integrals_error = []
    maximum = -999.0

    # Iterate over each sample group
    # sample is a tuple of form: (label, list_of_files, color)
    #                              [0]        [1]        [2]
    for sample in samples_group_by_process:
        histo = load_hist(sample[1], var)
        cut_integrals.append(histo.Integral(0, histo.GetNbinsX()+1))
        error = ctypes.c_double()
        integral = histo.IntegralAndError(0, histo.GetNbinsX()+1, error)
        cut_integrals_error.append(error.value)
        
    total_background = cut_integrals[0] + cut_integrals[1] + cut_integrals[2] + cut_integrals[3] + cut_integrals[4]
    total_background_error = np.sqrt(cut_integrals_error[0]**2 + cut_integrals_error[2]**2 + cut_integrals_error[2]**2 + cut_integrals_error[3]**2 + cut_integrals_error[4]**2)
    SB = cut_integrals[5] / np.sqrt(cut_integrals[5] + total_background)
    SBerror = np.sqrt(((cut_integrals[5] + cut_integrals_error[5]) / np.sqrt(cut_integrals[5] + cut_integrals_error[5] + total_background) - SB)**2 + (cut_integrals[5] / np.sqrt(cut_integrals[5] + total_background + total_background_error) - SB)**2)
    
    print("==========================================================\nAfter cut", i, "the yields are:\n")
    print("Z+jets =", cut_integrals[0], "+-", cut_integrals_error[0])
    print("llvv =", cut_integrals[1], "+-", cut_integrals_error[1])
    print("other =", cut_integrals[2], "+-", cut_integrals_error[2])
    print("ttb/Wt =", cut_integrals[3], "+-", cut_integrals_error[3])
    print("diboson =", cut_integrals[4], "+-", cut_integrals_error[4])
    print("Total Background =", total_background, "+-", total_background_error)
    print("ZH =", cut_integrals[5], "+-", cut_integrals_error[5])
    print("\nS/B =", cut_integrals[5] / total_background)
    print("S/sqrt(S+B) = ", SB, "+-", SBerror)
    print("==========================================================")


# Significance scan for signed phi
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