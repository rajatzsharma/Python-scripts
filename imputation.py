import numpy as np
import pandas as pd
import keep  # this one contains the 3 imports from below
# from keep import hhldkeep    # "HHLDKEEP_15.SAS"
# from keep import perskeep    # "PERSKEEP_15.SAS"
# from keep import iukeep      # "IUKEEP_15.SAS"

def imputation():
    # load the csv file that contains the Household Expenditure Survey 2015-16
    # df_sih = pd.read_csv(drive + "/abs_sih/Household Expenditure Survey 2015-16")

    # ABS/ATO/Welfare Benchmarks
    df_taxBM1 = pd.read_excel("\Benchmarks\Benchmarks_ALL_15.xls", sheet_name='Taxable_Inc')
    df_taxBM2 = df_taxBM1.T  # Transpose
    df_taxBM2.add_prefix('vingtile')  # add prefix
    df_taxBM2.drop(['_name_', '_label_'])
    df_taxBM2.iloc[1]['x'] = 1

    """
	***********************************************************************************************
										IMPUTATION SECTION
	***********************************************************************************************
	"""
    # ABS HOUSEHOLD FILE ------------------------------------------------------------------------------
    df_hhld = pd.read_csv('data/df_sih15bh.csv')  # this is the same as 'SET SIH.SIH15BH;'
    df_hhld.filter(
        items=keep.hhldkeep())  # only keep these columns in hhld (which I find weird given what I did on the previous line)

    # include statehec variable for inclusion later in IU and person level ABS data
    df_hhld_reg = df_hhld.filter(items=['ABSHID', 'STATEHEC'])  # we only keep these two colums for hhld_reg

    # IU FILE ------------------------------------------------------------------------------------------
    df_iu = pd.read_csv('data/df_sih15bi.csv')  # this is the same as 'SET SIH.SIH15BI;'
    df_iu['ABSHID'] = df_iu['ABSHID'].str.replace("SIH13", "SIH15")

    df_iu.filter(items=keep.iukeep())  # only keep necessary or potentially necessary IU variables
    randomid = [int(x[6:]) for x in df_iu['ABSHID']]
    INC_ID = randomid * 1000 + df_iu['ABSFID'] * 10 + df_iu['ABSIID']  # create inc id

    # Number of kids under different age group
    KID0T2BC = df_iu['IUFA0YB'] + df_iu['IUFA1YB'] + df_iu['IUFA2YB'] + df_iu['IUMA0YB'] + df_iu['IUMA1YB'] \
               + df_iu['IUMA2YB']  # 0 to two years old (females amd males)*/
    KID3T4BC = df_iu['IUFA3YB'] + df_iu['IUFA4YB'] + df_iu['IUMA3YB'] + df_iu['IUMA4YB']  # 3 to 4 years old*/
    KID5T9BC = df_iu['IUFA5YB'] + df_iu['IUFA6YB'] + df_iu['IUFA7YB'] + df_iu['IUFA8YB'] + df_iu['IUFA9YB'] \
               + df_iu['IUMA5YB'] + df_iu['IUMA6YB'] + df_iu['IUMA7YB'] + df_iu['IUMA8YB'] + df_iu[
                   'IUMA9YB']  # 5 to 9 years old*/
    KD1014BC = df_iu['IUFA10YB'] + df_iu['IUFA11YB'] + df_iu['IUFA12YB'] + df_iu['IUFA13YB'] + df_iu['IUFA14YB'] \
               + df_iu['IUMA10YB'] + df_iu['IUMA11YB'] + df_iu['IUMA12YB'] + df_iu['IUMA13YB'] + df_iu[
                   'IUMA14YB']  # 10 to 14 years old

    # Number of kids aged 10-12 and 13-14*/
    kid1012bc = df_iu['IUFA10YB'] + df_iu['IUFA11YB'] + df_iu['IUFA12YB'] + df_iu['IUMA10YB'] + df_iu['IUMA11YB'] + \
                df_iu['IUMA12YB']  # 10-12 years old*/
    kid1314bc = df_iu['IUFA13YB'] + df_iu['IUFA14YB'] + df_iu['IUMA13YB'] + df_iu['IUMA14YB']  # 13-14 years old*/

    # Dependent kids for PPS- kids aged under the age 8*/
    numdeps_pps = KID0T2BC + KID3T4BC + df_iu['IUFA5YB'] + df_iu['IUFA6YB'] + df_iu['UFA7YB'] + df_iu['IUMA5YB'] + \
                  df_iu['IUMA6YB'] + df_iu['IUMA7YB']

    # Dependent kids for PPP - kids aged under the age 6*/
    numdeps_ppp = KID0T2BC + KID3T4BC + df_iu['IUFA5YB'] + df_iu['IUMA5YB']
    natoccu = df_iu['TENREPCF']

    natoccu.replace(4, 6)
    for i in range(len(natoccu)):
        if df_iu['LNDLDIUC'][i] in [1, 3, 4, 7]:
            natoccu[i] = 4  # private renter
        elif df_iu['LNDLDIUC'][i] == 2:
            natoccu[i] = 3  # Govt */
        elif df_iu['LNDLDIUC'][i] in [5, 6]:
            natoccu[i] = 5

    df_ccout = pd.read_csv('data/IUCC2013.csv')  # no idea where this file is
    df_ccout.sort(by=['ABSHID'])

    df_iu = pd.merge(df_iu, df_ccout, on='ABSHID')
    df_iu.drop(['INC_ID'])

    # PERSON FILE  --------------------------------------------------------------------------------------
    df_pers = pd.read_csv('data/sih15bp.csv')  # SIH15BP
    df_pers.filter(items=keep.perskeep())

    ran_school = np.random.random()  # seed=1
    # RANDOMID = substr(ABShid,7,7)*1
    hh_id = randomid
    FAMNO = df_pers['ABSFID']
    IUNO = df_pers['ABSIID']
    pno = df_pers['ABSPID']
    fam_id = randomid * 100 + FAMNO
    INC_ID = randomid * 1000 + FAMNO * 10 + IUNO
    pers_id = randomid * 10000 + FAMNO * 100 + IUNO * 10 + pno
    iintcp = df_pers['INFINRCP'] + df_pers['INDEBRCP'] + df_pers['INPLNRCP'] + df_pers['CWIBTR'] + df_pers[
        'INPUTCP']  # Interest income including Trust income $pw
    iwcompcp = df_pers['IACSICP'] + df_pers[
        'IRWCCP']  # Current weekly income from Workers Compensation/Accident/Sickness
    intrtrcp = df_pers['CWIBTR'] + df_pers['INPUTCP']  # Current weekly income from trusts)
    irentcp = df_pers['IRNTCRCP'] + df_pers['IRNTRRCP']  # Current weekly income from property (res + non-res)
    iobtcp = df_pers['IOBTCP'] + df_pers['ISPCP']  # Unincorporated business income + silent partner income

    df_pers['YOAHBC'].replace(1, 0)  # yoahbc does not appear on the csv !!!!!!!!
    df_pers['YOAHBC'].replace(2, 1)
    df_pers['YOAHBC'].replace(3, 1)
    df_pers['YOAHBC'].replace(4, 2)

    # Impute INSTENRP using EDINBC, to these categories (THIS IS NOT IMPUTE!!!)
    df_pers['EDINBC'].replace(3, 1)
    df_pers['EDINBC'].replace(1, 1 + 1)
    df_pers['EDINBC'].replace(2, 2 + 1)

    # I'm initializing these variables as a numpy array of zeros
    FAMPOS = np.zeros(len(df_pers))  # FAMPOS in MATTS (relationship to family reference person)
    LFSTBCP = np.zeros(
        len(df_pers))  # LFSTBCP: Labour force status in current main and second job - create FT/PT split in addition
    LFSTFCP = np.zeros(len(df_pers))  # LFSTFCP: Labour force status in main job
    LFST2CP = np.zeros(len(df_pers))  # LFST2CP: Labour force status in second job
    ISonfile = np.zeros(len(df_pers))  # Flag for receipt of income support on survey file
    ss_flagp = np.zeros(len(df_pers))
    age_actp = np.zeros(len(df_pers))  # assign	the	actual age for age_actp

    for i in range(len(df_pers)):
        # high school student imputation using ABS Radl - see txt file in PolicyMod -
        # used to calculate hard coded numbers below
        if df_pers['AGEEC'][i] in [18, 19]:
            if df_pers['AGEEC'][i] == 19 and ran_school < 0.48:  # why are they doing this if again!?
                df_pers['EDINBC'][i] = 4
            if df_pers['AGEEC'][i] == 18 and ran_school < 0.03:
                df_pers['EDINBC'][i] = 4

        # Recode STUDSTCP
        if df_pers['HQUALCP'][i] == 8 and df_pers['EDINBC'][
            i] == 1:  # no non-school qualification, and  secondary school
            df_pers['STUDSTCP'][i] = 1  # still at school
        else:
            df_pers['STUDSTCP'][i] += 1

        # FAMPOS in MATTS (relationship to family reference person)
        # THIS CAN BI FIXED WITH A DICTIONARY
        if df_pers['RELATHCF'][i] == 2:
            FAMPOS[i] = 1  # reference
        elif df_pers['RELATHCF'][i] == 3:
            FAMPOS[i] = 3  # dep child
        elif df_pers['RELATHCF'][i] == 4:
            FAMPOS[i] = 4  # non-dep child of family
        elif df_pers['RELATHCF'][i] == 5:
            FAMPOS[i] = 5  # non-dep child of other relative
        elif df_pers['RELATHCF'][i] == 6:
            FAMPOS[i] = 6  # non-family individual
        elif df_pers['RELATHCF'][i] == 1:
            if df_pers['IUPOS'][i] == 1:
                FAMPOS[i] = 1  # reference
            elif df_pers['IUPOS'][i] == 2:
                FAMPOS[i] = 2  # partner

        # LFSTBCP: Labour force status in current main and second job - create FT/PT split in addition
        if df_pers['LFSCP'] == 2:
            LFSTBCP[i] = 3  # unemployed
        elif df_pers['LFSCP'][i] == 3:
            LFSTBCP[i] = 4  # NILF
        elif df_pers['LFSCP'][i] == 1:
            if df_pers['FTPTSTAT'][i] == 1:
                LFSTBCP[i] = 1  # FT emp
            elif df_pers['FTPTSTAT'][i] == 2:
                LFSTBCP[i] = 2  # PT emp

        # LFSTFCP: Labour force status in main job
        # Not employed
        if df_pers['LFSCP'][i] == 2:
            LFSTFCP[i] = 6  # Unemployed
        elif df_pers['LFSCP'][i] == 3:
            LFSTFCP[i] = 7  # NILF
        elif df_pers['LFSCP'][i] == 1:  # Employed
            if df_pers['STEMP1CF'][i] == 1:
                LFSTFCP[i] = 1  # FT employee
            elif df_pers['STEMP1CF'][i] == 2:
                LFSTFCP[i] = 2  # PT employee
            elif df_pers['STEMP1CF'][i] == 3:
                LFSTFCP[i] = 3  # Employer
            elif df_pers['STEMP1CF'][i] == 4:
                LFSTFCP[i] = 4  # Own acct worker etc
            elif df_pers['STEMP1CF'][i] == 0:
                LFSTFCP[i] = 0  # Not applicable

        # LFST2CP: Labour force status in second job
        if 2 <= df_pers['LFSCP'][i] <= 3:
            LFST2CP[i] = 0  # Not applicable
        elif df_pers['LFSCP'][i] == 1:
            if df_pers['STEMP2CF'][i] == 1:
                LFST2CP = 1  # Employee paid in cash */
            elif df_pers['STEMP2CF'][i] == 2:
                LFST2CP[i] = 2  # Employer, own account worker and other
            else:
                LFST2CP[i] = 0

        # Industry of occupation
        if df_pers['INDCE'][i] == 26:
            df_pers['INDCE'][i] = 0

    """ IAUSTCP,  = Austudy/ABSTUDY - even though it's not modelled in STINMOD
		IAGECP,   = Age Pension
		ICAREPCP, = Carer Payment
		IDISBCP,  = DVA Disability Pension
		IDSUPPCP, = Disability Support Pension
		INEWLSCP, = Newstart Allowance
		IOTHPCP,  = Other govt pensions and allowances
		IPARENCP, = Parenting payment
		IPARTNCP, = Partner Allowance
		ISERVCP,  = Service Pension
		ISICKCP,  = Sickness Allowance
		ISPECCP,  = Special Benefit
		IWARWCP,  = War Widow's Pension
		IWIDOWCP, = Widow Allowance
		IWIFECP,  = Wife Pension
		IYOUTHCP = Youth Allowance
	"""

    aux = df_pers['IAUSTCP'] + df_pers['IAGECP'] + df_pers['ICAREPCP'] + df_pers['IDISBCP'] + df_pers['IDSUPPCP'] + \
          df_pers['INEWLSCP'] + df_pers['IOTHPCP'] + df_pers['IPARENCP'] + df_pers['IPARTNCP'] + df_pers['ISERVCP'] + \
          df_pers['ISICKCP'] + df_pers['ISPECCP'] + df_pers['IWARWCP'] + df_pers['IWIDOWCP'] + df_pers['IWIFECP'] + \
          df_pers['IYOUTHCP']
    for i in range(len(df_pers)):
        if aux[i] > 0:
            ISonfile[
                i] = 1  # Flag for receipt of income support on survey file (DON'T KNOW IF THIS FLAG IS A VALUE FOR EVERY ROW)
        else:
            ISonfile[i] = 0

    """
	/*---------------------------------------------------------------*/
	/* FRINGE BENEFITS AND SALARY SACRIFICING                        */
	/* ssfbp     - cur.income salary sacrificed (except to super)    */
	/* non_ssfbp - cur.employer-provided benefits(not sal.sacrificed)*/
	/* ss_flagp  = 1 if reported income includes sal.sac. amts       */
	/* issscp	 - weekly income salary sacrificed for superannuation*/
	/* Zero vals.indicate fringe benefits in ABS data not reportable */
	/* Not included: ISSCCCP(child care), INSSHCP (shares),          */
	/* IWSBUCP (regular bonuses)                                     */
	/*---------------------------------------------------------------*/
	"""
    ssfbp = df_pers['IKHSSCP'] + df_pers['IKTSSCP'] + df_pers['ISSVTCP'] + df_pers['ISSCOCP'] + \
            df_pers['ISSOBCP'] + df_pers['ISSHPCP']
    non_ssfbp = df_pers['INSCOCP'] + df_pers['INSLOCP'] + df_pers['IKHNSCP'] + df_pers['IKTNSCP'] + \
                df_pers['IKVNSCP'] + df_pers['INSOBCP']

    for i in range(len(df_pers)):
        # If reported income included amount salary sacrificed
        if df_pers['WSSRICP'] == 1:  # SAME STORY: SS_FLAGP IS SUPPOSED TO BE A LIST?
            ss_flagp[i] = 1
        else:
            ss_flagp[i] = 0

        # Impute salary sacrificed super for self-employed
        if df_pers['IOBTCP'] > 0:
            # Assume that 10% of self-employed salary sacrifice */
            if np.random.random() <= 0.1 and df_pers['ISSSCP'] == 0:
                # hard coded numbers from old Treasury data set. Any update
                # would need to be a request from Treasury or use of Capita code
                if df_pers['IOBTCP'][i] * 365 / 7 < 10000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'] * 4.133
                elif df_pers['IOBTCP'][i] * 365 / 7 < 15000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.601
                elif df_pers['IOBTCP'][i] * 365 / 7 < 20000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.412
                elif df_pers['IOBTCP'][i] * 365 / 7 < 25000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.312
                elif df_pers['IOBTCP'][i] * 365 / 7 < 35000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.225
                elif df_pers['IOBTCP'][i] * 365 / 7 < 50000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.213
                elif df_pers['IOBTCP'][i] * 365 / 7 < 60000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.205
                elif df_pers['IOBTCP'][i] * 365 / 7 < 100000:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'][i] * 0.222
                else:
                    df_pers['ISSSCP'][i] = df_pers['IOBTCP'] * 0.200

        # Cukkoo - assign the actual age for age_actp
        # WHAT IS THIS PIECE OF CODE SUPPOSED TO DO!?!?!?!?! IT ASSIGNES THE SAME VALUE ALWAYS!!!!
        if df_pers['ageec'] <= 24:
            age_actp[i] = df_pers['ageec']  # + 14 single years of age
        elif 25 < df_pers['ageec'] < 54:
            age_actp[i] = df_pers['ageec']  # 25 - 54 yrs
        elif 55 <= df_pers['ageec'] <= 64:
            age_actp[i] = df_pers['ageec']  # + 38  single years of age
        else:
            age_actp[i] = df_pers['ageec']  # 65 and over
        age = df_pers['ageec']

    # sum of personal wealth - used for splitting household wealth between income units
    wealthp = df_pers['VSUPGCP'] + df_pers['VSUPNCP'] + df_pers['VFINCP'] + df_pers['VOFTCP'] + df_pers['VDEBCP'] + \
              df_pers['VPLNCP'] + df_pers['VINVOTCP'] + df_pers['VIBUSCP'] + df_pers['VUBUSCP'] + df_pers['VPUTTCP'] + \
              df_pers['VPRTCP'] + df_pers['VSIPCP'] + df_pers['VSHARCP']

    """
		VSUPGCP,  = super govt - assumed allocated pension
		VSUPNCP,  = super priv - assumed allocated pension
		VFINCP,   = financial inst's
		VOFTCP,	  = offset accounts
		VDEBCP,	  = debentures and bonds
		VPLNCP,	  = loans to other persons
		VINVOTCP, = Other financial investments
		VPUTTCP,  = public unit trusts
		VPRTCP,   = private trusts
		VSHARCP  = Shares
	 """

    fin_assetp = df_pers['VSUPGCP'] + df_pers['VSUPNCP'] + df_pers['VFINCP'] + df_pers['VOFTCP'] + df_pers['VDEBCP'] + \
                 df_pers['VPLNCP'] + df_pers['VINVOTCP'] + df_pers['VPUTTCP'] + df_pers['VPRTCP'] + df_pers['VSHARCP']

    return