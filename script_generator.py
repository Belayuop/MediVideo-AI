from openai import OpenAI
import json

def generate_structured_script(raw_text, api_key):
    client = OpenAI(api_key=api_key)
    
    system_prompt = (
        "You are an expert Medical Video Producer. Your task is to take medical "
        "raw text and convert it into a structured video script. "
        "Keep it professional, educational, and concise."
    )
    
    user_prompt = f"""
    Convert the following medical text into a series of short narration paragraphs.
    Format the output as a JSON list of strings, where each string is a 20-30 second narration.
    Text: {raw_text[:8000]}
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    # Expecting: {"scenes": ["Narration 1", "Narration 2", ...]}
    script_data = json.loads(response.choices[0].message.content)
    return script_data.get("scenes", [raw_text[:200]])
