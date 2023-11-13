import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers , activations , models , preprocessing , utils

with open('./dataset/narrativeqa dataset - cleaned.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

input_texts = []
target_texts = []

#Hi! Kung malakas po ang machine/laptop/desktop niyo, alisin niyo po ang "500" para magamit lahat ng nasa dataset
#If di po kaya ang 500, make it smaller then increase the epochs at line 90. Warning: 500epochs ito tapos ~5s per epoch
for line in lines[1:500]: 
    row = line.strip().split(',')

    if lines:
        input_text = row[0]
        target_text = row[1]
        input_texts.append(input_text)
        target_texts.append(target_text)

zippedList =  list(zip(input_texts, target_texts))
lines = pd.DataFrame(zippedList, columns = ['input' , 'output'])

input_lines = list()
for line in lines.input:
    input_lines.append(line)

tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(input_lines)
tokenized_input_lines = tokenizer.texts_to_sequences(input_lines)

length_list = list()
for token_seq in tokenized_input_lines:
    length_list.append(len(token_seq))
max_input_length = np.array(length_list).max()

padded_input_lines = preprocessing.sequence.pad_sequences(tokenized_input_lines, maxlen=max_input_length, padding='post')
encoder_input_data = np.array(padded_input_lines)

input_word_dict = tokenizer.word_index
num_input_tokens = len(input_word_dict) + 1

output_lines = list()
for line in lines.output:
    output_lines.append('<START> ' + line + ' <END>')

tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(output_lines)
tokenized_output_lines = tokenizer.texts_to_sequences(output_lines)

length_list = list()
for token_seq in tokenized_output_lines:
    length_list.append(len(token_seq))
max_output_length = np.array(length_list).max()

padded_output_lines = preprocessing.sequence.pad_sequences(tokenized_output_lines, maxlen=max_output_length, padding='post')
decoder_input_data = np.array(padded_output_lines)

output_word_dict = tokenizer.word_index
num_output_tokens = len(output_word_dict) + 1

decoder_target_data = list()
for token_seq in tokenized_output_lines:
    decoder_target_data.append(token_seq[1:])

padded_output_lines = preprocessing.sequence.pad_sequences(decoder_target_data, maxlen=max_output_length, padding='post' )
onehot_output_lines = utils.to_categorical(padded_output_lines, num_output_tokens)
decoder_target_data = np.array(onehot_output_lines)

encoder_inputs = tf.keras.layers.Input(shape=(None,))
encoder_embedding = tf.keras.layers.Embedding(num_input_tokens, 256, mask_zero=True) (encoder_inputs)
encoder_outputs, state_h, state_c = tf.keras.layers.LSTM(256, return_state=True, recurrent_dropout=0.2, dropout=0.2)(encoder_embedding)
encoder_states = [state_h , state_c]

decoder_inputs = tf.keras.layers.Input(shape=(None,  ))
decoder_embedding = tf.keras.layers.Embedding( num_output_tokens, 256 , mask_zero=True) (decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM(256, return_state=True, return_sequences=True, recurrent_dropout=0.2, dropout=0.2)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(num_output_tokens, activation=tf.keras.activations.softmax)
output = decoder_dense(decoder_outputs)

model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output)
model.compile(optimizer=tf.keras.optimizers.Adam(), loss='categorical_crossentropy')

# MODEL SAVING
#Hi! Kung malakas po ang machine/laptop/desktop niyo, taasan niyo po ang number of epochs
model.fit([encoder_input_data , decoder_input_data], decoder_target_data, batch_size=124, epochs=500)
model.save('./model/chatbot_model.h5')