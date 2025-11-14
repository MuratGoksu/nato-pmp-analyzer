# 🔧 NATO PMP Analyzer - Troubleshooting Guide

## 🎯 Purpose
This guide provides solutions to common problems and errors you may encounter when using the NATO PMP Analyzer.

---

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Startup Problems](#startup-problems)
3. [Upload Issues](#upload-issues)
4. [Chatbot Problems](#chatbot-problems)
5. [Dashboard & Visualization Issues](#dashboard--visualization-issues)
6. [Network Graph Problems](#network-graph-problems)
7. [Performance Issues](#performance-issues)
8. [API & Configuration Errors](#api--configuration-errors)
9. [Browser Compatibility](#browser-compatibility)
10. [Data & Session Issues](#data--session-issues)

---

## 🔨 Installation Issues

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Cause:** Dependencies not installed

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
```

---

### Error: "Python version not supported"

**Cause:** Python version < 3.10

**Solution:**
```bash
# Check Python version
python --version

# If < 3.10, install Python 3.10+
# Mac (Homebrew):
brew install python@3.10

# Ubuntu/Debian:
sudo apt install python3.10

# Create venv with specific version:
python3.10 -m venv venv
```

---

### Error: "pip: command not found"

**Cause:** pip not installed

**Solution:**
```bash
# Mac/Linux:
python3 -m ensurepip --upgrade

# Ubuntu/Debian:
sudo apt install python3-pip

# Verify:
pip --version
```

---

### Error: "Permission denied" during pip install

**Cause:** Insufficient permissions

**Solution:**
```bash
# Use virtual environment (recommended):
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# OR use --user flag (not recommended):
pip install --user -r requirements.txt
```

---

## 🚀 Startup Problems

### Error: "Address already in use"

**Cause:** Port 8501 is occupied

**Solution:**
```bash
# Option 1: Kill process on port 8501
lsof -ti:8501 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8501   # Windows (then kill PID)

# Option 2: Use different port
streamlit run app.py --server.port 8502

# Option 3: Find and close other Streamlit instances
ps aux | grep streamlit
kill [PID]
```

---

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'app.py'"

**Cause:** Wrong directory

**Solution:**
```bash
# Check current directory
pwd

# Navigate to correct directory
cd ~/Desktop/nato-pmp-analyzer

# Verify app.py exists
ls -l app.py

# Run from correct location
streamlit run app.py
```

---

### Error: "ModuleNotFoundError: No module named 'backend'"

**Cause:** Missing `backend/__init__.py` or PYTHONPATH issue

**Solution:**
```bash
# Check backend folder structure
ls -la backend/

# Ensure __init__.py exists
touch backend/__init__.py

# Run from project root directory
cd nato-pmp-analyzer
streamlit run app.py
```

---

### Application starts but shows blank page

**Cause:** Browser cache or JavaScript error

**Solution:**
1. **Hard refresh browser:**
   - Chrome/Firefox: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Safari: Cmd+Option+R

2. **Clear browser cache:**
   - Chrome: Settings → Privacy → Clear browsing data
   - Firefox: Settings → Privacy → Clear Data

3. **Try incognito/private mode**

4. **Check browser console for errors:**
   - F12 → Console tab

5. **Try different browser**

---

## 📤 Upload Issues

### Error: "Unsupported file format"

**Cause:** File type not supported

**Solution:**
- **Supported formats:** PDF (.pdf), Word (.docx, .doc)
- **Not supported:** Images (PNG, JPG), Text files (.txt), Excel (.xlsx)
- Convert unsupported formats to PDF/DOCX first

---

### Documents upload but processing fails

**Cause:** Corrupted file or scanned PDF

**Solution:**
1. **Check if file is scanned image:**
   - Open PDF in reader
   - Try to select text
   - If can't select text → it's a scanned image

2. **Use OCR to convert scanned PDFs:**
   - Adobe Acrobat (OCR feature)
   - Online tools: SmallPDF, PDF24
   - Desktop: Tesseract OCR

3. **Try different PDF:**
   - Export from original source
   - Re-save PDF with text layer
   - Check file isn't password-protected

---

### Upload hangs at "Processing..."

**Cause:** Large file or slow processing

**Solution:**
1. **Wait longer:**
   - Large files (>50 pages) can take 30+ seconds
   - Check terminal for progress logs

2. **Refresh and try again:**
   - Ctrl+R to refresh
   - Re-upload smaller batch

3. **Check file size:**
   - Very large files (>100MB) may timeout
   - Split into smaller documents

4. **Check terminal for errors:**
   - Look for Python exceptions
   - Check API key validity

---

### Error: "Failed to extract text from PDF"

**Cause:** PDF structure issue

**Solution:**
1. **Try re-saving PDF:**
   - Open in Adobe Reader
   - File → Save As → New filename

2. **Check PDF isn't encrypted:**
   - Some PDFs have copy protection
   - Remove protection first

3. **Use different PDF library (manual fix):**
   ```python
   # In backend/document_processor.py
   # Try alternative: pdfplumber instead of PyPDF2
   import pdfplumber
   ```

4. **Convert to DOCX:**
   - Use PDF to Word converter
   - Upload DOCX instead

---

### No metadata extracted

**Cause:** Document format doesn't match expected patterns

**Solution:**
1. **Check document contains:**
   - Project name in clear text
   - Budget mentioned as "€X million" or "M€"
   - Email addresses or names
   - Words "red", "amber", or "green" for status

2. **Improve extraction accuracy:**
   - Use standardized PMP templates
   - Ensure clear formatting
   - Include metadata in consistent format

3. **Manual verification:**
   - Expand document in upload page
   - Check what metadata was found
   - Adjust queries accordingly

---

## 💬 Chatbot Problems

### Error: "OPENAI_API_KEY not found!"

**Cause:** Missing or incorrect API key

**Solution:**
1. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

2. **Create .env if missing:**
   ```bash
   cp .env.example .env
   nano .env  # or use text editor
   ```

3. **Add API key:**
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```

4. **Verify no extra spaces:**
   - No spaces around `=`
   - No quotes around key
   - No trailing spaces

5. **Restart Streamlit:**
   - Ctrl+C to stop
   - `streamlit run app.py`

---

### Chatbot says "I don't have information..."

**Cause:** Documents not in RAG database or question not matched

**Solution:**
1. **Check RAG status in sidebar:**
   - Should show "🟢 RAG Active"
   - Should show "X chunks indexed"

2. **Re-upload documents:**
   - Clear browser (refresh)
   - Upload documents again
   - Wait for "RAG initialized" message

3. **Rephrase question:**
   - Be more specific
   - Use terms from your documents
   - Ask simpler question first

4. **Check source documents contain answer:**
   - Expand documents in upload page
   - Verify text is extracted correctly
   - Ensure information is actually in documents

---

### Chatbot very slow (>30 seconds)

**Cause:** API timeout or rate limiting

**Solution:**
1. **Check OpenAI API status:**
   - Visit: https://status.openai.com/
   - Check for outages

2. **Check API usage limits:**
   - Login to OpenAI dashboard
   - Check rate limits not exceeded
   - Verify account has credit

3. **Reduce document count:**
   - Fewer documents = faster queries
   - Remove unnecessary uploads

4. **Check internet connection:**
   - API requires internet
   - Test: `ping api.openai.com`

---

### Error: "Rate limit exceeded"

**Cause:** Too many API calls too quickly

**Solution:**
1. **Wait 60 seconds and retry**

2. **Reduce query frequency:**
   - Don't spam questions
   - Wait for responses to complete

3. **Upgrade OpenAI plan:**
   - Free tier: 3 requests/minute
   - Paid tier: Higher limits

4. **Check usage dashboard:**
   - https://platform.openai.com/usage
   - Monitor API calls

---

### Chatbot gives incorrect answers

**Cause:** AI hallucination or context limitation

**Solution:**
1. **Always check sources:**
   - Click "📚 Sources" button
   - Verify cited information
   - Cross-reference with original documents

2. **Rephrase question:**
   - Be more specific
   - Include context
   - Break complex questions into parts

3. **Treat as assistant, not oracle:**
   - AI can make mistakes
   - Use for research, not final decisions
   - Human verification required

4. **Report patterns:**
   - Note consistently wrong answers
   - Helps improve system

---

## 📊 Dashboard & Visualization Issues

### Dashboard shows "No documents processed"

**Cause:** No documents uploaded or session cleared

**Solution:**
1. **Upload documents:**
   - Go to Upload page
   - Add documents
   - Wait for processing

2. **Check sidebar:**
   - Should show processed documents
   - ✅ = successful processing

3. **Don't refresh browser:**
   - Refreshing clears session data
   - Need to re-upload documents

---

### Charts not displaying

**Cause:** Plotly rendering issue or browser compatibility

**Solution:**
1. **Refresh page:**
   - Ctrl+R or Cmd+R

2. **Check browser console:**
   - F12 → Console
   - Look for JavaScript errors

3. **Try different browser:**
   - Chrome recommended
   - Firefox also works well

4. **Disable browser extensions:**
   - Ad blockers may interfere
   - Privacy extensions may block scripts

5. **Update browser:**
   - Use latest version

---

### Status all showing GREEN when documents have issues

**Cause:** Status keywords not found in documents

**Solution:**
1. **Check documents contain status keywords:**
   - Words: "red", "amber", "green"
   - Case-insensitive matching

2. **Manually set status** (requires code change):
   ```python
   # In backend/document_processor.py
   # Modify _extract_status() to use different keywords
   ```

3. **Accept limitation:**
   - If documents don't mention status
   - All default to GREEN
   - Still provides other insights

---

### Export functionality not available

**Cause:** Feature not yet implemented in v0.4

**Solution:**
1. **Screenshot dashboards:**
   - Browser screenshot (Cmd+Shift+4 on Mac)
   - Or screenshot extensions

2. **Copy table data:**
   - Click and drag to select
   - Ctrl+C to copy
   - Paste into Excel

3. **Wait for future update:**
   - Export feature planned
   - See roadmap in README

4. **Manual export** (technical users):
   ```python
   # Access session_state programmatically
   # Export to CSV manually
   ```

---

## 🔗 Network Graph Problems

### Network graph shows "No relationships found"

**Cause:** Only one document or no common elements

**Solution:**
1. **Upload more documents:**
   - Need 2+ documents
   - More documents = more relationships

2. **Check documents have overlaps:**
   - Shared stakeholders (same emails)
   - Common technology keywords
   - Similar budget ranges
   - Same RAG status

3. **Adjust filters:**
   - Enable all relationship types in sidebar
   - Check all boxes

4. **Verify stakeholders extracted:**
   - Check upload page metadata
   - Ensure email addresses detected

---

### Network graph too cluttered

**Cause:** Many projects with many relationships

**Solution:**
1. **Use filters:**
   - Sidebar: uncheck relationship types
   - Focus on one type at a time

2. **Analyze subset:**
   - Upload only related projects
   - Create focused analysis

3. **Use zoom:**
   - Scroll to zoom in/out
   - Click and drag to pan

4. **Export screenshot:**
   - Focus on specific area
   - Screenshot for clarity

---

### Graph generation very slow

**Cause:** Complex network calculation

**Solution:**
1. **Expected for many projects:**
   - 10 projects: 5 seconds
   - 50 projects: 15+ seconds
   - Be patient

2. **Reduce document count:**
   - Analyze in batches
   - Focus on specific subset

3. **Simplify visualization:**
   - Use filters to reduce edges
   - Focus on key relationships

---

### Node labels overlapping

**Cause:** Layout algorithm limitations

**Solution:**
1. **Zoom in:**
   - Scroll to zoom
   - Larger view separates labels

2. **Hover for full name:**
   - Labels abbreviated on graph
   - Hover shows full details

3. **Screenshot and annotate:**
   - Take screenshot
   - Add labels manually

---

## ⚡ Performance Issues

### Application very slow to load

**Cause:** Large session state or slow connection

**Solution:**
1. **Refresh browser:**
   - Clear session state
   - Start fresh

2. **Close other tabs:**
   - Free up browser memory
   - Reduce resource contention

3. **Check system resources:**
   - CPU usage
   - Memory usage
   - Close unnecessary applications

4. **Reduce document count:**
   - Upload fewer documents
   - Process in batches

---

### High memory usage

**Cause:** Many documents in session state

**Solution:**
1. **Refresh browser:**
   - Clears session memory
   - Fresh start

2. **Upload fewer documents:**
   - Process in batches
   - Remove old uploads

3. **Close browser tabs:**
   - Each tab uses memory
   - Keep only analyzer open

4. **Restart browser:**
   - Free all memory
   - Fresh state

---

### ChromaDB errors after many uploads

**Cause:** Database corruption or disk full

**Solution:**
1. **Clear ChromaDB:**
   ```bash
   # Stop Streamlit (Ctrl+C)
   rm -rf chroma_db/
   # Restart Streamlit
   streamlit run app.py
   # Re-upload documents
   ```

2. **Check disk space:**
   ```bash
   df -h  # Mac/Linux
   # Ensure >1GB free
   ```

3. **Rebuild database:**
   - Delete chroma_db folder
   - Upload documents again
   - Database rebuilds automatically

---

## 🔑 API & Configuration Errors

### Error: "Invalid API key"

**Cause:** Wrong or expired API key

**Solution:**
1. **Verify API key:**
   - Login to https://platform.openai.com/api-keys
   - Check key is active
   - Copy exact key (including sk-proj- prefix)

2. **Update .env:**
   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```

3. **No spaces or quotes:**
   ```
   # WRONG:
   OPENAI_API_KEY = "sk-xxx"

   # CORRECT:
   OPENAI_API_KEY=sk-xxx
   ```

4. **Restart application:**
   - Environment variables loaded at startup
   - Must restart after changing .env

---

### Error: "Insufficient quota"

**Cause:** OpenAI account has no credits

**Solution:**
1. **Check account balance:**
   - https://platform.openai.com/usage
   - View remaining credits

2. **Add payment method:**
   - https://platform.openai.com/account/billing
   - Add credit card
   - Purchase credits

3. **Use free tier carefully:**
   - Limited requests
   - May need paid plan

---

### Error: "Connection timeout"

**Cause:** Network issue or API down

**Solution:**
1. **Check internet connection:**
   ```bash
   ping api.openai.com
   ```

2. **Check OpenAI status:**
   - https://status.openai.com/

3. **Check firewall:**
   - Ensure port 443 open
   - Allow HTTPS connections

4. **Try again later:**
   - May be temporary outage

5. **Check proxy settings:**
   - If behind corporate proxy
   - Configure proxy in environment

---

## 🌐 Browser Compatibility

### Application not working in Internet Explorer

**Cause:** IE not supported

**Solution:**
- **Use modern browser:**
  - Google Chrome (recommended)
  - Mozilla Firefox
  - Safari (Mac)
  - Microsoft Edge (not IE)

---

### Charts not interactive in Safari

**Cause:** Safari Plotly compatibility

**Solution:**
1. **Update Safari:**
   - Use latest version
   - Check for macOS updates

2. **Enable JavaScript:**
   - Safari → Preferences → Security
   - Enable JavaScript

3. **Clear cache:**
   - Safari → Clear History

4. **Try Chrome/Firefox:**
   - Best compatibility

---

### Mobile browser issues

**Cause:** Not optimized for mobile

**Solution:**
- **Use desktop browser:**
  - Application designed for desktop
  - Mobile support limited
  - Use laptop/desktop for best experience

---

## 💾 Data & Session Issues

### Data lost after browser refresh

**Cause:** Session state not persistent

**Solution:**
1. **Expected behavior:**
   - Streamlit session state is temporary
   - Refreshing clears all data
   - This is by design

2. **Avoid refreshing:**
   - Use navigation in sidebar
   - Don't use browser refresh

3. **Re-upload if needed:**
   - Keep source documents handy
   - Quick to re-upload

4. **Future enhancement:**
   - Persistent storage planned
   - Database backend coming

---

### Can't delete individual documents

**Cause:** Feature not implemented

**Solution:**
1. **Refresh browser:**
   - Clears all documents
   - Fresh start

2. **Upload only wanted documents:**
   - Skip unwanted files
   - Selective upload

3. **Wait for feature:**
   - Individual deletion planned
   - See roadmap

---

### Session expires unexpectedly

**Cause:** Streamlit timeout or browser settings

**Solution:**
1. **Keep browser tab active:**
   - Don't minimize for long periods
   - Interact periodically

2. **Check Streamlit config:**
   ```python
   # In .streamlit/config.toml (create if needed)
   [server]
   maxUploadSize = 200
   enableXsrfProtection = false
   ```

3. **Refresh and restart:**
   - Refresh browser
   - Re-upload documents

---

## 🆘 Getting More Help

### Still having issues?

1. **Check logs in terminal:**
   - Look for error messages
   - Copy exact error text

2. **Check documentation:**
   - [README.md](README.md)
   - [USER_GUIDE.md](USER_GUIDE.md)
   - [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)

3. **Search GitHub issues:**
   - https://github.com/MuratGoksu/nato-pmp-analyzer/issues
   - Someone may have had same problem

4. **Create GitHub issue:**
   - Describe problem clearly
   - Include error messages
   - Specify: OS, Python version, browser
   - Steps to reproduce

5. **Contact system administrator:**
   - If deployed in organization
   - IT support can help

---

## 📝 Reporting Bugs

**When reporting a bug, include:**

1. **Environment:**
   - OS: Windows/Mac/Linux
   - Python version: `python --version`
   - Browser: Chrome/Firefox/Safari
   - Application version: v0.4

2. **Steps to reproduce:**
   - What you did
   - In what order
   - What you expected

3. **Error message:**
   - Exact text
   - Screenshots helpful
   - Terminal output

4. **Context:**
   - How many documents
   - File sizes
   - Previous actions

**Example bug report:**
```
Title: Chatbot fails with "Rate limit exceeded" error

Environment:
- macOS 14.0
- Python 3.10.11
- Chrome 119
- v0.4

Steps:
1. Uploaded 5 PDF documents
2. Asked 3 questions in quick succession
3. 4th question fails with error

Error:
"Rate limit exceeded: wait 60 seconds"

Expected:
Question should be answered or show clearer message

Context:
Using free OpenAI tier
Documents total 50 pages
```

---

## 📚 Additional Resources

- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Technical Docs:** [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Streamlit Docs:** https://docs.streamlit.io/
- **OpenAI Docs:** https://platform.openai.com/docs/
- **GitHub Issues:** https://github.com/MuratGoksu/nato-pmp-analyzer/issues

---

## 📝 Document Version

**Troubleshooting Guide Version:** 1.0
**Last Updated:** November 14, 2025
**Compatible with:** NATO PMP Analyzer v0.4+

---

**Most problems have simple solutions - don't hesitate to ask for help!** 🚀
