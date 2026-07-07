# Introduction

To begin with, the below prompts were used with the `gemini-3.1-flash-lite` LLM, and with a max output token size of `1000`, and with a fixed temperature of `0.5`.

The analysis was done by ChatGPT 5.5, with some modifications and guidance done by me.

## Task

Explain what Artificial Intelligence is to a beginner.

---

# Prompts

## 1. Basic Prompt (Task only)

> Explain what Artificial Intelligence is in no more than 120 words.

---

## 2. Improved Prompt (Role + Task)

> You are an experienced technology teacher. Explain what Artificial Intelligence is in no more than 120 words.

---

## 3. Detailed Prompt (Role + Task + Context)

> You are an experienced technology teacher. Explain what Artificial Intelligence is to a high school student with no background in programming or computer science. Use simple language and relatable examples. Keep your explanation within 120 words.

---

## 4. Creative Prompt (Role + Task + Context + Format)

> You are an experienced technology teacher. Explain what Artificial Intelligence is to a high school student with no background in programming or computer science. Use simple language, relatable examples, and an everyday analogy. Format your response with a one-sentence definition, three key points, one real-world example, and a short conclusion. Limit your response to 120 words.

---

## 5. With Clear Constraints Prompt (Role + Task + Context + Format + Constraints)

> You are an experienced technology teacher. Explain what Artificial Intelligence is to a high school student with no background in programming or computer science. Use simple language, relatable examples, and an everyday analogy. Format your response with a one-sentence definition, three key points, one real-world example, and a short conclusion. Constraints: Maximum of 120 words. Avoid technical jargon. Use a friendly and encouraging tone. Do not use bullet points outside the required format. Ensure the explanation is easy for a complete beginner to understand.

---

# Best Prompt: Prompt 5 – With Clear Constraints

### Why?

It produced the clearest and most beginner-friendly explanation while following the requested structure and tone. The added constraints resulted in a concise, well-organized response with simple language, a relatable analogy, a real-world example, and an encouraging conclusion, making it the easiest for a high school student to understand.

# Comparisons & Output Quality

## Prompt 1 – Basic (Task only)

### Strengths
- ✅ Stayed within the 120-word limit (109 words).
- ✅ Provided a factually accurate explanation of AI.

### Weaknesses
- ❌ Too technical for beginners.
- ❌ Focused on defining AI rather than teaching the concept.
- ❌ No examples or analogies to improve understanding.
- ❌ Generic response due to the lack of role, audience, and formatting instructions.

---

## Prompt 2 – Improved (Role + Task)

### Strengths
- ✅ Stayed within the 120-word limit (109 words).
- ✅ Followed the assigned teacher role.
- ✅ More conversational and engaging than Prompt 1.
- ✅ Included an analogy and practical examples to improve understanding.

### Weaknesses
- ❌ No specific target audience, so the explanation was still somewhat general.
- ❌ No required structure or format, making the response less organized.
- ❌ Used more words explaining examples than simplifying the core concept.

> **Result:** A noticeable improvement over Prompt 1, but still lacked direction.

---

## Prompt 3 – Detailed (Role + Task + Context)

### Strengths
- ✅ Stayed within the 120-word limit (115 words).
- ✅ Successfully tailored the explanation for a high school student with no programming background.
- ✅ Used simple language and relatable examples.
- ✅ Balanced simplicity with factual accuracy.
- ✅ The Netflix recommendation example made the concept easy to relate to.

### Weaknesses
- ❌ No required output structure, so the response appeared as one paragraph.
- ❌ Key ideas were less visually organized, making them harder to scan quickly.

> **Result:** Much more beginner-friendly because the added context guided the model toward the intended audience.

---

## Prompt 4 – Creative (Role + Task + Context + Format)

### Strengths
- ✅ Stayed within the 120-word limit (114 words).
- ✅ Followed the assigned role and target audience.
- ✅ Followed the requested format (definition, key points, example, conclusion).
- ✅ Included an everyday analogy and a real-world example.
- ✅ The structured layout significantly improved readability.

### Weaknesses
- ❌ Still allowed some flexibility in wording and tone because no explicit constraints were given.
- ❌ Did not explicitly instruct the model to avoid technical jargon or maintain a friendly tone.

> **Result:** Easier to read and understand than Prompt 3 due to its clear organization.

---

## Prompt 5 – With Clear Constraints

### Strengths
- ✅ Stayed within the 120-word limit (115 words).
- ✅ Followed every instruction: role, task, context, format, and constraints.
- ✅ Used simple language, a friendly tone, and avoided unnecessary jargon.
- ✅ Maintained the requested structure throughout the response.
- ✅ Balanced clarity, accuracy, readability, and conciseness.
- ✅ Produced the most polished and beginner-friendly explanation.

### Weaknesses
- ⚠️ The numbered list slightly differed from the requested "three key points," but it still communicated the information effectively.

> **Result:** The strongest overall response because it most closely followed the prompt while producing the clearest, most organized, and most accessible explanation.