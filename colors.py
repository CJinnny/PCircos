'''
This code is used for:
    to_rgb: convert color name to rgb values, color names are copied from Circos
    palatte: make palatte for heatmap
'''

import numpy as np
import colorlover as cl
import random

def to_rgb(query, strict=False):
    rgb_dict={'white':'rgb(255,255,255)',
            'vvvvlgrey':'rgb(250,250,250)',
            'vvvlgrey':'rgb(240,240,240)',
            'vvlgrey':'rgb(230,230,230)',
            'vlgrey':'rgb(220,220,220)',
            'lgrey':'rgb(210,210,210)',
            'grey':'rgb(200,200,200)',
            'dgrey':'rgb(170,170,170)',
            'vdgrey':'rgb(140,140,140)',
            'vvdgrey':'rgb(100,100,100)',
            'vvvdgrey':'rgb(70,70,70)',
            'vvvvdgrey':'rgb(40,40,40)',
            'black':'rgb(0,0,0)',
            'vlred':'rgb(255,193,200)',
            'lred':'rgb(255,122,137)',
            'red':'rgb(247,42,66)',
            'dred':'rgb(205,51,69)',
            'vdred':'rgb(143,36,48)',
            'vvdred':'rgb(67,0,8)',
            'vlgreen':'rgb(204,255,218)',
            'lgreen':'rgb(128,255,164)',
            'green':'rgb(51,204,94)',
            'dgreen':'rgb(38,153,71)',
            'vvdgreen':'rgb(0,52,21)',
            'vlblue':'rgb(128,176,255)',
            'lblue':'rgb(64,137,255)',
            'blue':'rgb(54,116,217)',
            'dblue':'rgb(38,82,153)',
            'lpurple':'rgb(236,64,255)',
            'purple':'rgb(189,51,204)',
            'dpurple':'rgb(118,32,128)',
            'vlyellow':'rgb(255,253,202)',
            'lyellow':'rgb(255,252,150)',
            'yellow':'rgb(255,255,0)',
            'dyellow':'rgb(191,186,48)',
            'lime':'rgb(186,255,0)',
            'vlorange':'rgb(255,228,193)',
            'lorange':'rgb(255,187,110)',
            'orange':'rgb(255,136,0)',
            'dorange':'rgb(221,143,55)',
            'gpos100':'rgb(0,0,0)',
            'gpos':'rgb(0,0,0)',
            'gpos75':'rgb(130,130,130)',
            'gpos66':'rgb(160,160,160)',
            'gpos50':'rgb(200,200,200)',
            'gpos33':'rgb(210,210,210)',
            'gpos25':'rgb(200,200,200)',
            'gvar':'rgb(220,220,220)',
            'gneg':'rgb(255,255,255)',
            'acen':'rgb(217,47,39)',
            'stalk':'rgb(100,127,164)',
            'select':'rgb(135,177,255)',
            'chr1':'rgb(153,102,0)',
            'chr2':'rgb(102,102,0)',
            'chr3':'rgb(153,153,30)',
            'chr4':'rgb(204,0,0)',
            'chr5':'rgb(255,0,0)',
            'chr6':'rgb(255,0,204)',
            'chr7':'rgb(255,204,204)',
            'chr8':'rgb(255,153,0)',
            'chr9':'rgb(255,204,0)',
            'chr10':'rgb(255,255,0)',
            'chr11':'rgb(204,255,0)',
            'chr12':'rgb(0,255,0)',
            'chr13':'rgb(53,128,0)',
            'chr14':'rgb(0,0,204)',
            'chr15':'rgb(102,153,255)',
            'chr16':'rgb(153,204,255)',
            'chr17':'rgb(0,255,255)',
            'chr18':'rgb(204,255,255)',
            'chr19':'rgb(153,0,204)',
            'chr20':'rgb(204,51,255)',
            'chr21':'rgb(204,153,255)',
            'chr22':'rgb(102,102,102)',
            'chr23':'rgb(153,153,153)',
            'chrx':'rgb(153,153,153)',
            'chr24':'rgb(204,204,204)',
            'chry':'rgb(204,204,204)',
            'chrM':'rgb(204,204,153)',
            'chr0':'rgb(204,204,153)',
            'chrUn':'rgb(121,204,61)',
            'chrNA':'rgb(255,255,255)',
            'lum70chr1':'rgb(216,161,97)',
            'lum70chr2':'rgb(175,175,108)',
            'lum70chr3':'rgb(176,176,69)',
            'lum70chr4':'rgb(255,108,108)',
            'lum70chr5':'rgb(255,84,84)',
            'lum70chr6':'rgb(255,83,237)',
            'lum70chr7':'rgb(209,159,159)',
            'lum70chr8':'rgb(248,147,0)',
            'lum70chr9':'rgb(214,165,0)',
            'lum70chr10':'rgb(179,179,0)',
            'lum70chr11':'rgb(140,188,0)',
            'lum70chr12':'rgb(0,204,0)',
            'lum70chr13':'rgb(118,188,96)',
            'lum70chr14':'rgb(158,158,255)',
            'lum70chr15':'rgb(121,169,255)',
            'lum70chr16':'rgb(123,176,226)',
            'lum70chr17':'rgb(0,196,196)',
            'lum70chr18':'rgb(128,181,181)',
            'lum70chr19':'rgb(223,132,255)',
            'lum70chr20':'rgb(242,114,255)',
            'lum70chr21':'rgb(200,149,251)',
            'lum70chr22':'rgb(102,102,102)',
            'lum70chr23':'rgb(153,153,153)',
            'lum70chrX':'rgb(153,153,153)',
            'lum70chr24':'rgb(204,204,204)',
            'lum70chrY':'rgb(204,204,204)',
            'lum70chrM':'rgb(174,174,122)',
            'lum70chr0':'rgb(174,174,122)',
            'lum70chrUn':'rgb(108,191,38)',
            'lum70chrNA':'rgb(171,171,171)',
            'lum80chr1':'rgb(244,188,127)',
            'lum80chr2':'rgb(202,202,136)',
            'lum80chr3':'rgb(203,203,103)',
            'lum80chr4':'rgb(255,137,137)',
            'lum80chr5':'rgb(255,116,116)',
            'lum80chr6':'rgb(255,119,255)',
            'lum80chr7':'rgb(237,186,186)',
            'lum80chr8':'rgb(255,174,62)',
            'lum80chr9':'rgb(243,192,0)',
            'lum80chr10':'rgb(206,206,0)',
            'lum80chr11':'rgb(166,216,0)',
            'lum80chr12':'rgb(0,232,0)',
            'lum80chr13':'rgb(146,216,126)',
            'lum80chr14':'rgb(186,186,255)',
            'lum80chr15':'rgb(152,196,255)',
            'lum80chr16':'rgb(152,203,254)',
            'lum80chr17':'rgb(0,224,224)',
            'lum80chr18':'rgb(156,208,208)',
            'lum80chr19':'rgb(250,161,255)',
            'lum80chr20':'rgb(255,146,255)',
            'lum80chr21':'rgb(227,177,255)',
            'lum80chr22':'rgb(198,198,198)',
            'lum80chr23':'rgb(153,153,153)',
            'lum80chrX':'rgb(153,153,153)',
            'lum80chr24':'rgb(204,204,204)',
            'lum80chrY':'rgb(204,204,204)',
            'lum80chrM':'rgb(174,174,122)',
            'lum80chr0':'rgb(174,174,122)',
            'lum80chrUn':'rgb(108,191,38)',
            'lum80chrNA':'rgb(171,171,171)',
            'lum90chr1':'rgb(255,216,156)',
            'lum90chr2':'rgb(230,230,165)',
            'lum90chr3':'rgb(232,232,135)',
            'lum90chr4':'rgb(255,166,166)',
            'lum90chr5':'rgb(255,147,147)',
            'lum90chr6':'rgb(255,152,255)',
            'lum90chr7':'rgb(255,214,214)',
            'lum90chr8':'rgb(255,202,102)',
            'lum90chr9':'rgb(255,220,58)',
            'lum90chr10':'rgb(234,234,0)',
            'lum90chr11':'rgb(194,245,0)',
            'lum90chr12':'rgb(34,255,34)',
            'lum90chr13':'rgb(174,244,155)',
            'lum90chr14':'rgb(215,215,255)',
            'lum90chr15':'rgb(182,224,255)',
            'lum90chr16':'rgb(182,231,255)',
            'lum90chr17':'rgb(0,252,252)',
            'lum90chr18':'rgb(185,236,236)',
            'lum90chr19':'rgb(255,191,255)',
            'lum90chr20':'rgb(255,177,255)',
            'lum90chr21':'rgb(255,206,255)',
            'lum90chr22':'rgb(198,198,198)',
            'lum90chr23':'rgb(153,153,153)',
            'lum90chrX':'rgb(153,153,153)',
            'lum90chr24':'rgb(204,204,204)',
            'lum90chrY':'rgb(204,204,204)',
            'lum90chrM':'rgb(174,174,122)',
            'lum90chr0':'rgb(174,174,122)',
            'lum90chrUn':'rgb(108,191,38)',
            'lum90chrNA':'rgb(171,171,171)'
            }

    rgb_val_list = []
    for i in range(len(query)):
        key=query[i]
        if strict==True:
            if key not in rgb_dict.keys():
                raise ValueError('Color keys are not found in our dictionary!')
            else:
                rgb_val_list.append(rgb_dict[key])
        else:
            if key in rgb_dict.keys():
                rgb_val_list.append(rgb_dict[key])
            else:
                rgb_val_list.append(key)
        
    return np.array(rgb_val_list)

def palatte(heatmap_ncol=11, heatmap_scale='div', heatmap_palatte='RdBu', reverse=True):
    palatte = cl.scales[str(heatmap_ncol)][heatmap_scale][heatmap_palatte]
    if reverse == True:
        return palatte.reverse()
    else:
        return palatte

def random_rgb(length, seed=0):
    # a list of 710 rgb colors
    rgb_pool = ['rgb(0,0,0)', 'rgb(0,0,0)', 'rgb(0,0,0)', 'rgb(0,0,128)', 'rgb(0,0,139)', 'rgb(0,0,204)', 'rgb(0,0,205)', 'rgb(0,0,238)', 'rgb(0,0,255)', 'rgb(0,100,0)', 'rgb(0,104,139)', 'rgb(0,128,0)', 'rgb(0,128,128)', 'rgb(0,134,139)', 'rgb(0,139,0)', 'rgb(0,139,139)', 'rgb(0,139,69)', 'rgb(0,154,205)', 'rgb(0,178,238)', 'rgb(0,191,255)', 'rgb(0,196,196)', 'rgb(0,197,205)', 'rgb(0,199,140)', 'rgb(0,201,87)', 'rgb(0,204,0)', 'rgb(0,205,0)', 'rgb(0,205,102)', 'rgb(0,205,205)', 'rgb(0,206,209)', 'rgb(0,224,224)', 'rgb(0,229,238)', 'rgb(0,232,0)', 'rgb(0,238,0)', 'rgb(0,238,118)', 'rgb(0,238,238)', 'rgb(0,245,255)', 'rgb(0,250,154)', 'rgb(0,252,252)', 'rgb(0,255,0)', 'rgb(0,255,0)', 'rgb(0,255,127)', 'rgb(0,255,255)', 'rgb(0,255,255)', 'rgb(0,52,21)', 'rgb(100,100,100)', 'rgb(100,127,164)', 'rgb(100,149,237)', 'rgb(10,10,10)', 'rgb(102,102,0)', 'rgb(102,102,102)', 'rgb(102,102,102)', 'rgb(102,102,102)', 'rgb(102,139,139)', 'rgb(102,153,255)', 'rgb(102,205,0)', 'rgb(102,205,170)', 'rgb(104,131,139)', 'rgb(104,34,139)', 'rgb(105,105,105)', 'rgb(105,139,105)', 'rgb(105,139,34)', 'rgb(105,89,205)', 'rgb(106,90,205)', 'rgb(107,107,107)', 'rgb(107,142,35)', 'rgb(108,123,139)', 'rgb(108,166,205)', 'rgb(108,191,38)', 'rgb(108,191,38)', 'rgb(108,191,38)', 'rgb(110,110,110)', 'rgb(110,123,139)', 'rgb(110,139,61)', 'rgb(112,112,112)', 'rgb(112,128,144)', 'rgb(113,113,198)', 'rgb(113,198,113)', 'rgb(115,115,115)', 'rgb(117,117,117)', 'rgb(118,188,96)', 'rgb(118,238,0)', 'rgb(118,238,198)', 'rgb(118,32,128)', 'rgb(119,136,153)', 'rgb(120,120,120)', 'rgb(121,169,255)', 'rgb(121,204,61)', 'rgb(121,205,205)', 'rgb(122,103,238)', 'rgb(122,122,122)', 'rgb(122,139,139)', 'rgb(122,197,205)', 'rgb(122,55,139)', 'rgb(123,104,238)', 'rgb(123,176,226)', 'rgb(124,205,124)', 'rgb(124,252,0)', 'rgb(125,125,125)', 'rgb(125,158,192)', 'rgb(125,38,205)', 'rgb(126,192,238)', 'rgb(127,127,127)', 'rgb(127,255,0)', 'rgb(127,255,212)', 'rgb(128,0,0)', 'rgb(128,0,128)', 'rgb(128,128,0)', 'rgb(128,128,105)', 'rgb(128,128,128)', 'rgb(128,138,135)', 'rgb(128,176,255)', 'rgb(128,181,181)', 'rgb(128,255,164)', 'rgb(130,130,130)', 'rgb(130,130,130)', 'rgb(131,111,255)', 'rgb(131,139,131)', 'rgb(131,139,139)', 'rgb(13,13,13)', 'rgb(132,112,255)', 'rgb(132,132,132)', 'rgb(133,133,133)', 'rgb(135,135,135)', 'rgb(135,177,255)', 'rgb(135,206,235)', 'rgb(135,206,250)', 'rgb(135,206,255)', 'rgb(135,38,87)', 'rgb(137,104,205)', 'rgb(138,138,138)', 'rgb(138,43,226)', 'rgb(138,51,36)', 'rgb(138,54,15)', 'rgb(139,0,0)', 'rgb(139,0,139)', 'rgb(139,101,8)', 'rgb(139,102,139)', 'rgb(139,105,105)', 'rgb(139,105,20)', 'rgb(139,10,80)', 'rgb(139,115,85)', 'rgb(139,117,0)', 'rgb(139,119,101)', 'rgb(139,121,94)', 'rgb(139,123,139)', 'rgb(139,125,107)', 'rgb(139,125,123)', 'rgb(139,126,102)', 'rgb(139,129,76)', 'rgb(139,131,120)', 'rgb(139,131,134)', 'rgb(139,134,130)', 'rgb(139,134,78)', 'rgb(139,136,120)', 'rgb(139,137,112)', 'rgb(139,137,137)', 'rgb(139,139,0)', 'rgb(139,139,122)', 'rgb(139,139,131)', 'rgb(139,26,26)', 'rgb(139,28,98)', 'rgb(139,34,82)', 'rgb(139,35,35)', 'rgb(139,37,0)', 'rgb(139,54,38)', 'rgb(139,58,58)', 'rgb(139,58,98)', 'rgb(139,62,47)', 'rgb(139,69,0)', 'rgb(139,69,19)', 'rgb(139,71,137)', 'rgb(139,71,38)', 'rgb(139,71,93)', 'rgb(139,76,57)', 'rgb(139,87,66)', 'rgb(139,90,0)', 'rgb(139,90,43)', 'rgb(139,95,101)', 'rgb(139,99,108)', 'rgb(140,140,140)', 'rgb(140,140,140)', 'rgb(140,188,0)', 'rgb(141,182,205)', 'rgb(141,238,238)', 'rgb(142,142,142)', 'rgb(142,142,56)', 'rgb(142,229,238)', 'rgb(142,56,142)', 'rgb(143,143,143)', 'rgb(143,188,143)', 'rgb(143,36,48)', 'rgb(144,238,144)', 'rgb(145,145,145)', 'rgb(145,44,238)', 'rgb(146,216,126)', 'rgb(147,112,219)', 'rgb(148,0,211)', 'rgb(148,148,148)', 'rgb(150,150,150)', 'rgb(150,205,205)', 'rgb(151,255,255)', 'rgb(15,15,15)', 'rgb(152,196,255)', 'rgb(152,203,254)', 'rgb(152,245,255)', 'rgb(152,251,152)', 'rgb(153,0,204)', 'rgb(153,102,0)', 'rgb(153,153,153)', 'rgb(153,153,153)', 'rgb(153,153,153)', 'rgb(153,153,153)', 'rgb(153,153,153)', 'rgb(153,153,30)', 'rgb(153,204,255)', 'rgb(153,50,204)', 'rgb(154,192,205)', 'rgb(154,205,50)', 'rgb(154,255,154)', 'rgb(154,50,205)', 'rgb(155,205,155)', 'rgb(155,48,255)', 'rgb(156,102,31)', 'rgb(156,156,156)', 'rgb(156,208,208)', 'rgb(158,158,158)', 'rgb(158,158,255)', 'rgb(159,121,238)', 'rgb(159,182,205)', 'rgb(160,160,160)', 'rgb(160,82,45)', 'rgb(161,161,161)', 'rgb(162,181,205)', 'rgb(162,205,90)', 'rgb(163,163,163)', 'rgb(164,211,238)', 'rgb(165,42,42)', 'rgb(166,166,166)', 'rgb(166,216,0)', 'rgb(16,78,139)', 'rgb(168,168,168)', 'rgb(169,169,169)', 'rgb(170,170,170)', 'rgb(170,170,170)', 'rgb(171,130,255)', 'rgb(171,171,171)', 'rgb(171,171,171)', 'rgb(171,171,171)', 'rgb(171,171,171)', 'rgb(173,173,173)', 'rgb(173,216,230)', 'rgb(173,255,47)', 'rgb(174,174,122)', 'rgb(174,174,122)', 'rgb(174,174,122)', 'rgb(174,238,238)', 'rgb(174,244,155)', 'rgb(175,175,108)', 'rgb(176,176,176)', 'rgb(176,176,69)', 'rgb(176,196,222)', 'rgb(176,224,230)', 'rgb(176,226,255)', 'rgb(178,223,238)', 'rgb(178,34,34)', 'rgb(178,58,238)', 'rgb(179,179,0)', 'rgb(179,179,179)', 'rgb(179,238,58)', 'rgb(180,205,205)', 'rgb(180,238,180)', 'rgb(180,82,205)', 'rgb(181,181,181)', 'rgb(18,18,18)', 'rgb(182,224,255)', 'rgb(182,231,255)', 'rgb(183,183,183)', 'rgb(184,134,11)', 'rgb(184,184,184)', 'rgb(185,211,238)', 'rgb(185,236,236)', 'rgb(186,186,186)', 'rgb(186,186,255)', 'rgb(186,255,0)', 'rgb(186,85,211)', 'rgb(187,255,255)', 'rgb(188,143,143)', 'rgb(188,210,238)', 'rgb(188,238,104)', 'rgb(189,183,107)', 'rgb(189,189,189)', 'rgb(189,252,201)', 'rgb(189,51,204)', 'rgb(191,186,48)', 'rgb(191,191,191)', 'rgb(191,239,255)', 'rgb(191,62,255)', 'rgb(192,192,192)', 'rgb(192,255,62)', 'rgb(193,193,193)', 'rgb(193,205,193)', 'rgb(193,205,205)', 'rgb(193,255,193)', 'rgb(194,194,194)', 'rgb(194,245,0)', 'rgb(196,196,196)', 'rgb(197,193,170)', 'rgb(198,113,113)', 'rgb(198,198,198)', 'rgb(198,198,198)', 'rgb(198,226,255)', 'rgb(199,199,199)', 'rgb(199,21,133)', 'rgb(199,97,20)', 'rgb(200,149,251)', 'rgb(200,200,200)', 'rgb(200,200,200)', 'rgb(200,200,200)', 'rgb(201,201,201)', 'rgb(20,20,20)', 'rgb(202,202,136)', 'rgb(202,225,255)', 'rgb(202,255,112)', 'rgb(203,203,103)', 'rgb(204,0,0)', 'rgb(204,153,255)', 'rgb(204,204,153)', 'rgb(204,204,204)', 'rgb(204,204,204)', 'rgb(204,204,204)', 'rgb(204,204,204)', 'rgb(204,204,204)', 'rgb(204,255,0)', 'rgb(204,255,218)', 'rgb(204,255,255)', 'rgb(204,51,255)', 'rgb(205,0,0)', 'rgb(205,0,205)', 'rgb(205,102,0)', 'rgb(205,102,29)', 'rgb(205,104,137)', 'rgb(205,104,57)', 'rgb(205,105,201)', 'rgb(205,112,84)', 'rgb(205,129,98)', 'rgb(205,133,0)', 'rgb(205,133,63)', 'rgb(205,140,149)', 'rgb(205,145,158)', 'rgb(205,149,12)', 'rgb(205,150,205)', 'rgb(205,155,155)', 'rgb(205,155,29)', 'rgb(205,16,118)', 'rgb(205,170,125)', 'rgb(205,173,0)', 'rgb(205,175,149)', 'rgb(205,179,139)', 'rgb(205,181,205)', 'rgb(205,183,158)', 'rgb(205,183,181)', 'rgb(205,186,150)', 'rgb(205,190,112)', 'rgb(205,192,176)', 'rgb(205,193,197)', 'rgb(205,197,191)', 'rgb(205,198,115)', 'rgb(205,200,177)', 'rgb(205,201,165)', 'rgb(205,201,201)', 'rgb(205,205,0)', 'rgb(205,205,180)', 'rgb(205,205,193)', 'rgb(205,38,38)', 'rgb(205,41,144)', 'rgb(205,50,120)', 'rgb(205,51,51)', 'rgb(205,51,69)', 'rgb(205,55,0)', 'rgb(205,79,57)', 'rgb(205,85,85)', 'rgb(205,91,69)', 'rgb(205,92,92)', 'rgb(205,96,144)', 'rgb(206,206,0)', 'rgb(207,207,207)', 'rgb(208,32,144)', 'rgb(209,159,159)', 'rgb(209,209,209)', 'rgb(209,238,238)', 'rgb(209,95,238)', 'rgb(210,105,30)', 'rgb(210,180,140)', 'rgb(210,210,210)', 'rgb(210,210,210)', 'rgb(211,211,211)', 'rgb(212,212,212)', 'rgb(214,165,0)', 'rgb(214,214,214)', 'rgb(215,215,255)', 'rgb(216,161,97)', 'rgb(216,191,216)', 'rgb(217,217,217)', 'rgb(217,47,39)', 'rgb(218,112,214)', 'rgb(218,165,32)', 'rgb(219,112,147)', 'rgb(219,219,219)', 'rgb(220,20,60)', 'rgb(220,220,220)', 'rgb(220,220,220)', 'rgb(220,220,220)', 'rgb(221,143,55)', 'rgb(221,160,221)', 'rgb(222,184,135)', 'rgb(222,222,222)', 'rgb(223,132,255)', 'rgb(224,102,255)', 'rgb(224,224,224)', 'rgb(224,238,224)', 'rgb(224,238,238)', 'rgb(224,255,255)', 'rgb(227,168,105)', 'rgb(227,177,255)', 'rgb(227,207,87)', 'rgb(227,227,227)', 'rgb(229,229,229)', 'rgb(230,230,165)', 'rgb(230,230,230)', 'rgb(230,230,250)', 'rgb(232,232,135)', 'rgb(232,232,232)', 'rgb(23,23,23)', 'rgb(233,150,122)', 'rgb(234,234,0)', 'rgb(234,234,234)', 'rgb(235,235,235)', 'rgb(236,64,255)', 'rgb(237,145,33)', 'rgb(237,186,186)', 'rgb(237,237,237)', 'rgb(238,0,0)', 'rgb(238,0,238)', 'rgb(238,106,167)', 'rgb(238,106,80)', 'rgb(238,118,0)', 'rgb(238,118,33)', 'rgb(238,121,159)', 'rgb(238,121,66)', 'rgb(238,122,233)', 'rgb(238,130,238)', 'rgb(238,130,98)', 'rgb(238,149,114)', 'rgb(238,154,0)', 'rgb(238,154,73)', 'rgb(238,162,173)', 'rgb(238,169,184)', 'rgb(238,173,14)', 'rgb(238,174,238)', 'rgb(238,180,180)', 'rgb(238,180,34)', 'rgb(238,18,137)', 'rgb(238,197,145)', 'rgb(238,201,0)', 'rgb(238,203,173)', 'rgb(238,207,161)', 'rgb(238,210,238)', 'rgb(238,213,183)', 'rgb(238,213,210)', 'rgb(238,216,174)', 'rgb(238,220,130)', 'rgb(238,223,204)', 'rgb(238,224,229)', 'rgb(238,229,222)', 'rgb(238,230,133)', 'rgb(238,232,170)', 'rgb(238,232,205)', 'rgb(238,233,191)', 'rgb(238,233,233)', 'rgb(238,238,0)', 'rgb(238,238,209)', 'rgb(238,238,224)', 'rgb(238,44,44)', 'rgb(238,48,167)', 'rgb(238,58,140)', 'rgb(238,59,59)', 'rgb(238,64,0)', 'rgb(238,92,66)', 'rgb(238,99,99)', 'rgb(240,128,128)', 'rgb(240,230,140)', 'rgb(240,240,240)', 'rgb(240,240,240)', 'rgb(240,248,255)', 'rgb(240,255,240)', 'rgb(240,255,255)', 'rgb(24,116,205)', 'rgb(242,114,255)', 'rgb(242,242,242)', 'rgb(243,192,0)', 'rgb(244,164,96)', 'rgb(244,188,127)', 'rgb(244,244,244)', 'rgb(245,222,179)', 'rgb(245,245,220)', 'rgb(245,245,245)', 'rgb(245,255,250)', 'rgb(247,247,247)', 'rgb(247,42,66)', 'rgb(248,147,0)', 'rgb(248,248,255)', 'rgb(250,128,114)', 'rgb(250,161,255)', 'rgb(250,235,215)', 'rgb(250,240,230)', 'rgb(250,250,210)', 'rgb(250,250,250)', 'rgb(250,250,250)', 'rgb(252,230,201)', 'rgb(252,252,252)', 'rgb(25,25,112)', 'rgb(253,245,230)', 'rgb(255,0,0)', 'rgb(255,0,0)', 'rgb(255,0,204)', 'rgb(255,0,255)', 'rgb(255,105,180)', 'rgb(255,106,106)', 'rgb(255,108,108)', 'rgb(255,110,180)', 'rgb(255,114,86)', 'rgb(255,116,116)', 'rgb(255,119,255)', 'rgb(255,122,137)', 'rgb(255,125,64)', 'rgb(255,127,0)', 'rgb(255,127,36)', 'rgb(255,127,80)', 'rgb(255,128,0)', 'rgb(255,130,171)', 'rgb(255,130,71)', 'rgb(255,131,250)', 'rgb(255,136,0)', 'rgb(255,137,137)', 'rgb(255,140,0)', 'rgb(255,140,105)', 'rgb(255,146,255)', 'rgb(255,147,147)', 'rgb(255,152,255)', 'rgb(255,153,0)', 'rgb(255,153,18)', 'rgb(255,160,122)', 'rgb(255,165,0)', 'rgb(255,165,79)', 'rgb(255,166,166)', 'rgb(255,174,185)', 'rgb(255,174,62)', 'rgb(255,177,255)', 'rgb(255,181,197)', 'rgb(255,182,193)', 'rgb(255,185,15)', 'rgb(255,187,110)', 'rgb(255,187,255)', 'rgb(255,191,255)', 'rgb(255,192,203)', 'rgb(255,193,193)', 'rgb(255,193,200)', 'rgb(255,193,37)', 'rgb(255,20,147)', 'rgb(255,202,102)', 'rgb(255,204,0)', 'rgb(255,204,204)', 'rgb(255,206,255)', 'rgb(255,211,155)', 'rgb(255,214,214)', 'rgb(255,215,0)', 'rgb(255,216,156)', 'rgb(255,218,185)', 'rgb(255,220,58)', 'rgb(255,222,173)', 'rgb(255,225,255)', 'rgb(255,228,181)', 'rgb(255,228,193)', 'rgb(255,228,196)', 'rgb(255,228,225)', 'rgb(255,231,186)', 'rgb(255,235,205)', 'rgb(255,236,139)', 'rgb(255,239,213)', 'rgb(255,239,219)', 'rgb(255,240,245)', 'rgb(255,245,238)', 'rgb(255,246,143)', 'rgb(255,248,220)', 'rgb(255,250,205)', 'rgb(255,250,240)', 'rgb(255,250,250)', 'rgb(255,252,150)', 'rgb(255,253,202)', 'rgb(255,255,0)', 'rgb(255,255,0)', 'rgb(255,255,0)', 'rgb(255,255,224)', 'rgb(255,255,240)', 'rgb(255,255,255)', 'rgb(255,255,255)', 'rgb(255,255,255)', 'rgb(255,255,255)', 'rgb(255,48,48)', 'rgb(255,52,179)', 'rgb(255,62,150)', 'rgb(255,64,64)', 'rgb(255,69,0)', 'rgb(255,83,237)', 'rgb(255,84,84)', 'rgb(255,97,3)', 'rgb(255,99,71)', 'rgb(26,26,26)', 'rgb(28,134,238)', 'rgb(28,28,28)', 'rgb(30,144,255)', 'rgb(30,30,30)', 'rgb(31,31,31)', 'rgb(3,168,158)', 'rgb(32,178,170)', 'rgb(3,3,3)', 'rgb(33,33,33)', 'rgb(34,139,34)', 'rgb(34,255,34)', 'rgb(36,36,36)', 'rgb(38,153,71)', 'rgb(38,38,38)', 'rgb(38,82,153)', 'rgb(39,64,139)', 'rgb(40,40,40)', 'rgb(40,40,40)', 'rgb(41,36,33)', 'rgb(41,41,41)', 'rgb(43,43,43)', 'rgb(46,139,87)', 'rgb(46,46,46)', 'rgb(47,79,79)', 'rgb(48,128,20)', 'rgb(48,48,48)', 'rgb(50,205,50)', 'rgb(51,161,201)', 'rgb(51,204,94)', 'rgb(51,51,51)', 'rgb(53,128,0)', 'rgb(54,100,139)', 'rgb(54,116,217)', 'rgb(54,54,54)', 'rgb(5,5,5)', 'rgb(56,142,142)', 'rgb(56,56,56)', 'rgb(58,95,205)', 'rgb(59,59,59)', 'rgb(60,179,113)', 'rgb(61,145,64)', 'rgb(61,61,61)', 'rgb(61,89,171)', 'rgb(64,137,255)', 'rgb(64,224,208)', 'rgb(64,64,64)', 'rgb(65,105,225)', 'rgb(66,66,66)', 'rgb(67,0,8)', 'rgb(67,110,238)', 'rgb(67,205,128)', 'rgb(69,139,0)', 'rgb(69,139,116)', 'rgb(69,69,69)', 'rgb(70,130,180)', 'rgb(70,70,70)', 'rgb(71,60,139)', 'rgb(71,71,71)', 'rgb(72,118,255)', 'rgb(72,209,204)', 'rgb(72,61,139)', 'rgb(74,112,139)', 'rgb(74,74,74)', 'rgb(75,0,130)', 'rgb(77,77,77)', 'rgb(78,238,148)', 'rgb(79,148,205)', 'rgb(79,79,79)', 'rgb(81,81,81)', 'rgb(82,139,139)', 'rgb(82,82,82)', 'rgb(83,134,139)', 'rgb(84,139,84)', 'rgb(84,255,159)', 'rgb(84,84,84)', 'rgb(85,107,47)', 'rgb(85,26,139)', 'rgb(85,85,85)', 'rgb(87,87,87)', 'rgb(8,8,8)', 'rgb(89,89,89)', 'rgb(91,91,91)', 'rgb(92,172,238)', 'rgb(92,92,92)', 'rgb(93,71,139)', 'rgb(94,38,18)', 'rgb(94,94,94)', 'rgb(95,158,160)', 'rgb(96,123,139)', 'rgb(97,97,97)', 'rgb(99,184,255)', 'rgb(99,99,99)', ]

    random.seed(seed)
    return random.sample(rgb_pool, length)


