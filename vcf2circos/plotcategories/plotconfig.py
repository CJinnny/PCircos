#!/usr/local/bin/python3

"""
aim: Epurate module and func, handle parameters of circos plot
"""

from functools import lru_cache
import re
import json
import os
from typing import Generator
import pandas as pd

# from vcf2circos.vcfreader import VcfReader
from os.path import join as osj
from tqdm import tqdm
from vcf2circos.utils import timeit, cast_svtype
from pprint import pprint
import vcf
import time


class Plotconfig:
    """
    Options regroup options passed in args in json file otherwise
    it will be a empty dict,
    All func based on vcf input
    """

    def __init__(
        self,
        filename: str,
        options: dict,
        show: bool,
        file: dict,
        radius: dict,
        sortbycolor: bool,
        colorcolumn: int,
        hovertextformat: dict,
        trace_car: dict,
        data: list,
        layout: dict,
        rangescale: list,
        config_ring: dict,
    ):
        self.filename = filename
        self.options = options
        if not self.options.get("General", {}).get("title", None):
            self.options["General"]["title"] = os.path.basename(filename)
        self.show = self.cast_bool(show)
        self.file = file
        self.radius = radius
        self.sortbycolor = self.cast_bool(sortbycolor)
        self.colorcolumn = colorcolumn
        self.hovertextformat = hovertextformat
        self.trace_car = trace_car
        self.layout = layout
        self.rangescale = rangescale
        self.config_ring = config_ring
        self.vcf_reader = vcf.Reader(filename=filename, strict_whitespace=True, encoding="utf-8")
        self.colors = self.options["Color"]
        # In case of non coding genes (even in coding genes but same CDS) multiple lines, keep only the first to have non redundant file
        self.df_genes = pd.read_csv(
            osj(
                self.options["Static"],
                "Assembly",
                self.options["Assembly"],
                "genes." + self.options["Assembly"] + ".sorted.txt",
            ),
            header=0,
            sep="\t",
        ).drop_duplicates(subset="gene", keep="first")
        self.df_transcripts = pd.read_csv(
            osj(
                self.options["Static"],
                "Assembly",
                self.options["Assembly"],
                "transcripts." + self.options["Assembly"] + ".sorted.txt",
            ),
            header=0,
            sep="\t",
        )
        self.df_exons = pd.read_csv(
            osj(
                self.options["Static"],
                "Assembly",
                self.options["Assembly"],
                "exons." + self.options["Assembly"] + ".sorted.txt",
            ),
            header=0,
            sep="\t",
        )
        self.df_morbid = pd.read_csv(
            osj(self.options["Static"], "morbid.txt"),
            header=None,
            sep="\t",
            names=["genes"],
        )
        # Last function to be called to generate class attribute
        self.data = self.process_vcf()
        self.df_data = pd.DataFrame.from_dict(self.data)

    def data_nan_formatting(self):
        df_tmp = pd.DataFrame.from_dict(self.data)
        # df_tmp.to_csv("test_nanvar.tsv", sep="\t", header=True, index=False)
        df = df_tmp.dropna()
        if len(df_tmp.index) != len(df.index):
            print(
                "WARNING Removing ",
                str(len(df_tmp.index) - len(df.index)) + " Variations",
            )
        return df.astype(
            {
                "Chromosomes": str,
                "Genes": str,
                "Exons": str,
                "Variants": object,
                "Variants_type": str,
                "CopyNumber": object,
                "Color": str,
            }
        )

    @staticmethod
    def cast_bool(value: bool) -> str:
        if value:
            return "True"
        else:
            return "False"

    @timeit
    def process_vcf(self) -> dict:
        """
        Process Just one time vcf variants in a dict which contains all required informations for all type of var used after,
        Act as a plotconfig main\n
        """
        data = {
            "Chromosomes": [],
            "Genes": [],
            "Exons": [],
            "Record": [],
            "Variants": [],
            "Variants_type": [],
            "CopyNumber": [],
            "Color": [],
        }
        # VCF parsed file from PyVCF3
        self.breakend_record = []
        # self.breakend_genes = []
        for record in self.vcf_reader:
            # Could now do filter to only plot some specific gene or chromosomes
            if (
                self.chr_adapt(record) in self.options["Chromosomes"]["list"]
                or not self.options["Chromosomes"]["list"]
            ):
                # particular process for breakend
                if self.get_copynumber_type(record)[0] in ["BND"]:
                    self.breakend_record.append(record)
                elif self.get_copynumber_type(record)[0] in ["TRA"]:
                    continue
                else:
                    data["Chromosomes"].append(self.chr_adapt(record))
                    data["Genes"].append(self.get_genes_var(record))
                    data["Exons"].append("")
                    # TODO exons time consumming
                    data["Record"].append(record)
                    data["Variants"].append(record.INFO)
                    svtype, copynumber = self.get_copynumber_type(record)
                    #if record.CHROM == "chr6" and record.POS == 1089464612 :
                    #    print(record)
                    #    print(record.INFO)
                    #    print(self.get_copynumber_type(record))
                    #    #exit()
                    # ensure svtype is in capslock
                    svtype = svtype.upper()
                    assert svtype in self.options["Color"], (
                        "Wrong svtype in record "
                        + ", ".join(
                            [
                                str(record.CHROM),
                                str(record.POS),
                                str(record.REF),
                                str(record.ALT),
                            ]
                        )
                        + " check your vcf Exit"
                    )
                    assert isinstance(copynumber, int), "ERROR wrong copy number"
                    data["Variants_type"].append(svtype)
                    try:
                        data["Color"].append(self.colors[svtype])
                    except KeyError:
                        data["Color"].append(self.colors["CNV"])
                    if copynumber is None:
                        data["CopyNumber"].append(2)
                    else:
                        if copynumber > 5 and svtype not in ["SNV", "INDEL", "OTHER"]:
                            copynumber = 5
                        data["CopyNumber"].append(copynumber)
        return data

    def chr_adapt(self, record: object) -> str:
        """
        from PyVCF record return chromosome with 'chr'
        """
        try:
            re.match(r"[0-9]", record.CHROM).group()
            return "chr" + record.CHROM
        except AttributeError:
            if record.CHROM in ["X", "Y", "M"]:
                return "chr" + record.CHROM
            else:
                return record.CHROM

    def get_copynumber_type(self, record: object) -> tuple:
        """
        take VCF variant object and return variant type and number of copy in tuple
        REQUIRED monosample vcf
        """
        # if only copy number in alt....
        if "]" in str(record.ALT[0]) or "[" in str(record.ALT[0]):
            return ("BND", 2)
        if str(record.ALT[0]).startswith("<CN") and str(record.ALT[0]) != "<CNV>":
            cn = str(record.ALT[0])
            cn = cn.replace("<", "")
            cn = cn.replace(">", "")
            return ("CNV", int(cn[-1]))
        # if both copy number and sv type in alt
        if str(record.ALT[0]) == "<TRA>":
            return ("TRA", 2)
        if str(record.ALT[0]).startswith("<"):
            alt_tmp = str(record.ALT[0]).split(":")
            if len(alt_tmp) > 1:
                alt = alt_tmp[0]
                alt = alt.replace("<", "")
                cn = alt_tmp[1].replace(">", "")
                if cn.startswith("CN"):
                    return (alt, int(cn[-1]))

        # trying to retrieve usefull informations in info field
        alt = str(record.ALT[0])
        # checking if CopyNumber annotation in info field
        if record.INFO.get("SVTYPE", ""):
            svtype = record.INFO.get("SVTYPE", "")
            return (
                cast_svtype(svtype),
                self.get_copynumber_values(cast_svtype(svtype), record),
            )
        elif record.INFO.get("SV_type", ""):
            svtype = record.INFO.get("SV_type", "")
            return (
                cast_svtype(svtype),
                self.get_copynumber_values(cast_svtype(svtype), record),
            )
        # It's SV in ALT field and not compute before
        elif alt.startswith("<"):
            rep = {"<": "", ">": ""}
            svtype = alt
            for key, val in rep.items():
                svtype = svtype.replace(key, val)
            # in case of copy number in alt
            if re.search(r"$[0-9]+", svtype) != None:
                copynumber = re.search(r"$[0-9]+", svtype).group()
                return (cast_svtype(svtype), copynumber)
            else:
                svtype = svtype.split(":")[0]
                if len(svtype) > 1 and isinstance(svtype, list):
                    copynumber = svtype[1]
                    return (cast_svtype(svtype), copynumber)
                else:
                    return (
                        cast_svtype(svtype),
                        self.get_copynumber_values(cast_svtype(svtype), record),
                    )
        # SNV or INDEL identify y pyVCF
        elif record.var_type == "snp" or record.var_type == "indel":
            return (self.cast_snv_indels(record), 6)
        else:
            return ("OTHER", 6)

    def cast_snv_indels(self, record):
        if record.var_type == "snp":
            return "SNV"
        elif record.var_type == "indel":
            return "INDEL"

    def get_copynumber_values(self, svtype: str, record: object) -> int:
        """
        take VCF variant object (type of variant could help)and return copynumber as integer from 0 to 5 (which mean 5 or more but in general it 's super rare)\n
        REQUIRED monosample vcf
        """
        if record.INFO.get("CN") is not None:
            if isinstance(record.INFO.get("CN"), list):
                return int(record.INFO.get("CN")[0])
            else:
                return int(record.INFO.get("CN"))
        # list of sample TODO working only if vcf monosample
        else:
            # Need verificatons TODO
            genotype = record.samples[0].data.GT
            if genotype == "1/0" or "0/1":
                gt = 1
            elif genotype == "1/1":
                gt = 2
            else:
                gt = "0/0"

            if svtype in [
                "CNV",
                "INS",
                # "INV",
                # "DEL",
                "DUP",
            ]:
                # CNV or INS
                return gt + 1
            elif svtype == "INV":
                return 2
            elif svtype == "DEL":
                return 2 - gt

    def find_record_gene(self, coord: list) -> list:
        """
        From genomic coordinate, return a list of overlapping gene (if genes are not provided in info field)\n
        Greedy for now
        """
        if isinstance(coord[2], list):
            coord[2] = coord[2].split("|")
        gene_list = []
        # only chr for this variants
        refgene_chr = self.df_genes.loc[self.df_genes["chr_name"] == coord[0]]
        # 1Mb up and downstream
        if self.options["Genes"]["extend"]:
            # print(*[type(f) for f in coord])
            coord[1] = coord[1] - 1000000
            coord[2] = coord[2] + 1000000
            # if 1Mb down reach 0 in genomic position
            if coord[1] < 0:
                coord[1] = 0
            # print(coord)
            # exit()
        for j, rows in refgene_chr.iterrows():
            # variant start begin before a gene and stop inside or after
            if coord[1] <= rows["start"] and (
                coord[2] in range(rows["start"], rows["end"]) or coord[2] >= rows["end"]
            ):
                gene_list.append(rows["gene"])
            # sv only inside one gene
            if coord[1] >= rows["start"] and coord[2] <= rows["end"]:
                gene_list.append(rows["gene"])
            # SV all size done
            if coord[1] <= rows["start"] and coord[2] <= rows["end"]:
                break
        return list(set(gene_list))

    def string_to_unique(self, string):
        if "|" in string:
            return ",".join(list(set(string.split("|"))))
        elif "," in string:
            return ",".join(list(set(string.split(","))))
        else:
            return string

    def from_gene_to_unique(self, values: str) -> str:
        """
        example from IFT140|IFT140 to IFT140 if all values are the same otherwise keep all
        """
        if isinstance(values, str):
            return self.string_to_unique(values)
        elif isinstance(values, list):
            return ",".join([self.string_to_unique(f) for f in values])
        else:
            print("ERROR in Gene_name ", values)
            exit()

    def get_sv_length_annotations(self, record, field):
        #if field == "SV_end":
        #    gene_name = self.find_record_gene(
        #        [
        #            record.CHROM,
        #            record.POS,
        #            int(float(self.string_to_unique(record.INFO["SV_end"])[0])),
        #        ]
        #    )
        #    return gene_name
        #if isinstance(record.INFO[field], int):
        #    gene_name = self.find_record_gene(
        #        [record.CHROM, record.POS, int(record.POS) + record.INFO[field]]
        #    )
        if field in ["SV_length", "SVLEN"]:
            gene_name = self.find_record_gene(
                [record.CHROM, record.POS, record.POS+abs(record.INFO[field])]
            )
        elif field in ["SV_end", "END"]:
            gene_name = self.find_record_gene(
                [record.CHROM, record.POS, record.INFO[field]]
            )
        else:
            gene_name = []
        return gene_name
        #elif isinstance(record.INFO[field], list):
        #    if isinstance(record.INFO[field][0], int):
        #        gene_name = self.find_record_gene(
        #            [
        #                record.CHROM,
        #                record.POS,
        #                int(record.POS) + int(float(record.INFO[field][0])),
        #            ]
        #        )
        #    else:
        #        gene_name = self.find_record_gene(
        #            [
        #                record.CHROM,
        #                record.POS,
        #                int(record.POS) + int(float(self.string_to_unique(record.INFO[field][0]))),
        #            ]
        #        )
        #else:
        #    gene_name = self.find_record_gene(
        #        [
        #            record.CHROM,
        #            record.POS,
        #            int(record.POS) + int(float(self.string_to_unique(record.INFO[field])[0])),
        #        ]
        #    )
        #return gene_name

    def get_genes_var(self, record: object) -> str:
        """
        From PyVCF record return str containing list of overlapping genes\n
        Translocation have a different process, conf link class
        If extend options in config (get all genes located in 1Mb up and downstream of sv boundaries)
        """
        bad_values = [None, "", "."]
        bad_svtype = ["BND", "TRA", None]
        types_ = ["SVLEN", "SV_length","SV_end", "END"]

        gene_name = record.INFO.get("Gene_name")
        # Add chr if missing
        record.CHROM = self.chr_adapt(record)
        if not self.options["Genes"]["extend"]:
            # get overlapping genes in Gene_name INFO field
            if gene_name not in bad_values and isinstance(gene_name, str):
                return self.from_gene_to_unique(gene_name)
            elif isinstance(gene_name, list) and gene_name[0] not in bad_values:
                return self.from_gene_to_unique(gene_name)
            # No Gene_name annotation need to find overlapping gene in sv
            # if gene_name is None or (isinstance(gene_name, list) and gene_name[0] == None):
        #if (
        #    record.INFO.get("SVTYPE") not in bad_svtype
        #    or record.INFO.get("SV_type") not in bad_svtype
        #):
        if any([val for val in types_ if val in record.INFO]):
            try:
                gene_name = self.get_sv_length_annotations(record, "SVLEN")
                return ",".join(gene_name)
            except (KeyError, ValueError, TypeError):
                try:
                    # print(record.INFO["SV_length"])
                    gene_name = self.get_sv_length_annotations(record, "SV_length")
                    return ",".join(gene_name)
                except (KeyError, ValueError, TypeError):
                    try:
                        gene_name = self.get_sv_length_annotations(record, "SV_end")
                        return ",".join(gene_name)
                    except (KeyError, ValueError, TypeError):
                        try:
                            gene_name = self.get_sv_length_annotations(record, "END")
                            return ",".join(gene_name)
                        except (KeyError, ValueError, TypeError):
                            print(
                            "ERROR missing SVLEN annotation for record ",
                            record,
                        )
                        exit()
        # SNV indel
        else:
            alternate = int(str(max([len(alt) for alt in list(str(record.ALT))])))
            gene_name = self.find_record_gene(
                [
                    record.CHROM,
                    record.POS,
                    (int(record.POS) + alternate),
                ]
            )
            if not gene_name:
                gene_name = [""]
            return ",".join(gene_name)
