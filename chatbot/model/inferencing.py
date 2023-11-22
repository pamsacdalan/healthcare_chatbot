import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence

def chat(sentence, enc_model, dec_model, input_tokenizer, output_tokenizer, max_input_length, max_output_length):
    with open('./chatbot/model/input_tokenizer.pkl', 'rb') as input_tokenizer_file:
        input_tokenizer = pickle.load(input_tokenizer_file)

    with open('./chatbot/model/output_tokenizer.pkl', 'rb') as output_tokenizer_file:
        output_tokenizer = pickle.load(output_tokenizer_file)
        
    encoder_input_data = str_to_tokens(sentence, input_tokenizer, max_input_length)
    states_values = enc_model.predict(encoder_input_data)

    empty_target_seq = np.zeros((1, 1))
    empty_target_seq[0, 0] = output_tokenizer.word_index['start']
    decoded_translation = ''

    for x in range(max_output_length):
        dec_outputs, h, c = dec_model.predict([empty_target_seq] + states_values)

        sampled_word_index = np.argmax(dec_outputs[0, -1, :])

        sampled_word = [word for word, index in output_tokenizer.word_index.items() if index == sampled_word_index]
        if sampled_word:
            decoded_translation += ' {}'.format(sampled_word[0])

        if sampled_word_index == output_tokenizer.word_index['end']: #hard stopping the chatbot
            break

        empty_target_seq[0, 0] = sampled_word_index
        states_values = [h, c]

    return decoded_translation.strip()

def load_models():
    encoder_model = load_model('./chatbot/model/encoder_model.h5', compile=False)
    decoder_model = load_model('./chatbot/model/decoder_model.h5', compile=False)

    with open('./chatbot/model/input_tokenizer.pkl', 'rb') as input_tokenizer_file:
        input_tokenizer = pickle.load(input_tokenizer_file)

    with open('./chatbot/model/output_tokenizer.pkl', 'rb') as output_tokenizer_file:
        output_tokenizer = pickle.load(output_tokenizer_file)

    input_word_dict = {word: index + 1 for word, index in input_tokenizer.word_index.items()}
    max_input_length = len(input_word_dict)

    output_word_dict = {word: index + 1 for word, index in output_tokenizer.word_index.items()}
    max_output_length = len(output_word_dict)

    return encoder_model, decoder_model, input_tokenizer, output_tokenizer, input_word_dict, output_word_dict, max_input_length, max_output_length

def str_to_tokens(sentence, input_tokenizer, max_input_length):
    sentence = sentence.replace('?', '')
    input_words = sentence.lower().split()
    
    input_tokens_list = [input_tokenizer.word_index.get(word, 0) for word in input_words]
    padded_input_tokens = sequence.pad_sequences([input_tokens_list], maxlen=max_input_length, padding='post')
    encoder_input_data = np.array(padded_input_tokens)

    return encoder_input_data