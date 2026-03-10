"""
Content Generator Module
Handles API calls to OpenAI and generates blog content
"""

from openai import OpenAI, APIError, RateLimitError, AuthenticationError
from config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS
import time
import streamlit as st

# Initialize OpenAI client with API key
client = OpenAI(api_key=OPENAI_API_KEY)


def create_prompt(topic, keywords, tone, length):
    """Creates a detailed prompt for the content generation API."""
    tone_instructions = {
        "Professional": "Use formal language, industry terminology, and a structured approach.",
        "Casual": "Write in a friendly, conversational tone. Use simple language and relatable examples.",
        "Technical": "Use technical jargon, detailed explanations, and assume reader has some domain knowledge."
    }
    
    tone_desc = tone_instructions.get(tone, tone_instructions["Professional"])
    
    prompt = (
        f"Write a comprehensive blog article about '{topic}'.\n\n"
        f"Requirements:\n"
        f"- Include these keywords naturally: {keywords}\n"
        f"- Target length: approximately {length} words\n"
        f"- Tone: {tone_desc}\n"
        f"- Start with an engaging introduction\n"
        f"- Include 2-3 main sections with subheadings\n"
        f"- End with a conclusion\n"
        f"- Make it informative, well-structured, and engaging\n"
        f"- Use proper markdown formatting with headers (#, ##, ###)\n\n"
        f"Article:"
    )
    
    return prompt


def generate_blog(topic, keywords, tone, length, max_retries=5):
    """
    Generates blog content using OpenAI's API (v1.0.0+).
    Includes improved rate limit handling.
    
    Args:
        topic (str): The main topic for the article
        keywords (str): Comma-separated keywords to include
        tone (str): Desired tone (Professional, Casual, Technical)
        length (int): Target word count
        max_retries (int): Number of retries if API fails
        
    Returns:
        str: Generated blog article content
        
    Raises:
        Exception: If API call fails after max retries
    """
    
    prompt = create_prompt(topic, keywords, tone, length)
    
    for attempt in range(max_retries):
        try:
            # New OpenAI API syntax (v1.0.0+)
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert blog writer and content creator. Your articles are well-researched, engaging, and properly formatted."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.7,
                top_p=0.9,
            )
            
            # Extract the generated content using new API response format
            generated_content = response.choices[0].message.content.strip()
            return generated_content
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Exponential backoff: 10, 20, 40, 80, 160 seconds
                wait_time = 10 * (2 ** attempt)
                st.warning(f"⏳ Rate limited. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                raise Exception(
                    "🚫 API rate limit exceeded after multiple retries.\n\n"
                    "**Solutions:**\n"
                    "1. Wait 15-30 minutes before trying again\n"
                    "2. Reduce article length (try 300 words instead of 500+)\n"
                    "3. Check your OpenAI plan: https://platform.openai.com/account/billing/overview\n"
                    "4. If on free trial, upgrade to paid plan\n"
                    "5. Check your rate limits: https://platform.openai.com/account/rate-limits"
                )
                
        except APIError as e:
            if attempt < max_retries - 1:
                wait_time = 5
                st.warning(f"⚠️ API error. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                print(f"API error: {str(e)}. Retrying...")
                time.sleep(wait_time)
            else:
                raise Exception(f"❌ API Error: {str(e)}")
                
        except AuthenticationError:
            raise Exception(
                "🔐 Authentication failed!\n\n"
                "**Check:**\n"
                "1. Your `.env` file has `OPENAI_API_KEY=sk-...`\n"
                "2. Your API key is valid at: https://platform.openai.com/account/api-keys\n"
                "3. Restart the app after updating `.env`"
            )
        
        except Exception as e:
            error_msg = str(e)
            if "rate" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = 20
                    st.warning(f"⏳ Rate limit detected. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception("Rate limit exceeded. Please wait before trying again.")
            else:
                raise Exception(f"❌ Error: {error_msg}")
    
    raise Exception("Failed to generate content after multiple attempts")


def generate_title(topic, keywords):
    """
    Generates an SEO-friendly title for the article.
    
    Args:
        topic (str): Main topic
        keywords (str): Keywords
        
    Returns:
        str: Generated title
    """
    prompt = (
        f"Create a compelling, SEO-friendly blog title for an article about '{topic}' "
        f"that includes the keywords: {keywords}. "
        f"Return only the title, nothing else."
    )
    
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert content marketer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Blog Post: {topic}"


def generate_meta_description(content, max_length=160):
    """
    Generates a meta description for SEO.
    
    Args:
        content (str): The article content
        max_length (int): Maximum length for meta description
        
    Returns:
        str: Meta description
    """
    sentences = content.split('.')
    meta = sentences[0] + '.'
    
    if len(meta) > max_length:
        meta = meta[:max_length-3] + "..."
    
    return meta