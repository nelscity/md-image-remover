# -*- coding: utf-8 -*-
# Markdown Cleaner for Notepad++ Python Script Plugin
# Installation:
# 1. Install Python Script plugin via Plugins Admin in Notepad++
# 2. Go to Plugins > Python Script > New Script
# 3. Save this script with a name like "MarkdownCleaner.py"
# 4. Run via Plugins > Python Script > Scripts > MarkdownCleaner

import re
from Npp import editor, notepad, console

def process_remove_images(text):
    """Remove image references and definitions"""
    # Remove inline image references like ![]][image1]
    text = re.sub(r'!\[\]\[image\d+\]', '', text)
    # Remove image definitions like [image1]: url
    text = re.sub(r'^\[image\d+\]:.*$', '', text, flags=re.MULTILINE)
    return text

def process_remove_page_numbers(text):
    """Remove entire lines containing page numbers"""
    # Remove lines with "Page X" or "Page X of Y" patterns
    text = re.sub(r'^.*\bPage\s+\d+(?:\s+of\s+\d+)?.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove lines with "p. X", "p.X", "pp. X-Y" patterns
    text = re.sub(r'^.*\bp\.?\s*\d+(?:\s*-\s*\d+)?.*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Remove standalone "X of Y" patterns
    text = re.sub(r'^\s*\d+\s+of\s+\d+\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Clean up multiple consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def process_remove_double_spaces(text):
    """Remove double spaces recursively"""
    previous_text = None
    while text != previous_text:
        previous_text = text
        text = text.replace('  ', ' ')
    return text

def process_remove_list_spacing(text):
    """Remove blank lines between consecutive list items"""
    lines = text.split('\n')
    processed_lines = []
    
    i = 0
    while i < len(lines):
        current_line = lines[i]
        
        # Check if we need to look ahead
        if i + 2 < len(lines):
            next_line = lines[i + 1]
            line_after_next = lines[i + 2]
            
            # Check if current line is a list item
            is_current_list = bool(re.match(r'^\s*[-*+]\s', current_line) or 
                                  re.match(r'^\s*\d+\.\s', current_line))
            
            # Check if line after next is a list item
            is_line_after_next_list = bool(re.match(r'^\s*[-*+]\s', line_after_next) or 
                                          re.match(r'^\s*\d+\.\s', line_after_next))
            
            # If pattern matches, skip the blank line
            if is_current_list and next_line == '' and is_line_after_next_list:
                # Get indentation levels
                current_indent = re.match(r'^(\s*)', current_line).group(1)
                future_indent = re.match(r'^(\s*)', line_after_next).group(1)
                
                if current_indent == future_indent:
                    processed_lines.append(current_line)
                    i += 2  # Skip the blank line
                    continue
        
        processed_lines.append(current_line)
        i += 1
    
    return '\n'.join(processed_lines)

def process_convert_bullets(text):
    """Convert various bullet characters to markdown dash lists"""
    lines = text.split('\n')
    processed_lines = []
    
    # Bullet characters to convert (using Unicode escape sequences for Python 2.7)
    bullet_chars = u'[•▪▫‣◦⁃∙◆◇►▶▷▻]'
    
    for line in lines:
        # Ensure line is Unicode for Python 2.7
        if isinstance(line, str):
            line = line.decode('utf-8', 'ignore')
        
        if re.search(bullet_chars, line):
            # Get initial indentation
            indent_match = re.match(r'^(\s*)', line)
            initial_indent = indent_match.group(1) if indent_match else ''
            
            # Split on bullet characters and process
            parts = re.split(bullet_chars, line)
            parts = [part.strip() for part in parts if part.strip()]
            
            # Convert each part to a markdown list item
            for part in parts:
                if part:
                    processed_lines.append(u"{0}- {1}".format(initial_indent, part))
        else:
            processed_lines.append(line)
    
    # Join and encode back to UTF-8 for Python 2.7
    result = '\n'.join(processed_lines)
    if isinstance(result, unicode):
        result = result.encode('utf-8')
    return result

def lint_markdown(text):
    """Run basic markdown linting and return issues"""
    issues = []
    lines = text.split('\n')
    
    h1_count = 0
    first_non_empty_found = False
    first_non_empty_line = -1
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Track first non-empty line for MD041
        if not first_non_empty_found and line.strip():
            first_non_empty_found = True
            first_non_empty_line = line_num
        
        # MD009: Trailing spaces
        if line.endswith(' ') and line.strip():
            issues.append("Line {0}: MD009 - Trailing whitespace".format(line_num))
        
        # MD012: Multiple consecutive blank lines
        if i > 0 and i < len(lines) - 1:
            if line == '' and lines[i-1] == '' and lines[i+1] == '':
                issues.append("Line {0}: MD012 - Multiple consecutive blank lines".format(line_num))
        
        # MD018: No space after hash on heading
        if re.match(r'^#+[^\s#]', line):
            issues.append("Line {0}: MD018 - No space after hash on heading".format(line_num))
        
        # MD019: Multiple spaces after hash on heading
        if re.match(r'^#+\s{2,}', line):
            issues.append("Line {0}: MD019 - Multiple spaces after hash on heading".format(line_num))
        
        # MD013: Line length check removed per user preference
        # (line length checking disabled)
        
        # MD025: Track multiple top level headings
        if re.match(r'^#\s', line):
            h1_count += 1
        
        # MD026: Trailing punctuation in heading
        if re.match(r'^#+\s.*[\.,:;!]$', line):
            issues.append("Line {0}: MD026 - Trailing punctuation in heading".format(line_num))
        
        # MD030: Spaces after list markers
        list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s*', line)
        if list_match and line.strip():
            spaces_after = len(list_match.group(0)) - len(list_match.group(1)) - len(list_match.group(2))
            if spaces_after != 1:
                issues.append("Line {0}: MD030 - Should have 1 space after list marker (found {1})".format(line_num, spaces_after))
        
        # MD033: Inline HTML
        if re.search(r'<[^>]+>', line) and not re.search(r'<!--.*-->', line):
            issues.append("Line {0}: MD033 - Inline HTML detected".format(line_num))
    
    # MD025: Report multiple H1s
    if h1_count > 1:
        issues.append("MD025 - Multiple top level headings ({0} found)".format(h1_count))
    
    # MD041: First line should be top level heading
    if first_non_empty_line > 0 and lines[first_non_empty_line - 1].strip():
        if not re.match(r'^#\s', lines[first_non_empty_line - 1]):
            issues.append("Line {0}: MD041 - First line should be a top level heading".format(first_non_empty_line))
    
    # MD047: File should end with newline
    if lines and lines[-1] != '':
        issues.append("Line {0}: MD047 - File should end with a single newline".format(len(lines)))
    
    return issues

def main():
    """Main function to clean markdown"""
    console.show()
    console.clear()
    
    # Get current document text
    text = editor.getText()
    
    if not text.strip():
        console.write("No content to process!\n")
        return
    
    console.write("Starting Markdown cleanup...\n")
    
    # Step 1: Remove images
    console.write("1. Removing image references...\n")
    text = process_remove_images(text)
    
    # Step 2: Ask about page numbers
    # Note: Notepad++ Python Script doesn't have built-in dialogs, 
    # so we'll include this step by default. You can comment it out if not needed.
    console.write("2. Removing page numbers...\n")
    text = process_remove_page_numbers(text)
    
    # Step 3: Convert bullets
    console.write("3. Converting bullet characters...\n")
    text = process_convert_bullets(text)
    
    # Step 4: Remove list spacing
    console.write("4. Removing blank lines between list items...\n")
    text = process_remove_list_spacing(text)
    
    # Step 5: Remove double spaces
    console.write("5. Removing double spaces...\n")
    text = process_remove_double_spaces(text)
    
    # Step 6: Update the document
    editor.setText(text.strip())
    console.write("6. Document updated!\n\n")
    
    # Step 7: Run linter
    console.write("Running Markdown linter...\n")
    issues = lint_markdown(text)
    
    if issues:
        console.write("Found {0} linting issues:\n".format(len(issues)))
        console.write("-" * 50 + "\n")
        for issue in issues:
            console.write(issue + "\n")
    else:
        console.write("\nNo linting issues found!\n")
    
    console.write("\nMarkdown cleanup completed!\n")

# Configuration function for optional features
def main_with_options():
    """Alternative main function with configuration options"""
    console.show()
    console.clear()
    
    text = editor.getText()
    if not text.strip():
        console.write("No content to process!\n")
        return
    
    # Configuration options (modify these as needed)
    REMOVE_PAGE_NUMBERS = True  # Set to False to skip page number removal
    RUN_LINTER = True          # Set to False to skip linting
    
    console.write("Markdown Cleaner Configuration:\n")
    console.write("- Remove page numbers: {0}\n".format('Yes' if REMOVE_PAGE_NUMBERS else 'No'))
    console.write("- Run linter: {0}\n".format('Yes' if RUN_LINTER else 'No'))
    console.write("-" * 50 + "\n\n")
    
    # Always remove images
    text = process_remove_images(text)
    
    # Conditionally remove page numbers
    if REMOVE_PAGE_NUMBERS:
        text = process_remove_page_numbers(text)
    
    # Always do these steps
    text = process_convert_bullets(text)
    text = process_remove_list_spacing(text)
    text = process_remove_double_spaces(text)
    
    # Update document
    editor.setText(text.strip())
    
    # Conditionally run linter
    if RUN_LINTER:
        issues = lint_markdown(text)
        if issues:
            console.write("\nFound {0} linting issues:\n".format(len(issues)))
            for issue in issues:
                console.write(issue + "\n")
        else:
            console.write("\nNo linting issues found!\n")
    
    console.write("\nMarkdown cleanup completed!\n")

# Run the main function
if __name__ == '__main__':
    main()  # or use main_with_options() for configurable behavior