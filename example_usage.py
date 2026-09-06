import json
from client import PhoneticHomophoneSTTDisambiguator

def main():
    disambiguator = PhoneticHomophoneSTTDisambiguator()
    raw = "Deploy the microservice on cooper netties and connect it to postgress and caffka."
    result = disambiguator.disambiguate_transcript(raw)
    print("Phonetic Disambiguation Result:")
    print(json.dumps(result, indent=2))
    assert "Kubernetes" in result["disambiguated_transcript"]
    assert "PostgreSQL" in result["disambiguated_transcript"]
    assert "Kafka" in result["disambiguated_transcript"]
    print("Phonetic homophone disambiguator verification: PASS")

if __name__ == "__main__":
    main()
