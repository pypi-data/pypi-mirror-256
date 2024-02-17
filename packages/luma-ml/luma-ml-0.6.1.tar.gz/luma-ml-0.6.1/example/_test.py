import __local__
from luma.neural.multi_layer import MLPClassifier
from luma.preprocessing.scaler import StandardScaler
from luma.model_selection.split import TrainTestSplit

from sklearn.datasets import load_digits
import matplotlib.pyplot as plt


X, y = load_digits(return_X_y=True)

sc = StandardScaler()
X_sc = sc.fit_transform(X)

X_train, X_test, y_train, y_test = TrainTestSplit(X_sc, y,
                                                  test_size=0.2,
                                                  random_state=42).get

mlp = MLPClassifier(input_size=64,
                    hidden_sizes=[32, 16],
                    output_size=10,
                    max_epoch=1000,
                    learning_rate=0.0002,
                    lambda_=0.01,
                    dropout_rate=0.05,
                    activation='relu',
                    verbose=True)

mlp.fit(X_train, y_train)
print(mlp.score(X_test, y_test))
mlp.dump()

plt.plot(range(mlp.max_epoch), mlp.losses_, c='crimson')
plt.xlabel('Epochs')
plt.ylabel('Loss (Cross-Entropy)')
plt.title(f'MLP Loss with {type(mlp.act_).__name__} [Acc: {mlp.score(X_test, y_test):.4f}]')
plt.tight_layout()
plt.show()

