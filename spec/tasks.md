# Task Breakdown

## T1 – Acquire Article Content
- Fetch article by URL.
- Normalize HTML to markdown-ready plaintext.
- Persist source, title (if available), fetch timestamp, and status in SQLite.

## T2 – Summarize Key Points
- Input: cached article body.
- Output: 5–8 bullet markdown summary covering thesis and pivotal evidence.
- Constraints: cite paragraph references when possible.

## T3 – Surface Authorial Assumptions
- Input: cached article body.
- Output: markdown list of implicit assumptions with rationale.
- Constraints: flag contextual data required to validate assumption.

## T4 – Identify Potential Errors
- Input: cached article body.
- Output: markdown table listing suspected errors, category, confidence, and suggested verification steps.

## T5 – Compile Report
- Merge outputs from T2–T4 into unified markdown document.
- Save to user-selected output directory and optionally print to stdout.
- Append run metadata (model, timestamp, url, hash) to SQLite `analyses` table.
