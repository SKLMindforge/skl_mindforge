import os
from tokenizers import Tokenizer, decoders, pre_tokenizers
from tokenizers.processors import TemplateProcessing

class ZenithTokenizer:
    def __init__(self, model_filename="private_vocab_40k.json"):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, model_filename)
        
        if not os.path.exists(model_path):
            model_path = model_filename 
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Missing {model_filename}")
            
        # 1. Load the core engine
        self.tokenizer = Tokenizer.from_file(model_path)
        
        # 2. THE KILL SWITCH: Disable the Normalizer
        # This is the most important line. It stops the .json from deleting your tabs.
        self.tokenizer.normalizer = None 
        
        # 3. THE RECOVERY: Force Byte-Level Mapping
        # We use a Sequence to catch the Tab specifically and treat it as a byte.
        self.tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(
            add_prefix_space=False,
            use_regex=True
        )
        
        # 4. THE DECODER: 1:1 Parity
        self.tokenizer.decoder = decoders.ByteLevel(
            add_prefix_space=False, 
            trim_offsets=False
        )
        
        # 5. POST-PROCESSOR
        self.tokenizer.post_processor = TemplateProcessing(
            single="<s> $A </s>",
            pair="<s> $A </s> <s> $B </s>",
            special_tokens=[("<s>", 0), ("</s>", 1)],
        )
        self.vocab_size = self.tokenizer.get_vocab_size()
        
        # Watermark Data
        self.signature_id = 271227292
        self.signature_text = "SKL_ZENITH_PROPRIETARY_2026"

    def encode(self, text):
        if not text: return []
        # Encode WITHOUT special tokens for the forensics test
        return self.tokenizer.encode(str(text), add_special_tokens=False).ids

    def decode(self, ids, skip_special_tokens=True):
        decoded = self.tokenizer.decode(ids, skip_special_tokens=skip_special_tokens)

        # 6. STEM RECOVERY MAP (The Science Armor)
        manual_fixes = {
            "âĦı": "ℏ", "âĪĤ": "∂", "âĪĩ": "∇", "Î¨": "Ψ", "Î¦": "Φ", "âĪ®": "∮", 
            "âīĪ": "≈", "ÃĹ": "×", "âģ»": "⁻", "âĤĢ": "₀", "ÏĢ": "π", "âĪĢ": "∀", 
            "âĪĪ": "∈", "âĦĿ": "ℝ", "âĪĥ": "∃", "âī¡": "≡", "âĪŀ": "∞", "âĨĴ": "→",
            "Â²": "²", "Â³": "³", "âĪĨ": "∆", "âĪ´": "∝", "âĪ±": "±", "âĪ∓": "∓",
            "âīł": "≠", "âīħ": "≅", "âī¤": "≤", "âī¥": "≥", "âīŀ": "≪", "âīģ": "≫",
            "âĪ┤": "∴", "âĪµ": "∵", "âĪĦ": "∄", "âĪ¬": "¬", "âĪ§": "∧", "âĪ¨": "∨",
            "âĬķ": "⊕", "âĬĹ": "⊗", "âĬĻ": "⊙", "âĬĺ": "⊘", "âĬĽ": "⊛", "âĬŀ": "⊞",
            "âĬŁ": "⊟"
        }

        for mojibake, symbol in manual_fixes.items():
            decoded = decoded.replace(mojibake, symbol)

        return decoded

    def verify_authenticity(self):
        try:
            return self.signature_text in self.decode([self.signature_id])
        except:
            return False
