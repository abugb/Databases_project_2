# AGENTS.md

## Project Domain

- CS4432 Project 2 is an individual assignment on database indexing. Read the full handout in `Project 2.txt` or `Project 2.pdf` before designing or implementing. The goal is to understand how in-memory indexes change the work required to answer a lookup query.
- Use Python as the starting preference from Project 1. The handout permits Java, Python, or C++. Keep the command loop easy to follow and organize the indexing and record I/O logic separately where that makes the design clearer.

## Collaboration and Learning Preferences

- Ask follow-up questions when ambiguity could materially change the result, or if the user seems misled.
- Prioritize understanding the assignment and its database concepts. Review the relevant requirements together, explain the design in plain terms, and agree on the next implementation step with the user.
- Work in small steps. For explanation or review requests, explain what the current code does and give concrete feedback. For implementation requests, edit only the requested skeleton, function, or component and preserve the user's wording and unrelated choices.
- Let the user run the program and assignment tests by default. Provide copyable commands and explain what each check demonstrates. Run the program or tests directly when the user asks.
- Keep the implementation simple and focused on the handout. Assume commands use the specified syntax and handle the full set of valid query values, including values with no matching records. Keep comments and docstrings concise. For class state intentionally kept private, follow the user's Project 1 convention of double-leading underscores.
- Match the handout's command and output wording where it specifies exact text. Distinguish assignment requirements from optional design choices when explaining or reviewing the implementation.

## Dataset

- In this checkout, the supplied block files are `Project2Dataset/Project2Dataset/F1.txt` through `F99.txt`. The grader will place the directory containing those files directly under the program's working directory as `Project2Dataset`. Account for the extra archive directory when setting up local runs. Use only the dataset files and skip extraction metadata such as `.DS_Store` and `__MACOSX`.
- Each data file is one block with 100 concatenated 40-byte records and no newline separators. Use binary I/O and zero-based byte offsets. The `RandomV` field is four digits in the range `0001` through `5000` and precedes the final `...` of each record.

## Assignment Requirements

- Print `Program is ready and waiting for user command.` at startup and after each command. Wait for a command before reading data or building indexes.
- `CREATE INDEX ON Project2Dataset (RandomV)` builds both in-memory indexes in one pass through the data files. Store every matching record location as a file number and byte offset. The hash index maps each `RandomV` to its locations. The array index has 5,000 slots and must accommodate every value from 1 through 5,000 and multiple locations per slot. Print `The hash-based and array-based indexes are built successfully.` followed by the ready sentence.
- `SELECT * FROM Project2Dataset WHERE RandomV = v` uses the hash index when available and a full table scan otherwise.
- `SELECT * FROM Project2Dataset WHERE RandomV > v1 AND RandomV < v2` uses the array index when available and a full table scan otherwise. Both bounds are exclusive.
- `SELECT * FROM Project2Dataset WHERE RandomV != v` always uses a full table scan.
- For indexed queries, use both the file number and byte offset to retrieve records directly. Output every matching record, elapsed time in milliseconds, and the number of distinct data files read for the query. For equality and range queries, also identify the index used or report `Table Scan`. Indexed results may appear in a different order from scan results.
- When verifying, compare scan and indexed results for equality and range queries. Include duplicate values, values with no match, and exclusive range boundaries. Check that inequality still scans after index creation and that each query reports its own data-file count.

## Deliverables and Authorship

- The Canvas submission is one ZIP containing the full source code package and `Readme.txt`.
- The student must write `Readme.txt` themselves. The assistant may explain the requirements, review the student's draft, and point out factual discrepancies. Include the student's name and ID, Section I with compile and run steps, Section II with what works and what fails, and Section III with design choices beyond the handout.
