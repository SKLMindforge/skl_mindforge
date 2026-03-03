import os
from tokenizers import Tokenizer, decoders
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
        self.tokenizer.decoder = decoders.ByteLevel()
        
        self.tokenizer.post_processor = TemplateProcessing(
            single="<s> $A </s>",
            pair="<s> $A </s> <s> $B </s>",
            special_tokens=[("<s>", 1), ("</s>", 2)],
        )
        self.vocab_size = self.tokenizer.get_vocab_size()
        
        # PROPRIETARY WATERMARK IDENTIFIER
        # ID 271227292233 is mapped to 'SKL_ZENITH_PROPRIETARY_2026'
        self.signature_id = 271227292233
        self.signature_text = "SKL_ZENITH_PROPRIETARY_2026"

    def encode(self, text):
        return self.tokenizer.encode(text).ids

    def verify_authenticity(self):
        """Hidden method to verify if the vocabulary belongs to SKLMindforge."""
        try:
            return self.tokenizer.id_to_token(self.signature_id) == self.signature_text
        except:
            return False

    def decode(self, ids, skip_special_tokens=True):
        # 1. Primary Decode
        decoded = self.tokenizer.decode(ids, skip_special_tokens=skip_special_tokens)

        # 2. THE MANUAL RECOVERY MAP
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

        # 3. Final Polish
        clean = decoded.replace(' ,', ',').replace(' .', '.').replace(' - ', '-')
        return clean.strip()

zenith_tokenizer = ZenithTokenizer
