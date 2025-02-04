// script.js

document.addEventListener('DOMContentLoaded', () => {
    const removeImagesBtn = document.getElementById('removeImagesBtn');
    const copyToClipboardBtn = document.getElementById('copyToClipboardBtn');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
  
    removeImagesBtn.addEventListener('click', () => {
      let text = inputText.value;
  
      // Remove inline references: ![][imageX]
      text = text.replace(/!\[\]\[image\d+\]/g, '');
  
      // Remove reference lines: [imageX]: ...
      text = text.replace(/^\[image\d+\]:.*$/gm, '');
  
      // Set the processed text to the output textarea
      outputText.value = text.trim();
    });
  
    copyToClipboardBtn.addEventListener('click', () => {
      // Write the processed text to the clipboard
      const processedText = outputText.value;
      
      // Check if there's something to copy
      if (!processedText) {
        alert("There's no processed text to copy!");
        return;
      }
  
      // Use the Clipboard API (requires a secure context: HTTPS or localhost)
      navigator.clipboard.writeText(processedText)
        .then(() => {
          alert("Copied processed text to clipboard!");
        })
        .catch(err => {
          console.error("Failed to copy text: ", err);
          alert("Error copying to clipboard. See console for details.");
        });
    });
  });
  