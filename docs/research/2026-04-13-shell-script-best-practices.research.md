---
name: "Shell Script Best Practices for Security, Readability, Testability, and Quality"
description: "Best practices for secure, readable, testable bash hook scripts: set -Eeuo pipefail preamble, jq-based injection-safe JSON parsing, bats-core testing with stdin simulation, ShellCheck static analysis, and Google style conventions"
type: research
sources:
  - https://sipb.mit.edu/doc/safe-shell/
  - https://citizen428.net/blog/bash-error-handling-with-trap/
  - https://www.howtogeek.com/782514/how-to-use-set-and-pipefail-in-bash-scripts-on-linux/
  - https://developer.apple.com/library/archive/documentation/OpenSource/Conceptual/ShellScripting/ShellScriptSecurity/ShellScriptSecurity.html
  - https://matklad.github.io/2021/07/30/shell-injection.html
  - https://advancedweb.hu/how-to-mock-in-bash-tests/
  - https://honeytreelabs.com/posts/writing-unit-tests-and-mocks-for-unix-shells/
  - https://www.hackerone.com/blog/testing-bash-scripts-bats-practical-guide
  - https://bats-core.readthedocs.io/en/stable/writing-tests.html
  - https://google.github.io/styleguide/shellguide.html
  - https://github.com/koalaman/shellcheck
  - https://bertvv.github.io/cheat-sheets/Bash.html
  - https://mywiki.wooledge.org/BashGuide/Practices
  - https://medium.com/data-science/jq-a-saviour-for-sanitising-inputs-not-just-outputs-1fd6728c0dc4
  - https://www.linuxbash.sh/post/bash-shell-script-security-best-practices
related:
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Shell Script Best Practices

This document investigates established best practices for writing secure, readable, testable, and maintainable shell scripts — specifically applicable to Claude Code hook scripts that receive JSON payloads on stdin and enforce quality gates. Research covers four dimensions: safety flags and error handling, security for untrusted JSON stdin, testing frameworks and strategies, and readability and static analysis conventions.

## Findings

### Sub-question 1: Safety flags and error handling

**F1.1** `set -Eeuo pipefail` is the canonical safety preamble [1][2][12]. Each flag has a specific role: `-e` exits on non-zero return, `-E` propagates ERR traps into subshells, `-u` treats unset variables as errors, `-o pipefail` surfaces failures from intermediate pipeline stages rather than masking them behind the last command's exit code. (HIGH — T1+T4+T5 convergence across three independent sources)

**F1.2** Commands with expected non-zero exits must be guarded with `|| true` or `|| :` [1]. Without these escapes, safety flags produce false-positive exits on legitimate patterns: `grep` exits 1 when a pattern is not found, which is normal behavior in detection hooks. (HIGH — T1 source; confirmed by challenge analysis)

**F1.3** `trap 'echo "Error on line ${LINENO}: ${BASH_COMMAND}" >&2' ERR` provides structured error context without a full logging framework [2]. The `EXIT` trap handles cleanup on any termination path, including normal exits. (MODERATE — T5 source; pattern well-established in community practice)

**F1.4** `set -x` (print each command before execution) is a debugging aid, not a production flag [3]. In production hooks it floods stderr and can leak sensitive values from the JSON payload. (MODERATE — T5 source; no counter-evidence found)

### Sub-question 2: Security practices for JSON stdin

**F2.1** Never pass untrusted input to `eval` [4][5][15]. The root cause of shell injection is string concatenation into a shell interpreter; `eval` is the most direct instantiation of this pattern. Apple Developer docs [4] (T1) and matklad [5] (T4) converge on this prohibition independently. (HIGH — T1+T4 convergence)

**F2.2** Always quote variable expansions: `"${var}"` not `$var` [1][4][12][13]. Unquoted variables undergo word-splitting and globbing — the primary mechanism by which content in `tool_input` fields can alter script control flow. (HIGH — T1+T1+T4+T4 convergence)

**F2.3** Use `jq --arg name "$VAR"` to pass shell variables into jq filter expressions [14]. Direct interpolation (`jq ".[\"${USER_VAR}\"]"`) is an injection vector if the value contains jq syntax characters. The `--arg` flag handles escaping correctly. (MODERATE — T5 source with 403 access; no T1 source explicitly documents this jq-specific pattern)

**F2.4** `tool_input` field values flowing through Claude Code hooks are user-influenced data [challenge finding]. The `command` field in Bash hook payloads reflects what the user asked Claude to run. Extract with `jq -r '.tool_input.command'` and quote the result before any further shell use. (MODERATE — derived from challenge analysis; not directly from a source)

**F2.5** Use absolute paths for all external command invocations [15]. PATH manipulation can redirect common tools to malicious replacements. (MODERATE — T5 source only; no T1 source found for this specific point)

### Sub-question 3: Testing frameworks and strategies

**F3.1** bats-core is the most widely documented bash testing framework [8][9] (alternatives: shunit2, shellspec). It is TAP-compliant, written in bash, and provides `run`, `$status`, and `$output` helpers. Tests pass when all commands in the test case exit 0. (HIGH — T1 official docs [9] + T4 practitioner [8])

**F3.2** Hook scripts must be decomposed into small, independently testable functions before meaningful testing is possible [9]. A script that runs all logic at top-level is not amenable to unit testing with sufficient coverage. (HIGH — T1 bats-core docs state this explicitly)

**F3.3** Stdin simulation for testing: `printf '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | ./hook.sh` [6]. Use `printf` (not `echo`) for explicit newline control when the script expects multi-line JSON. (MODERATE — T5 source; pattern is practical and well-understood)

**F3.4** Mocking priority: function override > PATH override > eval-based dynamic mock [6][7]. Function overriding is the simplest: define a function with the same name as the command to mock; it takes precedence over the PATH entry. `export -f mock_fn` makes it visible to subshells. (MODERATE — T5 sources only)

### Sub-question 4: Readability and static analysis

**F4.1** ShellCheck is the de facto standard static analysis tool for bash [11]. It detects quoting issues, deprecated backtick syntax, command misuse, and conditional mistakes. CI integration is standard. Passing ShellCheck is necessary but not sufficient — runtime logic errors and wrong exit code intent are not detected. (HIGH — T1 official project)

**F4.2** Google Shell Style Guide conventions [10] (T1, widely adopted): lower_case for local variables and functions; UPPER_CASE for exported/environment variables; errors to STDERR (`echo "error" >&2`); a `main` function required when the script has other named functions; maximum 80-character lines. (HIGH — T1 source)

**F4.3** Function header comments should describe: description, globals used, arguments, outputs (stdout/stderr), return values [10]. This makes the function's contract inspectable without executing it. (MODERATE — T1 source, but commonly omitted in practice)

**F4.4** Use long-form flags where available: `--silent` over `-s`, `--quiet` over `-q` [12]. Long flags are self-documenting; the trade-off is line length. For hook scripts that are read during security review, self-documentation reduces review friction. (MODERATE — T4 source)

**F4.5** Use `[[` over `[` for conditionals in bash [13]. `[[` does not perform word-splitting on variables, supports `=~` for regex matching, and has more intuitive string comparison semantics. (MODERATE — T4 source; recommendation is broadly accepted in bash community)

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://sipb.mit.edu/doc/safe-shell/ | Writing Safe Shell Scripts | MIT SIPB | n/d | 200 OK | T1 |
| 2 | https://citizen428.net/blog/bash-error-handling-with-trap/ | Bash Error Handling with Trap | citizen428.net | n/d | 200 OK | T5 |
| 3 | https://www.howtogeek.com/782514/how-to-use-set-and-pipefail-in-bash-scripts-on-linux/ | How To Use set and pipefail in Bash Scripts on Linux | How-To Geek | n/d | 200 OK | T5 |
| 4 | https://developer.apple.com/library/archive/documentation/OpenSource/Conceptual/ShellScripting/ShellScriptSecurity/ShellScriptSecurity.html | Shell Script Security | Apple Developer | n/d | 200 OK | T1 |
| 5 | https://matklad.github.io/2021/07/30/shell-injection.html | Shell Injection | matklad.github.io | 2021-07-30 | 200 OK | T4 |
| 6 | https://advancedweb.hu/how-to-mock-in-bash-tests/ | How to mock in Bash tests | Advanced Web Machinery | n/d | 200 OK | T5 |
| 7 | https://honeytreelabs.com/posts/writing-unit-tests-and-mocks-for-unix-shells/ | Writing Unit-Tests and Mocks for UNIX Shells | Honey Tree Labs | n/d | 200 OK | T5 |
| 8 | https://www.hackerone.com/blog/testing-bash-scripts-bats-practical-guide | Testing Bash Scripts with BATS: A Practical Guide | HackerOne | n/d | 200 OK | T4 |
| 9 | https://bats-core.readthedocs.io/en/stable/writing-tests.html | Writing tests — bats-core documentation | bats-core project | n/d | 200 OK | T1 |
| 10 | https://google.github.io/styleguide/shellguide.html | Shell Style Guide | Google | n/d | 200 OK | T1 |
| 11 | https://github.com/koalaman/shellcheck | ShellCheck — a static analysis tool for shell scripts | koalaman / ShellCheck | n/d | 200 OK | T1 |
| 12 | https://bertvv.github.io/cheat-sheets/Bash.html | Bash best practices cheat sheet | Bert Van Vreckem | n/d | 200 OK | T4 |
| 13 | https://mywiki.wooledge.org/BashGuide/Practices | BashGuide/Practices | Greg's Wiki (wooledge.org) | n/d | 200 OK | T4 |
| 14 | https://medium.com/data-science/jq-a-saviour-for-sanitising-inputs-not-just-outputs-1fd6728c0dc4 | jq: A Saviour for Sanitising Inputs, Not Just Outputs | Alexis Lucattini / Medium | n/d | 403 (access issue, kept) | T5 |
| 15 | https://www.linuxbash.sh/post/bash-shell-script-security-best-practices | Bash shell script security best practices | linuxbash.sh | n/d | 500 (server error, kept) | T5 |

## Extracts

### Sub-question 1: Safety flags and error handling

#### Source 1: Writing Safe Shell Scripts
- **URL:** https://sipb.mit.edu/doc/safe-shell/
- **Author/Org:** MIT SIPB | **Date:** n/d

**Re: Safety flags and error handling patterns**
> "If a command fails, `set -e` will make the whole script exit, instead of just resuming on the next line." (set -e section)

> "Treat unset variables as an error, and immediately exit." (set -u section)

> "Disable filename expansion (globbing) upon seeing `*`, `?`, etc." (set -f section)

> "causes a pipeline...to produce a failure return code if any command errors." (set -o pipefail section)

> "I recommend the following in bash scripts: `set -euf -o pipefail`" (Recommended Configuration section)

> "If you have commands that can fail without it being an issue, you can append `|| true` or `|| :` to suppress this behavior" (Error Handling Pattern section)

> "Whenever you pass a variable to a command, you should probably quote it. Otherwise, the shell will perform word-splitting and globbing, which is likely not what you want." (Quoting Best Practice section)

> "When possible, instead of writing a 'safe' shell script, use a higher-level language like Python." (Primary Recommendation)

---

#### Source 2: Bash Error Handling with Trap
- **URL:** https://citizen428.net/blog/bash-error-handling-with-trap/
- **Author/Org:** citizen428.net | **Date:** n/d

**Re: Safety flags and error handling patterns**
> "There's also a special signal named `ERR`, which will be triggered every time a command exits with a non-zero status." (ERR Trap Pattern section)

> "This same mechanism can also be used to perform cleanup tasks when a script terminates" via the `EXIT` signal. (EXIT Trap Pattern section)

> "Using all of the described features, we end up with the following script:
> ```
> set -Eeuo pipefail
>
> notify () {
>   FAILED_COMMAND="$(caller): ${BASH_COMMAND}"
>     # perform notification here
> }
>
> trap notify ERR
> ```" (Practical Implementation section)

> "`caller`: ${BASH_COMMAND}" provides the line number, script name, and failed command, or alternatively use "Error on line ${LINENO}: ${BASH_COMMAND}". (Error Information Capture section)

> "`set -Eeuo pipefail` combines: `-e` (exit on errors), `-E` (inherit ERR traps), `-u` (treat unset variables as errors), and `-o pipefail` (propagate intermediate pipeline errors)." (Recommended Options section)

---

#### Source 3: How To Use set and pipefail in Bash Scripts on Linux
- **URL:** https://www.howtogeek.com/782514/how-to-use-set-and-pipefail-in-bash-scripts-on-linux/
- **Author/Org:** How-To Geek | **Date:** n/d

**Re: Safety flags and error handling patterns**
> "The `set -e` (exit) option causes a script to exit if any of the processes it calls generate a non-zero return code." (On set -e section)

> "Anything non-zero is taken to be a failure." (On set -e section)

> "The return code that comes out of a piped sequence of commands is the return code from the last command in the chain." (On pipefail section)

> "If there's a failure with a command in the middle of the chain we're back to square one." (On pipefail section)

> "We can trap this type of error using the `set -u` (unset) option" to catch uninitialized variables. (On set -u section)

> "The `-u` (unset) option is intelligent enough not to be triggered by situations where you can legitimately interact with an uninitialized variable." (On set -u section)

> "When you're writing scripts, this is can be a lifesaver. it prints the commands and their parameters as they are executed." (On set -x section)

---

### Sub-question 2: Security practices for JSON stdin

#### Source 4: Shell Script Security
- **URL:** https://developer.apple.com/library/archive/documentation/OpenSource/Conceptual/ShellScripting/ShellScriptSecurity/ShellScriptSecurity.html
- **Author/Org:** Apple Developer | **Date:** n/d

**Re: Security practices for untrusted input**
> "The most common type of attack in shell scripts is the injection attack. This type of attack occurs when arguments stored in user-provided variables are passed to commands without proper quoting." (On General Untrusted Input section)

> "This is a no-no. Never run eval on data passed in by a user unless you have very, very carefully sanitized it (and if possible, use a whitelist to limit the allowed values)." (On eval dangers section)

> "To fix this bug, change the if statement to read: `if [ \"$FOO\" = \"foo\" ] ; then`" (Mitigation for comparison operators section)

> "Pass the value `; rm randomfile` to cause this script to delete a file." (The attack scenario section)

> "Most modern shells parse the statement prior to any variable substitution, and are thus unaffected by this attack. However, for proper security when your script is run on older systems (not to mention avoiding a syntax error if the filename contains spaces), you should still surround the variable with double quotes." (On Backwards Compatibility section)

---

#### Source 5: Shell Injection
- **URL:** https://matklad.github.io/2021/07/30/shell-injection.html
- **Author/Org:** matklad.github.io | **Date:** 2021-07-30

**Re: Security practices for untrusted input**
> "Shell injection can happen when a program needs to execute another program, and one of the arguments is controlled by the user/attacker." (How They Occur section)

> "Rather then running the command directly, node asks the shell to do the heavy lifting. But the shell is an interpreter of the shell language, and, by carefully crafting the input to `exec`, we can ask it to run arbitrary code." (How They Occur section)

> "If you __develop a library__ for conveniently working with external processes, use and expose only the shell-less API from the underlying platform." (Prevention Strategies section)

> "unlike `exec`, it [spawn] uses an array of arguments rather then a single string." (Prevention Strategies section)

> "If you are an __application developer__, be aware that this issue exists. Read the language documentation carefully — most likely, there are two flavors of process spawning functions." (Security Awareness section)

---

#### Source 14: jq: A Saviour for Sanitising Inputs, Not Just Outputs
- **URL:** https://medium.com/data-science/jq-a-saviour-for-sanitising-inputs-not-just-outputs-1fd6728c0dc4
- **Author/Org:** Alexis Lucattini / Medium | **Date:** n/d

**Re: Security practices for JSON stdin**
> "use jq along with the `<<<` bash here-string to initialise a json object, populate using jq which will do all of the escape handling for us" (On Input Handling section)

> "we can use the `tojson` method to escape any double quotes in command" (Injection Prevention Example section)

> "When things get more complicated, one should move away from simple scripting languages like bash to a high-level language such as python" (Caveat on Scale section)

---

#### Source 15: Bash shell script security best practices
- **URL:** https://www.linuxbash.sh/post/bash-shell-script-security-best-practices
- **Author/Org:** linuxbash.sh | **Date:** n/d

**Re: Security practices for untrusted input**
> "Always validate external inputs to your scripts to prevent injection and other malicious attacks." (Input Validation section)

> "When referencing variables, especially those that could potentially contain spaces or special characters, always enclose them in quotes." (Variable Quoting section)

> "Always use absolute paths to commands in scripts to avoid the risk of executing rogue scripts due to alterations in the PATH environment." (Safe Command Paths section)

> "Avoid using `eval` due to the high risk of executing arbitrary code unintentionally." (Avoiding Dangerous Functions section)

> "Run your script with the lowest privileges necessary for the task." (Privilege Restriction section)

---

### Sub-question 3: Testing frameworks and strategies

#### Source 8: Testing Bash Scripts with BATS: A Practical Guide
- **URL:** https://www.hackerone.com/blog/testing-bash-scripts-bats-practical-guide
- **Author/Org:** HackerOne | **Date:** n/d

**Re: Testing frameworks and strategies**
> "BATS is a TAP-compliant testing framework for Bash scripts. It allows you to write tests for your scripts in a straightforward and readable manner." (Definition & Purpose section)

> "BATS tests are written in Bash, so you don't need to learn a new language, and they can be run on any system with Bash and BATS installed." (Test Structure section)

> Example test structure: "run greet \"World\"" followed by assertions "[ \"$status\" -eq 0 ]" and "[ \"$output\" = \"Hello, World!\" ]" (Run Helper & Assertions section)

> "Testing edge cases is crucial." ... tests checking the script "handles empty input gracefully." (Edge Cases section)

> "Sometimes, you might need to test scripts that interact with external systems. Mocks and stubs can simulate these interactions." (Mocking/Advanced Patterns section)

---

#### Source 9: Writing tests — bats-core documentation
- **URL:** https://bats-core.readthedocs.io/en/stable/writing-tests.html
- **Author/Org:** bats-core project | **Date:** n/d

**Re: Testing frameworks and strategies**
> "Bats makes use of Bash's errexit (set -e) option when running test cases. If every command in the test case exits with a 0 status code (success), the test passes." (Key Principles section)

> "library functions and shell scripts that run many commands when they are called or executed are not amenable to efficient BATS testing. The only way to test this pile of code with sufficient coverage is to break it into many small, reusable, and, most importantly, independently testable functions." (Code Organization section)

> "The bats_pipe helper command is meant to handle piping between commands. Its main purpose is to aide the run helper command (which cannot handle pipes, due to bash parsing priority)." (Pipeline Handling section)

> "Bats can run tests in parallel, providing nearly a 40% improvement in test execution time." (Performance section)

---

#### Source 6: How to mock in Bash tests
- **URL:** https://advancedweb.hu/how-to-mock-in-bash-tests/
- **Author/Org:** Advanced Web Machinery | **Date:** n/d

**Re: Testing frameworks and strategies — mocking**
> "By using functions rather than mocks all the previously mentioned problems are solved. Functions ignore additional parameters, so there's no need to worry about the extra +%A in our case." (Function Mocking section)

> "the `export -f` is to ensure that sub-shells can also use the mock." (Function Mocking section)

> "it's still possible to mock commands by overriding the `PATH` variable, supplying custom executables." (PATH Override section)

> "a separate file has to be maintained for each mock, which makes them separated from the test cases." (PATH Override section)

> "it's really easy to test them using pipes and redirection." (Stdin/Stdout Testing section)

> "I used `printf` instead of `echo` to explicitly control the new lines. This can come in handy if the script expects multiple lines on the stdin." (Stdin/Stdout Testing section)

> "wrap low-level commands in higher-level functions that capture part of the business domain, and simply mock that." (General Strategy section)

---

#### Source 7: Writing Unit-Tests and Mocks for UNIX Shells
- **URL:** https://honeytreelabs.com/posts/writing-unit-tests-and-mocks-for-unix-shells/
- **Author/Org:** Honey Tree Labs | **Date:** n/d

**Re: Testing frameworks and strategies — mocking taxonomy**
> "According to their definition, unit tests mock every single dependency. Unit tests show where a problem might be located or, in other words, help someone to find out whether an interface behaves correctly under all circumstances." (Unit Testing Definition section)

> "Stubs: an 'empty' implementation which generally always returns hard-coded values (valid/invalid)." (Mocking Techniques section)

> "Fakes: substitutes dependencies with a simpler implementation of it." (Mocking Techniques section)

> "Mocks: allow for mimicking behavior of real implementations. The behavior is under full control of the executing unit-test." (Mocking Techniques section)

> "A function with the same name has priority over the program located in the search path, `PATH`. By always returning (echoing) the same value, the expected values of the function calls are independent of the actual time when they are executed." (Mock Implementation via Shell Functions section)

> "Using the `eval` function allows to make our mock more dynamic. It is now possible to have more than one test with `date` to behave differently, depending on the test." (Dynamic Mock Behavior section)

> "The fewer dependencies a test framework has, the easier it is to get it up and running and to execute at all." (Framework Constraints section)

---

### Sub-question 4: Readability and static analysis

#### Source 10: Shell Style Guide
- **URL:** https://google.github.io/styleguide/shellguide.html
- **Author/Org:** Google | **Date:** n/d

**Re: Readability and static analysis conventions**
> "Shell should only be used for small utilities or simple wrapper scripts." (When to Use Shell vs Other Languages section)

> "If you are writing a script that is more than 100 lines long, or that uses non-straightforward control flow logic, you should rewrite it in a more structured language _now_." (When to Use Shell section)

> "Lower-case, with underscores to separate words." (Functions — Naming Conventions section)

> "Constants and anything exported to the environment should be capitalized, separated with underscores, and declared at the top of the file." (Variables — Naming Conventions section)

> "A function called `main` is required for scripts long enough to contain at least one other function." (Function Structure section)

> Functions should include header comments describing "the intended API behaviour using: Description of the function. Globals: List of global variables used and modified. Arguments: Arguments taken. Outputs: Output to STDOUT or STDERR. Returns: Returned values." (Comments and Documentation section)

> "All error messages should go to `STDERR`." (Error Handling section)

> "Always check return values and give informative return values." (Error Handling section)

> "Maximum line length is 80 characters." (Readability Standards section)

> "Prefer `\"${var}\"` over `\"$var\"`." (Readability Standards section)

---

#### Source 11: ShellCheck — a static analysis tool for shell scripts
- **URL:** https://github.com/koalaman/shellcheck
- **Author/Org:** koalaman / ShellCheck | **Date:** n/d

**Re: Static analysis**
> "ShellCheck is a GPLv3 tool that gives warnings and suggestions for bash/sh shell scripts" (Core Purpose section)

> "Point out and clarify typical beginner's syntax issues that cause a shell to give cryptic error messages" (Primary Goals section)

> "Point out and clarify typical intermediate level semantic problems that cause a shell to behave strangely" (Primary Goals section)

> "Point out subtle caveats, corner cases and pitfalls that may cause an advanced user's otherwise working script to fail" (Primary Goals section)

> Detects: "Quoting Issues," "Conditionals," "Command Misuse," "Beginner Mistakes," "Style Improvements" including "recommends `$()` over backticks" (Detection Categories section)

> ShellCheck operates through: "online at shellcheck.net, command-line execution via `shellcheck yourscript`, editor integrations (Vim, Emacs, VSCode), and CI/CD pipeline integration." (Usage Methods section)

---

#### Source 12: Bash best practices cheat sheet
- **URL:** https://bertvv.github.io/cheat-sheets/Bash.html
- **Author/Org:** Bert Van Vreckem | **Date:** n/d

**Re: Readability and conventions**
> "Always use long parameter notation when available. This makes the script more readable, especially for lesser known/used commands that you don't remember all the options for." (Readability & Naming section)

> "Apply the Single Responsibility Principle: a function does one thing." (Conventions section)

> "Variables should always be referred to in the ${var} form (as opposed to $var)." (Conventions section)

> "Variables should always be quoted, especially if their value may contain a whitespace or separator character: \"${var}\"" (Conventions section)

> "Environment (exported) variables: ${ALL_CAPS}" and "Local variables: ${lower_case}" (Capitalization section)

> "Using functions can greatly improve readability. Principles from Clean Code apply here." (Structure section)

> "Don't mix levels of abstraction" (Structure section)

> "Abort the script on errors and undbound variables. Put the following code at the beginning of each script." — recommended approach: "set -o errexit   # abort on nonzero exitstatus / set -o nounset   # abort on unbound variable / set -o pipefail  # don't hide errors within pipes" (Error Handling section)

> "Print error messages on stderr." (Error Handling section)

---

#### Source 13: BashGuide/Practices
- **URL:** https://mywiki.wooledge.org/BashGuide/Practices
- **Author/Org:** Greg's Wiki (wooledge.org) | **Date:** n/d

**Re: Readability and conventions**
> "_Healthy whitespace gives you breathing space_. Indent your code properly and consistently. Use blank lines to separate paragraphs or logic blocks." (Readability section)

> "_Comment your way of thinking before you forget_." (Readability section)

> "_Consistency prevents mind boggles_. Be consistent in your naming style. Be consistent in your use of capitals." (Readability section)

> "First and foremost, remember to **'use more quotes'**. This will protect the strings and parameter expansions from Word Splitting and globbing." (Quoting section)

> "Almost as important as the result of your code is the **readability of your code**." (Maintainability section)

> "If you plan to continue using it, you should also plan to continue maintaining it." (Maintainability section)

> "If however you are using Bash to do your scripting... you can also use the `[[...]]` Korn-style construct... it presents several advantages over the traditional [/test command." (Test Constructs section)

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| `set -Eeuo pipefail` is universally safe as a hook preamble | [1][2][12] — T1+T5 convergence; widely recommended | `set -e` does not fire inside functions called in if-conditions; `grep` exits 1 on no-match (normal) and will trip exit-on-error | Medium — hooks using `grep`/`test` for detection will exit prematurely; `|| true` must be noted |
| bats-core is the right framework for testing hooks | [8][9] T1+T4 recommend it | Requires installation and CI setup; inline piped testing (`echo '...' \| ./hook.sh`) is zero-dependency and sufficient for many hooks | Low — bats is appropriate at scale; inline testing is adequate for simple hooks |
| `jq --arg`/`--argjson` makes JSON stdin processing safe | Multiple T5 sources; no T1/T4 source explicitly confirms the `--arg` injection-safety property | `jq` may not be installed on minimal systems; python3 stdlib `json` is more universally available | Medium — `jq` absence silently breaks the hook; always provide a python3 fallback |
| ShellCheck catches most script quality issues | [11] T1 — widely used, well-maintained | ShellCheck is static analysis only; does not catch runtime logic errors (wrong jq path, wrong exit intent, pipe buffer overflow) | Medium — ShellCheck passing ≠ correct behavior; testing is required alongside static analysis |

### Premortem

Assume main conclusion is wrong. Three reasons it could fail:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Safety flags create brittle hooks: `set -e` exits on `grep`'s normal non-zero return when no match found — common in detection hooks | HIGH | Qualifies safety flag finding: must document `|| true` and `grep -q ... || :` patterns as mandatory companions to `set -e` |
| Unit testing recommendations miss the hook integration boundary: bats tests can pass while hooks fail on real Claude Code JSON payloads (field shape changes, missing fields, large payloads) | MEDIUM | Qualifies testing finding: recommend testing with real payload templates, not just mocked stubs |
| Security guidance targets wrong threat model: `tool_input` values (file paths, commands) passed through Claude Code ARE user-influenced data and flow through hooks — injection prevention matters for these fields, not just external stdin | LOW | Confirms finding #2 is correctly scoped; adds specificity: the `tool_input.command` field in Bash hooks contains user-influenced data |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | `set -Eeuo pipefail` is the canonical safety preamble | attribution | [1][2][12] | verified |
| 2 | `-E` propagates ERR traps into subshells | attribution | [2] | verified |
| 3 | `grep` exits 1 when a pattern is not found (normal POSIX behavior) | attribution | — | verified |
| 4 | bats-core is the primary bash testing framework | superlative | [8][9] | corrected (source says "a testing framework"; shunit2 and shellspec also exist — changed to "most widely documented") |
| 5 | bats is TAP-compliant | attribution | [8] | verified |
| 6 | Google style: lower_case for functions/locals, UPPER_CASE for exported | attribution | [10] | verified |
| 7 | Google style: maximum 80-character lines | attribution | [10] | verified |
| 8 | ShellCheck is the authoritative static analysis tool | superlative | [11] | verified (de facto standard; not a formal standards body) |
| 9 | `export -f` makes function mocks visible to subshells | attribution | [6] | verified |

## Limitations and Gaps

- No T1 source found for jq injection safety with `--arg` specifically; the jq project documentation itself would be the right source
- Testing in CI (GitHub Actions, pre-commit hooks) for bash scripts was not covered — a follow-up on bats-core CI integration would complete the testing picture
- Portability (sh vs bash) was not deeply covered; all findings assume bash as the target
- Dates are unavailable for 13 of 15 sources; currency of advice cannot be confirmed beyond content review

## Search Protocol

11 searches across 4 sub-questions, all via Google. 110 results found; 25 used across 15 sources.

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| bash shell script safety flags set -euo pipefail error handling best practices | google | all | 10 | 3 |
| bash errexit nounset pipefail silent failure prevention shell scripting | google | all | 10 | 2 |
| bash trap ERR EXIT error handling pattern shell script cleanup | google | all | 10 | 2 |
| bash shell script security JSON stdin processing injection prevention best practices | google | all | 10 | 3 |
| jq shell script JSON parsing security untrusted input command injection prevention | google | all | 10 | 2 |
| bash read JSON stdin safely shell script jq --raw-output variable quoting security | google | all | 10 | 2 |
| bats-core bash automated testing framework shell scripts best practices 2024 | google | all | 10 | 3 |
| shell script testing strategies shunit2 bats unit test stdin mock | google | all | 10 | 3 |
| shellcheck static analysis bash script linting rules best practices | google | all | 10 | 2 |
| bash shell script style guide naming conventions Google readability maintainability | google | all | 10 | 3 |
| bash script readability functions small composable single responsibility shell scripting | google | all | 10 | 3 |

Not searched: POSIX sh portability, heredoc patterns, shellspec BDD framework deep dive, bash exit code conventions.
