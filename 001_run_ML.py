exec(open("Utils.py").read(), globals())
exec(open("Utils_parallel.py").read(), globals())

SEED = 741
njob = 16

# exec(open("015_SPLITTING_DATA.py").read(), globals())
# exec(open("030_VARIABLES_SELECTION.py").read(), globals())
# exec(open("035_UNIVARIATE_VARIABLES_SELECTION.py").read(), globals())

#methods = ['ISIS', 'LASSO', 'DECISION_TREE',
methods = [ 'ISIS', 'LR_ACCURACY', 'E_NET', 'INFORMATION_GAIN', 'LASSO', 'RIDGE', 'DECISION_TREE', 'RANDOM_FOREST', 'GBM']
#method = 'ISIS'
# GET PREDICTOR
# ['LASSO', 'DECISION_TREE', 'RANDOM_FOREST', 'GBM',
#  'E_NET', 'INFORMATION_GAIN', 'LR_ACCURACY']
# ISIS
#nvar = 10

# predictors = extract_predictors( method, nvar, SEED)
# eff_nvar = len(predictors)
probs_to_check = np.arange(0.1, 0.91, 0.1)
DF = pd.DataFrame()

scheduled_model = 'running_model/'
create_dir( scheduled_model)

for method in methods:
    nvars = []
    all_nvars = np.concatenate( ([1], np.arange(10, 51, 10)))#, np.arange(70, 130, 30)))
    for i in all_nvars:
        predictors = extract_predictors(method, i, SEED)
        eff_nvar = len(predictors)
        if eff_nvar not in nvars:
            nvars.append( eff_nvar)
        # nvars = list(set( [el for el in nvars if el>=eff_nvar] ))
    for nvar in nvars:
        predictors = extract_predictors(method, nvar, SEED)
        eff_nvar = len(predictors)
        print method, nvar
        try:
            exec(open("041_TREE_BASED_MODELS.py").read(), globals())
        except:
            DF.to_csv( scheduled_model + '000_TREE_BASED_' + method + '_' + str(nvar) + '.csv')
        # >>>>>>>>> exec(open("042_SVM.py").read(), globals()) >>>>>>>>>>>>
        try:
            exec(open("043_REGULARIZED_METHODS.py").read(), globals())
        except:
            DF.to_csv( scheduled_model + '000_LASSO_' + method + '_' + str(nvar) + '.csv')
        try:
            exec(open("045_NAIVE_BAYES.py").read(), globals())
        except:
            DF.to_csv( scheduled_model + '000_NAIVE_BAYES_' + method + '_' + str(nvar) + '.csv')
        try:
            exec(open("046_KNN.py").read(), globals())
        except:
            DF.to_csv( scheduled_model + '000_KNN_' + method + '_' + str(nvar) + '.csv')
        DF.to_csv(  scheduled_model + '999_' + method + '_' + str(nvar) + '.csv' )





#for method in methods:

#method = methods[2]
nvars = []
all_nvars = np.concatenate( ([1], np.arange(10, 51, 10), np.arange(70, 130, 30)))

for i in all_nvars:
    predictors = extract_predictors(method, i, SEED)
    eff_nvar = len(predictors)
    if eff_nvar not in nvars:
        nvars.append( eff_nvar)
    # nvars = list(set( [el for el in nvars if el>=eff_nvar] ))

for nvar in nvars:
    predictors = extract_predictors(method, nvar, SEED)
    eff_nvar = len(predictors)
    print method, nvar
    try:
        exec(open("041_TREE_BASED_MODELS.py").read(), globals())
    except:
        DF.to_csv('000_TREE_BASED_' + method + '_' + str(nvar) + '.csv')
        # >>>>>>>>> exec(open("042_SVM.py").read(), globals()) >>>>>>>>>>>>
    try:
        exec(open("043_REGULARIZED_METHODS.py").read(), globals())
    except:
        DF.to_csv('000_LASSO_' + method + '_' + str(nvar) + '.csv')
    try:
        exec(open("045_NAIVE_BAYES.py").read(), globals())
    except:
        DF.to_csv('000_NAIVE_BAYES_' + method + '_' + str(nvar) + '.csv')
    try:
        exec(open("046_KNN.py").read(), globals())
    except:
        DF.to_csv('000_KNN_' + method + '_' + str(nvar) + '.csv')
    DF.to_csv( '999_' + method + '_' + str(nvar) + '.csv' )
