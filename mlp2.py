#%%
import pandas as pd
import os
from skimage.transform import resize
from skimage.io import imread
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
#%%
#Initial variables and sources
Cat=[]
for i in range(1,5):
    Cat.append(str(i))
#%%
wej_arr=[]
train_arr=[]
src1 = r"C:\Users\mrthe\Downloads\archive\coins\data\train3"
srcl=[]
for i in os.listdir(src1):
    src=(os.path.join(src1, i))
    for j in os.listdir(src):
        img_array = imread(os.path.join(src, j))
        srcl.append(os.path.join(src, j))
        resized = resize(img_array, (150, 150, 3))
        wej_arr.append(resized.flatten())
        train_arr.append(Cat.index(str(i)))

#%%
#Numpy matrix
wej = np.array(wej_arr)
train = np.array(train_arr)

#To dataframe
df=pd.DataFrame(wej)
df['Train']=train

#Indexing the dataframe
x=df.iloc[:,:-1]
y=df.iloc[:,-1]

#%%
#Reshape features
X = np.reshape(wej,(-1,300, 300, 1))

# Display the first image in training data
plt.figure(figsize=[5,5])
curr_img = np.reshape(X[0], (300,300))
plt.imshow(curr_img, cmap='gray')

#Transform to float and normalize
X = np.array(X, dtype=np.float32)
X /= 255

#Labels to numpy array
y = np.array(y)
#%%
#SHUFFLE
def unison_shuffled_copies(X, y):
    assert len(X) == len(y)
    p = np.random.permutation(len(X))
    return X[p], y[p]

#%%
X_train,y_train = unison_shuffled_copies(X,y)

#80/20 split
X_train, X_test = train_test_split(X, test_size=0.2, shuffle = False )
y_train, y_test = train_test_split(y, test_size=0.2, shuffle = False )
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#Model
model = Sequential([
    Flatten(input_shape=(300, 300)),

    # dense layer 1
    Dense(128, activation='relu'),

    # dense layer 2
    Dense(256, activation='relu'),

    # output layer
    Dense(2, activation='softmax')
])

tf.keras.optimizers.SGD(
    learning_rate=0.01,
    momentum=0.0,
    nesterov=False,
    name='SGD',
)
model.compile(optimizer='SGD', loss='categorical_crossentropy', metrics=['accuracy'])
#%%
exit = "e"
strain = "t"
stest = "r"
shelp = "h"
inp = None
#%%
while exit != inp:
    print('Aby rozpoczac uczenie wcisnij "T"', 'Aby rozpoczac test wcisnij "R"', 'Aby uzyska?? pomoc wcisnij "H"',
            'Aby zako??czy?? dzia??anie programu wci??niej "E"', sep='\n')
    inp = input()
    if inp == strain:
        #Train + plot
        model.fit(X_train, y_train, epochs=160, batch_size=2000)
        model.summary()
    elif inp == stest:
        #Test
        results = model.evaluate(X_test, y_test, verbose=1)
        print('test loss, test acc:', results)
    elif inp == shelp:
        print('Program natury problemu klasyfikacji obraz??w z wykorzystaniem algorytmu MLP','T - Rozpoczyna uczenie maszyny rozr????niania banana od jab??ka na bazie danych treningowych',
              'R - Rozpoczyna w??a??ciwy test algorytmu UWAGA je??li nie uruchomi??e?? wcze??niej trybu treningowego maszyna mo??e klasyfikowa?? "na ??lepo"',
              'E - Terminuje program oraz wy??wietla grafy', sep='\n')
#%%
model.fit(X_train, y_train, epochs=160, batch_size=2000)
        model.summary()
    elif inp == stest:
        #Test
        results = model.evaluate(X_test, y_test, verbose=1)
        print('test loss, test acc:', results)
#%%
def plot_learning_curve(
    estimator,
    title,
    X,
    y,
    axes=None,
    ylim=None,
    cv=None,
    n_jobs=None,
    train_sizes=np.linspace(0.1, 1.0, 5),
    ):
    if axes is None:
        _, axes = plt.subplots(1, 3, figsize=(20, 5))

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = learning_curve(
        estimator,
        X,
        y,
        cv=cv,
        n_jobs=n_jobs,
        train_sizes=train_sizes,
        return_times=True,
    )
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    axes[0].grid()
    axes[0].fill_between(
        train_sizes,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.1,
        color="r",
    )
    axes[0].fill_between(
        train_sizes,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.1,
        color="g",
    )
    axes[0].plot(
        train_sizes, train_scores_mean, "o-", color="r", label="Training score"
    )
    axes[0].plot(
        train_sizes, test_scores_mean, "o-", color="g", label="Cross-validation score"
    )
    axes[0].legend(loc="best")

    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, "o-")
    axes[1].fill_between(
        train_sizes,
        fit_times_mean - fit_times_std,
        fit_times_mean + fit_times_std,
        alpha=0.1,
    )
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    fit_time_argsort = fit_times_mean.argsort()
    fit_time_sorted = fit_times_mean[fit_time_argsort]
    test_scores_mean_sorted = test_scores_mean[fit_time_argsort]
    test_scores_std_sorted = test_scores_std[fit_time_argsort]
    axes[2].grid()
    axes[2].plot(fit_time_sorted, test_scores_mean_sorted, "o-")
    axes[2].fill_between(
        fit_time_sorted,
        test_scores_mean_sorted - test_scores_std_sorted,
        test_scores_mean_sorted + test_scores_std_sorted,
        alpha=0.1,
    )
    axes[2].set_xlabel("fit_times")
    axes[2].set_ylabel("Score")
    axes[2].set_title("Performance of the model")

    return plt

fig, axes = plt.subplots(3, 2, figsize=(10, 15))

X, y = load_digits(return_X_y=True)

title = "Learning Curves (Naive Bayes)"
cv = ShuffleSplit(n_splits=50, test_size=0.2, random_state=0)

estimator = GaussianNB()
plot_learning_curve(
    estimator, title, X, y, axes=axes[:, 0], ylim=(0.7, 1.01), cv=cv, n_jobs=4
)

title = r"Learning Curves (SVM, RBF kernel, $\gamma=0.001$)"
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
estimator = SVC(gamma=0.001)
plot_learning_curve(
    estimator, title, X, y, axes=axes[:, 1], ylim=(0.7, 1.01), cv=cv, n_jobs=4
)

plt.show()