import ChatInput from "@/components/chat/ChatInput";
import ChatBubble from "@/components/chat/ChatBubble";

const testMarkdown = `# Heading 1
## Heading 2
### Heading 3

This is a paragraph with **bold text**, *italic text*, and ***bold italic***. You can also use ~~strikethrough~~.

Here's a [link to Google](https://google.com) and an auto-link: https://github.com

---

### Lists

Unordered list:
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3

Ordered list:
1. First item
2. Second item
3. Third item

Task list:
- [x] Completed task
- [ ] Incomplete task
- [ ] Another task
`;

const testCodeBlocks = `### Code Examples

Inline code: Use \`console.log()\` to debug.

JavaScript with syntax highlighting:
\`\`\`javascript
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

const result = fibonacci(10);
console.log(\`Fibonacci(10) = \${result}\`);
\`\`\`

Python example:
\`\`\`python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

print(quicksort([3, 6, 8, 10, 1, 2, 1]))
\`\`\`

Code block without language:
\`\`\`
This is a plain code block
without any syntax highlighting
\`\`\`
`;

const testMath = `### Math Equations (LaTeX)

Inline math: The quadratic formula is $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$

Block math equations:

$$
\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}
$$

$$
\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}
$$

Einstein's famous equation: $E = mc^2$

Matrix example:
$$
\\begin{pmatrix}
a & b \\\\
c & d
\\end{pmatrix}
\\begin{pmatrix}
x \\\\
y
\\end{pmatrix}
=
\\begin{pmatrix}
ax + by \\\\
cx + dy
\\end{pmatrix}
$$
`;

const testTables = `### GFM Tables

| Feature | Status | Priority |
|---------|--------|----------|
| Markdown | ✅ Done | High |
| Code Blocks | ✅ Done | High |
| Math/LaTeX | ✅ Done | Medium |
| Tables | ✅ Done | Medium |
| Raw HTML | ✅ Done | Low |

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left | Center | Right |
| Text | Text | Text |
| More | Data | Here |
`;

const testBlockquotes = `### Blockquotes

> This is a blockquote. It can span multiple lines and is useful for quoting text or highlighting important information.

> **Nested blockquote:**
> > This is a nested blockquote inside another blockquote.
> > It demonstrates multiple levels of quoting.

> "The only way to do great work is to love what you do." - Steve Jobs
`;

const testHtml = `### Raw HTML Support

<details>
<summary>Click to expand</summary>

This content is hidden by default and can be revealed by clicking the summary.

- Hidden item 1
- Hidden item 2

</details>

<mark>This text is highlighted using HTML mark tag.</mark>

<sub>Subscript text</sub> and <sup>Superscript text</sup>
`;

export default function Page() {
  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      <ChatInput />

      {/* User message test */}
      <ChatBubble
        message="Hello, this is a test message. I'm adding more text here to make this message longer for testing purposes. This should help verify how the chat bubble handles longer content and text wrapping behavior."
        isUser={true}
        attachments={[{ name: "document.pdf", id: "/files/document.pdf" }, { name: "image.png", id: "/files/image.png" }]}
      />

      {/* Loading state test */}
      <ChatBubble loading />

      {/* Basic Markdown test */}
      <ChatBubble message={testMarkdown} />

      {/* Code blocks test */}
      <ChatBubble message={testCodeBlocks} />

      {/* Math/LaTeX test */}
      <ChatBubble message={testMath} />

      {/* Tables test */}
      <ChatBubble message={testTables} />

      {/* Blockquotes test */}
      <ChatBubble message={testBlockquotes} />

      {/* Raw HTML test */}
      <ChatBubble message={testHtml} />
    </div>
  );
}