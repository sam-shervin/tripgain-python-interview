# Gemini Integration Setup and Usage Guide

## Overview
This solution provides a Python script that integrates with Google Gemini 2.5 Flash API to automatically fetch, clean, and analyze webpage content with intelligent summarization.

## Prerequisites

### Required Libraries
```bash
pip install google-generativeai requests beautifulsoup4
```

### API Key Setup
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Set the environment variable:
   - **Linux/macOS**: `export GEMINI_API_KEY="your-api-key-here"`
   - **Windows (PowerShell)**: `$env:GEMINI_API_KEY="your-api-key-here"`
   - **Windows (CMD)**: `set GEMINI_API_KEY=your-api-key-here`

## How the Script Works

### Architecture Flow
1. **Fetch** → Retrieve raw HTML from the selected webpage
2. **Clean** → Parse and remove scripts, navigation, ads, and irrelevant content
3. **Prompt Engineering** → Create a custom analysis prompt with specific instructions
4. **Analyze** → Send cleaned content to Gemini 2.5 Flash
5. **Output** → Format and save results to `summary_output.txt`

### Key Components

#### 1. `fetch_webpage(url: str) -> str`
- Uses `requests` library with proper headers
- Handles timeout and error cases
- Returns raw HTML content

#### 2. `clean_html(html_content: str) -> str`
- Uses BeautifulSoup to parse HTML
- Removes: scripts, styles, navigation bars, footers, ads
- Cleans whitespace and regex patterns
- Limits output to 8000 characters (respects Gemini token limits)

#### 3. `create_analysis_prompt(content: str) -> str`
- Designs a creative, structured prompt
- Specifies:
  - Exact output format (3-5 bullet points + 1 insight line)
  - Focus areas (technology, business, trends)
  - Tone and structure requirements
- Embeds the cleaned content

#### 4. `analyze_with_gemini(prompt: str) -> str`
- Uses Gemini 2.5 Flash model
- Handles API communication and errors
- Returns formatted response

#### 5. `save_output(analysis: str, output_file: str)`
- Writes results to `summary_output.txt`
- Preserves formatting with UTF-8 encoding

## Usage

### Basic Execution
```bash
python tripgain_gemini_analysis.py
```

### Interactive Selection
When prompted, choose a source:
- **1** → Wikipedia: Artificial Intelligence
- **2** → BBC News: Technology
- **3** → CNN Business

### Example Output

```
============================================================
Summary:
• Artificial Intelligence is transforming multiple industries including healthcare and finance
• Machine learning models are becoming more accessible through cloud platforms
• Ethical concerns about AI bias and transparency are increasing
• Organizations are investing heavily in responsible AI practices
Insight:
AI adoption is shifting from novelty to necessity, with governance and ethics becoming central.
============================================================
```

## Prompt Design Strategy

The custom prompt is designed to:
1. **Set context**: "You are an expert content analyst"
2. **Specify output**: "Exactly 3-5 bullet points + 1 insight line"
3. **Guide focus**: "Technology trends, business impact, emerging challenges"
4. **Ensure format**: Strict formatting instructions to avoid parsing issues
5. **Embed content**: Clean webpage content provided for analysis

This approach ensures Gemini produces structured, insightful output rather than generic summaries.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not set` | Ensure environment variable is properly exported |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Connection timeout` | Check internet connection; increase timeout in code |
| `Gemini API error` | Verify API key is valid and has proper quota |
| `Empty output` | Try a different webpage; some sites may be blocked |

### Debug Mode
Add logging to track execution:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Output Structure

### File: `summary_output.txt`
```
Summary:
• Point 1
• Point 2
• Point 3
• Point 4
• Point 5
Insight:
Single-line insight explaining overall theme
```

## Advanced Customization

### Change Analysis Focus
Modify `create_analysis_prompt()` to focus on:
- **Ethical implications**: "Focus on ethical concerns and governance"
- **Business impact**: "Focus on market opportunities and revenue implications"
- **Technology depth**: "Focus on specific technologies and their innovations"

### Change Source URLs
Edit the `urls` dictionary in `main()`:
```python
urls = {
    "1": "https://your-custom-url.com",
    "2": "https://another-url.com"
}
```

### Adjust Cleaning Parameters
- Modify regex patterns in `clean_html()` for different content types
- Adjust 8000 character limit for different token constraints
- Add more tag removals if needed

## File Structure
```
project/
├── tripgain_gemini_analysis.py    # Main script
├── summary_output.txt             # Generated output (created after run)
└── setup_guide.md                 # This file
```

## Notes
- The script respects Gemini API rate limits
- Cleaned content is limited to 8000 characters to avoid token overages
- Output format is precisely validated before saving
- All errors are logged to stderr, output to stdout
