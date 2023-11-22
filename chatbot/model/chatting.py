from inferencing import load_models, chat

enc_model, dec_model, input_tokenizer, output_tokenizer, input_word_dict, output_word_dict, max_input_length, max_output_length = load_models()

def chatbot(sentence:str):
    response = chat(sentence, enc_model, dec_model, input_tokenizer, output_tokenizer, max_input_length, max_output_length)
    return (response.capitalize().rsplit(' ', 1)[0] + '.')

#response = chatbot("Who was Minnie?")
response = chatbot("Who is Mark Hunter?")
print('Bot: ' + response)