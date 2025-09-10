# modules/summarizer.py
from openai import OpenAI
from open_ai_api_creds import OpenAICreds


class Summarizer:
    def __init__(self, model: str = "gpt-4o-mini", context: str = ""):
        """
        Initialize summarizer with OpenAI API key and optional predefined context.
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

    def summarize(self, text: str) -> str:
        """
        Summarize the given text with optional predefined context.
        """
        if not text.strip():
            return "[Summarizer] No text provided to summarize."

        # Combine context and text
        parts = []
        if self.context:
            parts.append(f"Context:\n{self.context}")
        parts.append(f"Text to summarize:\n{text}")
        parts.append("Summarize the text above clearly and concisely.")
        prompt = "\n\n".join(parts)

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            return f"[Summarizer] Error: {e}"


if __name__ == "__main__":
    # Example usage
    context_text = "You are an assistant that creates concise summaries of social media posts about technology."
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

    summarizer = Summarizer(context=context_text)
    summary = summarizer.summarize(text_block)
    print("\n--- SUMMARY ---\n", summary)
