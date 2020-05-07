# Import Python Libraries
import numpy as np
import pandas as pd
from imputation import imputation
from uprating import uprating
from read_parameters import read_parameters

# Import SAS Filenames (that on Python are we will consider as scripts with code)
from inflate import inflate  # "INFLATE.SAS"
from ccare import ccare  # "Base Creation 2015.sas"
from gregwt import gregwt  # "gregwt_CJ.sas"
from gini import gini  # "gini.sas"

# Import SAS Libnames (that on python are known as Datasets)
# ARE THIS FILES EXCEL FILES???????????? I NEED THE EXTENSION
drive = "data/basefile/sas/"
df_basedata = pd.read_csv(drive + "/basedata")
df_compare = pd.read_csv(drive + "/compare")
df_hesbase = pd.read_csv(drive + "/hesbase")
df_altdata = pd.read_csv(drive + "/altdata")

df_ccout = pd.read_csv(drive + "childcare")
df_uprat2 = pd.read_csv(drive + "Uprating")


# seems like all this code is to define this function
def af(year, bmyr, prev, emtr, gap, sim, drive):
	# imputation()  # execute imputation function
	# uprating()  # execute uprating function
	read_parameters()  # execute read_parameters function
	# compare()  # The name Bern gave to this function is not clear enough

	return []


