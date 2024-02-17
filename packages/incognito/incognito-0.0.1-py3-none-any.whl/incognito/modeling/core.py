from typing import Union, List

from transformers import TokenClassificationPipeline, AutoModelForTokenClassification, AutoTokenizer


class PrivateTokenizer(AutoTokenizer):

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
        auto_tokenizer = super().from_pretrained(pretrained_model_name_or_path, *model_args, **kwargs)
        cls.incognito = Incognito()

        tokenizer_encode_plus = auto_tokenizer.encode_plus
        tokenizer_batch_encode_plus = auto_tokenizer.batch_encode_plus

        # Patch the encode_plus method
        def patched_encode_plus(text, *args, **kwargs):
            return tokenizer_encode_plus(
                text=cls.incognito(text), *args, **kwargs
            )

        auto_tokenizer.encode_plus = patched_encode_plus

        def patched_batch_encode_plus(batch_text_or_text_pairs, *args, **kwargs):
            return tokenizer_batch_encode_plus(
                batch_text_or_text_pairs=cls.incognito(batch_text_or_text_pairs), *args, **kwargs
            )

        auto_tokenizer.batch_encode_plus = patched_batch_encode_plus

        return auto_tokenizer

    @classmethod
    def incognito(cls, inputs):
        raise NotImplementedError("Cannot use incognito method before calling from_pretrained.")


class Incognito:
    def __init__(self, name="[NAME]", location="[LOCATION]", organization="[ORGANIZATION]"):
        self.NAME = name
        self.LOCATION = location
        self.ORGANIZATION = organization

        self.ner = TokenClassificationPipeline(
            model=AutoModelForTokenClassification.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl"),
            tokenizer=AutoTokenizer.from_pretrained("Davlan/distilbert-base-multilingual-cased-ner-hrl"),
            aggregation_strategy="simple",
        )

    def __call__(self, input: Union[str, List[str]]):

        converted = False
        if isinstance(input, str):
            converted = True
            input = [input]

        input_entities = self.ner(input)

        for i, entities in enumerate(input_entities):
            entities = sorted(entities, key=lambda x: x['start'], reverse=True)

            for entity in entities:
                if entity['entity_group'] == 'ORG':
                    placeholder = self.ORGANIZATION
                elif entity['entity_group'] == 'PER':
                    placeholder = self.NAME
                elif entity['entity_group'] == 'LOC':
                    placeholder = self.LOCATION
                else:
                    continue
                input[i] = input[i][:entity['start']] + placeholder + input[i][entity['end']:]

        if converted:
            return input[0]
        return input
