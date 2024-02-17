from transformers import AutoTokenizer

from incognito import Incognito, PrivateTokenizer


def test_incognito():
    model = Incognito()

    input = "My name is John Doe, I live in New York and I work at Starbucks."
    label = f"My name is {model.NAME}, I live in {model.LOCATION} and I work at {model.ORGANIZATION}."
    output = model(input)

    assert output == label

    batch_input = [input, input]
    batch_label = [label, label]
    batch_output = model(batch_input)

    assert batch_output == batch_label


def test_private_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("hf-internal-testing/tiny-random-bert")
    private_tokenizer = PrivateTokenizer.from_pretrained("hf-internal-testing/tiny-random-bert")

    input = "My name is John Doe, I live in New York and I work at Starbucks."
    label = f"My name is [NAME], I live in [LOCATION] and I work at [ORGANIZATION]."

    input_tokens = tokenizer.decode(tokenizer(input).input_ids)
    label_tokens = tokenizer.decode(tokenizer(label).input_ids)
    private_input_tokens = private_tokenizer.decode(private_tokenizer(input).input_ids)

    assert label_tokens == private_input_tokens
    assert input_tokens != label_tokens
    assert input_tokens != private_input_tokens

    batch_input = [input, input]
    batch_label = [label, label]

    batch_input_tokens = tokenizer.batch_decode(tokenizer(batch_input).input_ids)
    batch_label_tokens = tokenizer.batch_decode(tokenizer(batch_label).input_ids)
    batch_private_input_tokens = private_tokenizer.batch_decode(private_tokenizer(batch_input).input_ids)

    assert batch_label_tokens == batch_private_input_tokens
    assert batch_input_tokens != batch_label_tokens
    assert batch_input_tokens != batch_private_input_tokens
