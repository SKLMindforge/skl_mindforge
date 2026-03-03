import os
import re
import unicodedata
from tokenizers import Tokenizer
from tokenizers.processors import TemplateProcessing

class ZenithTokenizer:
    def __init__(self, model_filename="private_vocab_40k.json"):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, model_filename)
        
        if not os.path.exists(model_path):
            model_path = model_filename 
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Missing {model_filename}")
            
        self.tokenizer = Tokenizer.from_file(model_path)
        self.tokenizer.post_processor = TemplateProcessing(
            single="<s> $A </s>",
            pair="<s> $A </s> <s> $B </s>",
            special_tokens=[("<s>", 1), ("</s>", 2)],
        )
        self.vocab_size = self.tokenizer.get_vocab_size()

    def encode(self, text):
        return self.tokenizer.encode(text).ids

    def decode(self, ids, skip_special_tokens=True):
        """
        VERSION 0.1.5: Universal Math & Science Decoder.
        Uses Unicode Category Filtering to preserve math symbols while killing BPE junk.
        """
        # 1. Convert IDs to raw vocab tokens (no auto-spaces)
        tokens = [self.tokenizer.id_to_token(i) for i in ids]
        
        # 2. Filter out special tokens
        if skip_special_tokens:
            special = {"<s>", "</s>", "<pad>", "<unk>", "<mask()", "[CLS]", "[SEP]"}
            tokens = [t for t in tokens if t not in special]

        # 3. GLUE: Join without spaces
        raw_text = "".join(tokens)

        # 4. CONVERT BPE MARKERS
        clean = raw_text.replace('Ġ', ' ').replace('Ċ', '\n')
        
        # 5. TARGETED BPE GHOST REMOVAL
        # We kill the specific sequences that we know are artifacts
        junk_sequences = ['Â¹', 'ÃĤ', 'ÃĦ', 'ÅĤ', 'Ãł', 'Äł', '¹']
        for junk in junk_sequences:
            clean = clean.replace(junk, '')

        # 6. UNICODE CATEGORY FILTER (The Magic Step)
        # We keep ASCII, and any character that is a Letter, Number, Punctuation, or Math Symbol.
        # This preserves: ≈, ×, ±, ÷, √, ∞, ∫, and Greek letters (α, β, γ).
        def is_valid(char):
            if ord(char) < 128: return True  # Keep all standard ASCII
            cat = unicodedata.category(char)
            # Sm = Math Symbol, Sc = Currency, Sk = Modifier, So = Other Symbol
            # L = Letter (covers Greek), N = Number, P = Punctuation
            return cat.startswith(('S', 'L', 'N', 'P'))

        clean = "".join([c for c in clean if is_valid(c)])

        # 7. PUNCTUATION & MATH POLISH
        # Ensures math looks right: "c = 3" instead of "c=3" or "c  =  3"
        clean = clean.replace(' ,', ',').replace(' .', '.').replace(' ( ', ' (').replace(' )', ')')
        clean = clean.replace(' - ', '-') 
        
        # Final pass to collapse multi-spaces created by noise removal
        return " ".join(clean.split()).strip()

zenith_tokenizer = ZenithTokenizer
