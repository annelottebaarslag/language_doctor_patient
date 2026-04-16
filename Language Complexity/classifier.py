from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('ABEL_classifier/ALL.csv')



df["text"] = df["text"].astype(str)
df = df.dropna(subset=["text", "label"])


X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, stratify=df["label"], random_state=42
)


vectorizer = TfidfVectorizer(ngram_range=(1,3))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = LinearSVC()
clf.fit(X_train_vec, y_train)
y_pred = clf.predict(X_test_vec)

print(classification_report(y_test, y_pred))

# https://aneesha.medium.com/visualising-top-features-in-linear-svm-with-scikit-learn-and-matplotlib-3454ab18a14d

top_features = 10
coef = clf.coef_.ravel()
top_positive_coefficients = np.argsort(coef)[-top_features:]
top_negative_coefficients = np.argsort(coef)[:top_features]
feature_names = vectorizer.get_feature_names_out()
for pos_coef in reversed(top_positive_coefficients):
    print(f"{feature_names[pos_coef]}:{coef[pos_coef]}")
print("\n")
for neg_coef in top_negative_coefficients:
    print(f"{feature_names[neg_coef]}:{coef[neg_coef]}")

def plot_coefficients(classifier, feature_names, top_features):
    coef = classifier.coef_.ravel()

    # Get top positive and negative coefficients
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]

    # Combine
    top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    top_coef_values = coef[top_coefficients]

    # Colors
    colors = ['red' if c < 0 else 'blue' for c in top_coef_values]

    # Plot
    plt.figure(figsize=(15, 5))
    plt.bar(np.arange(2 * top_features), top_coef_values, color=colors)


    feature_names = np.array(feature_names)
    plt.xticks(np.arange(2 * top_features), feature_names[top_coefficients], rotation=60, ha='right')

    plt.ylabel("Coefficient value")
    plt.tight_layout()
    plt.show()


plot_coefficients(clf, vectorizer.get_feature_names_out(), top_features)