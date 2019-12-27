import pandas as pd

path = "C:\OmicData\YJM1342\GCA_000977265.3_Sc_YJM1342_v1_genomic.gff"
out = "C:\OmicData\YJM1342\GCA_000977265.3_Sc_YJM1342_v1_genomic_modified.gff"

dfrm = pd.read_csv(path, sep="\t", skiprows=7, header=None)

dfrm[dfrm[2]!="region"].to_csv(out, sep="\t", index=False, header=False)
