# llm-wiki-lite — step-by-step guide

The **no-scripts** way to build an LLM Wiki. The agent (the LLM) reads your raw sources and writes
the `wiki/` bundle by hand. There is nothing to install and no state file — the Markdown pages *are*
the knowledge base.

Use this when the corpus is small and personal and you value zero setup. For a large, long-lived
knowledge base where scripted automation and mechanical `lint`/`index` help, use the sibling
`llm-wiki` skill instead (`../llm-wiki/README.md`).

---

## 1. Prerequisites

None beyond the agent. No Python, no `pip install`, no API key beyond the one the agent already
uses. If you can chat with the agent, you can run this skill.

## 2. Project layout

```
your-project/
├── raw/                      # your immutable sources (you add files here)
├── wiki/                     # the OKF bundle the agent writes
│   ├── SCHEMA.md             #   conventions that govern this vault (authoritative)
│   ├── index.md              #   list of every page + candidates (reserved)
│   ├── log.md                #   change log (reserved)
│   ├── sources/              #   one summary per raw file
│   ├── entities/             #   people, companies, projects, tools
│   ├── concepts/             #   techniques, patterns, ideas
│   ├── relationships/        #   how two things relate / comparisons
│   └── overviews/            #   high-level synthesis
└── .agents/skills/llm-wiki-lite/
    ├── SKILL.md
    ├── README.md             # this file
    └── references/page-templates.md
```

`raw/` and `wiki/` sit at the project root. If `wiki/SCHEMA.md` does not exist yet, copy it from
the `llm-wiki` bundle or ask the agent to create it from the template — it must be present, because
it is the authoritative rulebook the agent follows.

## 3. One-time setup

1. Create the folders: `mkdir -p raw wiki/sources wiki/entities wiki/concepts wiki/relationships wiki/overviews`.
2. Make sure `wiki/SCHEMA.md` is in place (the conventions file).
3. **Decide raw file names before the first ingest.** A raw file's name (minus any date prefix and
   extension) becomes its permanent source ID, so renaming it later counts as a withdrawal plus a
   new source. Recommended form: `YYYY-MM-DD-slug.ext`.

## 4. Ingest your sources

1. Drop the source files into `raw/` (text formats: `.md`, `.txt`, `.html`, `.json`, `.csv`,
   `.xml`, `.rst`, `.yaml`; convert anything else to Markdown first).
2. Ask the agent:

   > Ingest the files from `raw/` using the **llm-wiki-lite** skill.

3. The agent will, **one source at a time, oldest first**:
   - read `wiki/SCHEMA.md`, `references/page-templates.md` and `wiki/index.md`;
   - read the raw file and write `wiki/sources/<slug>.md`;
   - add facts (with citations) to entity/concept pages, **creating a page only once something has
     3+ mentions** — otherwise listing it as a candidate in `index.md`;
   - add a relationship page if the source makes an explicit claim about how two things relate;
   - refresh `wiki/overviews/overview.md` if the big picture changed;
   - update `index.md` and `log.md`, then self-check against the quality checklist.

   Naming the skill matters — say "llm-wiki-lite" so the agent uses the hand-driven workflow rather
   than the scripted `llm-wiki` one.

## 5. Check the result

Open the new pages and `wiki/index.md`. A healthy first ingest of a single source produces a
source summary plus a list of candidates (nothing reaches 3 mentions yet, so there are no entity or
concept pages). Ask the agent to run its **quality checklist** (in `SKILL.md`) and report anything
it could not resolve.

## 6. Add more sources later

Repeat step 4. As the corpus grows, candidates cross the 3-mention threshold and the agent promotes
them to full pages, wires up relationships, and updates the overview. Because there is no change
tracking, tell the agent which files are new (or just "ingest anything in `raw/` that isn't in the
wiki yet").

## 7. Revise or remove a source

- **Changed a raw file?** Ask the agent to re-ingest it: it removes the old facts for that source
  and re-extracts them.
- **Removed a raw file?** Ask the agent to **prune** it: it deletes the summary, strips that
  source's facts from every page, deletes emptied pages, refreshes the remaining prose, and updates
  `index.md`/`log.md`.

## 8. Ask questions

> Using **llm-wiki-lite**, what do my sources say about semantic layers?

The agent reads `index.md`, opens the relevant pages, and answers with citations to concept IDs.

---

## Limits to be aware of

Because there are no scripts, everything — including the bookkeeping — is on the agent:

- **No mechanical lint or index.** You check links, citations and orphans by hand and update
  `index.md` yourself; the scripted skill has `lint` and `index` for this.
- **No batch reformat.** A template change means asking the agent to rewrite each page one by one,
  rather than running `ingest --all` over the corpus.
- **More effort per source.** The agent reads and writes every page in the chat; the scripted skill
  drives the model for you, which matters at dozens-to-hundreds of sources.
- **Pruning and updates are manual.** The agent finds and removes a withdrawn source's facts by
  hand; on a large wiki it may miss one.

If these start to bite — usually once you pass a few dozen sources — switch to `llm-wiki`. Both are
stateless and both have the LLM write the pages, so the `wiki/` bundle is the same shape; you just
run the scripts (`ingest`, `index`, `lint`) over your existing pages.
