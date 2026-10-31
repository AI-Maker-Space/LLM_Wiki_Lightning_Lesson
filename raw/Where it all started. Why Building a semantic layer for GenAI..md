---
title: "Where it all started. Why Building a semantic layer for GenAI."
source: "https://dragoscrintea.me/articles/01-where-it-all-started-why-building-a-semantic-layer-for-genai"
author:
published: 2026-01-16
created: 2026-10-24
description: "How I went from GenAI beginner in 2024 to launching semantido, an open-source semantic layer designed for the GenAI era."
tags:
  - "clippings"
---
![Hero image representing the relationship between an LLM and a set of database tables.](https://dragoscrintea.me/_next/static/media/hero_image_article_1.2fm_v4m_0-f-l.png)

## Intro

This is the first article in a series of eight articles about building semantic layer(s) for GenAI applications. Will cover what a semantic layer is, why it is important, and how you can build one yourself or if so choose, use an open-source one, for example, semantido, built by yours truly.

## The beginnings

We hear almost every day that data is at the core, and even "might" be the make-or-break success to a GenAI application. That comes as a total surprise, doesn’t it?

I guess someone needed to burn a lot of $$$ for an unrealized profit that will forever stay... unrealized, but I digress.

Mid-2024 I jumped on the GenAI bandwagon, out of pure curiosity. The noise was big and the signal very low. I could not make sense of anything. Fast-forward to 2025 I decided to invest a decent amount of money (~ GBP 15k) in getting at least a sense of direction. You can check my LinkedIn profile; I listed all my courses I took there.

For most of my career, I wore one of these two hats: Principal / Solution Architect or (Senior) Data Engineer. They gave me a good perspective on how systems are built, but also on the data they depend on.

All this was thrown to the bin in 2025, when the noise was even louder and the signal even smaller. Vibe coding, AI AI AI AI AI \* 25 times mentioned by Sundar Pichai at Google IO (have to give it to Google though, they pull a big rabbit out of their hat), fleet of agents managing your daily tasks, virtual workforce, fire lots of people (re-hired after) by Klarna, the latest Salesforce debacle, dare I mention MCP... and the list gets longer and longer.

To what all this you might ask? A mere 10% success rate of a decent AI project.

And what where the culprits? In my humble opinion, there were three: security, system architecture, i.e., how everything fits together (did I mention it was thrown away like it never existed before) and data.

![Three pillars showing the failure reasons for GenAI projects.](https://dragoscrintea.me/_next/static/media/gen_ai_success_rate.44z0tsxe0--jm.png)

I feel very close to the last two, though. I tried and tried and tried again to raise the awareness of their importance and not lose it all in the madness of AI-generated stuff aka slop. But I failed, after all, I am nobody. As a result, I decided to build and open-source application blueprints as well as semantido (the semantic layer for the GenAI era) to reach out to as many people as I can. Good engineering principles still count, maybe now more than ever. Pair that with a good system architecture will serve as a north-star for a successful GenAI project.

## My brittle experiments

Working with small and large businesses, you observe that most of their data is locked in one or many of the following: SQL stores, document stores, Confluence, plain old Word, PowerPoint, and PDF files. That will cover 80% if not more of the entire data a business generates in one way or another.

During my 2025 AI Makers bootcamp (Cohort 5) I built my own gym assistant agent... yes... a vertical agent (shameless plug – to be launched at the end of Q1 this year). The technology I used back then was Langchain (lots of Nurofen for generated headache), got better though, AstroJS and Supabase for the storage mechanism.

And so, I began to use a LLM to "generate" SQL queries based on the user prompt, for example, show me the exercises I burn the most calories on. This is known as Text2SQL. Surprise after surprise, the generated SQL was pretty brittle; sometimes it properly identified the table columns, sometimes not. I tried "better" prompt engineering, prompt decomposition, query rewriting, few-shots examples, even thought about divorcing from Langchain and go CrewAI (based on Langchain... go figure) and many more, with marginal improvements.

Then it hit me. It was in front of me all the time, and yet I decided to ignore it. The LLM had **NO IDEA** what those fields where, what they stored, and how they relate to each other.

## Enter the semantic world

Wikipedia provides this definition of semantic for linguistics:

> In linguistics, semantics is the scientific study of meaning. It is focusing on how words, phrases, and sentences convey concepts, ideas, and relationships, exploring what meaning is, how it's constructed, interpreted, and how complex meanings arise from simpler parts, distinct from syntax (structure) and pragmatics (meaning in context).

A *Large Language Model* is all about Language, and as a consequence, semantics play an important role.

The LLM missed not only the meaning but also the relationships between my tables. It would "hallucinate" on what a particular column might be. And before you throw anything at me... I did name the table columns to the best as I could, i.e., not amt, dst, or anything like that.

Adding table semantics to the context prompt improved my SQL generation by orders of magnitude. This also had a side effect; it improved my code structure by splitting the SQL generation in three parts (generation, validation, execution). Contrast and compare with Langchain, which provides a complicated way to build this, which I found mind-bending.

## Outro

In the next article will dive into what semantics are and why they are a **VERY** important piece in making GenAI application and agents reliable.

[Subscribe to my newsletter](#newsletter-form) to stay up to date with the latest articles and open-source projects.

**Disclaimer:**

- This article is a personal reflection of my own experiences and opinions and does not represent any of my employer(s) views.
- No AI was used in writing this article. I care about my readers and respect their time.
- The images used in this article have been generated with Gemini 3, based on the article text given in the prompt.
- [semantido](https://pypi.org/project/semantido/) , the open-source semantic layer built for GenAI applications, is available on GitHub.