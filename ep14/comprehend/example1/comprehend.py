import boto3
import json

client = boto3.client('comprehend', region_name='us-east-1')
with open('game_pr.txt') as raw_text:
    lines = raw_text.readlines()

def detect_entities(str):
    return client.detect_entities(
        Text=str,
        LanguageCode='en'
    )

def detect_key_phrases(str):
    return client.detect_key_phrases(
    Text=str,
    LanguageCode='en'
)

def detect_sentiment(str):
    return client.detect_sentiment(
        Text=str,
        LanguageCode='en'
    )
response = detect_entities("\n".join(lines))
# response = detect_key_phrases("\n".join(lines))

print(json.dumps(response, indent=3))

# for line in lines:
#     print("----")
#     print(f'line : {line}')
#     response = detect_sentiment("\n".join(lines))
#     print(json.dumps(response, indent=3))


