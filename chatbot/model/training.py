import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, activations, models, preprocessing, utils

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
#Hi! Kung malakas po ang machine/laptop/desktop niyo, taasan niyo po ang number of epochs at alisin ang hash
model.fit([encoder_input_data , decoder_input_data], decoder_target_data, batch_size=124, epochs=500)
model.save('./chatbot/model/chatbot_model.h5')

#model = tf.keras.models.load_model('./chatbot/model/chatbot_model.h5')

# INPUT FORMATTING
def make_inference_models():
    encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

    decoder_state_input_h = tf.keras.layers.Input(shape=(256,))
    decoder_state_input_c = tf.keras.layers.Input(shape=(256,))

    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_embedding , initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = tf.keras.models.Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return encoder_model , decoder_model

# NEED TO EDIT: ASCII CHARACTERS WILL PRODUCE AN ERROR
def str_to_tokens(sentence:str):
    words = sentence.lower().split()
    tokens_list = list()
    for word in words:
        tokens_list.append(input_word_dict[word])
    return preprocessing.sequence.pad_sequences([tokens_list], maxlen=max_input_length, padding='post')

enc_model , dec_model = make_inference_models()

def chatting(sentence:str):
    states_values = enc_model.predict(str_to_tokens(sentence))
    empty_target_seq = np.zeros((1, 1 ))
    empty_target_seq[0, 0] = output_word_dict['start']
    decoded_translation = ''
    dec_outputs , h , c = dec_model.predict([empty_target_seq] + states_values)
    sampled_word_index = np.argmax( dec_outputs[0, -1, :] )
    sampled_word = None
    for word, index in output_word_dict.items():
        if sampled_word_index == index :
            decoded_translation += '{}'.format(word)
            sampled_word = word

    return(decoded_translation)