# modules/keyword_extractor.py
from __future__ import annotations

import json
import re
from typing import List

from openai import OpenAI
from open_ai_api_creds import OpenAICreds


class KeywordExtractor:
    def __init__(self, model: str = "gpt-4o-mini", context: str = ""):
        """
        Initialize keyword extractor with OpenAI API key and optional predefined context.
        """
        creds = OpenAICreds()
        api_key = creds.get_open_api_key()
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError(
                "OpenAI API key not set. Please update open_ai_api_creds.json with a valid key."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.context = context.strip()

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract a list of keywords from the given text with optional predefined context.
        Returns a Python list of strings.
        """
        if not text.strip():
            return []

        # Build prompt
        sections = []
        if self.context:
            sections.append(f"Context:\n{self.context}")
        sections.append(f"Text to analyze:\n{text}")
        sections.append(
            "Task: Extract the main keywords (single words or short phrases). "
            "Return ONLY a JSON array of strings, e.g. [\"keyword one\", \"keyword two\"]. "
            "Do not include any other text."
        )
        prompt = "\n\n".join(sections)

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=200,
            )
            raw = (resp.choices[0].message.content or "").strip()

            # First try strict JSON parse
            try:
                data = json.loads(raw)
                if isinstance(data, list) and all(isinstance(x, str) for x in data):
                    return [x.strip() for x in data if x.strip()]
            except json.JSONDecodeError:
                pass

            # Fallback: try to extract a JSON array if the model wrapped it in text
            match = re.search(r"\[.*\]", raw, flags=re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group(0))
                    if isinstance(data, list) and all(isinstance(x, str) for x in data):
                        return [x.strip() for x in data if x.strip()]
                except json.JSONDecodeError:
                    pass

            # Last resort: split on commas/newlines
            return [kw.strip() for kw in re.split(r"[,\\n]+", raw) if kw.strip()]

        except Exception as e:
            print(f"[KeywordExtractor] Error: {e}")
            return []


if __name__ == "__main__":
    # Example usage
    context_text = "You are an assistant that extracts concise, relevant keywords for indexing social media posts about technology."
    text_block = """
    Just tested Loveable's latest AI design feature — it’s a total game-changer. 
    The tool takes plain text prompts and instantly generates high-quality app mockups. 
    I started with something super simple like 'a mobile app for ordering coffee' and 
    within seconds it produced multiple polished designs that looked ready for presentation.  

    What’s wild is how customizable it is. You can refine layouts, switch color palettes, 
    or even add UX components just by updating the text instructions. No need to drag and 
    drop endlessly — it feels like having a design partner who actually understands product vision.  

    For startups and indie developers this is going to save a *ton* of time. 
    Prototyping usually takes hours or days, but with Loveable it’s down to minutes. 
    Imagine validating product ideas on the same day you think of them. That’s huge.  

    Also worth mentioning: the export options are solid. You can pull the mockups directly 
    into Figma or share a live preview link with teammates. It really lowers the barrier 
    for non-designers to communicate their ideas effectively.  

    Overall, I’m seriously impressed. Loveable might just become my go-to tool for rapid design. 
    Curious to see how they evolve this tech further. #AI #Loveable #UX #Prototyping #Startups
    """

    extractor = KeywordExtractor(context=context_text)
    keywords = extractor.extract_keywords(text_block)
    print("\n--- KEYWORDS ---\n", keywords)

