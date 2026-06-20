import os
from groq import Groq
from dotenv import load_dotenv
from tools import search_web, read_webpage, create_study_plan, is_relevant
import json


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are LAURA, an intelligent study planning agent created by Fofana Maimouna, a software engineer and AI enthusiast.
Your job is to help users learn any subject by:
1. Searching for the best learning resources
2. Reading and evaluating those resources
3. Creating a personalised day-by-day study plan

Think step by step. Always search first, read the best results, then create the plan.
Be specific, practical and encouraging in your study plans.

If the provided resources are clearly unrelated to the subject (for example,
store locations, unrelated products, or random web pages), say so honestly
and create the plan based on your own knowledge of the subject instead of
forcing irrelevant resources into the plan.

NEVER invent or assume fake resources, titles, or content that wasn't actually
given to you. If no real resources were found, explicitly say so and use your
own training knowledge instead. Do not write phrases like "assuming the
resources are..." — only describe what is real.
If asked who created you or who you are, mention that you were built by
Fofana Maimouna as an AI study planning agent.
"""


def build_search_query(subject: str) -> str:
    """Ask the LLM to create an effective, unambiguous search query."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You write short, precise search engine queries. Reply with ONLY the query text, nothing else."},
            {"role": "user", "content": f"Write a search query to find the best tutorials for learning: {subject}. Make it specific enough to avoid ambiguous results."}
        ],
        max_tokens=50,
        temperature=0.2
    )
    return response.choices[0].message.content.strip().strip('"')


def run_agent(subject: str, duration: str, level: str, progress_callback=None) -> str:
    """Run LAURA agent to create a study plan."""

    # ── Step 1: Search ──────────────────────────────────────
    if progress_callback:
        progress_callback(f"Searching for {subject} resources...")

    query = build_search_query(subject)
    if progress_callback:
        progress_callback(f" Search query: {query}")

    raw_results = search_web(query, max_results=8)
    search_results = [r for r in raw_results if is_relevant(subject, r)]

    if not search_results:
        if progress_callback:
            progress_callback(" First search too vague, trying again...")
        query = f"how to learn {subject}"
        raw_results = search_web(query, max_results=8)
        search_results = [r for r in raw_results if is_relevant(subject, r)]

    if not search_results:
        search_results = raw_results[:5]  # last resort fallback

    if progress_callback:
        progress_callback(f"Found {len(search_results)} resources")

    # ── Step 2: Read top 3 resources ────────────────────────
    read_contents = []
    for idx, resource in enumerate(search_results[:3]):
        url = resource.get("url", "")
        if not url:
            continue

        if progress_callback:
            progress_callback(f"Reading resource {idx + 1}/3: {resource['title']}")

        content = read_webpage(url)
        read_contents.append({
            "title": resource["title"],
            "url": url,
            "content": content[:1500]
        })

    if progress_callback:
        progress_callback(f" Resources actually read: {len(read_contents)}")
        for item in read_contents:
            progress_callback(f"    {item['title'][:60]}")

    # ── Step 3: Build context block (hard stop if empty) ───
    if not read_contents:
        if progress_callback:
            progress_callback(" No resources could be read — using LLM knowledge only")
        context_block = "NO EXTERNAL RESOURCES WERE FOUND OR COULD BE READ."
    else:
        context_block = ""
        for i, item in enumerate(read_contents, 1):
            context_block += f"\n\n--- Resource {i}: {item['title']} ({item['url']}) ---\n{item['content']}"

    if progress_callback:
        progress_callback("LAURA is now writing your study plan...")

    # ── Step 4: Generate the plan ───────────────────────────
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
I want to learn: {subject}
Duration: {duration}
My level: {level}

Here is the ACTUAL CONTENT from resources found, if any:
{context_block}

CRITICAL RULES:
- NEVER invent or assume fake resources, titles, or content that wasn't actually given to you above
- If context_block says "NO EXTERNAL RESOURCES WERE FOUND", explicitly tell the user no resources
  could be retrieved, and clearly state you are using your own training knowledge instead
- Only cite [Resource 1], [Resource 2] etc if that resource was ACTUALLY provided above
- Do not write phrases like "assuming the resources are..." — only describe what is real

Using the real information above (or your own knowledge if none was found),
create a detailed day-by-day study plan structured week by week.
"""}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=3000,
        temperature=0.3
    )

    final_plan = response.choices[0].message.content

    if progress_callback:
        progress_callback("Study plan ready!")

    # ── Step 5: Append resource list ────────────────────────
    resource_list = create_study_plan(subject, duration, level, search_results[:5])

    return final_plan + "\n\n---\n" + resource_list