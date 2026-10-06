# 07 — Terminal Cleanliness & 42-Style Minimalism

1. **Zero Terminal Spam**: Commands like `make install` must hide verbose output and display a clean single-line progress indicator (`\r`).
2. **Error Visibility**: When any command fails, logs must be immediately dumped to stdout for rapid debugging.
3. **Clean Feedback**: Success states must report concise, actionable feedback with ANSI colors.
