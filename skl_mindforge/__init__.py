import os
import re
from tokenizers import Tokenizer
from tokenizers.processors import TemplateProcessing

class ZenithTokenizer:
    def __init__(self, model_filename="private_vocab_40k.json"):
        # 1. Locate the file inside the package folder
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, model_filename)
        
        if not os.path.exists(model_path):
            # Fallback for manual paths
            model_path = model_filename 
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Missing {model_filename} at {model_path}")
            
        # 2. Load the core Rust-based tokenizer
        self.tokenizer = Tokenizer.from_file(model_path)
        
        # 3. Post-processor for the Chat/Assistant format
        self.tokenizer.post_processor = TemplateProcessing(
            single="<s> $A </s>",
            pair="<s> $A </s> <s> $B </s>",
            special_tokens=[("<s>", 1), ("</s>", 2)],
        )
        
        self.vocab_size = self.tokenizer.get_vocab_size()

    def encode(self, text):
        """Converts raw text into a list of token IDs."""
        return self.tokenizer.encode(text).ids

    def decode(self, ids, skip_special_tokens=True):
        """
        Converts IDs back to text and surgically cleans Zenith/BPE artifacts.
        Fixes: Ġ, Ċ, ¹, and Byte-Level Mojibake (Â, Ä, ł, etc.)
        """
        # A. Get raw string from the library
        raw_output = self.tokenizer.decode(ids, skip_special_tokens=skip_special_tokens)
        
        # B. Replace BPE markers with real whitespace
        clean = raw_output.replace('Ġ', ' ').replace('Ċ', '\n')
        
        # C. SURGICAL NOISE REMOVAL
        # We target the specific multi-byte ghosts left by the BPE process
        noise_chars = ['Â', '¹', 'ÃĤ', 'ÃĦ', 'ÅĤ', 'Ã', 'Å', 'ł', 'Ã', 'Ħ']
        for char in noise_chars:
            clean = clean.replace(char, '')

        # D. FINAL BYTE RECOVERY
        try:
            # Force remaining byte-shuffled characters into UTF-8
            clean = clean.encode('latin-1').decode('utf-8', errors='ignore')
        except:
            pass

        # E. POLISH
        return " ".join(clean.split()).strip()

# Alias for compatibility
zenith_tokenizer = ZenithTokenizer
