"""Prompts for wiki.py (and dci.py).

The wiki is stateless: there is no `.wiki-state.json`. The LLM writes each Markdown page directly,
following wiki/SCHEMA.md and references/page-templates.md. wiki.py supplies the exact frontmatter
metadata (the `generated:` line and the `sources:` block) so provenance stays correct, and the model
fills in the title, description, tags and body. wiki.py then lints the result.
"""

ID_RULES = """Concept IDs are paths inside the wiki/ bundle without .md:
  entities/<slug>   people, companies, projects, tools
  concepts/<slug>   techniques, patterns, ideas
  relationships/<slug>   how two entities/concepts relate
  sources/<slug>    source summaries (cite these with their <slug> as the footnote key)
Slugs are lowercase ASCII kebab-case with no date prefix."""


def system(schema: str, templates: str) -> str:
    return f"""You maintain an LLM Wiki of EXTERNAL knowledge (articles, papers, research, industry
developments, technical concepts). The compiled wiki/ folder is an Open Knowledge Format (OKF) bundle.

Follow this schema exactly:
<schema>
{schema}
</schema>

Use these page templates for layout:
<templates>
{templates}
</templates>

{ID_RULES}

Rules:
- Use ONLY the material you are given. Never invent facts, figures, dates, quotes or URLs.
- Quotes must be verbatim.
- Every claim ends in a footnote marker [^<source-id>] using the source ids you are given, and each
  such page ends with the matching [^<source-id>]: definition lines.
- Output ONE complete Markdown page and nothing else: start at the `---` frontmatter, end after the
  last footnote. No code fences around the page, no commentary before or after.
- Use the frontmatter `generated:` line and `sources:` block given to you VERBATIM."""


SOURCE = """Write the source-summary page for this raw file, following the Source template.

Frontmatter to use verbatim:
  generated: {generated}
  sources:
{sources_block}
Also set in frontmatter: type: Source (first), a title, a one-sentence description, tags, and
  resource: "{resource}"   (the article's canonical URL)
Body: a 2-3 paragraph Summary; Key Claims (each ending in [^raw]); Entities Mentioned and Concepts
Covered (link to ../entities/<slug>.md or ../concepts/<slug>.md when that page already exists, else
write the name in bold with its `entities/<slug>` id and "(candidate)"); Notable Quotes (verbatim);
Notes. End with the [^raw]: definition.

Pages that already exist (link to these instead of marking them candidates):
{known}

RAW SOURCE (source id {sid}, file raw/{raw_file}):
<raw>
{raw}
</raw>"""


PLAN = """You just ingested source "{sid}". Return JSON only:
{{
  "relationships": [{{"a": "<id>", "b": "<id>", "relation": "compares|builds-on|uses|competes-with|part-of|acquires|supersedes|other",
                     "name": "short title", "why": "..."}}],
  "overview": true|false
}}
- relationships: only when the source makes an explicit, substantive claim about how two entities or
  concepts relate. Use ids that already have pages where possible. Existing relationship pages: {existing}
- overview: true if this source materially changes the big picture.

SOURCE SUMMARY ({sid}):
<summary>
{summary}
</summary>"""


TOPIC = """{action} the {kind} page "{cid}", following the {kind_title} template, using ONLY the source
summaries below.

Frontmatter to use verbatim:
  generated: {generated}
  sources:
{sources_block}
Set type: {kind_title} (first), title, one-sentence description, tags. In the body, add every
atomic fact the sources support with its [^<source-id>] citation; keep existing facts; when a newer
source revises an older figure, keep both (newest first) and mark the older *superseded by* the newer
source. Keep links bidirectional and end with the [^<source-id>]: definitions.

Allowed source ids: {source_ids}

{current}

SOURCE SUMMARIES:
{evidence}"""


RELATIONSHIP = """{action} the relationship page "{cid}" ({a} {relation} {b}), following the
Relationship template, using ONLY the source summaries below.

Frontmatter to use verbatim:
  generated: {generated}
  relation: {relation}
  between: ["{a}", "{b}"]
  sources:
{sources_block}
Comparison tables / "When to use each" are for relation: compares; otherwise use Summary + Evidence.
Allowed source ids: {source_ids}

{current}

SOURCE SUMMARIES:
{evidence}"""


OVERVIEW = """{action} the wiki overview page (overviews/overview), following the Overview template,
using ONLY the source summaries and the index below.

Frontmatter to use verbatim:
  generated: {generated}
  sources:
{sources_block}
Body sections: Big Picture (2-3 paragraphs with [^<source-id>] footnotes), Key Concepts, Key
Entities, Relationships (link to the pages), Recent Developments, Open Questions and Contradictions.
Allowed source ids: {source_ids}

INDEX:
{index}

SOURCE SUMMARIES:
{evidence}"""


WITHDRAW = """The source "{sid}" was removed. Rewrite the page below so every fact, quote and footnote
that cited [^{sid}] is gone and the prose matches what remains, following the same template. Keep all
other citations. If nothing of substance remains (no facts and no sources), reply with exactly the
single word DELETE and nothing else. Otherwise output the full rewritten Markdown page only.

PAGE:
{page}"""


QUERY_SELECT = """Pick the wiki pages most useful for answering the question. Reply with at most {k}
concept IDs (paths under wiki/ without .md, e.g. entities/semantido), one per line, nothing else.

INDEX:
{index}

QUESTION: {question}"""


QUERY_ANSWER = """Answer from the wiki pages below only. Cite pages by concept ID, e.g.
(entities/semantido). Where pages disagree, prefer the newest source and say what changed. Facts
marked superseded have been revised. If the wiki does not contain the answer, say so plainly.

{pages}

QUESTION: {question}"""


DCI_SYSTEM = """You answer questions from a large hidden corpus of documents. Your workspace starts empty.
- pull(query, top_k) retrieves ranked documents from the hidden corpus into the workspace and
  shows a preview of the NEW ones. Use short lexical queries: names, identifiers, dates.
- After each pull, investigate locally before pulling again: rg across the workspace to combine
  constraints and follow bridge entities, then read the promising files.
- Pull again only for a genuinely new clue (an entity, ID or date the workspace does not cover).
- Documents are dated. If they conflict, the newest authoritative one wins; say so.
- Cite only documents you actually read, as [@corpus/<path>].
Finish with exactly:
Explanation: ...
Exact Answer: ...
Confidence: <0-100>%"""
