# ANU Social Science
'''
Purpose of this script is to;
1. Calculate the coefficients of a regression model of poverty gap.
2. Identify optimal tax and transfer policies (TTP) settings.
3. Generate data for chart creation (which will be done in Tableau externally)
'''

# import packages
import pandas as pd
import numpy as np
import os
from pathlib import Path

# sklearn packages
from sklearn.linear_model import LinearRegression 
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

# scipy packages
from scipy.optimize import minimize

# file referencing
cwd = Path.cwd()
im_rep = os.path.join(cwd, "input")
ex_rep = os.path.join(cwd, "output")
data_fname = "alternative_baselines.xlsx"

endo = "POVGAP_HH" # there are three potential endogenous variables in the dataset
exo = ['ran_pen', 'ran_nsa', 'ran_pps', 'ran_ftb', 'ran_ra']

# import data
data = pd.read_excel(os.path.join(im_rep, data_fname))

# 1. prepare data
X1 = np.array(data[exo])
X2 = X1**2
X3 = X1**3
X = np.concatenate((X1, X2, X3), axis = 1)
# resulting X is a 1000 x 15 matrix

def run_regression(X, endo):
    # Regress the function
    y = data[endo]
    model = LinearRegression().fit(X, y)
    print("Model R-squared is {0}".format(model.score(X, y)))
    return model

model_povgap = run_regression(X, "POVGAP_HH")
# 99.41 R-squared, similar to what was discussed in the paper. paper uses sample of 25k, this is 1k 
##################



# 2. Run optimisation

# Budget parameters
thetas = [0.67, 0.09, 0.041, 0.172, 0.027] # this is the payment proportions in each area of social welfare spending e.g. 67% of spend goes to aged pension
total_exp = 100 # in billions
B = 1

# Constraints;
'''
Two constraints;
1. Budget expenditure - B >= sum(x)
2. Newstart must be no more than 90% of aged pension () - x[0]*0.9 - x[1] >= 0
3. Each x_i subject to min and max of 0.66*B and 1.5*B
'''

# initial guess
def run_optimisation(B, thetas, x0, model, hstress = False):

    # define function
    def f(x):
        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        x4 = x[3]
        x5 = x[4]
        y = model.intercept_ + model.coef_[0]*x1 + model.coef_[1]*x2 + model.coef_[2]*x3 + model.coef_[3]*x4 + model.coef_[4]*x5 + model.coef_[5]*x1**2 + model.coef_[6]*x2**2 + model.coef_[7]*x3**2 + model.coef_[8]*x4**2 + model.coef_[9]*x5**2 + model.coef_[10]*x1**3 + model.coef_[11]*x2**3 + model.coef_[12]*x3**3 + model.coef_[13]*x4**3 + model.coef_[14]*x5**3
        return y
    if hstress is False:
        def objective(x):
            return -f(x)
    else:
        def objective(x):
            return f(x)
    # this clause is written in because HSTRESS variables are not negative - so there is no need to multiply by -1.

    def constraint1(x):
        exp = thetas[0]*x[0] + thetas[1]*x[1] + thetas[2]*x[2] + thetas[3]*x[3] + thetas[4]*x[4]
        return B - exp

    def constraint2(x):
        return x[0]*1.47 - x[1]

    # Constraint parameters
    max_con = B*1.5
    min_con = B*0.666

    # define constraints in format required for minimize
    con1 = {'type' : 'eq', 'fun' : constraint1}
    con2 = {'type' : 'ineq', 'fun' : constraint2}
    constraints_all = [con1, con2]

    # the third constraint needs to be coded up differently
    b = (min_con, max_con)
    bounds_all = (b,b,b,b,b)

    # run optimisation
    # sol = minimize(objective, x0, 
    #     method = "COBYLA", bounds = bounds_all, constraints = constraints_all)
    sol = minimize(objective, x0, 
        method = "trust-constr", bounds = bounds_all, constraints = constraints_all)
    print(sol)
    print("\n Optimisation result success: {0}".format(sol.success))

    # test results - ensure they meet constraints
    print("\nbounding constraint: results should be between 0.666*B and 1.5*B, actual result is {0}".format(sol.x))
    print("\nconstraint 1: result should be 0, actual result is {0}".format(constraint1(sol.x)))
    print("\nconstraint 2: result should be (+), actual result is {0}".format(constraint2(sol.x)))

    return sol

x0 = [1.0, 1.0, 1.0, 1.0, 1.0]
sol_povgap = run_optimisation(1, thetas, x0, model_povgap)        
# success result and all constraints met
##################



# 3. data generation

# some clean columns
types_cc = ['Age Pension', 'Newstart Allowance', 'Parenting Payment (Single)', 'Family Tax Benefit (0-13 years)', 'Rent Assistance']
optimal_cc = ["Optimal " + x for x in types_cc]
current_cc = [x.replace("Optimal", "Current") for x in optimal_cc]
# current payment levels
payment_levels = [918.5, 559.6, 782, 216.05, 138.6] # these must be in the same order as exo

# first, let's generate the optimal payment levels for a variety of budget levels
total_spend = pd.DataFrame() # total spend in each area of welfare
prop_spend = pd.DataFrame() # proportion of spend in each area of welfare
optimals = pd.DataFrame() # optimal spend
poverty_gap = pd.DataFrame() 
B_list = np.arange(0.8, 1.22, 0.01)
B_list = [round(x, 2) for x in B_list]
for k in range(len(B_list)):
    B = B_list[k]
    print("\nRunning for Budget Constraint: {0}".format(B))
    sol = run_optimisation(B_list[k], thetas, x0, model_povgap)

    # record optimals
    opm_result = pd.DataFrame(sol.x).T
    opm_result.columns = exo
    opm_result.index = [B]
    optimals = optimals.append(opm_result)

    # record prop spend
    j = 0
    for i in opm_result:
        opm_result.loc[B, i] = opm_result.loc[B, i]*thetas[j]
        j += 1
    prop_spend = prop_spend.append(opm_result)

    # record total spend
    total_spend = total_spend.append(opm_result*total_exp)



# figure 3
poverty_gap = pd.DataFrame()
def objective_flex(x, model):
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    x4 = x[3]
    x5 = x[4]
    y = model.intercept_ + model.coef_[0]*x1 + model.coef_[1]*x2 + model.coef_[2]*x3 + model.coef_[3]*x4 + model.coef_[4]*x5 + model.coef_[5]*x1**2 + model.coef_[6]*x2**2 + model.coef_[7]*x3**2 + model.coef_[8]*x4**2 + model.coef_[9]*x5**2 + model.coef_[10]*x1**3 + model.coef_[11]*x2**3 + model.coef_[12]*x3**3 + model.coef_[13]*x4**3 + model.coef_[14]*x5**3
    return -y
current_gap = objective_flex([1,1,1,1,1], model_povgap)
for i in range(len(optimals)):
    gap = objective_flex(optimals.iloc[i,:].values, model_povgap)
    poverty_gap = poverty_gap.append(pd.DataFrame({
        'poverty_gap' : gap,
        'change' : (gap/current_gap - 1)*100}, index = [optimals.index[i]]
    ))
poverty_gap.columns = ['Poverty Gap ($)', 'Change in Poverty Gap (from Current Value)']
poverty_gap['Current Poverty Gap'] = current_gap
poverty_gap['Budget (billions of $)'] = total_exp*poverty_gap.index
poverty_gap.to_excel(os.path.join(ex_rep, "figure3 - change in poverty gap by budget expenditure (optimal settings).xlsx"))




# figure 4

# then calculate optimal payment levels
optimal_payments = pd.DataFrame()
for i in range(5):
    optimal_payments[optimals.columns[i]] = [x*payment_levels[i] for x in optimals.iloc[:, i]]
optimal_payments.columns = types_cc
optimal_payments['Percentile'] = optimals.index
optimal_payments['Budget (in $ billion)'] = optimal_payments['Percentile']*total_exp
optimal_payments['Payment Type'] = 'Optimal'

# add in current payment levels into optimal_payments, for ease of chart generation
current_payments = pd.DataFrame()
for i in range(len(optimal_payments)):
    current_payments = current_payments.append(pd.DataFrame(payment_levels).T)
current_payments.columns = types_cc
current_payments['Percentile'] = optimals.index
current_payments['Budget (in $ billion)'] = current_payments['Percentile']*total_exp
current_payments['Payment Type'] = 'Current'

# clean up and export
optimal_payments = pd.concat([optimal_payments, current_payments])
optimal_payments = optimal_payments.sort_values(['Percentile'])
optimal_payments.index = range(len(optimal_payments))
optimal_payments.to_excel(os.path.join(ex_rep, "figure4 - optimal payment levels by budget change.xlsx"))




# figure 8 - need to run for different exo variables.
'''
Each chart requires the following datapoints;
1. Current payment level
2. POVGAP optimal value
3. POVGAPAH optimal value
4. HSTRESS optimal value 

Each row is a payment type
'''
# first store models
model_povgapah = run_regression(X, "POVGAPAH_HH")
model_hstress = run_regression(X, "HSTRESSGAP")
figure8 = pd.DataFrame()

for j in range(len(B_list)):
    B = B_list[j]
    sol_povgap = run_optimisation(B, thetas, x0, model_povgap)
    sol_povgapah = run_optimisation(B, thetas, x0, model_povgapah)
    sol_hstress = run_optimisation(B, thetas, x0, model_hstress, True)

    for i in range(5):
        current_payment = payment_levels[i]
        figure8 = figure8.append(pd.DataFrame({
            'Welfare Payment Type' : types_cc[i],
            'Current Payment' : current_payment,
            'Optimal Household Poverty Gap' : sol_povgap.x[i]*current_payment,
            'Optimal Household Poverty Gap (After housing costs)' : sol_povgapah.x[i]*current_payment,
            'Optimal Household Stress' : sol_hstress.x[i]*current_payment
        }, index = [B]))
figure8['Budget (billions in $)'] = figure8.index*total_exp
figure8['Percentile'] = figure8.index

figure8.to_excel(os.path.join(ex_rep, "figure8 - optimal payment levels by measure.xlsx"))








# Supporting documentation

# https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.LinearConstraint.html#scipy.optimize.LinearConstraint
# https://www.youtube.com/watch?v=cXHvC_FGx24



# Data required;

# current payment - should be in the current parameters dataset. (parameters_base18)