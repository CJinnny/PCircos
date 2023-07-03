from vcf2circos.plotcategories.plotconfig import Plotconfig
from vcf2circos.utils import Colorpal, chr_valid
import pandas as pd
from os.path import join as osj

# space, space between ring in option.example.json
# height hauteur du ring
# positon position from center


class Ideogram(Plotconfig):
    def __init__(self, plotconfig):
        self.plotconfig = plotconfig
        self.chr_conf = pd.read_csv(
            osj(
                self.options["Static"],
                "Assembly",
                self.options["Assembly"],
                "chr." + self.options["Assembly"] + ".sorted.txt",
            ),
            sep="\t",
            header=0,
        )
        self.degreerange = [0, 360]
        self.showfillcolor = self.cast_bool(True)
        self.chrannotation = (
            {
                "show": "True",
                "radius": {"R": 1.25},
                "fonttype": "bold",
                "textangle": {"angleoffset": 0, "anglelimit": 360},
                "layout": {
                    "xref": "x",
                    "yref": "y",
                    "showarrow": False,
                    "font": {"size": 10, "color": "black"},
                },
            },
        )
        self.customoptions = {
            "customlabel": "True",
            "customspacing": "False",
            "customcolor": 3,
        }
        self.npoints = 1000
        self.radius = {"R0": 1.0, "R1": 1.1}
        self.layout = {
            "type": "path",
            "opacity": 0.9,
            "layer": "above",
            "line": {"color": "gray", "width": 2},
        }
        self.majortick = {
            "show": "True",
            "spacing": 30000000,
            "radius": {"R0": 1.1, "R1": 1.125},
            "layout": {
                "type": "path",
                "opacity": 0.9,
                "layer": "above",
                "line": {"color": "black", "width": 1},
            },
        }
        self.minortick = {
            "show": "True",
            "spacing": 5000000,
            "radius": {"R0": 1.1, "R1": 1.118},
            "layout": {
                "type": "path",
                "opacity": 0.9,
                "line": {"color": "black", "width": 0.5},
            },
        }
        self.ticklabel = {
            "show": "True",
            "spacing": 30000000,
            "radius": {"R": 1.16},
            "textformat": "Mb",
            "textangle": {"angleoffset": -90, "anglelimit": 360},
            "layout": {
                "xref": "x",
                "yref": "y",
                "showarrow": False,
                "font": {
                    "family": "Times New Roman",
                    "size": 8,
                    "color": "black",
                },
            },
        }

    def __getattr__(self, item):
        if hasattr(self.plotconfig, item):
            return getattr(self.plotconfig, item)

    def data_ideogram(self, chr_link):
        # need to know if BND have chr mate in no called chromosome
        true_chr = self.data["Chromosomes"]
        true_chr.extend(chr_link)
        chromosomes = list(set(true_chr))
        if self.options["Chromosomes"]["all"] is True:
            tmp = self.chr_conf.loc[self.chr_conf["chr_name"].isin(chr_valid())]
        else:
            tmp = self.chr_conf.loc[self.chr_conf["chr_name"].isin(chromosomes)]
        data = {
            "chr_name": tmp["chr_name"].to_list(),
            "chr_size": tmp["size"].to_list(),
            "chr_label": tmp["chr_name"].to_list(),
            "chr_color": list(Colorpal(len(tmp["chr_name"].to_list()))),
        }
        return data

    def merge_options(self, chr_link):
        dico = {}
        dico["patch"] = {}
        # ideo = Ideogram()
        dico["patch"]["file"] = {
            "path": "",
            "header": "infer",
            "sep": "\t",
            "dataframe": {"orient": "columns", "data": self.data_ideogram(chr_link)},
        }
        dico["patch"]["show"] = self.show
        dico["patch"]["degreerange"] = self.degreerange
        dico["patch"]["showfillcolor"] = self.showfillcolor
        dico["patch"]["chrannotation"] = {
            "show": "True",
            "radius": {"R": 1.25},
            "fonttype": "bold",
            "textangle": {"angleoffset": 0, "anglelimit": 360},
            "layout": {
                "xref": "x",
                "yref": "y",
                "showarrow": False,
                "font": {"size": 10, "color": "black"},
            },
        }
        dico["patch"]["customoptions"] = {
            "customlabel": "True",
            "customspacing": "False",
            "customcolor": 3,
        }
        dico["patch"]["npoints"] = self.npoints
        dico["patch"]["radius"] = self.radius
        dico["patch"]["layout"] = self.layout
        dico["majortick"] = self.majortick
        dico["minortick"] = self.minortick
        dico["ticklabel"] = self.ticklabel
        return dico
