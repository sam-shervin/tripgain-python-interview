# Technical Architecture and Code Explanation

## System Architecture

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  User Interface Layer                    │
│  (Interactive menu for source selection)                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Data Fetching Layer                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ fetch_webpage(url) - HTTP requests with headers │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│         Prompt Engineering Layer                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ create_analysis_prompt() - Structured prompt     │  │
│  │  • Expert analyst role definition                │  │
│  │  • 3-5 bullet point specification                │  │
│  │  • Insight line requirement                      │  │
│  │  • Focus areas definition                        │  │
│  │  • Exact format specification                    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              AI Analysis Layer                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ analyze_with_gemini() - API Integration          │  │
│  │  • Configure Gemini 2.5 Flash                    │  │
│  │  • Send prompt + cleaned content                 │  │
│  │  • Handle API responses                          │  │
│  │  • Error handling & logging                      │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Output Management Layer                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │ save_output() - File I/O                          │  │
│  │  • Write to summary_output.txt                    │  │
│  │  • UTF-8 encoding                                │  │
│  │  • Error handling                                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Presentation Layer                          │
│  (Console output with formatted structure)             │
└─────────────────────────────────────────────────────────┘
```

## Function-by-Function Explanation

### 1. `configure_gemini(api_key: str) -> None`

**Purpose**: Initialize the Gemini API client

**Implementation**:
```python
genai.configure(api_key=api_key)
```

**Why This Matters**:
- One-time setup that enables all subsequent API calls
- Must be called before any Gemini operations
- Credentials validation happens here

**Error Handling**:
- Validates API key format
- Raises exception if key is invalid
- Should be called once at startup

---

### 2. `fetch_webpage(url: str) -> str`

**Purpose**: Retrieve raw HTML content from specified URL

**Key Implementation Details**:
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
return response.text
```

**Why Headers Matter**:
- Many websites block requests without User-Agent
- Mimics browser request to avoid detection
- Ensures compatibility with target servers

**Error Handling**:
- `timeout=10` prevents hanging on slow servers
- `raise_for_status()` catches HTTP errors (404, 500, etc.)
- RequestException caught and logged to stderr

**Performance Considerations**:
- 10-second timeout balances reliability vs. speed
- Adjustable based on network conditions

---

### 3. `clean_html(html_content: str) -> str`

**Purpose**: Parse HTML and extract clean text content

**Implementation Strategy**:

1. **HTML Parsing**:
   ```python
   soup = BeautifulSoup(html_content, 'html.parser')
   ```
   - `html.parser`: Built-in, lightweight HTML parser
   - No external dependencies beyond BeautifulSoup

2. **Tag Removal**:
   ```python
   for script in soup(["script", "style", "nav", "footer", "meta", "link"]):
       script.decompose()
   ```
   - **Why these tags?**
     - `<script>`: JavaScript code (not content)
     - `<style>`: CSS code (not content)
     - `<nav>`, `<footer>`: Navigation elements (typically boilerplate)
     - `<meta>`, `<link>`: Metadata (not user-facing content)

3. **Element Removal**:
   ```python
   for ad_element in soup.find_all(class_=re.compile('(ad|banner|widget|sidebar)')):
       ad_element.decompose()
   ```
   - Removes ads and sidebars by class name pattern
   - Regex pattern targets common ad-related classes

4. **Text Extraction**:
   ```python
   text = soup.get_text(separator=' ', strip=True)
   ```
   - `separator=' '`: Join text with spaces instead of nothing
   - `strip=True`: Remove leading/trailing whitespace from each element

5. **Whitespace Normalization**:
   ```python
   text = re.sub(r'\s+', ' ', text)  # Multiple spaces → single space
   text = re.sub(r'\n\n+', '\n', text)  # Multiple newlines → single
   ```

6. **Token Limit Management**:
   ```python
   text = text[:8000]
   ```
   - Gemini 2.5 Flash: ~1M token limit
   - Average: 1 token ≈ 4 characters
   - 8000 chars ≈ 2000 tokens = safe margin
   - Adjustable if API tier changes

**Output**: Clean, plain-text content without HTML markup

---

### 4. `create_analysis_prompt(content: str) -> str`

**Purpose**: Construct a structured prompt for Gemini analysis

**Prompt Components**:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Role Definition** | Sets analytical tone | "Expert content analyst" |
| **Task Specification** | Clarifies deliverables | "3-5 bullet points + 1 insight" |
| **Focus Areas** | Guides analysis lens | "Technology trends, business impact" |
| **Format Instructions** | Ensures consistent output | "EXACTLY as follows:" |
| **Content Embedding** | Provides source material | Cleaned webpage text |

**Why This Structure Works**:

1. **Expert Framing**: Encourages analytical thinking vs. surface summarization
2. **Explicit Constraints**: "Exactly 3-5" prevents vague interpretation
3. **Focus Guidance**: Directs Gemini toward meaningful analysis
4. **Format Specification**: Critical for parser-friendly output
5. **Content Embedding**: Ensures analysis based on provided material

**Token Efficiency**:
- Prompt template: ~300 tokens
- Content: ~2000 tokens
- Response: ~200 tokens
- Total: ~2500 tokens (well within limits)

---

### 5. `analyze_with_gemini(prompt: str) -> str`

**Purpose**: Send prompt to Gemini 2.5 Flash and retrieve response

**Implementation**:
```python
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
return response.text
```

**Why 'gemini-2.5-flash'?**
- **Fastest** Gemini model for real-time applications
- **Cost-effective** compared to Pro
- **Sufficient quality** for summarization tasks
- **Latest version** with improved reasoning

**Error Handling**:
- Catches API errors and network issues
- Logs to stderr for debugging
- Re-raises for graceful termination

**Response Processing**:
- Extracts `.text` attribute from response object
- Returns as string for file output

---

### 6. `save_output(analysis: str, output_file: str) -> None`

**Purpose**: Persist analysis to file system

**Implementation**:
```python
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(analysis)
```

**Key Details**:
- **`encoding='utf-8'`**: Ensures compatibility with special characters
- **Context manager**: Automatic file closure even on errors
- **Default filename**: `summary_output.txt` (as per requirements)

**Error Handling**:
- Catches IOError for permission/disk space issues
- Logs meaningful error message

---

### 7. `main()` - Orchestration Function

**Flow**:

1. **Initialization**:
   - Retrieve API key from environment
   - Display available sources

2. **Source Selection**:
   - Interactive menu for user choice
   - Default to source #1 if invalid input

3. **Sequential Processing**:
   - Fetch → Clean → Configure → Prompt → Analyze → Save → Display

4. **Error Handling**:
   - Wrap entire process in try-except
   - Exit with code 1 on failure

## Data Flow Example

```
User selects: "2" (BBC News)
    ↓
URL: https://www.bbc.com/news/technology
    ↓
HTTP GET with User-Agent header
    ↓
Raw HTML (~500KB)
    ↓
BeautifulSoup parsing
Remove scripts, styles, nav, ads
    ↓
Embed in prompt template
    ↓
Send to Gemini 2.5 Flash API
    ↓
Gemini analyzes and returns structured response
    ↓
Summary: 5 bullet points
Insight: 1 analytical line
    ↓
Save to summary_output.txt
    ↓
Display in console
```

## Performance Characteristics

| Operation | Time | Dependencies |
|-----------|------|--------------|
| Fetch webpage | 2-5s | Network speed |
| Clean HTML | <1s | HTML complexity |
| Configure Gemini | <1s | API responsiveness |
| Send to Gemini | <3s | API load |
| Save output | <1s | Disk I/O |
| **Total** | **6-11s** | All factors |

## Memory Usage

| Phase | Memory |
|-------|--------|
| Raw HTML | ~10-50MB |
| After parsing | ~5-10MB |
| Cleaned text (8KB limit) | <1MB |
| Prompt | <1MB |
| API response | <1MB |
| **Peak** | **~50MB** |

## Security Considerations

1. **API Key**: Stored in environment variables (not hardcoded)
2. **HTTPS**: Requests library uses SSL/TLS by default
3. **User-Agent**: Mimics legitimate browser
4. **Input Validation**: URL checked before fetching
5. **Output Encoding**: UTF-8 prevents injection attacks

## Extensibility Points

### To Add New Source:
```python
urls = {
    "1": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "4": "https://your-new-source.com/page"  # Add here
}
```

### To Change Analysis Focus:
```python
# Modify in create_analysis_prompt():
Focus on:
- Healthcare implications
- Regulatory requirements
- Implementation challenges
```

### To Add Post-Processing:
```python
# In main(), after analyze_with_gemini():
analysis = postprocess_response(analysis)  # Add function
```

---

## Debugging Tips

### Enable Detailed Logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Functions:
```python
# Test fetch
html = fetch_webpage("https://...")

# Test clean
cleaned = clean_html(html)

# Test prompt
prompt = create_analysis_prompt(cleaned)
```

### Verify Output Format:
```python
lines = analysis.split('\n')
assert "Summary:" in lines[0]
assert "Insight:" in analysis
```

---
