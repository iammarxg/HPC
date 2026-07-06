# Introduction

To begin with, the below prompts were used with the `gemini-3.1-flash-lite` LLM, and with a max output token size of `10000000`, and with a fixed temperature of `0.5`.

And the analysis was done by ChatGPT 5.5, with some modifications and guidance done by me.

## Task

**Chosen Task:** Write a Bash script to back up a folder.

---

# Prompts

## 1. Basic Prompt

> Write a bash script to backup a folder.

---

## 2. Improved Prompt

> Write a bash script that takes a source folder as input and creates a compressed tar backup of it in a destination folder, appending the current date to the filename.

---

## 3. Detailed Prompt

> You are a DevOps engineer creating an automated backup solution. Write a bash script that accepts three command-line arguments: a source directory, a destination directory, and the maximum number of old backups to retain. Include error handling to check if the source exists before running, and add comments explaining the logic for deleting older backups.

---

## 4. Creative Prompt

> Act as a strict system administrator designing a secure compliance backup utility. Write a bash script that creates a rotating tar backup of a source folder to a destination folder, keeping a specified number of old backups. The script must also generate a SHA-256 checksum of the newly created archive for integrity verification and append a timestamped record of the operation, including the checksum and backup size, to a log file.

---

## 5. With Clear Constraints Prompt

> Write a bash script that backs up a source directory to a destination, manages a retention policy for old backups, generates a SHA-256 checksum, and writes to a log file. You must adhere to the following constraints: The script must accept exactly three arguments (source, destination, retention limit). Use only standard GNU utilities. If the source directory is missing, the script must exit immediately with code 1. Limit your text explanation outside the code block to exactly three bullet points.

---

# Prompt Evaluation

| Prompt Type | Evaluation | Comments |
|-------------|------------|----------|
| **Basic** | ✅ Excellent | Very simple with almost no guidance, exactly what a basic prompt should be. |
| **Improved** | ✅ Excellent | Adds inputs, desired behavior, and output requirements while remaining concise. |
| **Detailed** | ✅ Excellent | Introduces a role, detailed requirements, command-line arguments, comments, and error handling. |
| **Creative** | ✅ Excellent | Gives the AI a specific persona and requests production-style features such as logging and integrity verification. |
| **With Clear Constraints** | ✅ Good | Clearly defines restrictions regarding arguments, utilities, exit codes, and output formatting. |

---

# Output Comparison

## 1. Basic Output

**Prompt Compliance:** ⭐⭐⭐⭐⭐ (5/5)

### Strengths

- Successfully creates a compressed backup.
- Uses `tar`.
- Includes timestamped filenames.
- Easy to understand.
- Suitable for beginners.

### Weaknesses

- Uses hardcoded source and destination paths.
- No command-line arguments.
- Limited error handling.

---

## 2. Improved Output

**Prompt Compliance:** ⭐⭐⭐⭐⭐ (5/5)

### Strengths

- Accepts source and destination as arguments.
- Automatically creates the destination directory.
- Includes timestamped filenames.
- Checks that the source directory exists.
- Produces a reusable script.

### Weaknesses

- No retention policy.
- No backup integrity verification.

---

## 3. Detailed Output

**Prompt Compliance:** ⭐⭐⭐⭐⭐ (5/5)

### Strengths

- Fully follows the requested DevOps role.
- Accepts three command-line arguments.
- Validates user input.
- Checks that the source directory exists.
- Implements backup retention.
- Includes explanatory comments.
- Provides usage instructions.
- Well organized and practical.

### Weaknesses

- Uses `ls` for file handling, which is acceptable here but not always considered the safest scripting practice.

---

## 4. Creative Output

**Prompt Compliance:** ⭐⭐⭐⭐☆ (4.5/5)

### Strengths

- Successfully adopts the requested system administrator role.
- Creates rotating backups.
- Generates SHA-256 checksums.
- Records operations in a log file.
- Includes security recommendations.
- Uses strict Bash options (`errexit`, `nounset`, `pipefail`).

### Weaknesses

- Uses hardcoded configuration values instead of command-line arguments.
- Slightly exceeds the requested functionality by adding deployment guidance.

---

## 5. Clear Constraints Output

**Prompt Compliance:** ⭐⭐☆☆☆ (2/5)

### Strengths

- Accepts three arguments.
- Produces exactly three bullet points outside the code block.
- Validates the source directory.
- Logs backup operations.

### Weaknesses

- Uses `rsync` instead of creating a compressed tar archive.
- Interprets the retention limit as days instead of the number of backups.
- Does not strictly follow the requested backup strategy.
- Does not fully satisfy the "standard GNU utilities" requirement.

---

# Overall Comparison

| Prompt | Output Quality | Followed Instructions | Complexity | Practicality |
|---------|---------------|----------------------|------------|--------------|
| Basic | Good | Excellent | Low | Good |
| Improved | Very Good | Excellent | Medium | Very Good |
| Detailed | Excellent | Excellent | High | Excellent |
| Creative | Excellent | Very Good | High | Excellent |
| Clear Constraints | Fair | Poor | Medium | Good |

---

# Best Prompt

## Winner: Detailed Prompt

### Why?

The **Detailed Prompt** produced the strongest overall result because it provided enough context, structure, and guidance without being overly restrictive.

Compared with the earlier prompts, it clearly specified:

- The AI's role (DevOps engineer)
- The required functionality
- The expected inputs
- Error handling
- Documentation requirements

As a result, the generated script included:

- Command-line argument validation
- Source directory verification
- Automatic destination directory creation
- Timestamped backups
- Backup retention management
- Well-written comments
- Clear usage instructions

The response closely matched every requirement in the prompt while remaining practical and easy to understand.

Although the **Creative Prompt** generated a more production-ready script with checksum generation, logging, and security enhancements, it hardcoded configuration values instead of accepting command-line arguments, making it slightly less aligned with the requested task.

The **Basic** and **Improved** prompts produced functional scripts but lacked many advanced features found in the Detailed version.

The **Clear Constraints** prompt produced the weakest result because the AI failed to follow several explicit instructions, including creating a tar archive and implementing the requested retention policy correctly.

---

# Final Conclusion

This exercise demonstrates that prompt quality has a direct impact on AI-generated results.

As additional context, roles, instructions, formatting requirements, and constraints were added, the generated scripts became increasingly accurate, maintainable, and feature-rich.

The **Detailed Prompt** achieved the best balance between specificity and flexibility, producing the most complete and accurate solution while fully satisfying the requested requirements.