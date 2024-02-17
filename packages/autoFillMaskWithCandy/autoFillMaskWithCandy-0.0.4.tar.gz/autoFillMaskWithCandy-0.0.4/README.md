# autoFillMaskWithCandy

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Elatot (c) 2024

# PyTorch and Transformers

This Python package provides advanced text processing functionalities utilizing PyTorch and Hugging Face's Transformers library. It includes capabilities for setting up a tokenizer and model from Hugging Face, automatically masking differing words in sentences, calculating the probability of candidate words, and more.

# Features

- Initialize tokenizer and model from Hugging Face's Transformer library.
- Automatically mask differing words in a set of input sentences.
- Calculate the probability of a candidate word.
- Show masked inputs and provide scores for candidate words.
- Replace masked words with the most probable candidates.

# Limitations

- May not be compatible with model using <mask> inference key like roBerta LLM. This algorithm uses [CLS] and [SEP] which are compatible with Bert and electra.

# Installation
- To use this package, you need to have Python installed on your system, along with PyTorch and the Transformers library. If you haven't installed these dependencies yet, you can do so using pip:

```bash
pip install torch transformers
pip install autoFillMaskWithCandy==0.0.4
```

# Examples of Usage

```python
from autoFillMaskWithCandy import setTokenModel, show_mask_fill, mask_fill_replaced

# Set the model for tokenizer
model_name = "Your-Model-Name-Here"
setTokenModel(model_name)

# Example sentences
input_sentences = [
    "Pasensya heto lng ako, bobo sa pagaral",
    "Pasensya hito lng ako, bobo sa pagaral",
    "Pasensya heto lng ako, bubo sa pagaral",
    "Pasensya hito lng ako, bubo sa pagaral"
]

# Show masked input and scores for candidate words
show_mask_fill(input_sentences)

# Print the sentence with masked words replaced
print(mask_fill_replaced(input_sentences))

```
- Replace "Your-Model-Name-Here" with the model name you want to use from Hugging Face.


