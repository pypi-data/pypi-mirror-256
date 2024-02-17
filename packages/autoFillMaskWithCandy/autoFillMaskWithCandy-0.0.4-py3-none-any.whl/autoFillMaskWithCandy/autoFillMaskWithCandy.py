import torch
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForMaskedLM

# function to set you model from hugging face as the model and tokenizer
def setTokenModel(model_name):
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)

# function to automatically mask differing words
def mask_differing_words(input_sentences):
    # Tokenize the input sentences
    tokenized_sentences = [sentence.split() for sentence in input_sentences]

    # Find differing words
    differing_words = set()
    for i in range(len(tokenized_sentences[0])):
        for j in range(1, len(tokenized_sentences)):
            if tokenized_sentences[0][i] != tokenized_sentences[j][i]:
                differing_words.add((i, tokenized_sentences[0][i]))

    # Organize differing words by their index
    differing_words = sorted(list(differing_words), key=lambda x: x[0])

    # Mask differing words in each sentence
    masked_inputs = []
    for sentence_tokens in tokenized_sentences:
        masked_tokens = sentence_tokens.copy()
        for index, word in differing_words:
            masked_tokens[index] = "[MASK]"
        masked_inputs.append(" ".join(masked_tokens))

    # Create candidates list for each differing word
    candidates_list = [[] for _ in differing_words]
    for k, (index, word) in enumerate(differing_words):
        candidates = set()
        for sentence_tokens in tokenized_sentences:
            candidates.add(sentence_tokens[index])
        candidates_list[k] = list(candidates)

    unique_masked_inputs = list(set(masked_inputs))

    return unique_masked_inputs, candidates_list

# function to calculate the probability of a candidate
def get_candidate_probability(candidate_tokens, mask_index, tokenized_text):
    # replace the masked token with the candidate tokens
    tokenized_candidate = ["[CLS]"]
    for i in range(len(tokenized_text)):
        if i == mask_index:
            tokenized_candidate += candidate_tokens
        else:
            tokenized_candidate.append(tokenized_text[i])

    # convert tokenized sentence to input IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokenized_candidate)

    # convert input IDs to tensors
    input_tensor = torch.tensor([input_ids])

    # get the logits from the model
    with torch.no_grad():
        logits = model(input_tensor).logits[0]

    # calculate the probability of the candidate word
    probs = softmax(logits, dim=-1)
    probs = probs[range(len(input_ids)), input_ids]
    prob = torch.prod(probs)

    return prob.item()

#funtion to show the masked input and provide the scores 
def show_mask_fill(input_sentences):
    unique_masked_inputs, candidates_list = mask_differing_words(input_sentences)

    # tokenize the input sentence
    tokenized_text = tokenizer.tokenize(unique_masked_inputs[0])
    mask_token_indices = [i for i, token in enumerate(tokenized_text) if token == "[MASK]"]

    print(f"Masked Input: {unique_masked_inputs[0]}\n")

    # evaluating the probability of each candidate word for each mask
    for mask_index, candidates in zip(mask_token_indices, candidates_list):
        for candidate in candidates:
            candidate_tokens = tokenizer.tokenize(candidate)
            candidate_probability = get_candidate_probability(candidate_tokens, mask_index,tokenized_text)
            print(f"Mask {mask_index + 1}, {candidate:<20} {candidate_probability}")

def mask_fill_replaced(input_sentences):
    unique_masked_inputs, candidates_list = mask_differing_words(input_sentences)

    for input_sentence in unique_masked_inputs:
        # Tokenize the input sentence
        tokenized_text = tokenizer.tokenize(input_sentence)
        # Find indices of masked tokens
        mask_token_indices = [i for i, token in enumerate(tokenized_text) if token == "[MASK]"]

    # Create a copy of the original tokenized text
    replaced_text = tokenized_text.copy()

    # Evaluate the probability of each candidate word for each mask
    for mask_index, candidates in zip(mask_token_indices, candidates_list):
        # Find the candidate with the highest probability
        best_candidate = max(candidates, key=lambda candidate: get_candidate_probability(tokenizer.tokenize(candidate), mask_index, tokenized_text))
        # Replace the mask with the best candidate in the copied text
        replaced_text[mask_index] = best_candidate

    # Join tokens to form complete words
    replaced_sentence = tokenizer.convert_tokens_to_string(replaced_text)

    #print(f"Original Sentence: {input_sentence}")

    # Print the replaced sentence
    #print(f"{replaced_sentence}")

    return replaced_sentence

'''
input_sentences = [
    "Pasensya heto lng ako, bobo sa pagaral",
    "Pasensya hito lng ako, bobo sa pagaral",
    "Pasensya heto lng ako, bubo sa pagaral",
    "Pasensya hito lng ako, bubo sa pagaral"
]
#modelInput=("GKLMIP/bert-tagalog-base-uncased")
#modelInput=("GKLMIP/electra-tagalog-base-uncased")
modelInput=("bert-base-uncased")
setTokenModel(modelInput)
show_mask_fill(input_sentences)
print(f"\n{mask_fill_replaced(input_sentences)}")

'''


