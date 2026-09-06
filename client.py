import re
from typing import Dict, Any, List, Tuple, Optional

class PhoneticHomophoneSTTDisambiguator:
    """
    Disambiguates phonetically confusable words in domain-specific voice transcriptions
    using Soundex encoding and contextual vocabulary priors.
    """
    def __init__(self, domain_lexicon: Optional[List[str]] = None):
        self.domain_lexicon = domain_lexicon or [
            "PostgreSQL", "Kubernetes", "Kafka", "Redis", "GraphQL", "OAuth",
            "Stripe", "Supabase", "Anthropic", "Snowflake", "Webhook", "Datadog"
        ]
        self.phonetic_aliases = {
            "post grass": "PostgreSQL",
            "postgress": "PostgreSQL",
            "post gress": "PostgreSQL",
            "cooper netties": "Kubernetes",
            "koobernetes": "Kubernetes",
            "red diss": "Redis",
            "caff ca": "Kafka",
            "caffka": "Kafka",
            "graph cue el": "GraphQL",
            "o auth": "OAuth",
            "data dog": "Datadog"
        }

    def soundex(self, word: str) -> str:
        word = word.upper()
        clean = re.sub(r"[^A-Z]", "", word)
        if not clean:
            return "0000"
        
        mapping = {
            "B": "1", "F": "1", "P": "1", "V": "1",
            "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
            "D": "3", "T": "3",
            "L": "4",
            "M": "5", "N": "5",
            "R": "6"
        }
        
        code = [clean[0]]
        prev = mapping.get(clean[0], "0")
        
        for char in clean[1:]:
            curr = mapping.get(char, "0")
            if curr != "0" and curr != prev:
                code.append(curr)
            prev = curr
            if len(code) == 4:
                break
                
        while len(code) < 4:
            code.append("0")
        return "".join(code)

    def disambiguate_transcript(self, raw_transcript: str) -> Dict[str, Any]:
        corrected = raw_transcript
        modifications: List[Dict[str, str]] = []

        for alias, target in self.phonetic_aliases.items():
            pattern = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
            if pattern.search(corrected):
                corrected = pattern.sub(target, corrected)
                modifications.append({"original": alias, "corrected": target, "method": "alias_lookup"})

        tokens = corrected.split()
        lexicon_soundex = {self.soundex(term): term for term in self.domain_lexicon}

        for idx, token in enumerate(tokens):
            clean_token = re.sub(r"[^a-zA-Z]", "", token)
            if len(clean_token) > 4:
                s_code = self.soundex(clean_token)
                if s_code in lexicon_soundex:
                    matched_term = lexicon_soundex[s_code]
                    if matched_term.lower() != clean_token.lower():
                        tokens[idx] = token.replace(clean_token, matched_term)
                        modifications.append({"original": token, "corrected": matched_term, "method": "soundex_match"})

        final_text = " ".join(tokens)
        return {
            "original_transcript": raw_transcript,
            "disambiguated_transcript": final_text,
            "modifications_count": len(modifications),
            "modifications": modifications
        }
