import pandas as pd
def inflate():
    drive = "<instert path here>"
    df_uprate_f = pd.read_excel(drive + '\Basefile\Uprating\Uprating_15.xlsx', sheet_name='final')  # review what is SAS getnames

    from dsmod import dsmod  # no idea what is that function
    outds_info = df_uprate_f.info()
    outds_desc = df_uprate_f.describe()

    df_aux = outds_info[outds_info['name'] != 'x']
    # file dsmod  # review what is this doing on SAS
    # dsmod = 'something we dont know yet'
    newname = dsmod['name']
    newname.str.replace([0], '_')

    for i in range(len(dsmod)):
        if dsmod['name'][i] !=  newname[i]:
            dsmod['name'][i] = dsmod['name'][i] + ' = ' + newname[i]

    df_uprate_f
    dsmod()  # this is line 34
    "hello=world"

