# Analyzing 3 Claude Skills

So I looked at three of the skills Claude has access to and tried to figure out when they'd actually kick in and why they exist in the first place. Here's what I found:

## 1. docx (Word Documents)

**What problem does it solve?**
Basically, if you just ask an AI to "write me a report," you'd normally just get a wall of text back. This skill is what makes it actually produce a real .docx file with proper formatting — like table of contents, headers, page numbers, that kind of stuff you'd expect in an actual Word document.

**When does it trigger?**
It kicks in when someone says "Word doc," ".docx," or asks for something like a report/memo/letter/template as an actual file (not just text in the chat). Also works if you're trying to pull info out of an existing Word file, even if you're gonna use that info somewhere else afterward.

## 2. xlsx (Spreadsheets)

**What problem does it solve?**
Spreadsheets are annoying because you can't just dump data in there — formulas need to be right, formatting matters, and a lot of real-world data is messy (headers in the wrong place, random blank rows, etc). This skill handles making sure the output is an actual usable spreadsheet and not just data that looks like a table.

**When does it trigger?**
Whenever the main thing being asked for IS a spreadsheet — like fixing an existing .csv/.xlsx, building one from nothing, or cleaning up messy data into something organized. Even something casual like "clean up the xlsx in my downloads" counts.


## 3. skill-creator (meta skill)

**What problem does it solve?**
This one's different because it's not making something for the end user directly — it's for building/improving OTHER skills. So it's like... a skill about skills. It helps write new ones, edit old ones, and even test if a skill's description is actually good at triggering when it should.

**When does it trigger?**
When someone wants to create a new skill, edit one, or specifically improve how well a skill's description "catches" the right requests (like doing evals/benchmarks on it).