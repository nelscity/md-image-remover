// script.js

document.addEventListener('DOMContentLoaded', () => {
    const removeImagesBtn = document.getElementById('removeImagesBtn');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
  
    removeImagesBtn.addEventListener('click', () => {
      // Grab original Markdown
      let text = inputText.value;
  
      // Remove inline references: ![][imageX]
      // This pattern looks for "![]["image" followed by any number] and closes bracket
      text = text.replace(/!\[\]\[image\d+\]/g, '');
  
      // Remove reference lines: [imageX]: ...
      // This pattern looks for lines starting with [image<number>]: plus the rest of the line
      text = text.replace(/^\[image\d+\]:.*$/gm, '');
  
      // Output the stripped text
      outputText.value = text.trim();
    });
  });
  