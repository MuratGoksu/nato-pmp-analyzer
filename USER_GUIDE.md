# 📖 NATO PMP Analyzer - User Guide

## 🎯 Purpose
This guide provides detailed instructions for end users to effectively use the NATO PMP Analyzer for project portfolio analysis.

**Target Audience:** Project Managers, Portfolio Analysts, Strategic Planners, Decision Makers

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Uploading Documents](#uploading-documents)
3. [Using the Chatbot](#using-the-chatbot)
4. [Exploring the Dashboard](#exploring-the-dashboard)
5. [Stakeholder Network Analysis](#stakeholder-network-analysis)
6. [Project Relationship Networks](#project-relationship-networks)
7. [Best Practices](#best-practices)
8. [Frequently Asked Questions](#frequently-asked-questions)
9. [Tips & Tricks](#tips--tricks)

---

## 🚀 Getting Started

### First Time Login

1. **Access the Application**
   - Open your web browser (Chrome, Firefox, or Safari recommended)
   - Navigate to: `http://localhost:8501`
   - Wait for the application to load (5-10 seconds)

2. **Understand the Interface**
   - **Sidebar (Left):** Navigation menu and system status
   - **Main Area (Center):** Content and features
   - **Status Indicators:** Real-time system information

3. **Navigation**
   - Use the sidebar radio buttons to switch between pages:
     - 🏠 Home
     - 📤 Upload Documents
     - 💬 Chatbot
     - 📈 Dashboard
     - 👥 Stakeholder Network
     - 🔗 Network Graph

### Understanding the Home Page

**Key Metrics Displayed:**
- **Documents Processed:** Number of PMPs analyzed
- **AI Engine Status:** RAG active or pattern matching mode
- **Words Processed:** Total content analyzed

**What You'll See:**
- Feature checklist (what's available)
- Quick status overview
- Getting started tips

---

## 📤 Uploading Documents

### Step 1: Navigate to Upload Page

1. Click **"📤 Upload Documents"** in the sidebar
2. You'll see the upload interface

### Step 2: Prepare Your Documents

**Supported Formats:**
- ✅ PDF (.pdf)
- ✅ Word Documents (.docx, .doc)

**Document Requirements:**
- Maximum file size: Recommended <50MB per file
- Clear, readable text (not scanned images)
- Proper PMP structure helps extraction accuracy

**Best Practices:**
- Use official PMP templates when possible
- Include project name in filename
- Ensure stakeholder contact info is present
- Include budget information in standard formats (€X.X million)

### Step 3: Upload Files

1. **Click "Browse files"** button
2. **Select one or more documents:**
   - Hold Ctrl/Cmd to select multiple files
   - Or drag and drop files onto the upload area
3. **Review file list:**
   - Check file names
   - Verify file sizes
   - Note file types

### Step 4: Process Documents

1. **Click "🚀 Process Documents"** button
2. **Wait for processing:**
   - Progress bar shows completion status
   - Each document takes 2-5 seconds
   - Status messages appear during processing

3. **What Happens During Processing:**
   - Text extraction from PDF/DOCX
   - Metadata extraction:
     - Project name
     - Budget amounts
     - Key dates
     - Stakeholder emails/names
     - RAG status (Red/Amber/Green)
   - Vector embeddings created (for AI search)
   - Document added to knowledge base

### Step 5: Verify Upload Success

**After processing completes:**
- ✅ Success message appears
- ✅ Documents listed in sidebar with checkmarks
- ✅ RAG status shows "Active" (green)
- ✅ Document count updates

**Review Uploaded Documents:**
1. Scroll down to "📚 Document Library"
2. Click to expand any document
3. Review extracted metadata:
   - Project name
   - Status (RED/AMBER/GREEN)
   - Word count
   - Budget found
   - Dates identified
   - Stakeholders listed
4. Check text preview (first 500 characters)

**If Upload Fails:**
- Error message will show specific issue
- Check file format is supported
- Verify file isn't corrupted
- Try uploading one file at a time
- See [Troubleshooting](#troubleshooting) section

---

## 💬 Using the Chatbot

### Overview

The chatbot allows you to ask questions about your project portfolio in natural language. It uses AI (GPT-4) to understand your questions and search across all uploaded documents.

### Accessing the Chatbot

1. Click **"💬 Chatbot"** in the sidebar
2. Ensure documents are uploaded first (warning appears if none exist)

### Types of Questions You Can Ask

#### **1. Counting & Statistics**
```
How many projects are in the portfolio?
How many projects are RED status?
How many stakeholders are identified?
```

#### **2. Project Information**
```
List all project names
Show me all projects
What projects are currently active?
```

#### **3. Risk & Status Queries**
```
Which projects are at risk?
Show me RED status projects
What are the issues with AMBER projects?
Why is [Project Name] marked RED?
```

#### **4. Budget Analysis**
```
What's the total budget across all projects?
Which projects have the largest budgets?
Show me projects with budgets over €10 million
What's the average project budget?
```

#### **5. Stakeholder Questions**
```
Who are the key stakeholders?
Which stakeholders work on multiple projects?
Show me project managers for Cyber projects
List all email addresses found
```

#### **6. Technology & Themes**
```
Which projects involve Artificial Intelligence?
Show me Cyber security projects
What projects mention Quantum computing?
Which projects work on Cloud migration?
```

#### **7. Strategic Alignment**
```
Which projects support Digital Transformation?
Show me projects aligned with NATO priorities
What initiatives focus on modernization?
Which projects contribute to operational readiness?
```

#### **8. Complex Queries**
```
Which RED projects have budgets over €10M and involve Cyber?
Show projects started in 2024 with AI and Cloud technologies
Find projects with shared stakeholders and similar budgets
```

### How to Use the Chatbot

**Step 1: Type Your Question**
- Click in the chat input box at the bottom
- Type your question in plain English
- Press Enter or click Send

**Step 2: Wait for Response**
- "Thinking..." indicator appears
- Processing takes 3-8 seconds
- AI searches all documents and generates answer

**Step 3: Review the Answer**
- Answer appears in chat
- **Source citations** are provided when available
- Click "📚 Sources" to expand and see:
  - Document name
  - Project name
  - RAG status
  - Relevant text snippet

**Step 4: Ask Follow-up Questions**
- Continue the conversation
- Reference previous answers
- Drill deeper into specific topics

**Step 5: Clear Chat (Optional)**
- Click "🗑️ Clear Chat History" to start fresh
- Useful when switching topics

### Tips for Better Results

**✅ DO:**
- Be specific in your questions
- Use proper project names if known
- Ask one thing at a time
- Include context (e.g., "RED status projects")
- Check source citations for accuracy

**❌ DON'T:**
- Ask extremely vague questions
- Combine too many unrelated queries
- Expect answers about documents not uploaded
- Rush - give AI time to respond

### Understanding Responses

**Response Quality Indicators:**
- **With Sources:** High confidence, evidence-based
- **Without Sources:** Calculated from metadata
- **"I don't have information...":** No relevant data found

**RAG (Retrieval-Augmented Generation) Explained:**
- AI doesn't just guess or make things up
- It searches your actual documents
- Pulls relevant passages
- Synthesizes an answer based on evidence
- Cites sources for verification

---

## 📈 Exploring the Dashboard

### Overview

The Dashboard provides visual analytics and portfolio health metrics at a glance.

### Accessing the Dashboard

1. Click **"📈 Dashboard"** in the sidebar
2. Ensure documents are uploaded (warning if none exist)

### Dashboard Components

#### **1. Status Metrics (Top Row)**

Three key indicators:
- **🔴 Critical (RED):** Projects at high risk
- **🟡 Warning (AMBER):** Projects with concerns
- **🟢 Healthy (GREEN):** On-track projects

**How to Use:**
- Quick portfolio health check
- Identify number of at-risk projects
- Track overall status distribution

#### **2. Risk Distribution Chart**

**Pie Chart showing:**
- Percentage breakdown by status
- Color-coded segments (Red/Amber/Green)
- Interactive hover for exact counts

**How to Use:**
- Visual portfolio health assessment
- Compare risk levels at a glance
- Screenshot for reports/presentations

#### **3. Portfolio Health Score**

- Percentage of GREEN projects
- "At Risk" count (RED + AMBER)

**Interpretation:**
- 80%+ health = Strong portfolio
- 60-80% = Acceptable with concerns
- <60% = Action required

#### **4. RED Projects Detail Table**

**Shows if any RED projects exist:**
- Project name (truncated to 25 chars)
- Status
- Word count
- Budget mentions count

**How to Use:**
- Quickly identify critical projects
- Export data for further analysis
- Share with leadership

### Interactive Features

**Charts:**
- **Hover:** See exact values
- **Zoom:** Scroll to zoom in/out (if enabled)
- **Pan:** Click and drag to move around

**Tables:**
- **Sortable:** Click column headers
- **Full-width:** Optimized for readability

### Refreshing Data

- Dashboard updates automatically when new documents are uploaded
- No manual refresh needed
- Real-time reflection of your portfolio

---

## 👥 Stakeholder Network Analysis

### Overview

Understand who works on which projects and identify collaboration patterns.

### Accessing Stakeholder Network

1. Click **"👥 Stakeholder Network"** in the sidebar
2. Ensure documents with stakeholder info are uploaded

### Understanding the Statistics

**Top Metrics Row:**
- **Unique Stakeholders:** Total people identified
- **Total Mentions:** How many times stakeholders appear
- **Avg per Project:** Average stakeholder count
- **Most Connected:** Person involved in most projects

### Using the Stakeholder Directory

**Search & Filter:**
1. **Search Box:**
   - Type name or email
   - Real-time filtering
   - Case-insensitive

2. **Min Projects Filter:**
   - Show only stakeholders on X+ projects
   - Find key connectors
   - Reduce noise

**Directory Table:**
- Lists all stakeholders
- Shows project count
- Lists up to 3 projects (+ more indicator)
- Sorted by project count (most connected first)

### Stakeholder Overlap Analysis

**Purpose:** Find projects sharing team members

**Table Shows:**
- Project pairs with shared stakeholders
- Number of shared people
- Names of shared stakeholders (up to 3)

**Use Cases:**
- Identify collaboration opportunities
- Spot resource conflicts
- Find subject matter experts
- Coordinate related projects

### Stakeholder Distribution Charts

**Chart 1: Stakeholders per Project**
- Bar chart
- Shows team size for each project
- Color gradient by count
- Interactive tooltips

**Chart 2: Top 10 Most Connected**
- Horizontal bar chart
- Shows people involved in most projects
- Identifies key connectors
- Useful for resource planning

### Stakeholder Network Graph

**Generate Interactive Visualization:**
1. Click **"🔄 Generate Network Visualization"** button
2. Wait for graph to render (5-10 seconds)

**What You See:**
- **Nodes (circles):** Projects
- **Edges (lines):** Shared stakeholders
- **Node size:** Number of stakeholders on that project
- **Labels:** Project names (abbreviated)

**Interactive Features:**
- **Hover over nodes:** See project details and stakeholder count
- **Zoom:** Scroll to zoom in/out
- **Pan:** Click and drag to move

**Interpreting the Graph:**
- Connected nodes = shared team members
- Larger nodes = more stakeholders
- Dense clusters = highly collaborative groups
- Isolated nodes = projects with unique teams

### Detailed Stakeholder Breakdown

**Select individual stakeholder:**
1. Use dropdown at bottom
2. Select a name
3. View:
   - All projects they're involved in
   - Total project count
   - Detailed project list

**Use Cases:**
- Track individual workload
- Find experts in specific areas
- Coordinate schedules
- Identify knowledge silos

---

## 🔗 Project Relationship Networks

### Overview

Visualize how projects connect through stakeholders, technologies, budgets, and status.

### Accessing Network Graph

1. Click **"🔗 Network Graph"** in the sidebar
2. Ensure multiple documents are uploaded

### Understanding Relationship Types

**Four Types Detected Automatically:**

1. **🔴 Stakeholder Overlap (Red lines)**
   - Projects sharing team members
   - Strength = number of shared people

2. **🔵 Technology Keywords (Teal lines)**
   - Projects using similar technologies
   - AI, Cyber, Quantum, Cloud, 5G, etc.
   - Strength = number of common keywords

3. **🟡 Budget Similarity (Yellow lines)**
   - Projects with similar budget ranges
   - Helps identify comparable initiatives

4. **🟢 Status Alignment (Green lines)**
   - Projects with same RAG status
   - All RED, all AMBER, or all GREEN

### Using the Network Controls

**Sidebar Filter (Relationship Type):**
- Check/uncheck relationship types
- Focus on specific connections
- Reduce visual complexity

**Example:**
- Uncheck "stakeholder" to see only tech relationships
- Check only "budget" to compare similar-cost projects

### Network Statistics

**Top Row Metrics:**
- **Projects:** Total nodes in network
- **Relationships:** Total connections found
- **Avg Connections:** Average links per project

**Relationship Breakdown:**
- Bar chart showing count by type
- Table with exact numbers

### Projects Table

**Shows all projects in network:**
- Project name
- RAG status
- Word count
- Number of stakeholders

**Sortable by any column**

### Relationship Details

**Shows up to 10 relationships:**
- Source project ↔️ Target project
- Relationship type
- Description

**Example:**
> **Quantum Initiative** ↔️ **Cyber Defense**
> 🏷️ Technology - 3 common keyword(s)

### Generating the Network Visualization

**Create Interactive Graph:**
1. Click **"🔄 Generate Network Visualization"**
2. Wait 5-15 seconds for rendering
3. Graph appears with legend

**Graph Components:**

**Nodes (Circles):**
- Each circle = one project
- **Size:** Based on connection count (bigger = more connected)
- **Color:** Based on RAG status
  - 🟢 Green = GREEN status
  - 🟡 Yellow = AMBER status
  - 🔴 Red = RED status
  - ⚫ Gray = Unknown status
- **Label:** Abbreviated project name

**Edges (Lines):**
- Each line = one relationship
- **Color:** Based on relationship type (see legend)
  - Red = Stakeholder
  - Teal = Technology
  - Yellow = Budget
  - Green = Status
- **Thickness:** Relationship strength

**Interactive Features:**
- **Hover over nodes:** See project details
  - Full name
  - Status
  - Word count
  - Stakeholder count
  - Number of connections
- **Hover over edges:** See relationship details
- **Zoom:** Scroll wheel
- **Pan:** Click and drag background

### Interpreting the Network

**Patterns to Look For:**

1. **Dense Clusters**
   - Highly related projects
   - Strong collaboration
   - Potential for synergy

2. **Isolated Nodes**
   - Independent projects
   - Unique focus areas
   - May lack collaboration

3. **Hub Nodes** (large, many connections)
   - Central to portfolio
   - Cross-cutting initiatives
   - Strategic importance

4. **Bridge Nodes**
   - Connect different clusters
   - Knowledge transfer points
   - Coordination opportunities

**Use Cases:**
- Identify duplicate efforts
- Find collaboration opportunities
- Understand portfolio structure
- Communicate relationships to leadership
- Plan resource allocation
- Strategic portfolio planning

---

## 🎯 Best Practices

### Document Upload

**✅ Best Practices:**
- Upload all related PMPs at once for complete analysis
- Use standardized PMP templates when possible
- Include current/updated versions only
- Name files clearly (avoid "doc1.pdf", use "ProjectName_PMP_v2.pdf")
- Upload in batches if you have 50+ documents

**❌ Avoid:**
- Uploading scanned images (low extraction accuracy)
- Mixing PMP documents with unrelated files
- Uploading duplicate/old versions
- Using special characters in filenames

### Chatbot Usage

**✅ Best Practices:**
- Start with simple questions to understand capabilities
- Be specific (use project names, dates, amounts)
- Check source citations before making decisions
- Ask follow-up questions for clarity
- Save important answers (screenshot or copy text)

**❌ Avoid:**
- Asking about documents not uploaded
- Extremely complex multi-part questions
- Expecting 100% accuracy without verification
- Making critical decisions without source verification

### Dashboard & Analytics

**✅ Best Practices:**
- Refresh regularly as portfolio changes
- Screenshot charts for presentations
- Cross-reference with chatbot for details
- Monitor RED project count trends
- Share with stakeholders regularly

**❌ Avoid:**
- Relying solely on visuals without context
- Ignoring outliers in data
- Forgetting to update after new uploads

### Network Analysis

**✅ Best Practices:**
- Use filters to focus on specific relationship types
- Generate graphs for stakeholder presentations
- Identify collaboration gaps
- Look for unexpected connections
- Document insights found

**❌ Avoid:**
- Over-interpreting weak relationships
- Assuming all connections are equally important
- Ignoring context of relationships

---

## ❓ Frequently Asked Questions

### General Questions

**Q: How many documents can I upload?**
> A: There's no hard limit. We've tested with 10-50 documents successfully. Very large portfolios (100+) may take longer to process.

**Q: Can I delete documents after uploading?**
> A: Currently, you'd need to refresh the application to clear all data. Individual document deletion is planned for future versions.

**Q: How accurate is the metadata extraction?**
> A: Approximately 85% accurate for well-formatted PMPs. Accuracy depends on document quality and structure.

**Q: What languages are supported?**
> A: Currently English only. The underlying AI (GPT-4) supports many languages, so multilingual support is possible in future versions.

### Upload Questions

**Q: Why did my upload fail?**
> A: Common reasons:
> - Unsupported file format
> - Corrupted file
> - File too large (>100MB)
> - Scanned PDF (images, not text)
> - Network connection issue

**Q: How long does processing take?**
> A: 2-5 seconds per document on average. Large documents (50+ pages) may take 10-15 seconds.

**Q: Can I upload the same document twice?**
> A: Yes, but it will be processed as a separate entry. Avoid duplicates for clean data.

### Chatbot Questions

**Q: Why is the chatbot slow?**
> A: RAG queries involve:
> 1. Understanding your question (AI processing)
> 2. Searching vector database
> 3. Retrieving relevant passages
> 4. Generating answer
> This takes 3-8 seconds typically. Complex queries may take up to 15 seconds.

**Q: Can the chatbot make mistakes?**
> A: Yes. Always check source citations. The AI bases answers on document content but may occasionally misinterpret. Treat it as an assistant, not a replacement for human judgment.

**Q: Why doesn't it understand my question?**
> A: Try:
> - Rephrasing more clearly
> - Being more specific
> - Breaking complex questions into parts
> - Using terms from your documents

### Dashboard Questions

**Q: Why are all my projects GREEN?**
> A: The system detects RAG status from keywords (red, amber, green) in documents. If your PMPs don't explicitly mention status, they default to GREEN.

**Q: Can I export dashboard data?**
> A: Screenshot capability is built-in (browser feature). CSV/Excel export is planned for future versions.

**Q: How often does the dashboard update?**
> A: Automatically after each document upload. No manual refresh needed.

### Network Questions

**Q: Why don't I see any relationships?**
> A: Possible reasons:
> - Only one document uploaded (need 2+ for relationships)
> - Documents don't share stakeholders/technologies
> - Check filters aren't hiding all relationship types

**Q: What if my network graph is messy?**
> A: Use filters to focus on one relationship type at a time. With many projects, graphs naturally become complex.

**Q: Can I customize relationship detection?**
> A: Currently uses predefined logic. Custom relationship rules are planned for enterprise versions.

---

## 💡 Tips & Tricks

### Power User Tips

1. **Batch Processing**
   - Upload all docs at once, not one-by-one
   - Saves time on RAG initialization

2. **Question Templates**
   - Save your common questions
   - Build a library of useful queries

3. **Screenshot Everything**
   - Browser screenshot for reports
   - Network graphs for presentations
   - Dashboard metrics for leadership

4. **Combine Features**
   - Use chatbot to identify issues
   - Use dashboard to quantify problems
   - Use networks to find solutions

5. **Regular Updates**
   - Re-upload when PMPs change
   - Keep portfolio analysis current
   - Track trends over time

### Keyboard Shortcuts

- **Ctrl/Cmd + R:** Refresh page
- **Ctrl/Cmd + Plus/Minus:** Zoom in/out
- **Ctrl/Cmd + 0:** Reset zoom
- **Ctrl/Cmd + F:** Find on page
- **Tab:** Navigate between inputs

### Browser Recommendations

**Best Experience:**
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Safari (macOS latest)

**Adequate:**
- Microsoft Edge (latest)

**Not Recommended:**
- Internet Explorer
- Very old browser versions

---

## 📞 Getting Help

### If You Encounter Issues

1. **Check [Troubleshooting Guide](TROUBLESHOOTING.md)**
2. **Review [Technical Documentation](TECHNICAL_DOCUMENTATION.md)**
3. **Contact your system administrator**
4. **Check GitHub Issues:** https://github.com/MuratGoksu/nato-pmp-analyzer/issues

### Providing Feedback

We welcome your feedback!
- What features do you use most?
- What's confusing or difficult?
- What would you like to see added?

---

## 📝 Document Version

**User Guide Version:** 1.0
**Last Updated:** November 14, 2025
**Compatible with:** NATO PMP Analyzer v0.4+

---

**Happy Analyzing!** 🚀

For technical details, see [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
