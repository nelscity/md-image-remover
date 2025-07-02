// script.js – enhanced with page-number removal, Markdown linting, and robust library handling

/**
 * Utilities provided:
 *  1. Remove image references            (button: #removeImagesBtn)
 *  2. Remove page‑number artefacts       (button: #removePageNumbersBtn)
 *  3. Lint Markdown with markdownlint    (button: #lintMarkdownBtn)
 *  4. Copy the processed text to clipboard (button: #copyToClipboardBtn)
 *
 *  External dependency for #3 (place **before** this script):
 *      <script src="https://cdn.jsdelivr.net/npm/markdownlint-cli@0.45.0/markdownlint.min.js"></script>
 *
 *  That bundle exposes a global `markdownlint` object which offers
 *  either a synchronous API (`markdownlint.sync`) or an async Promise
 *  API (`markdownlint.lint`). This script detects what’s available at
 *  runtime.
 */

document.addEventListener('DOMContentLoaded', () => {
  /* ───────────────────────────────────────────────────────── Buttons */
  const removeImagesBtn      = document.getElementById('removeImagesBtn');
  const removePageNumbersBtn = document.getElementById('removePageNumbersBtn');
  const lintMarkdownBtn      = document.getElementById('lintMarkdownBtn');
  const copyToClipboardBtn   = document.getElementById('copyToClipboardBtn');

  /* ───────────────────────────────────────────────────────── Textareas */
  const inputText  = document.getElementById('inputText');
  const outputText = document.getElementById('outputText');

  const writeOutput = (text) => {
    outputText.value = text.trim();
  };

  /* ───────────────────────────────────────────────────────── Img removal */
  const removeImages = () => {
    let text = inputText.value;
    text = text.replace(/!\[\]\[image\d+\]/g, '');     // inline refs
    text = text.replace(/^\[image\d+\]:.*$/gm, '');      // definitions
    writeOutput(text);
  };

  /* ───────────────────────────────────────────────────────── Page‑numbers */
  const removePageNumbers = () => {
    let text = inputText.value;
    text = text.replace(/^[ \t]*Page[ \t]+\d+(?:[ \t]+of[ \t]+\d+)?[ \t]*$/gim, '');
    text = text.replace(/\n{3,}/g, '\n\n');
    writeOutput(text);
  };

  /* ───────────────────────────────────────────────────────── Lint */
  const lintMarkdown = async () => {
    const text = (outputText.value || inputText.value || '').trim();
    if (!text) { alert('No Markdown content found to lint.'); return; }

    const md = window.markdownlint;
    if (!md) {
      alert('markdownlint library not loaded – ensure the CDN script is before script.js');
      return;
    }

    const options = { strings: { doc: text }, config: { default: true } };
    let results = null;

    try {
      // Prefer sync API if present (fast & simple)
      if (typeof md.sync === 'function') {
        results = md.sync(options);
      } else if (typeof md.lintSync === 'function') {
        results = md.lintSync(options);
      } else if (typeof md.lint === 'function') {
        // markdownlint-cli browser build exposes an async .lint() returning a Promise
        results = await md.lint(options);
      } else {
        alert('markdownlint API not found (expected sync, lintSync, or lint).');
        return;
      }
    } catch (err) {
      console.error('markdownlint failed:', err);
      alert('An error occurred while linting. See console for details.');
      return;
    }

    const errors = results.doc || [];
    if (errors.length === 0) {
      alert('✅ No Markdown issues found!');
    } else {
      const message = errors
        .map(e => `Line ${e.lineNumber}: ${e.ruleNames.join('/')}` +
                  ` — ${e.ruleDescription}`)
        .join('\n');
      alert(`Markdown issues found:\n\n${message}`);
    }
  };

  /* ───────────────────────────────────────────────────────── Clipboard */
  const copyToClipboard = () => {
    const processedText = outputText.value.trim();
    if (!processedText) { alert("There's no processed text to copy!"); return; }

    navigator.clipboard.writeText(processedText)
      .then(() => alert('Copied processed text to clipboard!'))
      .catch(err => { console.error('Failed to copy:', err); alert('Error copying text.'); });
  };

  /* ───────────────────────────────────────────────────────── Event binds */
  removeImagesBtn?.addEventListener('click', removeImages);
  removePageNumbersBtn?.addEventListener('click', removePageNumbers);
  lintMarkdownBtn?.addEventListener('click', lintMarkdown);
  copyToClipboardBtn?.addEventListener('click', copyToClipboard);
});
