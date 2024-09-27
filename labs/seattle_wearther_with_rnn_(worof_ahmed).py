# -*- coding: utf-8 -*-
"""Seattle Wearther with RNN (worof ahmed).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JJFQUtB0ifOieHaRzrAm8ut2zaOyxfgg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, GRU, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.utils import to_categorical

data = pd.read_csv('seattle-weather.csv')
data.head()

# Data Preprocessing
label_encoder = LabelEncoder()
data['weather_encoded'] = label_encoder.fit_transform(data['weather'])

scaler = MinMaxScaler()
data[['precipitation', 'temp_max', 'temp_min', 'wind']] = scaler.fit_transform(
    data[['precipitation', 'temp_max', 'temp_min', 'wind']]
)

X = data[['precipitation', 'temp_max', 'temp_min', 'wind']].values
y = data['weather_encoded'].values

# Check class imbalance
class_counts = np.bincount(y)
print(f"Class distribution: {class_counts}")

# Reshape X to 3D shape (samples, timesteps, features) with multiple timesteps (e.g., 5 days)
timesteps = 5
X_new = []
y_new = []
for i in range(len(X) - timesteps):
    X_new.append(X[i:i+timesteps])
    y_new.append(y[i+timesteps])

X_new = np.array(X_new)
y_new = np.array(y_new)

# One-hot encode target labels
y_new = to_categorical(y_new)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

def build_rnn_model(input_shape, output_units):
    model = Sequential()
    model.add(SimpleRNN(64, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(SimpleRNN(64))
    model.add(Dense(output_units, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def build_gru_model(input_shape, output_units):
    model = Sequential()
    model.add(GRU(64, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(64))
    model.add(Dense(output_units, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def build_lstm_model(input_shape, output_units):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(64))
    model.add(Dense(output_units, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def build_bidirectional_model(input_shape, output_units):
    model = Sequential()
    model.add(Bidirectional(LSTM(64, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dense(output_units, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Input shape for the models
input_shape = (timesteps, X_train.shape[2])
output_units = y_train.shape[1]

rnn_model = build_rnn_model(input_shape, output_units)
gru_model = build_gru_model(input_shape, output_units)
lstm_model = build_lstm_model(input_shape, output_units)
bidirectional_model = build_bidirectional_model(input_shape, output_units)
rnn_model.summary()
gru_model.summary()
lstm_model.summary()
bidirectional_model.summary()

print("Training RNN Model...")
rnn_history = rnn_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=2)

print("Training GRU Model...")
gru_history = gru_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=2)

print("Training LSTM Model...")
lstm_history = lstm_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=2)

print("Training Bidirectional LSTM Model...")
bidirectional_history = bidirectional_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), verbose=2)

# Evaluate each model
print("Evaluating RNN Model...")
rnn_accuracy = rnn_model.evaluate(X_test, y_test, verbose=0)
print(f'RNN Accuracy: {rnn_accuracy}')

print("Evaluating GRU Model...")
gru_accuracy = gru_model.evaluate(X_test, y_test, verbose=0)
print(f'GRU Accuracy: {gru_accuracy}')

print("Evaluating LSTM Model...")
lstm_accuracy = lstm_model.evaluate(X_test, y_test, verbose=0)
print(f'LSTM Accuracy: {lstm_accuracy}')

print("Evaluating Bidirectional LSTM Model...")
bidirectional_accuracy = bidirectional_model.evaluate(X_test, y_test, verbose=0)
print(f'Bidirectional LSTM Accuracy: {bidirectional_accuracy}')

!pip install pydot graphviz

from tensorflow.keras.utils import plot_model
plot_model(rnn_model, to_file='rnn_model.png', show_shapes=True, show_layer_names=True)
plot_model(gru_model, to_file='gru_model.png', show_shapes=True, show_layer_names=True)
plot_model(lstm_model, to_file='lstm_model.png', show_shapes=True, show_layer_names=True)
plot_model(bidirectional_model, to_file='bidirectional_model.png', show_shapes=True, show_layer_names=True)

def plot_training_history(history, model_name):
    plt.figure(figsize=(12, 5))

    # Accuracy plot
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title(f'{model_name} Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{model_name} Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Plot accuracy and loss for each model
plot_training_history(rnn_history, 'RNN')
plot_training_history(gru_history, 'GRU')
plot_training_history(lstm_history, 'LSTM')
plot_training_history(bidirectional_history, 'Bidirectional LSTM')