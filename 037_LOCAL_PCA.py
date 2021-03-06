exec(open("Utils.py").read(), globals())

dir_images = 'Images/'

dir_reg = 'DATA/CLASSIFICATION/'
data = pd.read_csv( dir_reg + "pre_training_set.csv" )

variables = data.columns[ 0:251 ]

X = data[ variables ]
X = X.fillna( method = 'ffill')
# correlation_matrix( df = X, path = dir_images + 'Correlation_plot.png')

cor_matrix = X.corr().fillna( 0 )# method = 'ffill')
cor_matrix = abs(cor_matrix)

# cor_matrix[ 'BIG_CL_X' ]
# sns.kdeplot( cor_matrix[ col ], shade = True )
# plt.show()

groups = []
k = 10
threshold = 0.5
check = 0

for col in cor_matrix.columns:
    FLG = any( col in g for g in groups)
    if FLG == True:
        print ''' Variable''', col, ''' already exist in a group'''
    else:
        # col = cor_matrix.columns[5]
        group = cor_matrix[ col ].nlargest(k + 1)[ cor_matrix[ col ]!= 1 ]
        group = group[ group > threshold ].index
        groups.append(group)
        check += 1
print check

gs = []
for g in groups:
    if len(g) >2 :
        gs.append(g)
groups = gs

unique = set(x for l in groups for x in l)
len( unique )

assign_df = pd.DataFrame()

for cluster in groups:
    # cluster = groups[1]
    for el in cluster:
        #el = cluster[0]
        check_list = [item for item in cluster if item != el]
        np.max( cor_matrix[ cor_matrix.index == el][check_list])
        max = np.max(cor_matrix[cor_matrix.index == el][check_list].max())
        assign_df = assign_df.append( [[el, max]])

cols = ['VAR', 'COR_MAX']
assign_df.columns = cols

df = assign_df

for el in set(df.VAR):
    #el = [set(df.VAR)][1]
    current_df = pd.DataFrame(df[df.VAR == el ].max()).transpose()
    df = df[df.VAR != el]
    df = df.append(current_df)


for i in range( len(groups)):
    #i = 1
    group = groups[i]
    for el in group:
        #el = group[1]
        cor_max = df[df.VAR == el ].COR_MAX
        if round(cor_max - np.max(cor_matrix[el][group].max()), 4)== 0.0000:
            continue
        else:
            group = group[group != el]
            groups[i] = group

unique = set(x for l in groups for x in l)
len( groups )
len( unique )


check = 0
indexes = []
for j in range(len(groups)):
    if len(groups[j]) >2 :
        check +=1
    else:
        print(g)
        groups[ groups.index == j]

pca_groups = []

for group in groups:
    if len(group)>2:
        print 'length is ', len(group)
        print group
        pca_groups.append(group)

unique = set(x for l in groups for x in l)
len(unique)

# lasciare la variabile dentro il gruppo dove ha la correlazione maggiore
# X_scaled = X.transpose().copy()
# # X_scaled.to_csv( 'clustering.csv', index = True)
# # calcolare su tutti i dati
# from sklearn import preprocessing
#
# for col in X_scaled.columns:
#     mean = np.mean( X_scaled[col])
#     std = np.std( X_scaled[col])
#     X_scaled[col] = (X_scaled[col] - mean)/std
#
#
# from matplotlib import pyplot as plt
# from scipy.cluster.hierarchy import dendrogram, linkage
#
#
# D = linkage( X_scaled, method = 'single', metric = 'euclidean' )
#
# plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# dendrogram(
#     D,
#     leaf_rotation=90.,  # rotates the x axis labels
#     leaf_font_size=8.,  # font size for the x axis labels
# )
# plt.show()







directory = 'DATA/CLASSIFICATION/'
data = pd.read_csv( directory + "dataset.csv" )

SEED = 123
njobs = 2
print data.shape

variable_score = pd.DataFrame()


variable_sub_dataset, modeling_dataset = train_test_split( data, test_size = 0.9,
                                                           random_state = SEED)

# variable_sub_dataset.to_csv( directory + 'pre_training_set.csv', index = False)
# modeling_dataset.to_csv( directory + 'modeling_dataset.csv', index = False)
from sklearn.feature_selection import SelectKBest, mutual_info_classif, f_classif
from sklearn.linear_model import LogisticRegression

log = LogisticRegression()

variables = variable_sub_dataset.columns[ 0:251 ]
variable_score[ 'VARIABLE' ] = variables

X = variable_sub_dataset[ variables ]
X = X.fillna( method = 'ffill')

Y = variable_sub_dataset['Y']

F_value, p_value = f_classif(X, Y)
variable_score[ 'ANOVA_pvalue' ] = p_value

IG = np.around( mutual_info_classif(X, Y), 3)
variable_score[ 'INFORMATION_GAIN' ] = IG



indexes_var = np.percentile( IG, 90)

variables[ np.where( p_value<0.1) ]

accuracy = []
for var in variables:
    # var = variables[ 2 ]
    x = pd.DataFrame(X[ var ])
    pred = log.fit( x, Y ).predict_proba(x)
    prediction_log = []

    for p in pred:
        prediction_log.append( p[1] )
    prediction_log = np.array(prediction_log)
    prediction_log = (prediction_log>0.5)*1
    current_accuracy = np.around( skl.metrics.accuracy_score(Y, prediction_log), 2 )
    accuracy.append(current_accuracy)
    print( var, current_accuracy)

variable_score[ 'LR_ACCURACY' ] = accuracy
univariate_var_sel = variable_score.copy()

univariate_var_sel.to_csv( 'results/univariate_var_sel.csv', index = False)





























































target_variable = 'Y'
col_energy = 'ENERGY'


X = variable_sub_dataset.drop( [target_variable, col_energy], axis = 1)#.astype('float32')
X = X.fillna( method = 'ffill')
print pd.isnull(X).sum() > 0


Y = variable_sub_dataset[ target_variable ]
x_names = X.columns

df_importance = pd.DataFrame( )
df_importance[ 'Variable' ] = x_names

##################################################
# variable_sub_dataset.to_csv( 'dataset_reduced.csv', index = False)

#################### LASSO ##########################
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score

grid_values = {'penalty': ['l1'],
               'C': np.arange(0.0001, 1, 0.0005)}

log_reg = LogisticRegression()

lr_cv = GridSearchCV(log_reg, param_grid = grid_values)
lr = lr_cv.fit(X, Y)

# print( lr.best_estimator_)
print( lr.best_params_ )
print( lr.best_score_)
print len(lr.best_estimator_.coef_[ abs(lr.best_estimator_.coef_)>1])
print len(lr.best_estimator_.coef_[ abs(lr.best_estimator_.coef_)>0.5])
print len(lr.best_estimator_.coef_[ abs(lr.best_estimator_.coef_)>0.1])
print len(lr.best_estimator_.coef_[ abs(lr.best_estimator_.coef_)>0])


coeff_lasso = lr.best_estimator_.coef_[0]
df_importance[ 'LASSO' ] = coeff_lasso
######################################################

############# Decision Tree ###########################
decision_tree = tree.DecisionTreeClassifier()

dt_parameters = {'max_depth': range(5, 50, 10),
                 'min_samples_leaf': range(50, 400, 50),
                 'min_samples_split': range( 100, 500, 100),
                 'criterion': ['gini', 'entropy']}

decision_tree = GridSearchCV( tree.DecisionTreeClassifier(), dt_parameters, n_jobs = njobs )
decision_tree = decision_tree.fit( X, Y )
tree_model = decision_tree

print( tree_model.best_params_ )
print( tree_model.best_score_)

importance_dt = tree_model.best_estimator_.feature_importances_

print len(importance_dt[ abs(importance_dt)>1])
print len(importance_dt[ abs(importance_dt)>0.5])
print len(importance_dt[ abs(importance_dt)>0.0001])
print len(importance_dt[ abs(importance_dt)>0])
print len(importance_dt)

df_importance[ 'DECISION_TREE' ] = importance_dt
#########################################################


#######################################
''' RANDOM FOREST '''
random_forest = RandomForestClassifier()

parameters = {'n_estimators': range(100, 900, 100),
              'max_features': [ 10, 15, 25],
              'max_depth':  [5, 10, 15],
              'min_samples_split': range( 100, 900, 400)
              }
random_forest = GridSearchCV( RandomForestClassifier(), parameters, n_jobs = njobs)
random_forest = random_forest.fit( X, Y )
rf_model = random_forest

importance_rf = rf_model.best_estimator_.feature_importances_

print len(importance_rf[ abs(importance_rf)>1])
print len(importance_rf[ abs(importance_rf)>0.05])
print len(importance_rf[ abs(importance_rf)>0.01])
print len(importance_rf)

df_importance[ 'RANDOM_FOREST' ] = importance_rf

##################################################################
''' GRADIENT BOOSTING MACHINE '''

gbm = GradientBoostingClassifier()

parameters_gbm = {'n_estimators': [100, 150, 200, 300],
              'learning_rate': [0.1, 0.05, 0.01],
              'max_depth': [4, 6, 8],
              'min_samples_leaf': [20, 50],
              'max_features': [1.0, 0.3, 0.1]
              }
gbm = GridSearchCV( GradientBoostingClassifier(), parameters_gbm, n_jobs = njobs)
gbm = gbm.fit( X, Y )
gbm_model = gbm

importance_gbm = gbm_model.best_estimator_.feature_importances_

df_importance[ 'GBM' ] = importance_gbm
##################################################


##################################################
''' Elastic Net '''
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV

# Use grid search to tune the parameters:


eNet = SGDClassifier()

eNet_parameters = { "l1_ratio": np.arange(0.001, 1, 0.005),
                    'loss': ["log"],
                    'penalty': ["elasticnet"]}


eNet = GridSearchCV(eNet, eNet_parameters, scoring='accuracy', cv=5, n_jobs = 2)
eNet = eNet.fit(X, Y)
eNet_model = eNet.best_estimator_

print( eNet_model.score(X, Y) )

coeff_eNet = eNet_model.coef_[0]
df_importance[ 'Elastic_Net' ] = coeff_eNet


# print( lr.best_estimator_)
print( lr.best_params_ )
print( lr.best_score_)
print len(coeff_eNet[ abs(coeff_eNet)>1])
print len(coeff_eNet[ abs(coeff_eNet)>0.5])
print len(coeff_eNet[ abs(coeff_eNet)>0.1])
print len(coeff_eNet[ abs(coeff_eNet)>0])

np.percentile( coeff_eNet , np.arange(0.05, 1, 0.05))
np.max( coeff_eNet , np.arange(0.25, 1, 0.25))

#Y = ((X-min_X)/(max_X-min_X))*max_Y-min_Y + min_Y

max_prev = np.max(coeff_eNet)
min_prev = np.min(coeff_eNet)

norm_coeff_eNet = normalization(abs(coeff_eNet))

sns.kdeplot( norm_coeff_eNet, shade = True )
plt.show()

sns.kdeplot( coeff_eNet, shade = True )
plt.show()


##############################################

df_importance[ 'LASSO' ] = np.around(df_importance[ 'LASSO' ], 2)
df_importance[ 'DECISION_TREE' ] = np.around(df_importance[ 'DECISION_TREE' ], 4)
df_importance[ 'RANDOM_FOREST' ] = np.around(df_importance[ 'RANDOM_FOREST' ], 4)
df_importance[ 'GBM' ] = np.around(df_importance[ 'GBM' ], 4)
df_importance[ 'Elastic_Net' ] = np.around(df_importance[ 'Elastic_Net' ], 2)

df_importance.to_csv( 'results/importance.csv', index = False)


importance_ranked = pd.DataFrame()
importance_ranked['VARIABLE'] = df_importance.Variable
importance_ranked['LASSO'] =  abs(df_importance.LASSO).rank()
importance_ranked['DECISION_TREE'] = abs(df_importance.DECISION_TREE).rank()
importance_ranked['RANDOM_FOREST'] = abs(df_importance.RANDOM_FOREST).rank()
importance_ranked['GBM'] = abs(df_importance.GBM).rank()
importance_ranked['E_NET'] = abs(df_importance.Elastic_Net).rank()

importance_ranked.to_csv( 'results/importance_ranked.csv', index = False)
