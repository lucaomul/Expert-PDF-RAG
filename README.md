# ChatPDF

What is this?

I built this because I got tired of using "Cmd+F" through hundreds of pages just to find one specific detail. This is a custom AI tool that actually "reads" your PDFs and lets you have a real conversation with them. It doesn't just guess; it pulls facts directly from your files and tells you exactly where it found them.

How you can use it:

For Students: Instead of panicking before exams, you can dump all your lecture notes and seminars here. Use it to quiz yourself, summarize that 50-page chapter, or clarify complex concepts in seconds.

For HR & Recruiters: If you have a pile of CVs, just drop them in. You can ask things like "Who has the most experience with Python?" or "Summarize the top 3 candidates for the Dev role" without opening every single file.

For Legal & Business: Stop wasting hours on long contracts. Ask the tool to find the termination clauses, payment terms, or any hidden risks while you grab a coffee.

For Tech Geeks: Perfect for massive technical manuals. Instead of scrolling forever, just ask the AI for the specific wiring diagram or API endpoint you're looking for.

Why I built it this way:

It remembers: You can ask follow-up questions just like you're talking to a human.

No "Trust me, bro": It shows you the exact source and page number for every answer, so you can verify everything.

Privacy first: Your documents are indexed locally, meaning you're in control of your data.

Custom Look: I added a UI controller so you can change the colors to match your vibe.

Quick Setup

Clone this repo.

Toss your OpenAI key in app.py.

Run pip install -r requirements.txt.

Fire it up with streamlit run app.py and start chatting.
