# IMPORTING MODULES
import pandas as pd
import numpy as np
import os
from pathlib import Path

def read_parameters(sim=False):
    # df_altdata = pd.read_csv(drive + "/altdata") - DO WE NEED THESE TWO LINES?
    # df_basedata = pd.read_csv(drive + "/basedata")
    drive = Path.cwd()
    df_base = pd.read_csv(os.path.join(drive, "input\\accbase190.csv"))
    parameters_path = os.path.join(drive, 'input\\Parameters_Base18.xls')
    month = 12

    # ****************************************************************************************
    # READ IN PARAMETERS #
    # ****************************************************************************************

    # lines 32 - 221
    # read in parameter spreadsheets
    df_pension = pd.read_excel(parameters_path, sheet_name='Pension', skiprows=3)
    df_allowance = pd.read_excel(parameters_path, sheet_name='Allowance', skiprows=5)
    df_ftb = pd.read_excel(parameters_path, sheet_name='FTB', skiprows=4)
    df_childcare = pd.read_excel(parameters_path, sheet_name='Childcare', skiprows=4)
    df_maintmat= pd.read_excel(parameters_path, sheet_name='MaintMat', skiprows=5)
    df_supplements= pd.read_excel(parameters_path, sheet_name='Supplements', skiprows=4)
    df_energy = pd.read_excel(parameters_path, sheet_name='Energy', skiprows=4)
    df_tax = pd.read_excel(parameters_path, sheet_name='TAX', skiprows=6)

    # merge pension Allowance Childcare FTB MaintMat Supplements Energy Tax;
    df_params = pd.concat([df_pension,
                           df_allowance,
                           df_ftb,
                           df_childcare,
                           df_maintmat,
                           df_supplements,
                           df_energy,
                           df_tax], axis=1)

    df_pen2 = df_params[['PEN_S', 'PEN_C', 'PENTOT_S', 'PENTOT_C']]
    df_nsa2 = df_params[['NSA21_S', 'NSA60_S', 'NSADEP_S', 'NSA21_C1', 'NSA21_C2']]
    df_pps2 = df_params[['PPS', 'PPS_SUP']]
    df_ftb2 = df_params[['FTBA0_13', 'FTBA13_15', 'FTBA16_19', 'FTBA16_19NS', 'FTBASUPP', 'FTBA0_19B', 'FTBB0_5C', 'FTBBNC', 'FTBB0_5S', 'FTBBNS', 'FTBBSUPP']]
    df_ra2  = df_params[['AL0S', 'RNTAL1S', 'RNTAL2S', 'RNTAL0C', 'RNTAL1C', 'RNTAL2C']]

    if sim is False:
        ran_pen = np.random.uniform() * 0.8333 + 0.6666
        ran_nsa = np.random.uniform() * 0.8333 + 0.6666
        ran_pps = np.random.uniform() * 0.8333 + 0.6666
        ran_ftb = np.random.uniform() * 0.8333 + 0.6666
        ran_ra =  np.random.uniform() * 0.8333 + 0.6666

    else:
        gap = [9999,9998, 9997]
        ppenst = 0  # not defined in SAS so I invented the value
        pnsast = 0  # not defined in SAS so I invented the value
        pppsst = 0  # not defined in SAS so I invented the value
        pftbst = 0  # not defined in SAS so I invented the value
        prast = 0  # not defined in SAS so I invented the value

        ppen = 0  # not defined in SAS so I invented the value
        pnsa = 0  # not defined in SAS so I invented the value
        ppps = 0  # not defined in SAS so I invented the value
        pftb = 0  # not defined in SAS so I invented the value
        pra = 0  # not defined in SAS so I invented the value

        pahpen = 0  # not defined in SAS so I invented the value
        pahnsa = 0  # not defined in SAS so I invented the value
        pahpps = 0  # not defined in SAS so I invented the value
        pahftb = 0  # not defined in SAS so I invented the value
        pahra = 0  # not defined in SAS so I invented the value
        ran_pen = gap[0] * ppenst + gap[1] * ppen  + gap[2] * pahpen
        ran_nsa = gap[0] * pnsast + gap[1] * pnsa, gap[2] * pahnsa
        ran_pps = gap[0] * pppsst + gap[1] * ppps, gap[2] * pahpps
        ran_ftb = gap[0] * pftbst + gap[1] * pftb, gap[2] * pahftb
        ran_ra =  gap[0] * prast + gap[1]* pra + gap[2] * pahra

    df_pen2= df_pen2*ran_pen
    df_nsa2= df_nsa2*ran_nsa
    df_pps2= df_pps2*ran_pps
    df_ftb2= df_ftb2*ran_ftb
    df_ra2 = df_ra2*ran_ra

    # df_iu_2 = merge basedata.base&BMYR.&emtr  # no idea what is this

    # included original baseworld basefile rather than work.iu_2
    df_iu_2.drop(columns=['PEN_S',
                          'PEN_C',
                          'PENTOT_S',
                          'PENTOT_C',
                          'NSA21_S',
                          'NSA60_S',
                          'NSADEP_S',
                          'NSA21_C1',
                          'NSA21_C2',
                          'PPS',
                          'PPS_SUP',
                          'FTBA0_13',
                          'FTBA13_15',
                          'FTBA16_19',
                          'FTBA16_19NS',
                          'FTBASUPP',
                          'FTBA0_19B',
                          'FTBBNC',
                          'FTBB0_5S',
                          'FTBBNS',
                          'FTBBSUPP',
                          'RNTAL0S',
                          'RNTAL1S',
                          'RNTAL2S',
                          'RNTAL0C',
                          'RNTAL1C',
                          'RNTAL2C'])
    # data iu_2; set iu_2;
    # retain ran_pen ran_nsa ran_pps ran_ftb ran_ra

    # initialise some variables
    df_base['r_pentype'] = float('nan')  # '    '
    df_base['s_pentype'] = float('nan')  # '    '

    # types of allowance
    df_base['r_alltyper']= float('nan')  # '    '
    df_base['s_alltyper']= float('nan')  # '    '
    df_base['s1_alltyper'] = float('nan')  # '    '
    df_base['s2_alltyper'] = float('nan')  # '    '
    df_base['s3_alltyper'] = float('nan')  # '    '

    # general pension
    df_base['r_pension'] = 0
    df_base['s_pension'] = 0

    # rent assistance
    df_base['r_cra'] = 0
    df_base['s_cra'] = 0

    df_base['r_pensiontaxable'] = 0
    df_base['s_pensiontaxable'] = 0

    df_base['r_pension'] = 0
    df_base['s_pension'] = 0

    df_base['r_allow'] = 0
    df_base['s_allow'] = 0
    df_base['s1_allow'] = 0
    df_base['s2_allow'] = 0
    df_base['s3_allow'] = 0

    df_base['asstest'] = 0  # type of part pensioners category

    # deemed income
    # appropriate rate of deeming calculations
    df_base['deeming_thrsh'] = 1 * df_base.DEEMTHC[df_base['iutype'] == 1] + \
                               2 * df_base.DEEMTHC[df_base['iutype'] == 2] + \
                               3 * df_base.DEEMTHS[df_base['iutype'] == 2] + \
                               4 * df_base.DEEMTHS[df_base['iutype'] == 2]
    df_base['deeming_inc'] = 0

    df_base['deeming_as_assets'] = df_base.R_fin_assetp + df_base.S_fin_assetp
    for i in range(len(df_base['deeming_as_assets'])):
        if df_base.deeming_as_assets[i] < df_base.deeming_thrsh[i]:
            df_base['deeming_inc'][i] = max(0, df_base.deeming_as_assets * df_params.DEEMRT1)
        else:
            df_base['deeming_inc'][i] = (df_base.deeming_thrsh * df_base.DEEMRT1) + (df_base.deeming_as_assets - df_base.deeming_thrsh) * df_base.DEEMRT2

    df_base['deeming_inc'] = df_base.deeming_inc / 26

    df_base['R_IOBTCP_'] = max(0, df_base.R_IOBTCP)
    df_base['S_IOBTCP_'] = max(0, df_base.R_IOBTCP)  # remove negative values as losses not counted for SS income
    df_base['R_irentcp_'] = max(0, df_base.R_irentcp)
    df_base['S_irentcp_'] = max(0, df_base.S_irentcp)

    # deeming_inc / 2,         # Deeming income for IU
    # R_IncTaxSuperImpA, S_IncTaxSuperImpA,
    # R_IWSUCP, S_IWSUCP,      # weekly employee income
    # R_IOBTCP_, S_IOBTCP_,    # own unincorporated business - losses set to 0
    # R_irentcp_, S_irentcp_,  # rental property income - losses set to 0
    # R_IROYARCP, S_IROYARCP,  # Royalties
    # R_IWCOMPCP, S_IWCOMPCP,  # Workers Compensation
    # R_ISSSCP, S_ISSSCP,      # Salary Sacrificed super contributions
    # R_IOREGUCP, S_IOREGUCP,  # Other regular income
    # R_IOSEASCP, S_IOSEASCP)) # Overseas pensions and benefits */

    df_base['ssincome'] = 2 * (df_base['deeming_inc'] / 2 + df_base[['R_IncTaxSuperImpA',
                                                                    'S_IncTaxSuperImpA',
                                                                    'R_IWSUCP', 'S_IWSUCP',
                                                                    'R_IOBTCP_', 'S_IOBTCP_',
                                                                    'R_irentcp_', 'S_irentcp_',
                                                                    'R_IROYARCP', 'S_IROYARCP',
                                                                    'R_IWCOMPCP', 'S_IWCOMPCP',
                                                                    'R_ISSSCP', 'S_ISSSCP',
                                                                    'R_IOREGUCP', 'S_IOREGUCP',
                                                                    'R_IOSEASCP', 'S_IOSEASCP']].sum(axis=1))
    df_base['r_ss_flagp'] = 1
    df_base['s_ss_flagp'] = 1
    df_base['r_ssded'] = (-1)*df_base.r_ss_flagp * df_base.r_issscp * 2  # deduct super salary sacrifice where already included in reported employee income
    df_base['s_ssded'] = (-1)*df_base.s_ss_flagp * df_base.s_issscp * 2
    df_base['ssincome'] = df_base.ssincome + df_base.r_ssded + df_base.s_ssded


    # not including super income as now deemed from 2015 onwards - people are grandfathered so could be problematic ?
    # child support not included as no longer taxable

    # drop r_ssded s_ssded;
    # dont know how to translate drop

    # private income calculation
    def priv(v, df):
        v = str(v)  # this is just in case you don't type a string as input
        # I am going to make the assumption that these variables inside the funtion are columns from a dataframe
        privincomec =  ['_IWSUCP',
                       '_iobtcp',
                       '_IINTCP',
                       '_IDIVTRCP',
                       '_irentcp',
                       '_IROYARCP',
                       '_IINVORCP',
                       '_IncTaxSuperImpA',
                       '_IWCOMPCP',
                       '_IPNHHCP',
                       '_IOREGUCP',
                       '_ICHLDSCP',
                       '_IOSEASCP']

        for i in range(len(privincomec)):
            privincomec[i] = var + privincomec[i]

        df_privincomec = df[privincomec]  # choosing the columns from the dataframe
        var_privincomec = np.round(np.sum(df_privincomec), decimals=2)
        var_ssincome = sum(var_privincomec, -df[var +'_ICHLDSCP'], df[var +'_IDISBCP'], df[var+'_IWARWCP'])
        return var_ssincome
        # note private income here does not include deeming as per ssincome

    df_base['r_ssincome'] = priv(v='R', df=df_base)
    df_base['s_ssincome'] = priv(v='S', df=df_base)
    df_base['s1_ssincome'] = priv(v='S1', df=df_base)
    df_base['s2_ssincome'] = priv(v='S2', df=df_base)
    df_base['s3_ssincome'] = priv(v='S3', df=df_base)

    df_base['r_ssincome'] = (df_base['r_ssincome'] + df_base['r_ssded']) * 2  # remove salary sacrifice amounts where already included (see code above)
    df_base['s_ssincome'] = (df_base['s_ssincome'] + df_base['s_ssded']) * 2

    df_base['SSINCOME_ALL'] = sum(df_base['r_ssincome'], df_base['s_ssincome'])  # special variable for allowances income test for both ref and spouse

    # assessable asset for income unit
    df_base['as_assets'] = (df_base['WEALTHH'] - (df_base['HVALUECH'] - df_base['LIASDCH'])) * df_base['wealth_share']  # HH level assessable wealth
    df_base['as_assets'] = fillna(0)  # set assets equals to zero when value is missing

    # run pension code - DVA, AGE, DSP, PPS, CARER
    df_base['DVAr'] = 0
    df_base['DVAs'] = 0

    # DVA - purely based on ABS SIH
    # R_IDISBCP  # Current weekly income from disability pension (DVA)
    # R_ISERVCP  # Current weekly income from service pension (DVA)
    # R_IWARWCP  # Current weekly income from war widows pension (DVA)
    df_base['DVAr'] = df_base[['R_IDISBCP', 'R_ISERVCP', 'R_IWARWCP']].sum(axis=1)
    df_base['DVAs'] = df_base[['S_IDISBCP', 'S_ISERVCP', 'S_IWARWCP']].sum(axis=1)
    for i in range(len(df_base['DVAr'])):
        if df_base['DVAr'][i] > 0:
            df_base['r_pentype'][i] = 'DVA'
            df_base['r_pension'][i] = df_base['DVAr'][i]
        if df_base['DVAs'][i] > 0:
            df_base['s_pentype'][i] = 'DVA'
            df_base['s_pension'][i] = df_base['DVAs'][i]

    # lines: 221-662
    # rent assistance for age pension - no rent reduction macro for DFISA
    def rentcalc(rentass, df_base):
        # derive minimum rent
        df_base['minrent'] = (df_base['iutype'] in [1, 2]) * df_base['SSTOTDEP']['SSTOTDEP'== 0] * df_base['MRNTAL0C'] + \
                                (df_base['iutype'] in [1, 2]) * (df_base['SSTOTDEP'] in [1, 2]) * df_base['MRNTAL1C'] + \
                                (df_base['iutype'] in [1, 2]) * df_base['SSTOTDEP']['SSTOTDEP' > 2] * df_base['MRNTAL0S'] + \
                                (df_base['iutype'] in [3, 4]) * df_base['SSTOTDEP']['SSTOTDEP' == 0] * df_base['MRNTAL0S'] + \
                                (df_base['iutype'] in [3, 4]) * (df_base['SSTOTDEP'] in [1, 2]) * df_base['MRNTAL1S'] + \
                                (df_base['iutype'] in [3, 4]) * df_base['SSTOTDEP']['SSTOTDEP' > 2] * df_base['MRNTAL2S']

        df_base['maxcra'] = (df_base['iutype'] in [1, 2]) * df_base['SSTOTDEP']['SSTOTDEP' == 0] * df_base['RNTAL0C'] + \
                             (df_base['iutype'] in [1, 2]) * (df_base['SSTOTDEP'] in [1, 2]) * df_base['RNTAL1C'] + \
                             (df_base['iutype'] in [1, 2]) * df_base['SSTOTDEP']['SSTOTDEP' > 2] * df_base['RNTAL2C'] + \
                             (df_base['iutype'] in [3, 4]) * df_base['SSTOTDEP']['SSTOTDEP' == 0] * df_base['RNTAL0S'] + \
                             (df_base['iutype'] in [3, 4]) * (df_base['SSTOTDEP'] in [1, 2]) * df_base['RNTAL1S'] + \
                             (df_base['iutype'] in [3, 4]) * df_base['SSTOTDEP']['SSTOTDEP' > 2] * df_base['RNTAL2S']


        if df_base['natoccu'] == 4 and df_base['iurent'] * 2 > df_base['minrent']:
            df_base[rentass] = max(0, ((df_base['iurent'] * 2 - df_base['minrent']) * 0.75))
            if df_base[rentass] > df_base['maxcra']:
                df_base[rentass] = df_base['maxcra']

    # lines: 1035 - 1089
    # AGE/DSP/CARER calculations - eligibility and entitlement
    def pen(age, sex, pentype, pension, pensioni, pensiona, pers, pensiontaxable, paytest, df_base):
        # flag for both ref and spouse on pension and therefore both receive 50% of CRA

        if (df_base['iutype'] in [1, 2]) and \
                (df_base[age] >= sum(df_base[sex][sex == 1] * df_base['PENSAGE_M'], df_base[sex][sex == 2] * df_base['PENSAGE_F'])) and \
                (df_base[age] >= sum(df_base[sex][sex == 1] * df_base['PENSAGE_M'], df_base[sex][sex == 2] * df_base['PENSAGE_F'])) or \
                (sum(df_base[pers+'IDSUPPCP', df_base[pers+'ICAREPCP']]) > 0):
            df_base['cra_cpl'] = 1


        if (df_base[pers+'IDSUPPCP'][pers+'IDSUPPCP' > 0]) or \
                (df_base[pers+'ICAREPCP'][pers+'ICAREPCP' > 0]) or \
                (df_base[age] >= sum((df_base[sex][sex == 1]) * df_base['PENSAGE_M'], (df_base[sex][sex == 2]) * df_base['PENSAGE_F'])) and \
                (df_base[pentype][pentype == '    ']):

            df_base['penmax'] = (df_base['iutype'] in [1,2]) * sum(df_base['PEN_C'], df_base['PENTOT_C']) + \
                                (df_base['iutype'] in (3,4)) * sum(df_base['PEN_S'], df_base['PENTOT_S'])

            df_base['IncFree'] = (df_base['iutype'] in [1,2]) * df_base['INCTST1_C'] + \
                                 (df_base['iutype'] in [3,4]) * df_base['INCTST1_S']

            df_base['energysupp'] = (df_base['iutype'] in [1, 2]) * df_base['PENPAYC_ES'] + \
                                 (df_base['iutype'] in [3, 4]) * df_base['PENPAYS_ES']

            rentcalc('r_cra', df_base)
            if df_base['cra_cpl'] == 1:
                df_base['r_cra'] /= 2  # pensioner couple

            df_base['penmaxtot'] = sum(df_base['penmax'], df_base['r_cra'], df_base['energysupp'])
            df_base[pensioni] = max(0, (df_base['penmaxtot'] - (df_base['ssincome'] > df_base['IncFree']) * (df_base['ssincome'] - df_base['IncFree']) * df_base['INCTAP']))  # income test only

            # asset test free area calculation

            df_base['assfree'] = (df_base['iutype'] in [1,2]) * (df_base['natoccu'] in [1,2]) * df_base['ASSTST1_C'] + (df_base['iutype'] not in [1,2]) * (df_base['natoccu'] in [1,2]) * df_base['ASSTST1_S'] + \
                                 (df_base['iutype'] in [1,2]) * (df_base['natoccu'] not in [1,2]) * df_base['ASSTST2_C'] + (df_base['iutype'] not in [1,2]) * (df_base['natoccu'] not in [1,2]) * df_base['ASSTST2_S']

            df_base[pensiona] = max(0, (df_base['penmaxtot'] - (df_base['as_assets'] > df_base['assfree']) * (df_base['as_assets'] - df_base['assfree']) *
                                ((df_base['iutype'] in [1,2]) * df_base['ASSTAP'] / 2 + (df_base['iutype'] in [3,4]) * df_base['ASSTAP'])))

            df_base[pension] = min(df_base[pensioni], df_base[pensiona]) # final pension entitlement

            if df_base[pension] > 0:
                df_base[pentype] = 'AGE'

                if df_base[pension] == df_base['penmaxtot']:
                    df_base[paytest] = 1  # max rate recipient
                elif df_base[pensioni] < df_base[pensiona]:
                    df_base[paytest] = 2  # income test recipient
                else:
                    df_base[paytest] = 3  # income test recipient

                # carer payment
                if df_base[pers+'ICAREPCP'] > 0:
                    df_base[pentype] = 'CARE'

                # DPS payment
                if df_base[pers+'IDSUPPCP'] > 0:
                    df_base[pentype] = 'DSP'

        if sum(df_base['r_cra'], df_base['energysupp']) <= df_base[pension]:
            df_base[pensiontaxable] = df_base[pension] - sum(df_base['r_cra'], df_base['energysupp'])
        elif 0 < df_base[pension] < sum(df_base['r_cra'], df_base['energysupp']):
            df_base[pensiontaxable] = 0
        else:
            df_base[pensiontaxable] = 0


    pen('r_age_act', 'r_sexp', 'r_pentype', 'r_pension', 'r_pension_i', 'r_pension_a', 'r_', 'r_pensiontaxable', 'r_paytest', df_base)
    pen('s_age_act', 's_sexp', 's_pentype', 's_pension', 's_pension_i', 's_pension_a', 's_', 's_pensiontaxable', 's_paytest', df_base)


    # lines: 1097 - 1130
    # Parenting Payment single pension
    def pps(age, pentype, pension, pensiontaxable, df_base):
        df_base['IF_PPS'] = df_base['PPSTHRSH'] + df_base['PPS_DEP'] * (df_base['numdeps_pps'] - 1)

        # cut off for PPS and PPP
        df_base['ppscutoff1'] = df_base['IF_PPS'] + ((df_base['PPS'] + df_base['PPS_SUP'] + df_base['PARPAYS_ES']) / df_base['PPSTAP'])
        df_base['Tot_PPS'] = df_base['PPS'] + df_base['PPS_SUP'] + df_base['PARPAYS_ES']

        if df_base['SSINCOME'] <= df_base['IF_PPS']:
            df_base[pension] = df_base['Tot_PPS']
        elif df_base['IF_PPS'] < df_base['SSINCOME'] <= df_base['ppscutoff1']:
            df_base[pension] = max(0, (df_base['Tot_PPS'] - ((df_base['SSINCOME'] - df_base['IF_PPS']) * df_base['PPSTAP'])))

        if df_base[pension] > 0:
            df_base[pentype] = 'PPS'

        if df_base[pension] == df_base['Tot_PPS']:
            df_base['r_paytest'] = 1
        elif 0 < df_base[pension] < df_base['Tot_PPS']:
            df_base['r_paytest'] = 2

        if df_base[pension] > 0:
            df_base[pensiontaxable] = df_base[pension]
            df_base[pension] += (df_base['PHARALS'] + (df_base['INCBONS'] / 13) + (df_base['TELALS1'] / 6.5))


    if df_base['Iutype'] == 3 and df_base['numdeps_pps'] > 0 and df_base['r_pension'] <= 0:
        df_base['test'] = 1
        pps('r_age_act', 'r_pentype', 'r_pension', 'r_pensiontaxable', df_base)

    # lines 1140 - 1198
    # Allowances module
    def allow(age, sex, alltype, allow, allow_ind_nsa, ssincome, pers, ref, df_base):
        # SIH based only payments

        # Austudy or Abstudy
        if df_base[pers+'IAUSTCP'] > 0 and sum(df_base['r_pension'], df_base['s_pension']) <= 0:
            df_base[alltype] = 'AUST'
            df_base[allow] = (df_base[pers+'IAUSTCP'] * 2) * 1.025 ** (df_base['year']-2015)

        # youth allowance
        if df_base[pers+'IYOUTHCP'] > 0 and sum(df_base['r_pension'], df_base['s_pension']) <= 0:
            df_base[alltype] = 'YUTH'
            df_base[allow] = (df_base[pers+'IYOUTHCP'] * 2) * 1.025 ** (df_base['year']-2015)  # alter to fortnightly

        # New start - single
        if (df_base['AGE_IND'] <= df_base[age] < sum((df_base[sex][sex == 1]) * df_base['PENSAGE_M'], (df_base[sex][sex == 2]) * df_base['PENSAGE_F'])) and \
            (df_base[pers+'INEWLSCP'] > 0 or df_base[pers+'IPARENCP'] > 0 or df_base[pers+'ISICKCP'] > 0 or df_base[pers+'ISPECCP'] > 0 or df_base[pers+'IWIDOWCP'] > 0) and \
            sum(df_base['r_pension'], df_base['s_pension']) <= 0:

            # max rate
            df_base['allmax'] = (df_base['iutype']['iutype'] == 4) * (df_base[age] < df_base['AGE_HIGH']) * df_base['NSA21_S'] + \
                                (df_base['iutype']['iutype'] == 4) * (df_base[age] >= df_base['AGE_HIGH']) * df_base['NSA60_S'] + \
                                (df_base['iutype']['iutype'] == 3) * (df_base[age] < df_base['AGE_HIGH']) * df_base['NSADEP_S'] + \
                                (df_base['iutype']['iutype'] == 3) * (df_base[age] >= df_base['AGE_HIGH']) * df_base['NSADEP_S'] + \
                                (df_base['iutype']['iutype'] == 1) * (df_base[age] < df_base['AGE_HIGH']) * df_base['NSA21_C2'] + \
                                (df_base['iutype']['iutype'] == 2) * (df_base[age] < df_base['AGE_HIGH']) * df_base['NSA21_C1']

            # energy supplement
            df_base['energysupp'] = (df_base['iutype']['iutype' == 4]) * df_base['NSA_S_ES'] + \
                                    (df_base['iutype']['iutype' == 3]) * df_base['NSADEP_S_ES'] + \
                                    (df_base['iutype']['iutype' == 1]) * df_base['NSADEP_P_ES'] + \
                                    (df_base['iutype']['iutype' == 2]) * df_base['NSADEP_P_ES']

            # rent assistance NOT for IUs with deps
            df_base['minrent'] = (df_base['iutype']['iutype' == 2]) * df_base['MRNTAL0C'] + (df_base['iutype']['iutype' == 4]) * df_base['MRNTAL0S']
            df_base['maxcra'] = (df_base['iutype']['iutype' == 2]) * df_base['RNTAL0C'] + (df_base['iutype']['iutype' == 4]) * df_base['RNTAL0S']

            if df_base['natoccu'] == 4 and df_base['iurent'] * 2 > df_base['minrent']:
                df_base['dfr_cra'] = max(0, (df_base['iurent'] * 2 - df_base['minrent']) * 0.75)
                if df_base['r_cra'] > df_base['maxcra']:
                    df_base['r_cra'] = df_base['maxcra']

            df_base['allmax'] = df_base['allmax'] + df_base['energysupp'] + df_base['r_cra'] * df_base[ref]

            # insert correct taper
            df_base['NSATP1'] = sum((df_base['iutype']['iutype' == 3]) * df_base['NSATAP1_SP'], (df_base['iutype']['iutype' != 3]) * df_base['NSATAP1'])
            df_base['NSATP2'] = sum((df_base['iutype']['iutype' == 3]) * df_base['NSATAP2_SP'], (df_base['iutype']['iutype' != 3]) * df_base['NSATAP2'])

            if df_base[ssincome] < df_base['NSATHR1']:
                df_base[allow_ind_nsa] = df_base['allmax']
            elif df_base[ssincome] < df_base['NSATHR2']:
                df_base[allow_ind_nsa] = df_base['allmax'] - \
                                         (df_base[ssincome] - df_base['NSATHR1']) * df_base['NSATP1']
            elif df_base[ssincome] >= df_base['NSATHR2']:
                df_base[allow_ind_nsa] = df_base['allmax'] - \
                                         (df_base[ssincome] - df_base['NSATHR2']) * df_base['NSATP2'] - \
                                         (df_base['NSATHR2'] - df_base['NSATHR1']) * df_base['NSATP1']


            if df_base[allow_ind_nsa] > 0 and df_base[pers+'INEWLSCP'] > 0:
                df_base[alltype] = 'NSA'
            elif df_base[allow_ind_nsa] > 0 and df_base[pers+'ISICKCP'] > 0:
                df_base[alltype] = 'SICK'
            elif df_base[allow_ind_nsa] > 0 and df_base[pers+'ISPECCP'] > 0:
                df_base[alltype] = 'SPEC'

            if df_base[allow_ind_nsa] > 0:
                df_base[allow_ind_nsa] = df_base[allow_ind_nsa] + df_base['INCBONS'] / 13 * \
                                         (df_base['iutype'] in [3,4]) + df_base['INCBONC'] / 13 * \
                                         (df_base['iutype'] in [1,2]) + df_base['PHARALS'] * \
                                         (df_base['iutype'] in [3])

    # calling allow function
    if df_base['iutype'] in [1, 2]:
        allow('r_age_act', 'r_sexp', 'r_alltype', 'r_allow', 'r_allow_ind_nsa', 'r_ssincome', 'R_', eval(df_base['r_ssincome'] <= df_base['s_ssincome']), df_base)
        allow('s_age_act', 's_sexp', 's_alltype', 's_allow', 's_allow_ind_nsa', 's_ssincome', 'S_', eval(df_base['s_ssincome'] < df_base['r_ssincome']), df_base)

    if df_base['iutype'] in [3, 4]:
        allow('r_age_act', 'r_sexp', 'r_alltype', 'r_allow', 'r_allow_ind_nsa', 'r_ssincome', 'R_', 1, df_base)

    # check and reduction for NSA couple IU (partner income test)
    if df_base['iutype'] in [1, 2]:
        if df_base['r_allow_ind_nsa'] > 0 and df_base['s_allow_ind_nsa'] < 0:
            df_base['r_allow_ind_nsa'] = max(0, sum(df_base['r_allow_ind_nsa'], (df_base['s_allow_ind_nsa'] < 0) * df_base['s_allow_ind_nsa'] * df_base['PINTAP'] / df_base['NSATAP2']))
            if df_base['r_allow_ind_nsa'] <= 0 and df_base['r_alltype'] == 'NSA':
                df_base['r_alltype'] = '   '

        if df_base['s_allow_ind_nsa'] > 0 and df_base['r_allow_ind_nsa'] < 0:
            df_base['s_allow_ind_nsa'] = max(0, sum(df_base['s_allow_ind_nsa'], (df_base['r_allow_ind_nsa'] < 0) * df_base['r_allow_ind_nsa'] * df_base['PINTAP'] / df_base['NSATAP2']))
            if df_base['s_allow_ind_nsa'] <= 0 and df_base['s_alltype'] == 'NSA':
                df_base['s_alltype'] = '   '

    # PARENTING PAYMENT PARTNERED - SPECIAL CASE OF NSA WHERE YOUNGEST CHILD AGE < 6 YEARS
    # - assumes PPP and NSA are the same payment in terms of $ received any deviation from this existing policy implies new code required

    if df_base['iutype'] == 1 and df_base['numdeps_ppp'] > 0 and sum(df_base['r_allow_ind_nsa'], df_base['s_allow_ind_nsa']) > 0:
        if df_base['r_allow_ind_nsa'] >= df_base['s_allow_ind_nsa']:
            df_base['r_alltype'] = 'PPP'
        else:
            df_base['s_alltype'] = 'PPP'

    # lines 1246 - 1295
    # cases where one partner has a pension
    def allowpens(age, sex, alltype, allow, allow_ind_nsa, pers, ref, pension, df_base):
        # SIH based only playments

        # Austudy or Abstudy
        if df_base[pers+'IAUSTCP'] > 0 and sum(df_base['r_pension'], df_base['s_pension']) <= 0:
            df_base[alltype] = 'AUST'
            df_base[allow] = (df_base[pers+'IAUSTCP'] * 2) * 1.025 ** (df_base['year'] - 2015)

        # Youth Allowance
        if df_base[pers+'IYOUTHCP'] > 0 and sum(df_base['r_pension'], df_base['s_pension']) <= 0:
            df_base[alltype] = 'YUTH'
            df_base[allow] = (df_base[pers+'IYOUTHCP'] * 2) * 1.025 ** (df_base['year'] - 2015)

        # Newstart - single
        if (df_base['AGE_IND'] <= df_base[age] < sum((df_base[sex][sex == 1]) * df_base['PENSAGE_M'], (df_base[sex][sex == 2]) * df_base['PENSAGE_F'])) and \
            (df_base[pers+'INEWLSCP'] > 0 or df_base[pers+'IPARENCP'] > 0 or df_base[pers+'ISICKCP'] > 0 or df_base[pers+'ISPECCP'] > 0 or df_base[pers+'IWIDOWCP'] > 0) and \
            sum(df_base['r_pension'], df_base['s_pension']) > 0:

            # max rate

            df_base['penage'] = sum((df_base[sex][sex == 1]) * df_base['PENSAGE_M'], (df_base[sex][sex == 2]) * df_base['PENSAGE_F'])

            df_base['allmax'] = (df_base['iutype']['iutype' == 1]) * (df_base[age] < df_base['penage']) * df_base['NSA21_C2'] + \
                                (df_base['iutype']['iutype' == 2]) * (df_base[age] < df_base['penage']) * df_base['NSA21_C1']

            # Energy Supplement
            df_base['energysupp'] = (df_base['iutype']['iutype' == 1]) * df_base['NSADEP_P_ES'] + (df_base['iutype']['iutype' == 2]) * df_base['NSADEP_P_ES']

            df_base['allmax'] += df_base['energysupp']

            # insert correct taper
            df_base['NSATP1'] = sum((df_base['iutype']['iutype' == 3]) * df_base['NSATAP1_SP'], (df_base['iutype']['iutype' != 3]) * df_base['NSATAP1'])
            df_base['NSATP2'] = sum((df_base['iutype']['iutype' == 3]) * df_base['NSATAP2_SP'], (df_base['iutype']['iutype' != 3]) * df_base['NSATAP2'])

            if df_base['ssincome'] / 2 < df_base['NSATHR1']:
                df_base[allow_ind_nsa] = df_base['allmax']
            elif df_base['ssincome'] / 2 < df_base['NSATHR2']:
                df_base[allow_ind_nsa] = max(0, df_base['allmax'] -
                                         (df_base['ssincome'] / 2 - df_base['NSATHR1']) * df_base['NSATP1'])
            elif df_base['ssincome'] / 2 >= df_base['NSATHR2']:
                df_base[allow_ind_nsa] = max(0, df_base['allmax'] -
                                         (df_base['ssincome'] / 2 - df_base['NSATHR2']) * df_base['NSATP2'] -
                                         (df_base['NSATHR2'] - df_base['NSATHR1']) * df_base['NSATP1'])

            if df_base[allow_ind_nsa] > 0:
                df_base[allow_ind_nsa] = df_base[allow_ind_nsa] + df_base['INCBONC'] / 13 * (df_base['iutype'] in [1,2])

            if df_base[allow_ind_nsa] > 0 and df_base[pers+'INEWLSCP'] > 0:
                df_base[alltype] = 'NSA'
            elif df_base[allow_ind_nsa] > 0 and df_base[pers+'ISICKCP']> 0:
                df_base[alltype] = 'SICK'
            elif df_base[allow_ind_nsa] > 0 and df_base[pers+'ISPECCP']> 0:
                df_base[alltype] = 'SPEC'

            if df_base[pension] > 0:
                df_base[allow_ind_nsa] = 0

    if df_base['iutype'] in [1, 2]:
        allowpens('r_age_act', 'r_sexp', 'r_alltype', 'r_allow', 'r_allow_ind_nsa', 'R_', eval(r_ssincome <= s_ssincome), 'r_pension', df_base)
        allowpens('s_age_act', 's_sexp', 's_alltype', 's_allow', 's_allow_ind_nsa', 'S_', eval(s_ssincome < r_ssincome), 's_pension', df_base)

        # PARENTING PAYMENT PARTNERED - SPECIAL CASE FOR NSA WHERE YOUNGEST CHILD AGE < 6 YEARS

        # assume PPP and NSA are the same payment in terms of $ received and deviation
        # from this existing policy implies new code required

    if df_base['iutype'] == 1 and df_base['numdeps_ppp'] > 0 and sum(df_base['r_allow_ind_nsa'], df_base['s_allow_ind_nsa']) > 0:
        if df_base['r_allow_ind_nsa'] >= df_base['s_allow_ind_nsa']:
            df_base['r_alltype'] = 'PPP'
        else:
            df_base['s_alltype'] = 'PPP'

    if df_base['r_allow_ind_nsa'] > 0:
        df_base['r_allow'] = df_base['r_allow_ind_nsa']
    if df_base['s_allow_ind_nsa'] > 0:
        df_base['s_allow'] = df_base['s_allow_ind_nsa']

    if sum(df_base['r_cra'], df_base['energysupp']) <= df_base['r_allow']:  # <= allmax
        df_base['r_allowtaxable'] = df_base['r_allow'] - sum(df_base['r_cra'], df_base['energysupp']) - df_base['INCBONC'] / 13 * (df_base['iutype'] in [1,2])
    elif 0 < df_base['r_allow'] < sum(df_base['r_cra'], df_base['energysupp']):
        df_base['r_allowtaxable'] = 0

    if sum(df_base['energysupp']) <= df_base['s_allow']:  # <=  allmax
        df_base['s_allowtaxable'] = df_base['s_allow'] - sum(df_base['energysupp']) - df_base['INCBONC'] / 13 * (df_base['iutype'] in [1,2])
    elif 0 < df_base['s_allow'] < sum(df_base['energysupp']):
        df_base['s_allowtaxable'] = 0

    if df_base['r_alltype'] == 'NSA' and df_base['iutype'] == 3:
        df_base['r_allow'] += (df_base['TELALS1'] / 6.5)  # add in telephone allowance

    # Youth Allowance Calculations for CRA

    if (df_base['r_alltype'] in ['YUTH', 'YUTH'] or df_base['s_alltype'] in ['YUTH', 'YUTH']) and df_base['r_cra'] == 0:
        # rent assistance NOT for IUs with deps

        df_base['minrent'] = (df_base['iutype']['iutype' == 2]) * df_base['MRNTAL0C'] + (df_base['iutype']['iutype' == 4]) * df_base['MRNTAL0S']
        df_base['maxcra'] = (df_base['iutype']['iutype' == 2]) * df_base['RNTAL0C'] + (df_base['iutype']['iutype' == 4]) * df_base['RNTAL0S']

        if df_base['natoccu'] == 4 and df_base['iurent'] * 2 > df_base['minrent']:
            df_base['r_cra'] = max(0, (df_base['iurent'] * 2 - df_base['minrent']) * 0.75)
            if df_base['r_cra'] > df_base['maxcra']:
                df_base['r_cra'] = df_base['maxcra']

    df_base['r_allow'] = sum(df_base['r_allow'], df_base['r_cra'])

    # Adjusted Taxable Income Calculation

    # INITIALISE VARIABLES

    # TAXABLE INCOME
    df_base['r_tinc'] = 0
    df_base['s_tinc'] = 0
    df_base['s1_tinc'] = 0
    df_base['s2_tinc'] = 0
    df_base['s3_tinc'] = 0

    # NET INCOME (PER DEDUCTIONS)
    df_base['r_ninc'] = 0
    df_base['s_ninc'] = 0
    df_base['s1_ninc'] = 0
    df_base['s2_ninc'] = 0
    df_base['s3_ninc'] = 0

    # PRIVATE INCOME
    df_base['r_privinc'] = 0
    df_base['s_privinc'] = 0
    df_base['s1_privinc'] = 0
    df_base['s2_privinc'] = 0
    df_base['s3_privinc'] = 0

    # TRANSFER INCOME
    df_base['r_trinc'] = 0
    df_base['s_trinc'] = 0
    df_base['s1_trinc'] = 0
    df_base['s2_trinc'] = 0
    df_base['s3_trinc'] = 0

    # ANNUAL WORKING INCOME OF MATURE AGE WORKER
    df_base['r_mainc'] = 0
    df_base['s_mainc'] = 0

    # ADJUSTED TAXABLE INCOME
    df_base['r_adjtax'] = 0
    df_base['s_adjtax'] = 0
    df_base['adjtaxp'] = 0  # Parental
    df_base['s1_adjtax'] = 0
    df_base['s2_adjtax'] = 0
    df_base['s3_adjtax'] = 0

    # IMPUTATION CREDIT/DIVIDEND REBATE
    df_base['r_divreb'] = 0
    df_base['s_divreb'] = 0
    df_base['s1_divreb'] = 0
    df_base['s2_divreb'] = 0
    df_base['s3_divreb'] = 0

    # FLAG TO ADD BACK ON NON-TAXABLE PENSIONS AND BENEFITS TO ATI
    df_base['r_atiflag'] = 0
    df_base['s_atiflag'] = 0

    if df_base['s1_IYOUTHCP'] > 0:
        df_base['s1_alltype'] = 'YUTH'
        df_base['s1_allow'] = (df_base['s1_IYOUTHCP'] * 2) * 1.025 ** (df_base['year'] -2015)  # alter to fortnightly

    if df_base['s2_IYOUTHCP'] > 0:
        df_base['s2_alltype'] = 'YUTH'
        df_base['s2_allow'] = (df_base['s2_IYOUTHCP'] * 2) * 1.025 ** (df_base['year'] -2015)  # alter to fortnightly

    if df_base['s3_IYOUTHCP'] > 0:
        df_base['s3_alltype'] = 'YUTH'
        df_base['s3_allow'] = (df_base['s3_IYOUTHCP'] * 2) * 1.025 ** (df_base['year'] -2015)  # alter to fortnightly

        # CALCULATE NET ASSESSABLE INCOME

        # develop private income with dividend rebate
    def incdiv(pers):
        if df_base[pers+'age'] > 0 and df_base[pers+'IDIVTRCP'] > 0:
            df_base[pers+'divreb'] = (0.96 * df_base[pers+'IDIVTRCP'] * .3 / (1 - .3))

    incdiv('r_')
    incdiv('s_')
    incdiv('s1_')
    incdiv('s2_')
    incdiv('s3_')

    # develop private income with dividend rebate
    def privinc(pers):
        if df_base[pers+'age'] > 0:
            df_base[pers+'privinc'] = sum(df_base[pers+'privincomec'], df_base[pers+'divreb'])

    privinc('r_')
    privinc('s_')
    privinc('s1_')
    privinc('s2_')
    privinc('s3_')

    # CALCULATE REFS TRANSFER INCOME
    df_base['r_traninc'] = sum(df_base['r_pension'], df_base['r_allow'])
    df_base['s_traninc'] = sum(df_base['s_pension'], df_base['s_allow'])

    # CALCULATE NET INCOME FOR REFERENCE

    # BP have greatly simplified net income - could be problems with some DVA payment
    # and carer pensioners over age of pension age

    df_base['r_ninc'] = sum(df_base['r_privinc'] * 2, df_base['r_allowtaxable'], df_base['r_pensiontaxable'],
                 -df_base['r_pensiontaxable'] * (df_base['r_pentype'] in ['DSP' 'DVA' 'CARE']), -df_base['r_ICHLDSCP'] * 2)

    # -2*r_deduc*(age_actr ge 55)
    # potentially include in later version of model - super data not overly helpful and
    # may require data from ATO

    # CALCULATE NET INCOME FOR SPOUSE

    if df_base['s_AGEEC'] > 0:
        df_base['s_ninc'] = sum(df_base['s_privinc'] * 2, df_base['s_allowtaxable'], df_base['s_pensiontaxable'],
                     -df_base['s_pensiontaxable'] * (df_base['s_pentype'] in ['DSP' 'DVA' 'CARE']), -df_base['s_ICHLDSCP'] * 2)

    """
    # -------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    #                                   Jetro Section
    # -------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    """

    # *--------------------------------------------------------------------*
    # *------------------------IMPUTE TAXABLE INCOME-----------------------*
    # *--------------------------------------------------------------------*;
    #   DEFINE MACRO TO IMPUTE        */
    #   DEDUCTIONS AND REDUCE NET     */
    #   INCOME TO GIVE TAXABLE INCOME */
    #
    # /* Macro to calculate tax deductions */
    # ~BP REmove Work Deductions (this will lead to some minor differences
    # in results but perhaps at this point not worth the effort */

    df_base['r_ninc'] *= 26  # ANNUALIZED NET INCOME
    df_base['s_ninc'] *= 26

    # DEDUCTIONS FOR OTHER RUNS
    # CORRECT TAXABLE INCOME - EXCLUDE SALARY - SACRIFICED AMTS
    # FOR THOSE WHO INCLUDED THIS IN THEIR REPORTED INCOME
    df_base['r_tinc'] = df_base.r_ninc - df_base.r_totded + -df_base.R_ss_flagp * df_base.r_issscp * 52 - df_base.R_ss_flagp * df_base.r_ssfbp * 52

    df_base.loc[df_base['s_AGEEC'] > 0, 's_tinc'] = df_base.s_ninc - df_base.s_totded + df_base.S_ss_flagp * df_base.s_issscp * 52 - df_base.S_ss_flagp * df_base.s_ssfbp * 52

    # *--------------------------------------------------------------------*
    # *---------------CALCULATE ADJUSTED TAXABLE INCOME--------------------*
    # *---------------------- REF AND SPOUSE ------------------------------*
    # *--------------------------------------------------------------------*

    mask = (df_base['r_pentype'] in ['DSP' 'DVA' 'CARE']) & (df_base['r_irentcp'] < 0)
    df_base['r_adjtax'][mask] = df_base.r_tinc + df_base.r_pensiontaxable * df_base.r_pentype * 26 + \
                                df_base.r_irentcp * abs(df_base.r_irentcp * 52) - df_base.r_ICHLDSCP * 52 + \
                                df_base.R_ss_flagp * df_base.r_issscp * 52 + df_base.R_ss_flagp * df_base.r_ssfbp * 52 + \
                                df_base.r_non_ssfbp * 52

    mask = (df_base['df_s_AGEEC'] > 0) & (df_base['s_pentype'] in ['DSP' 'DVA' 'CARE']) & (df_base['s_irentcp'] < 0) & (
                df_base['S_ss_flagp'] == 0)
    df_base['s_adjtax'][mask] = df_base.s_tinc + df_base.s_pensiontaxable * df_base.s_pentype * 26 + \
                                df_base.s_irentcp * abs(df_base.s_irentcp) * 52 - \
                                df_base.s_ICHLDSCP * 52 + df_base.S_ss_flagp * df_base.s_issscp * 52 + \
                                df_base.S_ss_flagp * df_base.s_ssfbp * 52 + df_base.s_non_ssfbp * 52

    df_base.loc[df_base['s_AGEEC'] > 0, 'adjtaxip'] = df_base.r_adjtax + df_base.s_adjtax
    df_base.loc[df_base['s_AGEEC'] <= 0, 'adjtaxip'] = df_base.r_adjtax

    # UP TO HERE ... MUST ADD IN SHARELOSSES and deductions to ATI ????? AND ADJTAXIP NOT REALLY
    # HIGH ENOUGH IT WOULD SEEM
    # FTB CALCUALATION
    #
    # Rent Assistance
    mask = (df_base['iutype'] == 1) & (df_base['SSFAMDEP'] <= 2) & (df_base['iurent'] * 2 >= df_base['mrntal1c'])
    df_base['r_cra'][mask] = min([df_base.rntal1c, -(df_base.rntal1c - (df_base.iurent * 2 - df_base.mrntal1c) * 0.75)])

    mask = (df_base['iutype'] == 1) & (df_base['SSFAMDEP'] > 2) & (df_base['iurent'] * 2 >= df_base['mrntal2c'])
    df_base['r_cra'][mask] = min([df_base.rntal2c, -(df_base.rntal2c - (df_base.iurent * 2 - df_base.mrntal2c) * 0.75)])

    mask = (df_base['iutype'] == 2) & (df_base['SSFAMDEP'] <= 2) & (df_base['iurent'] * 2 >= df_base['mrntal1c'])
    df_base['r_cra'][mask] = min([df_base.rntal1c, -(df_base.rntal1c - (df_base.iurent * 2 - df_base.mrntal1c) * 0.75)])

    mask = (df_base['iutype'] == 2) & (df_base['SSFAMDEP'] > 2) & (df_base['iurent'] * 2 >= df_base['mrntal2c'])
    df_base['r_cra'][mask] = min([df_base.rntal2c, -(df_base.rntal2c - (df_base.iurent * 2 - df_base.mrntal2c) * 0.75)])

    mask = (df_base['iutype'] == 3) & (df_base['SSFAMDEP'] <= 2) & (df_base['iurent'] * 2 >= df_base['mrntal1s'])
    df_base['r_cra'][mask] = min([df_base.rntal1s, -(df_base.rntal1s - (df_base.iurent * 2 - df_base.mrntal1s) * 0.75)])

    mask = (df_base['iutype'] == 3) & (df_base['SSFAMDEP'] > 2) & (df_base['iurent'] * 2 >= df_base['mrntal2s'])
    df_base['r_cra'][mask] = min([df_base.rntal2s, -(df_base.rntal2s - (df_base.iurent * 2 - df_base.mrntal2s) * 0.75)])

    df_base.loc[df_base['r_cra'] < 0, 'r_cra'] = 0

    # Family Tax Benefits- PART A
    df_base['Tot_FTBA1'] = 0
    df_base['Tot_FTBA2'] = 0
    df_base['Max_FTBA1'] = 0
    df_base['Max_FTBA2'] = 0
    df_base['FTB'] = 0
    df_base['Tot_FTBB'] = 0
    df_base['FTBB_flag'] = 0

    # number of kids
    df_base['totdep012'] = df_base['DEP_LT13']
    df_base['totdep1315'] = df_base['DEP13_15']
    df_base['totdep16p'] = df_base['DEPSTUDT']
    df_base['totdep019'] = df_base['SSTOTDEP']

    # Include MYEFO 16 supp income test for FTB A - actually applies from Jan 1 2017 -
    # if doing quarterly may like to adjust
    # include for 2017 onwards only in final code ~BP Budget 2017
    df_base.loc[(df_base['year'] > 2016) & (df_base['adjtaxip'] <= df_base['FTBASUPPTHRSH']), 'FTBASUPP'] = df_base.adjtaxip * df_base.FTBASUPP

    # include for 2017 onwards only in final code ~BP Budget 2017
    df_base.loc[(df_base['year'] == 2016) & (df_base['adjtaxip'] > df_base['FTBASUPPTHRSH']), 'FTBASUPP'] = df_base.FTBASUPP / 2

    # Maximum rate of FTBA per number of kids
    # Add rent assistance to the maximum rate of FTB partA method1 - must have kids
    df_base.loc[df_base['totdep019'] > 0, 'Max_FTBA1'] = df_base.totdep012 * (df_base.FTBA0_13 + df_base.FTBASUPP) + \
                                                         df_base.totdep1315 * (df_base.FTBA13_15 + df_base.FTBASUPP) + \
                                                         df_base.totdep16p * (df_base.FTBA16_19 + df_base.FTBASUPP) + \
                                                         df_base.r_cra * 26 * df_base.totdep019

    df_base['Tot_energy_ftb1'] = df_base.totdep012 * df_base.FTBAS0_13_ES + df_base.totdep1315 * df_base.FTBAS13_15_ES + \
                                 df_base.totdep16p * df_base.FTBAS16_19_ES

    df_base['Max_FTBA2'] = df_base.totdep019 * df_base.FTBA0_19B
    df_base['Tot_energy_ftb2'] = df_base.totdep019 * df_base.FTBAS0_19_ES

    # Calculate FTBA Entitlement based on two methods
    # Method 1 - INCREASED TAPER FOR INCOMES OVER THRESHOLD 1
    df_base['HIINC_K'] = (df_base['FTBATHR1'] - df_base['FTBATHR2']) * df_base['FTBARED']  # High income constant component, to save making the formula more messy
    df_base.loc[df_base['r_traninc'] + df_base['s_traninc'] > 0, 'Tot_FTBA1'] = df_base.Max_FTBA1 + df_base.Tot_energy_ftb1
    df_base.loc[df_base['adjtaxip'] <= df_base['FTBATHR2'], 'Tot_FTBA1'] = df_base.Max_FTBA1 + df_base.Tot_energy_ftb1
    df_base.loc[df_base['adjtaxip'] <= df_base['FTBATHR1'], 'Tot_FTBA1'] = df_base.Max_FTBA1 + df_base.Tot_energy_ftb1 - (df_base.adjtaxip - df_base.FTBATHR2) * df_base.FTBARED
    df_base.loc[df_base['adjtaxip'] > df_base['FTBATHR1'], 'Tot_FTBA1'] = df_base.Max_FTBA1 + df_base.Tot_energy_ftb1 - df_base.HIINC_K - (df_base.adjtaxip - df_base.FTBATHR1) * df_base.FTBARED2
    df_base.loc[df_base['Tot_FTBA1'] < 0, 'Tot_FTBA1'] = 0
    df_base.loc[(df_base.Max_FTBA1 + df_base.Tot_energy_ftb1 - df_base.Tot_energy_ftb1 / df_base.FTBARED < df_base.adjtaxip) & (df_base.adjtaxip < df_base.FTBATHR2 + (df_base.Max_FTBA1 + df_base.Tot_energy_ftb1) / df_base.FTBARED), 'Tot_FTBA1'] = df_base.Tot_energy_ftb1

    # /* maintenance reduction where applicable */
    df_base['maintrdc'] = 0
    # reduction taper
    mask = (df_base['s_AGEEC'] > 0)
    df_base['MAINEX'][mask] = df_base.MAINEX2
    df_base['MAINAD'][mask] = df_base.MAINAD1
    mask = (df_base['s_AGEEC'] <= 0)
    df_base['MAINEX'][mask] = df_base.MAINEX1
    df_base['MAINAD'][mask] = df_base.MAINAD2

    df_base.loc[(df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] + df_base['r_ICHLDSCP'] == 0), 'mainfree'] = 0
    df_base.loc[(df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] + df_base['r_ICHLDSCP'] == 1), 'mainfree'] = df_base.MAINLMT1
    df_base.loc[(df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] > 0) & (df_base['r_ICHLDSCP'] + df_base['r_ICHLDSCP'] == 2), 'mainfree'] = df_base.MAINLMT2

    mask = (df_base['mainfree'] > 0)
    df_base.loc[mask, 'maintthr'] = df_base.mainfree + ((df_base.totdep019 - df_base.totdep16p) - 1) * df_base.MAINAD
    df_base.loc[mask & ((df_base['r_ICHLDSCP'] + df_base['s_ICHLDSCP']) * 52 > df_base['maintthr']), 'maintrdc'] = (df_base.r_ICHLDSCP + df_base.s_ICHLDSCP) * 52 - df_base.maintthr * df_base.MAINEX

    df_base['Tot_FTBA1'] = df_base['Tot_FTBA1'] - df_base['maintrdc']

    # Method 2
    df_base.loc[df_base['totdep019'] > 1, 'HIFA_FTB_BASE'] = df_base.FTBATHR1 + df_base.FTBAADB * (df_base.totdep019 - 1) * df_base.totdep019
    df_base['Tot_FTBA2'] = df_base.totdep019 * (df_base.FTBA0_19B + df_base.FTBASUPP + df_base.FTBAS0_19_ES)
    df_base['Tot_FTBA2_Max'] = df_base.totdep019 * (df_base.FTBA0_19B + df_base.FTBASUPP + df_base.FTBAS0_19_ES)

    df_base.loc[df_base['adjtaxip'] > df_base['HIFA_FTB_BASE'], 'Tot_FTBA2'] = (df_base.Tot_FTBA2 - (df_base.adjtaxip - df_base.HIFA_FTB_BASE) * df_base.FTBAREDB)
    df_base.loc[df_base['Tot_FTBA2'] < 0, 'Tot_FTBA2'] = 0
    mask = (df_base.HIFA_FTB_BASE + (df_base.Tot_FTBA2_Max - df_base.Tot_energy_ftb2) / df_base.FTBAREDB < df_base.adjtaxip) & (df_base.adjtaxip < df_base.HIFA_FTB_BASE + (df_base.Tot_FTBA2_Max / df_base.FTBAREDB))
    df_base['Tot_FTBA2'][mask] = df_base.Tot_energy_ftb2

    df_base['Tot_FTBA'] = df_base[['Tot_FTBA1', 'Tot_FTBA2']].max(axis=1)  # Total Family Tax Benefits part A
    df_base.loc[df_base['Tot_FTBA'] < 0, 'Tot_FTBA'] = 0

    # Family Tax Benefits- Part B
    # check the eligibility for FTBB
    # THIS SET OF IF/ELSE IF AN ABSOLUTE MESS ON THE SAS VERSION!!!!!!!!!!!!!!!
    mask = (df_base['Iutype'] == 3) & (df_base['totdep019'] > 0)
    df_base.loc[mask & (df_base['KID0T2BC'] + df_base['KID3T4BC'] > 0) & (df_base['adjtaxip'] <= df_base['FTBBTHRP']), 'Tot_FTBB'] = df_base.FTBB0_5S + df_base.FTBBSUPP + df_base.FTBSB0_5_ES  # single parents
    df_base.loc[mask & (df_base['adjtaxip'] <= df_base['FTBBTHRP']), 'Tot_FTBB'] = df_base.FTBBNS + df_base.FTBBSUPP + df_base.FTBBS0_5N_ES
    df_base.loc[mask, 'Tot_FTBB'] = 0

    mask = (df_base['Iutype'] == 1) & (df_base['totdep019'] > 0)
    df_base.loc[mask & (df_base['KID0T2BC'] + df_base['KID3T4BC'] > 0) & (df_base[['r_adjtax', 's_adjtax']].max(axis=1) <= df_base[
            'FTBBTHRP']), 'Tot_ftbb'] = df_base.FTBB0_5C + df_base.FTBBSUPP + df_base.FTBSB0_5_ES
    df_base.loc[mask & (df_base[['r_adjtax', 's_adjtax']].max(axis=1) <= df_base.FTBBTHRP), 'Tot_ftbb'] = df_base.FTBBNC + df_base.FTBBSUPP + df_base.FTBBS0_5N_ES

    df_base.loc[mask & (df_base[['r_adjtax', 's_adjtax']].min(axis=1) > df_base.FTBBPTHRC), 'Tot_ftbb'] = df_base.Tot_ftbb - \
                                                                                                  df_base[['r_adjtax',
                                                                                                           's_adjtax']].min(
                                                                                                      axis=1) - df_base.FTBBPTHRC * df_base.STBBSORC
    df_base.loc[df_base['Tot_ftbb'] < 0, 'Tot_ftbb'] = 0

    mask2 = (0 < (df_base[['r_adjtax', 's_adjtax']].min(axis=1) - df_base.FTBBPTHRC) * df_base.STBBSORC)
    mask3 = ((df_base[['r_adjtax', 's_adjtax']].min(axis=1) - df_base.FTBBPTHRC) * df_base.STBBSORC < df_base.FTBSB0_5_ES)
    df_base.loc[mask & (df_base['KID0T2BC'] + df_base['KID3T4BC'] > 0) & mask2 & mask3, 'Tot_ftbb'] = df_base.FTBSB0_5_ES
    df_base.loc[mask & (df_base['KID0T2BC'] + df_base['KID3T4BC'] == 0) & mask2 & mask3, 'Tot_ftbb'] = df_base.FTBBS0_5N_ES
    df_base.loc[mask & (df_base['YEAR'] >= 2016) & (df_base['totDEP012'] == 0), 'TOT_FTBB'] = 0  # FTB-B PHASED OUT FOR COUPLES WHERE OLDEST CHILD 13+

    df_base['FTB'] = df_base.Tot_FTBA + df_base.Tot_FTBB  # Total Family Tax Benefits per year*/

    # Special Supplements Calculation
    # carer allowance
    df_base.loc[df_base['r_ICAREACP'] > 0, df_base['r_care_allow']] = df_base['CARERAL']
    df_base.loc[df_base['s_ICAREACP'] > 0, df_base['s_care_allow']] = df_base['CARERAL']
    df_base.loc[df_base['s1_ICAREACP'] > 0, df_base['s1_care_allow']] = df_base['CARERAL']
    df_base.loc[df_base['s2_ICAREACP'] > 0, df_base['s2_care_allow']] = df_base['CARERAL']
    df_base.loc[df_base['s3_ICAREACP'] > 0, df_base['s3_care_allow']] = df_base['CARERAL']

    # Carer Supplement
    df_base.loc[df_base['r_ICAREACP'] > 0, df_base['r_care_supp']] = df_base['CARESUP'] / 26
    df_base.loc[df_base['s_ICAREACP'] > 0, df_base['s_care_supp']] = df_base['CARESUP'] / 26
    df_base.loc[df_base['s1_ICAREACP'] > 0, df_base['s1_care_supp']] = df_base['CARESUP'] / 26
    df_base.loc[df_base['s2_ICAREACP'] > 0, df_base['s2_care_supp']] = df_base['CARESUP'] / 26
    df_base.loc[df_base['s3_ICAREACP'] > 0, df_base['s3_care_supp']] = df_base['CARESUP'] / 26

    # Pensioner education supplement */
    def pened(pers, df):
        pers = str(pers)
        pentype = pers + 'pentype'  # string concatenation
        alltype = pers + 'alltype'
        STUDSTCP = pers + 'STUDSTCP'
        mask1 = (df[pentype] in ['CARE' 'DVA' 'PPS'])
        mask2 = (df[alltype] == 'NSA') & (df['iutype'] == 3)
        mask3 = (df[STUDSTCP] in [1, 2])
        df[pers + 'penedsupp'][mask1 & mask3] = df['penedsup']
        df[pers + 'penedsupp'][mask2 & mask3] = df['penedsup']

    pened(pers='r_', df=df_base)
    pened(pers='s_', df=df_base)
    pened(pers='s1_', df=df_base)
    pened(pers='s2_', df=df_base)
    pened(pers='s3_', df=df_base)

    def suptot(pers, df):
        df[pers + 'suptot'] = df[pers + 'penedsupp'] + df[pers + 'care_allow'] + df[pers + 'care_supp']

    suptot(pers='r_', df=df_base)
    suptot(pers='s_', df=df_base)
    suptot(pers='s1_', df=df_base)
    suptot(pers='s2_', df=df_base)
    suptot(pers='s3_', df=df_base)

    # School Kids Bonus
    # number of kids for school kids bonus
    df_base['skbonprim'] = df_base.KID5T9BC + df_base.kid1012bc
    df_base['skbonsec'] = df_base.totdep019 - (df_base.KID0T2BC + df_base.KID3T4BC + df_base.skbonprim)
    df_base['r_suptot'] = 0
    df_base['s_suptot'] = 0

    # ONE-OFF ENERGY PAYMENT FOR 2016-17 FOR PENSIONERS ONLY - INLUDING SINGLE PARENTS
    # ONE-OFF ENERGY PAYMENT FOR 2018-19 FOR PENSIONERS ONLY - INLUDING SINGLE PARENTS
    column_list = ['r_pension', 's_pension', 'r_allow', 's_allow']
    for c in column_list:
        df_base.loc[(df_base[c] > 0) & (df_base['year'] == 2018) & (
                    df_base['iutype'] in [3, 4]), 'r_suptot'] = df_base.iutype * 75 / 26
        df_base.loc[(df_base[c] > 0) & (df_base['year'] == 2018) & (
                    df_base['iutype'] in [1, 2]), 'r_suptot'] = df_base.r_suptot + df_base.iutype * 125 / 26 / 2
        df_base.loc[(df_base[c] > 0) & (df_base['year'] == 2018) & (
                    df_base['iutype'] in [3, 4]), 's_suptot'] = df_base.iutype * 0
        df_base.loc[(df_base[c] > 0) & (df_base['year'] == 2018) & (
                    df_base['iutype'] in [1, 2]), 's_suptot'] = df_base.s_suptot + df_base.iutype * 125 / 26 / 2

    df_base.loc[(df_base['Tot_FTBA'] > 0) & (df_base['adjtaxip'] < df_base['FTBBTHRP']), 'r_suptot'] = df_base.r_suptot + df_base.skbonprim * df_base.SBPRIM / 26 + df_base.skbonsec * df_base.SBSECON / 26  # add SKB on to supps for reference person only * /
    df_base.loc[(df_base['Tot_FTBA'] > 0) & (df_base['adjtaxip'] < df_base['FTBBTHRP']), 'skbon'] = df_base.skbonprim * df_base.SBPRIM / 26 + df_base.skbonsec * df_base.SBSECON / 26

    df_base['carsup'] = df_base[['r_care_supp', 's_care_supp', 's1_care_supp', 's2_care_supp', 's3_care_supp']].sum(axis=1)
    df_base['carall'] = df_base[['r_care_allow', 's_care_allow', 's1_care_allow', 's2_care_allow', 's3_care_allow']].sum(axis=1)
    df_base.loc[df_base['Tot_FTBA1'] < df_base['Tot_FTBA2'], 'r_cra'] = 0
    df_base.loc[df_base[['r_pension', 's_pension', 'r_allow', 's_allow']].sum(axis=1) == 0, 'r_cra'] = 0

    """
    /* Childcare Calculation */
    /*
    If LDC calculate CCB pct rate = 100% if income less than IFarea
    tapers aways at two different rates eventually to 0 by about $160K
    loadings for PT (10% extra) and multiple children and school age children less
    hours max 50 per hour for ccb
    24 hr work test for more than 15 hrs ccb

    1. Calculate max weekly benefit (including multiple child loading)
    2. Calculate actual max benefit
    3. Calculate per cent (based on taper rate and number of kids)
    4. Calculate CCB including * part time loading
    """
    # %IF &YEAR > 2017 %THEN %DO;  # ?????????????????????????
    # /*********************NEW CHILDCARE SUBSIDY**********************************************/
    df_base['ccr_tot'] = 0  # set to zero 	for the new childcare system * /
    df_base['ccb_tot'] = 0
    df_base.loc[df_base[(1 <= df_base['typea1']) & (df_base['typea1'] <= 5) & (1 <= df_base.typea2) &
                        (df_base.typea2 <= 5) & (1 <= df_base.typea3) & (df_base.typea3 <= 5) & (1 <= df_base.typea4) &
                        (df_base.typea4 <= 5)], 'formkids'] = df_base[['typea1', 'typea2', 'typea3', 'typea4']].sum(axis=1)
    df_base['r_HRSWKAEC_CC'] = df_base.r_HRSWKAEC
    df_base['S_HRSWKAEC_CC'] = df_base.S_HRSWKAEC  # CHILDCARE	SUBSIDY RELATED HOURS WORKED VARIABLE

    # /* NEW CODE for budget 2017-18 BP MAY 2017 */
    # /* DETERMINE NEW ACTIVITY TEST */
    # /* assume students are passing the activity test - assign them full time working hours - QUITE GENEROUS!
    df_base.loc[df_base['r_STUDSTCP'] in [1, 2], 'r_HRSWKAEC_CC'] = 24.5
    df_base.loc[df_base['s_STUDSTCP'] in [1, 2], 's_HRSWKAEC_CC'] = 24.5

    # ADJUST HOURS WORKED UP FOR TRANSITIONING TO EMPLOYMENT SOCIAL SECURITY PAYMENTS
    df_base.loc[df_base['R_ALLOW'] > 0, 'r_HRSWKAEC_CC'] = 24.5
    df_base.loc[df_base['S_ALLOW'] > 0, 'S_HRSWKAEC_CC'] = 24.5

    df_base.loc[(df_base['r_PENTYPE'] == 'PPS') & (df_base['numdeps_ppp'] == 0), 'r_HRSWKAEC_CC'] = 24.5
    df_base.loc[(df_base['r_PENSION'] > 0) & (df_base['r_PENTYPE'] != 'PPS'), 'r_HRSWKAEC_CC'] = 24.5
    df_base.loc[(df_base['s_PENTYPE'] == 'PPS') & (df_base['numdeps_ppp'] == 0), 's_HRSWKAEC_CC'] = 24.5
    df_base.loc[(df_base['s_PENSION'] > 0) & (df_base['r_PENTYPE'] != 'PPS'), 's_HRSWKAEC_CC'] = 24.5

    # END OF ADJUSTMENT TO HOURS WORKED
    df_base.loc[df_base['S_HRSWKAEC_CC'].notna(), 'hrswk'] = df_base[['R_HRSWKAEC_CC', 'S_HRSWKAEC_CC']].min(axis=1)
    df_base.loc[df_base['S_HRSWKAEC_CC'].isna(), 'hrswk'] = df_base['R_HRSWKAEC_CC']

    df_base.loc[df_base[
                    'hrswk'] > 0, 'hrswk'] = 2 * df_base.hrswk  # SIH definitions are in actual number of hours and convert to fortnightly */

    # SUM OVER 4 POSSIBLE CHILDCARE CHILDREN

    df_base[
        'grosscostACT'] = df_base.hoursa1 * df_base.costa1 + df_base.hoursa2 * df_base.costa2 + df_base.hoursa3 * df_base.costa3 + \
                          df_base.hoursa4 * df_base.costa4 + df_base.hoursb1 * df_base.costb1 + df_base.hoursb2 * df_base.costb2 + \
                          df_base.hoursb3 * df_base.costb3 + df_base.hoursb4 * df_base.costb4

    def cctyp(var1, var2, df):
        df.loc[str(df[var1]) == '9', var2] = 'INF'
        df.loc[str(df[var1]) in ['1', '5'], var2] = 'S'
        df.loc[str(df[var1]) == '2', var2] = 'L'
        df.loc[str(df[var1]) == '3', var2] = 'F'
        df.loc[str(df[var1]) == '4', var2] = 'NS'
        df.loc[str(df[var1]) not in ['1', '2', '3', '4', '5', '9'], var2] = 'N'

    cctyp(var1='typea1', var2='typeaa1', df=df_base)
    cctyp(var1='typea2', var2='typeaa2', df=df_base)
    cctyp(var1='typea3', var2='typeaa3', df=df_base)
    cctyp(var1='typea4', var2='typeaa4', df=df_base)
    cctyp(var1='typeb1', var2='typebb1', df=df_base)
    cctyp(var1='typeb2', var2='typebb2', df=df_base)
    cctyp(var1='typeb3', var2='typebb3', df=df_base)
    cctyp(var1='typeb4', var2='typebb4', df=df_base)

    def ccs(var, df):  # NO IDEA WHAT IS THIS SYNTAX
        # only formal care to count in new policy
        df.loc[df['typeaa' + var] not in ['F', 'L', 'S', 'NS'], 'hoursa' + var] = 0
        df.loc[df['typeaa' + var] not in ['F', 'L', 'S', 'NS'], 'costa' + var] = 0

        df.loc[df['typebb' + var] not in ['F', 'L', 'S', 'NS'], 'hoursb' + var] = 0
        df.loc[df['typebb' + var] not in ['F', 'L', 'S', 'NS'], 'costb' + var] = 0

        df['grosscostACT' + var] = df['hoursa' + var] * df['costa' + var] + df['hoursb' + var] * df['costb' + var]

        # kids must have positive hours in formal care
        mask_1 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > 0)

        # -----------------------------------------------------------------------------------------
        # LOW INCOME FAMILIES */
        mask_01 = (df.adjtaxip < df.CCINC_L)
        df.loc[mask_1 & mask_01, 'RATE'] = df.CCSUB_L

        mask_001 = (df.hrswk < df.act1)
        mask_0001 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.WRKHRS / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_001 & mask_0001] = ((df.WRKHRS / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_001 & mask_0001] = ((df.WRKHRS / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_002 = (df.hrswk < df.act2)
        mask_0002 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax1 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk < df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_004 = (df['typea' + var] == 2) & (df['typea' + var] in [3, 4]) & (df['typea' + var] in [1, 5])
        mask_005 = (df['typeb' + var] == 2) & (df['typeb' + var] in [3, 4]) & (df['typeb' + var] in [1, 5])
        df['costa' + var][mask_1 & mask_01 & mask_004] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['costb' + var][mask_1 & mask_01 & mask_005] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['grosscost' + var][mask_1 & mask_01] = df['hoursa' + var] * df['costa' + var] + df['hoursb' + var] * df['costb' + var]
        df.loc[df['grosscost' + var] > 0, 'ccr' + var] = df.RATE * df['grosscost' + var] * 52

        # MIDDLE INCOME FAMILIES --------------------------------------------------------------------------------------
        mask_01 = (df.CCINC_L < df.adjtaxip) & (df.adjtaxip < df.CCINC_U1)
        df.loc[mask_1 & mask_01, 'RATE'] = df.CCSUB_L - ((1 - (df.adjtaxip - df.CCINC_U1) / (df.CCINC_L - df.CCINC_U1)) * (df.CCSUB_L - df.CCSUB_U))

        mask_001 = (df.hrswk < df.act1)
        df['hoursa' + var][mask_1 & mask_01 & mask_001] = 0
        df['hoursb' + var][mask_1 & mask_01 & mask_001] = 0

        mask_002 = (df.hrswk <= df.act2)
        mask_0002 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax1 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk <= df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk > df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_004 = (df['typea' + var] == 2) & (df['typea' + var] in [3, 4]) & (df['typea' + var] in [1, 5])
        mask_005 = (df['typeb' + var] == 2) & (df['typeb' + var] in [3, 4]) & (df['typeb' + var] in [1, 5])
        df['costa' + var][mask_1 & mask_01 & mask_004] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['costb' + var][mask_1 & mask_01 & mask_005] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['grosscost' + var][mask_1 & mask_01] = df['hoursa' + var] * df['costa' + var] + df['hoursb' + var] * df['costb' + var]
        df.loc[df['grosscost' + var] > 0, 'ccr' + var] = df.RATE * df['grosscost' + var] * 52

        # UPPER MIDDLE INCOME FAMILIES -------------------------------------------------------------------------------
        mask_01 = (df.adjtaxip < df.CCCAPTHR)
        df.loc[mask_1 & mask_01, 'RATE'] = df.CCSUB_U

        mask_001 = (df.hrswk < df.act1)
        df['hoursa' + var][mask_1 & mask_01 & mask_001] = 0
        df['hoursb' + var][mask_1 & mask_01 & mask_001] = 0

        mask_002 = (df.hrswk <= df.act2)
        mask_0002 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax1 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk <= df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk > df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_004 = (df['typea' + var] == 2) & (df['typea' + var] in [3, 4]) & (df['typea' + var] in [1, 5])
        mask_005 = (df['typeb' + var] == 2) & (df['typeb' + var] in [3, 4]) & (df['typeb' + var] in [1, 5])
        df['costa' + var][mask_1 & mask_01 & mask_004] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['costb' + var][mask_1 & mask_01 & mask_005] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.ldc + df['typea' + var] * df.fdc + df['typea' + var] * df.oshc
        df['grosscost' + var][mask_1 & mask_01] = df['hoursa' + var] * df['costa' + var] + df['hoursb' + var] * df['costb' + var]
        df.loc[df['grosscost' + var] > 0, 'ccr' + var] = df.RATE * df['grosscost' + var] * 52

        # UPPER INCOME FAMILIES - should parameterise these ------------------------------------------------------------
        mask_01 = (df.adjtaxip > df.CCCAPTHR)
        df.loc[mask_1 & mask_01, 'RATE'] = df.CCSUB_U

        mask_001 = (df.CCINC_U2 <= df.adjtaxip) &  (df.adjtaxip <= df.CCINC_U3)
        df.loc[mask_1 & mask_01 & mask_001, 'RATE'] = df.CCSUB_U - (((df.adjtaxip-df.CCINC_U2) / (df.CCINC_U3-df.CCINC_U2)) * (df.CCSUB_U-df.CCSUB_U2))

        mask_001 = (df.CCINC_U3 <= df.adjtaxip) & (df.adjtaxip <= df.CCINC_U4)
        df.loc[mask_1 & mask_01 & mask_001, 'RATE'] = df.CCSUB_U2

        # Highest income familes > 350, 000 ----------------------------------------------------------------------------
        mask_01 = (df.adjtaxip >= df.CCINC_U4)
        df.loc[mask_1 & mask_01 & mask_001, 'RATE'] = 0

        mask_001 = (df.hrswk <= df.act1)
        df['hoursa' + var][mask_1 & mask_01 & mask_001] = 0
        df['hoursb' + var][mask_1 & mask_01 & mask_001] = 0

        mask_002 = (df.hrswk <= df.act2)
        mask_0002 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax1 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_002 & mask_0002] = ((df.AcTmax1 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk <= df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax2 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax2 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax2 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_003 = (df.hrswk > df.act3)
        mask_0003 = (df[['hoursa' + var, 'hoursb' + var]].sum(axis=1) > df.AcTmax3 / 2)
        df['hoursa' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursa' + var]
        df['hoursb' + var][mask_1 & mask_01 & mask_003 & mask_0003] = ((df.AcTmax3 / 2) / (df['hoursa' + var] + df['hoursb' + var])) * df['hoursb' + var]

        mask_004 = (df['typea' + var] == 2) & (df['typea' + var] in [3, 4]) & (df['typea' + var] in [1, 5])
        mask_005 = (df['typeb' + var] == 2) & (df['typeb' + var] in [3, 4]) & (df['typeb' + var] in [1, 5])
        df['costa' + var][mask_1 & mask_01 & mask_004] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.subldc + df['typea' + var] * df.subfdc + df['typea' + var] * df.oshc
        df['costb' + var][mask_1 & mask_01 & mask_005] = df[['costa' + var, 'typea' + var]].min(axis=1) * df.subldc + df['typea' + var] * df.subfdc + df['typea' + var] * df.oshc
        df['grosscost' + var][mask_1 & mask_01] = df['hoursa' + var] * df['costa' + var] + df['hoursb' + var] * df['costb' + var]
        df.loc[df['grosscost' + var] > 0, 'ccr' + var] = df[df.RATE * df['grosscost' + var] * 52, 'CCTHR'].min(axis=1)


    ccs(var='1', df=df_base)
    ccs(var='2', df=df_base)
    ccs(var='3', df=df_base)
    ccs(var='4', df=df_base)

    df_base['cctreb1'] = df_base.ccr1
    df_base['cctreb2'] = df_base.ccr2
    df_base['cctreb3'] = df_base.ccr3
    df_base['cctreb4'] = df_base.ccr4
    df_base['grosscost'] = df_base.grosscostACT

    df_base['cctrebu'] = (df_base.cctreb1 - df_base.cctreb4) / 52
    df_base['cctreb'] = df_base.cctrebu
    df_base['cctrebr'] = df_base.cctrebu
    df_base['cctrebs'] = 0
    df_base['OutOfPocketCCu'] = df_base.grosscost - df_base.cctrebu
    df_base['cc_tot'] = df_base.cctrebu

    df_base['r_traninc'] = df_base.r_pension + df_base.r_allow + df_base.ftb / 26 + df_base.r_suptot + df_base.cc_tot * 2
    df_base['s_traninc'] = df_base.s_pension + df_base.s_allow + df_base.s_suptot
    df_base['s1_traninc'] = df_base.s1_allow + df_base.s1_suptot
    df_base['s2_traninc'] = df_base.s2_allow + df_base.s2_suptot
    df_base['s3_traninc'] = df_base.s3_allow + df_base.s3_suptot

    # /**************end loop for CCS*********************/
    df_base['u_traninc'] = sum(r_traninc, s_traninc, s1_traninc, s2_traninc, s3_traninc)


    # SIMULATE PERSONAL INCOME TAXATION */


    #  DEFINE MACRO TO CALCULATE   */
    #  INCOME TAX LIABILITY        */
    #  CALCULATE TAX LIABILITIES   */
    #  IN THE BASE OR USER DEFINED */
    #  TAX STEPS                   */
    def inctax(tinc, inctax, df):
        df.loc[df[tinc] == 0, inctax] = 0


    # ARRAY taxarray {3, 5} PITHRSH1 - PITHRSH5 mtr1 - mtr5 tax1 - tax5

    for i in range(1, 4):
        if taxarray[2, i] != .and taxarray[2, i+1] !=.:
            taxarray[3, i] = (taxarray[1, i + 1] - taxarray[1, i]) * taxarray[2, i]
        if i != 1 and taxarray[3, i] != .:
            taxarray[3, i] = taxarray[3, i] + taxarray[3, i - 1]
        df.loc[df[tinc] > 0, 'inctax'] = 0
        elif tinc > 0:  # DO
        for i in range(5, 1, -1):
            if i == 5:
                taxflag = 0
            if taxarray[1, i] < tinc and taxarray[1, i] != .and taxflag == 0:
                if i == 1:
                    inctax = tinc * taxarray[2, 1]
                else:
                    inctax = (tinc - taxarray[1, i]) * taxarray[2, i] + taxarray[3, i - 1]
                    taxflag = 1

    inctax('r_tinc', 'r_inctax', df=df_base)
    inctax('s_tinc', 's_inctax', df=df_base.loc[df_base['s_AGEEC'] > 0])
    inctax('s1_tinc', 's1_inctax', df=df_base.loc[df_base['s1_AGEEC'] > 0])
    inctax('s2_tinc', 's2_inctax', df=df_base.loc[df_base['s2_AGEEC'] > 0])
    inctax('s3_tinc', 's3_inctax', df=df_base.loc[df_base['s3_AGEEC'] > 0])


    def lomidreb(pers):
        taxinc = pers.tinc
        lomidreb = pers.lomidreb
        LOMIDREB2 = LOMIDREB + (LOMIDTHR2 - LOMIDTHR1) * LOMIDRT1
        SELECT;
        WHEN( & taxinc
        LE
        LOMIDTHR1) & lomidreb = LOMIDREB
        WHEN( & taxinc
        LE
        LOMIDTHR2) & lomidreb = LOMIDREB + (& taxinc - LOMIDTHR1) * LOMIDRT1
        WHEN( & taxinc
        LE
        LOMIDTHR3) & lomidreb = LOMIDREB2
        OTHERWISE
        lomidreb = MAX(0, (LOMIDREB2 - (& taxinc - LOMIDTHR3) * LOMIDRT2))


    lomidreb(PERS=r_)
    if s_ageec > 0:
        % lomidreb(PERS=s_)
    if s1_ageec > 0:
        % lomidreb(PERS=s1_)
    if s2_ageec > 0:
        % lomidreb(PERS=s2_)
    if s3_ageec > 0:
        % lomidreb(PERS=s3_)

    #  SAPTO - include transferability
    r_NG_shares = round(abs(min(r_IDIVTRCP - r_est_intd / 52, 0)), .01)
    s_NG_shares = round(abs(min(s_IDIVTRCP - s_est_intd / 52, 0)), .01)

    # calculate SAPTO assesable income
    r_otinc = sum(r_tinc, (R_ss_flagp=1) * (r_issscp * 52), (R_ss_flagp=1) * (r_ssfbp * 52), r_non_ssfbp * 52,
                  (r_irentcp < 0) * ABS(r_irentcp * 52), r_NG_shares * 52)
    s_otinc = sum(s_tinc, (S_ss_flagp=1) * (s_issscp * 52), (S_ss_flagp=1) * (s_ssfbp * 52), s_non_ssfbp * 52,
                  (s_irentcp < 0) * ABS(s_irentcp * 52), s_NG_shares * 52)


    # Eligible for SAPTO
    # couples are tested under the combined income test but then SAPTO calculated on individual test
    # any leftover is given to other partner to use - need to incorporate this http://www.superguide.com.au/smsfs/no-tax-retirement-sapto */

    def sapto(pers):
        if sum(pers.pension) > 0 or (pers.age_act >= sum((pers.sexp=1) * PENSAGE_M, (pers.sexp=2) * PENSAGE_F)):
            sapto_flag = 1
        if iutype in [1, 2]:
            otinc = sum(r_otinc, s_otinc) / 2
        else:
            otinc = r_otinc
            # need to change here as potential for income greater than threshold of $37K where higher rate comes into play */
            sapto_loinc_th = PITHRSH2 + (LOINCREB + SENREBS * (iutype in (3 4)) + SENREBC * (iutype in (1 2))) / MTR2;
            pers.sapto = SENREBS * (iutype in (3 4)) + SENREBC * (iutype in (1 2))
            # .125 is the SAPTO phase out rate */
            pers.sapto = max(0, pers.sapto - (pers.otinc > sapto_loinc_th) * (pers.otinc - sapto_loinc_th) * SENRWR)


    sapto(pers=r_)
    sapto(pers=s_)
    s1_sapto = 0
    s2_sapto = 0
    s3_sapto = 0

    # SAPTO transferability between partners
    if iutype in [1, 2]:
        if sum(r_sapto, s_sapto) > 0:
            # Where reference person has larger income */
            if s_otinc < sapto_loinc_th and r_otinc > sapto_loinc_th:
                # calculate unused SAPTO from spouse */
                s_unused_sapto = max(0, SENREBC - max(0, 0.15 * (s_otinc - 6000)))
                # calculate updated threshold */
                sapto_loinc_th = PITHRSH2 + sum(LOINCREB, SENREBC, s_unused_sapto) / MTR2
                # calculated new SAPTO amount */
                r_sapto = max(0, sum(SENREBC, s_unused_sapto) - (r_otinc > sapto_loinc_th) * sum(r_otinc,
                                                                                                 -sapto_loinc_th) * SENRWR)
            # Where spouse has larger income */
            if r_otinc < sapto_loinc_th and s_otinc > sapto_loinc_th:
                # calculate unused SAPTO from spouse */
                r_unused_sapto = max(0, SENREBC - max(0, 0.15 * (r_otinc - 6000)))
                # calculate updated threshold */
                sapto_loinc_th = PITHRSH2 + sum(LOINCREB, SENREBC, r_unused_sapto) / MTR2
                # calculated new SAPTO amount */
                s_sapto = max(0, sum(SENREBC, r_unused_sapto) - (s_otinc > sapto_loinc_th) * sum(s_otinc,
                                                                                                 -sapto_loinc_th) * SENRWR)

    # BENTO - Beneficiary Tax Offset
    r_bento = 0
    s_bento = 0
    s1_bento = 0
    s2_bento = 0
    s3_bento = 0


    def bento(pers):
        if pers.allow * 26 < 37000:
            pers.bento = max(0, (pers.allow * 26 - 6000) * 0.15)
        else:
            pers.bento = (37000 - 6000) * 0.15 + (pers.allow * 26 - 37000) * .15  # /* would be very unusual for allow > 37K


    bento(pers='R_')
    bento(pers='S_')
    bento(pers='s1_')
    bento(pers='s2_')
    bento(pers='s3_')

    # /* MEDICARE LEVY */
    # 1. Calculate individual levy amount
    # 2. Calculate family reduction amount
    # 3. Share reduction if couple, transfer any unused amount to other partner
    famthr = 0


    def medlev(pers):
        if iutype in [4]:  # /* couple no kids and singles */
            pers.medstep = sum((pers.pension > 0) * MEDPEN1S, (pers.pension=0) * MEDTHR1S)
            if pers.sapto > 0 then pers.medstep = MEDPEN1S
        if iutype in [1, 2, 3]:
            pers.medstep = sum((pers.pension > 0) * MEDPEN1S, (pers.pension=0) * MEDTHR1S)
            if pers.sapto > 0:
                pers.medstep = MEDPEN1S
        if pers.tinc > pers.medstep:
            pers.medlev = min((pers.tinc - pers.medstep) * MEDLEVSHR1, pers.tinc * MEDLEVR1)
        # family threshold
        if iutype in [1, 2, 3] and (pers.pension > 0):
            pers.famthr = sum(MEDPEN1C, SSTOTDEP * MEDINC1)
        elif iutype in [1, 2, 3]:
            pers.famthr = sum(MEDTHR1C, SSTOTDEP * MEDINC1)
        # Budget Repair levy
        pers.brlevy = 0
        if pers.tinc > BR_THRESH:
            pers.brlevy = (pers.tinc - BR_THRESH) * BR_RATE
        pers.NetTax = max(0, sum(pers.inctax, pers.brlevy, -pers.sapto, -pers.bento, -pers.loincreb,
                                 -pers.lomidreb)) - pers.divreb * 52


    medlev(pers=R_)
    medlev(pers=S_)
    medlev(pers=S1_)
    medlev(pers=S2_)
    medlev(pers=S3_)

    # family reduction for medicare
    if iutype in [1 2 3]:
        if sum(r_tinc, s_tinc) le r_famthr:
            r_medlev = 0;
            s_medlev = 0
        if sum(r_tinc, s_tinc) > r_famthr:
            famred = max(0, (MEDLEVR1 * r_famthr) - (sum(r_tinc, s_tinc) - r_famthr) * (MEDLEVSHR1 - MEDLEVR1))
            r_famred = r_tinc / sum(r_tinc, s_tinc) * famred
            s_famred = s_tinc / sum(r_tinc, s_tinc) * famred
            r_medlev = sum(r_medlev, -r_famred)
            s_medlev = sum(s_medlev, -s_famred)
            if r_medlev < 0:
                s_medlev = s_medlev - abs(r_medlev)
            if s_medlev < 0:
                r_medlev = r_medlev - abs(s_medlev)
            r_medlev = max(0, r_medlev)
            s_medlev = max(0, s_medlev)
    r_nettax = r_nettax + r_medlev
    s_nettax = s_nettax + s_medlev
    s1_nettax = s1_nettax + s1_medlev;
    s2_nettax = s2_nettax + s2_medlev;
    s3_nettax = s3_nettax + s3_medlev;
    Nettaxiu = sum(r_nettax, s_nettax, s1_nettax, s2_nettax, s3_nettax)
    Inctaxiu = sum(r_inctax, s_inctax, s1_inctax, s2_inctax, s3_inctax)
    medleviu = sum(r_medlev, s_medlev, s1_medlev, s2_medlev, s3_medlev)
    brleviu = sum(r_brlevy, s_brlevy, s1_brlevy, s2_brlevy, s3_brlevy)

    # ~BP
    r_dispinc = sum(r_privinc, r_traninc / 2, -r_nettax / 52, r_IncNonTaxSuperImpA)
    s_dispinc = sum(s_privinc, s_traninc / 2, -s_nettax / 52, s_IncNonTaxSuperImpA)
    s1_dispinc = sum(s1_privinc, s1_traninc / 2, -s1_nettax / 52)
    s2_dispinc = sum(s2_privinc, s2_traninc / 2, -s2_nettax / 52)
    s3_dispinc = sum(s3_privinc, s3_traninc / 2, -s3_nettax / 52)
    u_dispinc = sum(r_dispinc, s_dispinc, s1_dispinc, s2_dispinc, s3_dispinc)
    traninciu = sum(r_traninc, s_traninc, s1_traninc, s2_traninc, s3_traninc) / 2

    data
    wts(keep=abshid
    WT_PM)
    set
    basedata.base & BMYR. & emtr
    proc
    sort;
    by
    abshid

    proc
    sort
    data = iu_2;
    by
    abshid

    data
    altdata.base & BMYR. & emtr
    merge
    iu_2
    wts;
    by
    abshid

    # OLD BASEFILE NUMBERS FOR POVERTY AND HOUSING STRESS BASELINE VALUES

    proc
    sort
    data = BASEdata.base & BMYR. & emtr;
    by
    abshid

    proc
    means
    data = BASEdata.base & BMYR. & emtr
    sum
    noprint
    var
    u_dispinc
    TRPAY1CH
    iurent;
    by
    abshid;
    output
    out = hh_summary_old
    sum = dispinc_hh
    TRPAY1CH_hh
    WKRENTCH_hh;
    run

    data
    hh_summary_old(drop=dispinc_hh
    TRPAY1CH_hh
    WKRENTCH_hh)
    set
    hh_summary_old
    dispinc_hh_old = dispinc_hh
    TRPAY1CH_hh_old = TRPAY1CH_hh
    WKRENTCH_hh_old = WKRENTCH_hh

    # NEW RESULTS FOR ALTERNATIVE WORLD
    proc
    sort
    data = altdata.base & BMYR. & emtr;
    by
    abshid;

    proc
    means
    data = altdata.base & BMYR. & emtr
    sum
    noprint;
    var
    u_dispinc
    wklyexp
    wklyexp_rest
    TRPAY1CH / * WKRENTCH * / iurent; / *rent
    was
    being
    double
    counted * /
    by
    abshid;
    output
    out = hh_summary
    sum = dispinc_hh
    wklyexp_hh
    wklyexp_rest_hh
    TRPAY1CH_hh
    WKRENTCH_hh;
    run;

    data
    hh(keep=sexrh
    DEP1524B
    GCCSA11C
    LFSRH
    AGERHEC
    NUMU15BC
    DCOMPH
    NOEMPHBC
    TENURECF
    dispsch8
    wealthh
    agehh
    equivh
    STATEHEC
    hhtype
    WT_PM
    abshid
    PERSHBC
    wtpersHH
    ran_: );
    set
    altdata.base & BMYR. & emtr;
    by
    abshid;

    if first.abshid;

    if DCOMPH in [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15]:
        hhtype = 'Couple Children'
    elif DCOMPH in (21, 22, 23, 24, 17, 18, 19, 20):
        hhtype = 'Single Parent'
    elif DCOMPH in [1, 16]:
        hhtype = 'Couple Only'
    elif DCOMPH in [32]:
        hhtype = 'Lone Person'
    else:
        hhtype = 'Other'

    if R_AGEEC <= 24:
        ageHH = '15 to 24'  # age 15 to 24 */
    elif R_AGEEC <= 34:
        ageHH = '25 to 34'  # age 25 to 34 */
    elif R_AGEEC <= 44:
        ageHH = '35 to 44'  # age 35 to 44 */
    elif R_AGEEC <= 54:
        ageHH = '45 to 54'  # age 45 to 54 */
    elif R_AGEEC <= 64:
        ageHH = '55 to 64'  # age 55 to 64 */
    elif R_AGEEC <= 74:
        ageHH = '65 to 74'  # age 65 to 74 */
    else:
        ageHH = '75 and over'

    wtpersHH = WT_PM * PERSHBC
    hh = merge
    hh
    hh_summary
    hh_summary_old;
    by
    abshid
    HHSIZE = PERSHBC

    # /* create dummy variable for couple only or single person by age */
    if hhtype in ['Couple Only', 'Lone Person']:
        nokidsfamily = 1
    else:
        nokidsfamily = 0

    if nokidsfamily == 1:
        if AGERHEC < 36:
            agenokids = 35
        elif AGERHEC < 51:
            agenokids = 50
        elif AGERHEC < 66:
            agenokids = 65
        elif AGERHEC < 76:
            agenokids = 75
        else:
            agenokids = 85  # need to change to actual 85+
    elif nokidsfamily == 0:
        agenokids = 0

    adults = PERSHBC - sum(NUMU15BC)
    if DCOMPH in [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15]:
        famHH = 1  # couple and deps */
    elif DCOMPH in (21, 22, 23, 24, 17, 18, 19, 20):
        famHH = 2  # single parent and deps
    elif DCOMPH in (1, 16):
        famHH = 3  # couple only
    elif DCOMPH in (32):
        famHH = 4  # lone person
    else:
        famHH = 5  # other/multiple/group

    if NOEMPHBC == 0:
        PreEmpPeop = 0
    else:
        PreEmpPeop = 1
    lnwealth = max(0, log(wealthh))
    Lndispincome = max(0, log(dispsch8))
    LNHHSIZE = log(HHSIZE)
    eqdisphh = dispinc_hh / equivh
    eqdisphh_old = dispinc_hh_old / equivh
    wklyexp_hh = wklyexp_hh * 52
    dispinc_hh = dispinc_hh * 52
    dispinc_hh_old = dispinc_hh_old * 52
    wklyexp_rest_hh = wklyexp_rest_hh * 52
    hcosthh = sum(TRPAY1CH_hh, WKRENTCH_hh)
    ahdispinc_hh_eq = (sum(dispinc_hh, -hcosthh * 52) / equivh) / 52
    ahdispinc_hh_eq_old = (sum(dispinc_hh_old, -hcosthh * 52) / equivh) / 52

    # 2 per cent limit
    proc
    univariate
    data = hh
    var
    eqdisphh_old
    weight
    wtpersHH / * wt_pm * /
    output
    out = pctlimit
    pctlpts = 1
    to
    2
    by
    1
    pctlpre = pct

    data
    _null_
    set
    pctlimit
    call
    symput('pct2', put(pct2, 5.2))

    # 10 percentiles above 2% limit
    proc
    univariate
    data = hh
    var
    eqdisphh_old
    weight
    wtpersHH
    output
    out = newhh
    pctlpts = 10
    to
    100
    by
    10
    pctlpre = pct

    # median income
    data
    _null_
    set
    newhh
    call
    symput('medinc', put(pct50, 5.2))

    # 40th percentile for housing stress
    data
    _null_;
    set
    newhh;
    call
    symput('hstpc40', put(pct40, 5.2))

    # median income for after-houisng poverty
    proc
    univariate
    data = hh
    var
    ahdispinc_hh_eq_old
    weight
    wtpersHH / * wt_pm * /
    *where
    eqdisphh_old > & pct2
    output
    out = newAHhh
    pctlpts = 10
    to
    100
    by
    10
    pctlpre = pctAH

    data
    _null_
    set
    newAHhh
    call
    symput('medincAH', put(pctAH50, 5.2))

    data
    newhh;
    set
    newhh;
    x = 1;
    data
    newAHhh;
    set
    newAHhh;
    x = 1;

    data
    hh;
    merge
    hh
    newhh
    newAHhh;
    by
    x;
    if eqdisphh <= pct20:
        qntl = 1
    elif eqdisphh <= pct40:
        qntl = 2
    elif eqdisphh <= pct60:
        qntl = 3
    elif eqdisphh <= pct80:
        qntl = 4
    elif eqdisphh <= pct100:
        qntl = 5

    data
    orig(keep=u_traninc
    Nettaxiu
    ftb
    cc_tot
    ccb_tot
    ccr_tot
    abshid
    WT_PM)
    set
    altdata.base & BMYR. & emtr

    u_traninc = u_traninc * 26  # /* fortnightly payments */

    proc
    means
    sum(noprint)
    var
    u_traninc
    Nettaxiu
    ftb
    cc_tot
    ccb_tot
    ccr_tot
    by
    abshid
    id
    wt_pm
    output
    out = orig_hh
    sum =

    proc
    sort
    data = hh;
    by
    abshid;
    proc
    sort
    data = orig_hh;
    by
    abshid;
    run;

    data
    hh & year;
    merge
    hh
    orig_hh;
    by
    abshid;
    sim = & gap;
    y = & medinc;
    ah = & medincAH;

    if AGERHEC <= 35:
        age = 1  # < 35
    elif AGERHEC <= 50:
        age = 2  # < 50
    elif AGERHEC <= 65:
        age = 3  # < 65
    else:
        age = 4  # 65+

    if DCOMPh in [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15]:
        famHH = 1  # couple and deps
    elif DCOMPh in [21, 22, 23, 24, 17, 18, 19, 20]:
        famHH = 2  # single parent and deps
    elif DCOMPh in [1, 16]:
        famHH = 3  # couple only
    elif DCOMPh in [32]:
        famHH = 4  # lone person
    else:
        famHH = 5  # other/multiple/group

    pov50 = 0
    pov50AH = 0
    hstress3040 = 0
    pov50ch = 0

    if eqdisphh < medinc / 2 and eqdisphh > pct2:
        pov50 = PERSHBC  # poverty persons

    if eqdisphh < medinc / 2 and eqdisphh > pct2:
        pov50ch = NUMU15BC  # children in poverty persons

    if ahdispinc_hh_eq < medincAH / 2 and eqdisphh > pct2:
        pov50AH = PERSHBC  # AH poverty persons

    if eqdisphh < hstpc40 and (hcosthh * 52) / dispinc_hh > 0.3 and eqdisphh > pct2:
        hstress3040 = 1  # housing stress

    POVGAP_HH = (eqdisphh >& pct2) * (eqdisphh < & medinc / 2) * (
            eqdisphh - & medinc / 2) * equivh * 52  # Poverty gap HH only
    POVGAPAH_HH = (eqdisphh >& pct2) * (ahdispinc_hh_eq < & medincAH / 2) * (
            ahdispinc_hh_eq - & medincAH / 2) * equivh * 52  # AH Poverty gap HH only */
    HSTRESSGAP = (hstress3040 = 1) * ((hcosthh * 52) - (dispinc_hh * 0.3));
    run;

    proc
    means
    sum;
    var
    POVGAP_HH
    pov50
    pov50ch
    pov50AH
    POVGAPAH_HH
    hstress3040
    HSTRESSGAP;
    weight
    wt_pm;
    id
    ran_:;
    output
    out = hhpovgap & gap
    sum =;

    if sim == 1:
        compare()