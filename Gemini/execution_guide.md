# Gemini Integration - Complete Execution Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set API Key
```bash
# Linux/macOS
export GEMINI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here
```

### Step 3: Run Script
```bash
python tripgain_gemini_analysis.py
```

---

## Detailed Execution Walkthrough

### Prerequisites Check
Before running, ensure you have:
- Python 3.8 or higher
- Active internet connection
- Valid Google Gemini API key
- All dependencies installed

### API Key Acquisition
1. Visit: https://aistudio.google.com/apikey
2. Click "Create API key"
3. Copy the generated key
4. Set as environment variable (see Step 2 above)

### Running the Script

#### Option A: Interactive Mode (Recommended)
```bash
python tripgain_gemini_analysis.py
```

You will be prompted to select a source:
```
Available sources:
  1. https://en.wikipedia.org/wiki/Artificial_intelligence
  2. https://www.bbc.com/news/technology
  3. https://edition.cnn.com/business

Select source (1-3) [default: 1]: 
```

#### Option B: Direct Execution
The script selects Wikipedia by default if no input is provided.

---

## Execution Flow Diagram

```
START
  ↓
Check API Key
  ↓
Select Webpage Source
  ↓
Fetch HTML Content
  ↓
Clean & Parse HTML
  ├─ Remove scripts/styles
  ├─ Remove navigation elements
  ├─ Extract text content
  └─ Limit to 8000 characters
  ↓
Create Analysis Prompt
  ├─ Set expert analyst role
  ├─ Specify 3-5 bullet points
  ├─ Request insight line
  └─ Embed cleaned content
  ↓
Send to Gemini 2.5 Flash API
  ↓
Receive Structured Response
  ├─ Summary section (5 bullets)
  └─ Insight section (1 line)
  ↓
Save to summary_output.txt
  ↓
Display in Console
  ↓
END
```

---

## Output Validation

### Expected Output Format
```
Summary:
• Point 1
• Point 2
• Point 3
• Point 4
• Point 5
Insight:
Single line insight about overall theme
```

### File Output
**File**: `summary_output.txt`
- Created in same directory as script
- UTF-8 encoded
- Contains exact output from Gemini
- Preserves all formatting

---

## Troubleshooting Guide

### Problem: "GEMINI_API_KEY not set"
**Cause**: Environment variable not properly configured
**Solution**:
```bash
# Verify it's set
echo $GEMINI_API_KEY  # Linux/macOS
echo %GEMINI_API_KEY%  # Windows CMD

# If empty, set it again
export GEMINI_API_KEY="your-key"
```

### Problem: "ModuleNotFoundError"
**Cause**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
# Or install individually
pip install google-generativeai requests beautifulsoup4
```

### Problem: "Connection timeout"
**Cause**: Network issue or slow connection
**Solution**:
```python
# Increase timeout in fetch_webpage function
response = requests.get(url, headers=headers, timeout=20)  # Changed from 10
```

### Problem: "Gemini API error" or "Invalid API key"
**Cause**: API key invalid or revoked
**Solution**:
1. Visit https://aistudio.google.com/apikey
2. Generate a new key
3. Update environment variable
4. Retry

### Problem: "Empty or incomplete output"
**Cause**: Some websites may block scraping
**Solution**:
- Try a different source (select 1, 2, or 3)
- Check if website has Terms of Service restrictions
- Verify your User-Agent header

### Problem: "Unicode decode error"
**Cause**: Encoding issue with webpage content
**Solution**:
```python
# Modify fetch_webpage function
response = requests.get(url, headers=headers, timeout=10)
response.encoding = 'utf-8'
```

### Problem: "Output file not created"
**Cause**: Permission issue or directory problem
**Solution**:
```bash
# Check write permissions
ls -la  # Linux/macOS
dir    # Windows

# Ensure you're in correct directory
pwd    # Linux/macOS
cd     # Windows
```

---

## Performance Optimization

### For Faster Execution
1. **Reduce content size**: Modify character limit in `clean_html()`
   ```python
   text = text[:5000]  # Reduced from 8000
   ```

2. **Use smaller sources**: BBC and CNN usually have smaller content than Wikipedia

3. **Cache webpage content**: Store HTML locally for testing
   ```python
   with open('cached_content.html', 'r') as f:
       html_content = f.read()
   ```

### For Better Output Quality
1. **Increase character limit** (if API allows):
   ```python
   text = text[:10000]  # Increased from 8000
   ```

2. **Customize prompt focus**: Modify `create_analysis_prompt()` for specific domains

3. **Iterate on insights**: Run multiple times with different prompts

---

## Script Customization Examples

### Example 1: Always Use Specific Source
```python
# In main() function, replace:
# choice = input("Select source...")
# With:
choice = "2"  # Always use BBC News
```

### Example 2: Save Multiple Analyses
```python
# In main() function, after save_output():
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_output(analysis, f"summary_output_{timestamp}.txt")
```

### Example 3: Custom Focus Area
```python
# Modify create_analysis_prompt() focus section:
Focus on:
- Healthcare applications and diagnostics
- Regulatory compliance requirements
- Implementation challenges
- Patient data privacy considerations
```

---

## File Structure After Execution

```
project_directory/
├── tripgain_gemini_analysis.py    # Main executable
├── requirements.txt                # Dependencies
├── quickstart.sh                   # Setup script
├── summary_output.txt              # Generated output
├── setup_guide.md                  # Setup documentation
├── prompt_design.md                # Prompt reasoning
└── execution_guide.md              # This file
```

---

## Testing the Setup

### Minimal Test Script
```python
import os
import google.generativeai as genai

# Test 1: Check API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key set: {bool(api_key)}")

# Test 2: Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✓ Gemini configured successfully")
except Exception as e:
    print(f"✗ Configuration error: {e}")

# Test 3: Make simple request
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Say 'Hello from Gemini'")
    print(f"✓ API response: {response.text}")
except Exception as e:
    print(f"✗ API error: {e}")
```

Save as `test_setup.py` and run: `python test_setup.py`

---

## Support Resources

- **Google Gemini Docs**: https://ai.google.dev/docs
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/
- **Python Requests**: https://requests.readthedocs.io/

---

## Success Indicators

After successful execution, you should see:
- ✓ Script completes without errors
- ✓ `summary_output.txt` file created
- ✓ Output contains 5 bullet points + 1 insight
- ✓ Content matches source webpage theme
- ✓ Insight line is analytical, not just summary
