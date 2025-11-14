# 🎬 NATO PMP Analyzer - Demo Script

## 🎯 Demo Objective
Demonstrate how the NATO PMP Analyzer automates project portfolio analysis using AI, saving time and providing strategic insights for decision-makers.

---

## ⏱️ Demo Duration: 10-15 minutes

---

## 📋 Pre-Demo Checklist

### System Setup (5 minutes before demo)
- [ ] Open terminal and navigate to project folder
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Verify .env has valid OPENAI_API_KEY
- [ ] Start application: `streamlit run app.py`
- [ ] Open browser to http://localhost:8501
- [ ] Clear any old session data (refresh browser)
- [ ] Have 3-5 sample PDF documents ready
- [ ] Close unnecessary browser tabs
- [ ] Set browser zoom to 100%
- [ ] Disable notifications/distractions

### Documents to Use
Prepare 3-5 sample NATO PMP documents (PDF or DOCX):
- Mix of different project types (Cyber, AI, Quantum, etc.)
- Mix of RAG statuses (RED, AMBER, GREEN)
- Include stakeholder information
- Include budget information

---

## 🎬 Demo Script (Step-by-Step)

### **PART 1: Introduction (2 minutes)**

**[Show Home Page]**

**Script:**
> "Welcome! Today I'm going to demonstrate the NATO PMP Analyzer, an AI-powered tool that revolutionizes how we analyze and understand our project portfolio."
>
> "The challenge: NATO manages hundreds of projects across different programmes of work. Manually reviewing these documents to find connections, identify risks, and prevent duplication is extremely time-consuming."
>
> "Our solution: An intelligent system that automatically extracts metadata, identifies relationships, and allows you to query your entire portfolio using natural language."

**Key Points to Mention:**
- ✅ Automated document processing
- ✅ AI-powered analysis with GPT-4
- ✅ Natural language queries
- ✅ Network visualization
- ✅ Real-time insights

---

### **PART 2: Document Upload (3 minutes)**

**[Navigate to Upload Documents page]**

**Script:**
> "Let's start by uploading some Project Management Plans. The system supports both PDF and Word documents."

**Actions:**
1. Click "📤 Upload Documents" in sidebar
2. Click "Browse files"
3. Select 3-5 sample documents
4. Show file list with names and sizes
5. Click "🚀 Process Documents"

**While Processing (Talk over progress bar):**
> "Watch as the system processes each document. For each one, it's:
> - Extracting the full text
> - Identifying the project name, budget, dates, and stakeholders
> - Detecting the RAG status (Red, Amber, Green)
> - Creating vector embeddings for semantic search
> - Building a searchable knowledge base"

**After Processing:**
> "Notice the sidebar now shows all processed documents with checkmarks. The RAG status shows we have X chunks indexed and ready for intelligent queries."

**Expand one document to show:**
- Extracted metadata (project name, status, word count)
- Budget information
- Stakeholder list
- Text preview

**Script:**
> "The system successfully extracted all this metadata automatically - no manual data entry required!"

---

### **PART 3: Chatbot Demo (4 minutes)**

**[Navigate to Chatbot page]**

**Script:**
> "Now comes the powerful part - asking questions using natural language. The chatbot uses GPT-4 and Retrieval-Augmented Generation to provide accurate, source-backed answers."

**Demo Questions (ask these in order):**

**Question 1: Simple Count**
```
How many projects are currently in the portfolio?
```
**Script:**
> "Simple questions get instant answers with a complete breakdown."

**Question 2: Risk Analysis**
```
Which projects are marked as RED status and why?
```
**Point out:**
- AI-generated answer
- Source citations
- Expand sources to show details

**Script:**
> "Notice it not only tells us which projects, but explains WHY they're at risk, pulling evidence directly from the documents."

**Question 3: Complex Query**
```
What are the main technologies used across all Cyber-related projects?
```
**Script:**
> "It can analyze across multiple documents, identifying themes and patterns."

**Question 4: Stakeholder Query**
```
Which projects share common stakeholders?
```

**Question 5: Strategic Query**
```
Which projects directly support NATO's Digital Transformation strategy?
```
**Script:**
> "This is where RAG shines - understanding context and strategic alignment across the entire portfolio."

**Key Points:**
- ✅ Click "📚 Sources" to show document references
- ✅ Highlight the project name, status, and text snippet
- ✅ Emphasize accuracy through source citations

---

### **PART 4: Dashboard Analytics (2 minutes)**

**[Navigate to Dashboard page]**

**Script:**
> "The dashboard provides instant portfolio health visibility for decision-makers."

**Show:**
1. **KPI Metrics at top**
   > "At a glance: X projects critical, Y warning, Z healthy"

2. **Risk Distribution Pie Chart**
   > "Visual breakdown of portfolio health"

3. **Project Data Table**
   > "Sortable table with all key metadata"

4. **Click on RED projects section**
   > "Drill down into at-risk projects for immediate action"

**Key Message:**
> "Leadership can instantly see portfolio health without reading hundreds of pages."

---

### **PART 5: Stakeholder Network (2 minutes)**

**[Navigate to Stakeholder Network page]**

**Script:**
> "One of the biggest challenges is preventing duplication and encouraging collaboration. The stakeholder network reveals hidden connections."

**Show:**
1. **Statistics at top**
   > "X unique stakeholders across Y projects, with an average of Z per project"

2. **Search/Filter Demo**
   - Type a stakeholder name in search
   - Show their project involvement

3. **Stakeholder Overlap Analysis**
   > "This table shows which project pairs share team members - perfect for identifying collaboration opportunities"

4. **Distribution Charts**
   - Point to stakeholders per project chart
   - Point to top 10 most connected stakeholders

5. **Click "Generate Network Visualization"**
   - Let graph generate
   - Hover over nodes to show details

**Script:**
> "This network graph visualizes collaboration patterns. Larger nodes have more stakeholders. Connected nodes share team members. This helps us identify:
> - Who the key connectors are
> - Which projects should be talking to each other
> - Potential resource conflicts"

---

### **PART 6: Network Graph (2 minutes)**

**[Navigate to Network Graph page]**

**Script:**
> "Finally, the relationship network shows ALL types of connections between projects."

**Show:**
1. **Network Statistics**
   > "X projects with Y relationships detected automatically"

2. **Relationship Breakdown**
   > "Four types: Stakeholder overlap, shared technologies, similar budgets, same status"

3. **Use Filters (in sidebar)**
   - Uncheck "stakeholder"
   - Show how graph focuses on technology connections
   - Re-enable all filters

4. **Click "Generate Network Visualization"**
   - Show interactive graph with color-coded edges
   - Hover over nodes (project details)
   - Hover over edges (relationship details)

**Script:**
> "Look at these color-coded relationships:
> - Red lines: Shared stakeholders
> - Teal lines: Common technologies like AI, Cyber, Quantum
> - Yellow lines: Similar budget ranges
> - Green lines: Same RAG status
>
> Node size represents connectivity - highly connected projects are larger. Node color shows status - green for healthy, red for at-risk."

**Key Insight:**
> "This reveals the hidden fabric of your portfolio - which projects are related, where synergies exist, and which initiatives should be coordinated."

---

### **PART 7: Conclusion & Benefits (1 minute)**

**[Return to Home page]**

**Script:**
> "In just 15 minutes, we've:
> - ✅ Processed X documents automatically
> - ✅ Extracted metadata with 85% accuracy
> - ✅ Answered complex strategic questions using AI
> - ✅ Visualized portfolio health
> - ✅ Mapped stakeholder networks
> - ✅ Revealed hidden project relationships
>
> **What would this take manually?**
> - Days of reading documents
> - Hours of spreadsheet work
> - Manual stakeholder mapping
> - Risk of missing connections
>
> **With the NATO PMP Analyzer:**
> - Upload and go
> - Instant insights
> - AI-powered analysis
> - Always up-to-date
>
> **Business Value:**
> - 🎯 Prevent project duplication
> - 🤝 Encourage collaboration
> - ⚠️ Identify risks early
> - 📊 Strategic alignment visibility
> - ⏱️ Save hundreds of hours
> - 💰 Better resource allocation"

---

## 💡 Demo Tips

### Do's ✅
- **Speak slowly and clearly**
- **Pause after each major point**
- **Use hand gestures to point at screen**
- **Make eye contact with audience**
- **Ask "Can everyone see this?" before starting**
- **Have backup documents ready**
- **Know your sample data well**
- **Practice question transitions**
- **Smile and show enthusiasm**

### Don'ts ❌
- **Don't rush through features**
- **Don't apologize for the UI**
- **Don't say "um" or "uh"**
- **Don't refresh the page unnecessarily**
- **Don't skip source citations**
- **Don't ignore questions**
- **Don't forget to breathe**

---

## 🎤 Handling Questions

### Common Questions & Answers

**Q: "How accurate is the metadata extraction?"**
> A: "Currently 85% accurate for project names, budgets, dates, and stakeholders. We use pattern matching and NLP. For critical applications, we recommend human review, but it dramatically reduces manual effort."

**Q: "What about data security?"**
> A: "Documents are processed locally. Only text chunks are sent to OpenAI's API for embedding and query responses. We don't store documents on external servers. For production, we can deploy entirely on-premise."

**Q: "How much does OpenAI cost?"**
> A: "For this PoC, approximately €10-20 for testing. In production, estimated €0.10-0.50 per document depending on size. Compare this to hours of manual analysis."

**Q: "Can it handle classified documents?"**
> A: "The current PoC uses cloud AI. For classified documents, we can deploy using on-premise LLMs like LLaMA 2 or government-approved AI services."

**Q: "How long does processing take?"**
> A: "2-5 seconds per document on average. Batch processing 100 documents takes 5-10 minutes including vectorization."

**Q: "What languages does it support?"**
> A: "Currently English. OpenAI's GPT-4 supports 50+ languages, so multilingual support is feasible."

**Q: "Can we customize the metadata extraction?"**
> A: "Absolutely! The extraction patterns are configurable. We can add custom fields specific to your PMP templates."

**Q: "What's the technology stack?"**
> A: "Python backend with Streamlit UI, OpenAI GPT-4 for AI, ChromaDB for vector storage, LangChain for RAG orchestration, Plotly for visualizations."

---

## 🔧 Troubleshooting During Demo

### If something goes wrong:

**Upload fails:**
- "Let me try with a different document"
- Have backup documents ready

**Chatbot slow to respond:**
- "The AI is analyzing all documents for the most accurate answer"
- Fill time by explaining RAG process

**Network graph doesn't generate:**
- "Let me show you the relationship data table instead"
- Fallback to dashboard

**Browser crashes:**
- "I have a backup demo ready"
- Keep a second browser tab open

---

## 📸 Screenshot Opportunities

Take screenshots during demo for later use:
- Home page with metrics
- Upload page with document list
- Chatbot with complex query + sources
- Dashboard with charts
- Stakeholder network graph
- Project relationship network

---

## 🎯 Success Metrics

**Your demo is successful if audience:**
- ✅ Understands the time-saving value
- ✅ Sees the AI in action
- ✅ Gets excited about network graphs
- ✅ Asks "When can we use this?"
- ✅ Discusses their own use cases
- ✅ Requests a follow-up meeting

---

**Good luck with your demo! You've built an impressive tool - now show it off with confidence!** 🚀
