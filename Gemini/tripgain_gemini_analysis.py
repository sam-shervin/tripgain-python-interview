#!/usr/bin/env python3
"""
Gemini Integration and Intelligent Summarization Script
Fetches webpage content, cleans HTML, and uses Gemini 2.5 Flash for analysis.
"""

import os
import sys
import re
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configure Gemini API
def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)


def fetch_webpage_text(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        text = soup.get_text(separator=" ", strip=True)
        return text

    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}", file=sys.stderr)
        raise


def create_analysis_prompt(content: str) -> str:
    """
    Create a custom prompt for Gemini to analyze the webpage content.

    Args:
        content: The cleaned webpage content

    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an expert content analyst. Analyze the following webpage content and provide:

1. A summary in exactly 3-5 concise bullet points that capture the main topics and key information.
2. One short insight line (max 20 words) that explains the overall theme, trend, or significance of the content.

Focus on:
- Technology trends and innovations
- Business impact and applications
- Emerging challenges or opportunities
- Industry shifts and future directions

Format your response EXACTLY as follows (no additional text):
Summary:
• <first point>
• <second point>
• <third point>
• [optional fourth point]
• [optional fifth point]
and so on...
Insight:
<single sentence insight about the overall theme>

Webpage Content:
{content}"""

    return prompt


def analyze_with_gemini(prompt: str) -> str:
    """
    Send the prompt to Gemini 2.5 Flash and get the analysis.

    Args:
        prompt: The custom analysis prompt

    Returns:
        Gemini's response text
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error communicating with Gemini: {e}", file=sys.stderr)
        raise


def save_output(analysis: str, output_file: str = "summary_output.txt") -> None:
    """
    Save the analysis output to a file.

    Args:
        analysis: The analysis text from Gemini
        output_file: Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis)
        print(f"Output saved to {output_file}", file=sys.stderr)
    except IOError as e:
        print(f"Error saving output file: {e}", file=sys.stderr)
        raise


def main():
    """Main execution function."""

    # Configuration
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # URL selection (modify this to choose different sources)
    urls = {
        "1": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "2": "https://www.bbc.com/news/technology",
        "3": "https://edition.cnn.com/business"
    }

    print("Available sources:", file=sys.stderr)
    for key, url in urls.items():
        print(f"  {key}. {url}", file=sys.stderr)

    choice = input("Select source (1-3) [default: 1]: ").strip() or "1"

    if choice not in urls:
        print("Invalid choice. Using default source.", file=sys.stderr)
        choice = "1"

    selected_url = urls[choice]
    print(f"\nFetching content from: {selected_url}", file=sys.stderr)

    try:
        # Step 1: Fetch webpage
        print("Step 1: Fetching webpage...", file=sys.stderr)
        text_content = fetch_webpage_text(selected_url)

        # Step 3: Configure Gemini
        print("Step 3: Configuring Gemini API...", file=sys.stderr)
        configure_gemini(api_key)

        # Step 4: Create prompt
        print("Step 4: Creating analysis prompt...", file=sys.stderr)
        prompt = create_analysis_prompt(text_content)

        # Step 5: Get analysis from Gemini
        print("Step 5: Sending to Gemini 2.5 Flash for analysis...", file=sys.stderr)
        analysis = analyze_with_gemini(prompt)
        # save 'prompt' to a file for debugging
        with open("debug_prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        # Step 6: Save and display output
        print("Step 6: Saving output...", file=sys.stderr)
        save_output(analysis)

        # Print to console in required format
        print("\n" + "="*60)
        print(analysis)
        print("="*60)

    except Exception as e:
        print(f"Error during execution: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
