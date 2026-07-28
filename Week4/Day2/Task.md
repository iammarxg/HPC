## Comparing skill-creator vs theme-factory: input and output

For this task I used both skill-creator and theme-factory to see how they work differently. Basically what I put in and what I got out of each one.

### skill-creator

**Input:** I just told it what I wanted in one sentence "create a skill that will help me with week 6's n8n tasks" and gave it a screenshot of my curriculum table. Instead of just guessing what I meant, skill-creator actually asked me two follow-up questions first (like what the skill should mainly help with, and if it should track my progress), which I thought was kind of smart honestly.

**Output:** It gave me a full, packaged `.skill` file, not just a plan or description. Like an actual working thing: a `SKILL.md` with all the instructions, a `references/curriculum.md` file that had the whole day-by-day breakdown and common mistakes (which I didn't even ask for, it just pulled that from the table itself), and a progress checklist template. It even checked its own work before giving it to me — it found a YAML error and fixed it on its own, then packaged the whole thing into a downloadable file with a "Save skill" button.

So basically: I gave skill-creator a one-liner and a picture, and it gave me back a fully built, ready-to-install skill package with three files.

### theme-factory

**Input:** Just a short description both times — first "simple modern web theme for a word counter website," then later "theme for a 23rd birthday party for a man." For the second one it also asked me two quick questions (what I was making it for and what vibe I wanted) before it did anything.

**Output:** This one didn't give me a file at all — just options and ideas in the chat. The first time it showed me a PDF with all 10 of its built-in themes and recommended two that fit, then just waited for me to pick one. The second time none of the presets really worked for a birthday thing, so it made up a custom palette and font pairing (with actual hex codes and font names and a little "best used for" blurb), but again it stopped there and waited for me to approve it before doing anything else.

So theme-factory's input was just a short description, and what I got back was more like a proposal — either a shortlist or a custom idea — not a finished thing, since it never went past that stage without me confirming something.

### The core difference

- **skill-creator basically finishes the job for you.** You give it a goal and it interviews you, builds it, checks it, and hands you a file that's ready to go — all in one go.
- **theme-factory stops and makes you decide.** It narrows things down (either picking from its presets or making something custom) but then it deliberately pauses and waits for me instead of just going ahead.
- Both of them ask questions when what I said wasn't specific enough, but skill-creator's questions are there to help it finish building, while theme-factory's questions are there to help it make a proposal it then just sits on.
- Neither one did anything until it had enough info from me, but "enough" means something different for each — for skill-creator that's enough to build the whole skill, and for theme-factory that's enough to show me some options.