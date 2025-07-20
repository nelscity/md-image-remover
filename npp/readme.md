# Markdown Cleaner for Notepad++

A Python script for Notepad++ that automatically cleans and formats Markdown documents by removing artifacts, converting special characters, and checking for common formatting issues.

## Features

- **Remove image references**: Cleans up broken image links like `![]][image1]` and `[image1]: url`
- **Remove page numbers**: Eliminates page number artifacts from PDFs (e.g., "Page 5", "Page 12 of 35", "p. 5")
- **Convert bullet characters**: Transforms Unicode bullets (•, ▪, ►, etc.) into standard markdown dashes (-)
- **Fix list formatting**: Removes unnecessary blank lines between list items
- **Clean whitespace**: Removes double spaces throughout the document
- **Markdown linting**: Checks for common markdown issues and reports them with line numbers

## Requirements

- Notepad++ (any recent version)
- Python Script plugin for Notepad++

## Installation

### Step 1: Install Python Script Plugin

1. Open Notepad++
2. Go to `Plugins` → `Plugins Admin`
3. Search for "Python Script"
4. Check the box next to "Python Script" and click `Install`
5. Restart Notepad++ when prompted

### Step 2: Add the Script

1. In Notepad++, go to `Plugins` → `Python Script` → `New Script`
2. Enter a filename (e.g., `mdcleaner.py`)
3. Copy and paste the script content
4. Save the file

### Step 3: Create a Keyboard Shortcut (Optional)

1. Go to `Plugins` → `Python Script` → `Configuration`
2. In the "User Scripts" section, select your script
3. Click `Add` to add it to the menu
4. Click `OK`
5. Go to `Settings` → `Shortcut Mapper`
6. Click on the `Plugin commands` tab
7. Find your script in the list
8. Double-click and assign a shortcut (e.g., `Ctrl+Alt+M`)

## Usage

### Basic Usage

1. Open your Markdown file in Notepad++
2. Run the script using one of these methods:
   - Go to `Plugins` → `Python Script` → `Scripts` → `mdcleaner`
   - Use your keyboard shortcut if configured
3. A console window will appear showing the cleaning progress
4. Your document will be automatically updated

### What the Script Does

The script performs these operations in order:

1. **Removes image references**
   - Before: `Here is an image ![]][image1] in the text`
   - After: `Here is an image  in the text`

2. **Removes page numbers** (optional)
   - Before: `Some text\nPage 5\nMore text`
   - After: `Some text\nMore text`

3. **Converts bullet characters**
   - Before: `• First item\n• Second item`
   - After: `- First item\n- Second item`

4. **Removes blank lines between list items**
   - Before: `- Item 1\n\n- Item 2`
   - After: `- Item 1\n- Item 2`

5. **Removes double spaces**
   - Before: `This  has  double  spaces`
   - After: `This has double spaces`

6. **Runs markdown linting** and reports issues

## Configuration

### Using the Alternative Configuration Function

The script includes two main functions:

- `main()` - Runs all operations by default
- `main_with_options()` - Allows customization

To use custom options:

1. Edit the script file
2. At the bottom, change:
   ```python
   if __name__ == '__main__':
       main()  # Change this to main_with_options()
   ```

3. In `main_with_options()`, modify these settings:
   ```python
   REMOVE_PAGE_NUMBERS = True  # Set to False to keep page numbers
   RUN_LINTER = True          # Set to False to skip linting
   ```

## Linting Rules

The script checks for these markdown issues:

- **MD009**: Trailing whitespace at end of lines
- **MD012**: Multiple consecutive blank lines
- **MD018**: No space after hash in headings (e.g., `#Heading`)
- **MD019**: Multiple spaces after hash in headings
- **MD025**: Multiple top-level headings in the same document
- **MD026**: Trailing punctuation in headings
- **MD030**: Wrong number of spaces after list markers
- **MD032**: Lists not surrounded by blank lines
- **MD033**: Inline HTML detected
- **MD041**: First line should be a top-level heading
- **MD047**: File should end with a single newline

Note: Line length checking (MD013) has been disabled as it's often not relevant for markdown files.

## Console Output Example

```
Starting Markdown cleanup...
1. Removing image references...
2. Removing page numbers...
3. Converting bullet characters...
4. Removing blank lines between list items...
5. Removing double spaces...
6. Document updated!

Running Markdown linter...
Found 3 linting issues:
--------------------------------------------------
Line 5: MD019 - Multiple spaces after hash on heading
Line 23: MD009 - Trailing whitespace
Line 45: MD030 - Should have 1 space after list marker (found 2)

Markdown cleanup completed!
```

## Tips

1. **Backup your files**: While the script is safe, it's always good practice to backup important documents
2. **Review linting issues**: The linter helps identify formatting problems but doesn't fix them automatically
3. **Page number removal**: This feature is aggressive and removes entire lines containing page numbers. Review the results if your document has legitimate uses of the word "Page"
4. **Unicode support**: The script handles Unicode bullet characters properly in documents

## Troubleshooting

### "No content to process!"
- Make sure you have a document open in Notepad++ before running the script

### Encoding errors
- The script includes UTF-8 encoding support. If you still have issues, ensure your document is saved with UTF-8 encoding

### Script doesn't appear in menu
- Make sure you've added it via `Plugins` → `Python Script` → `Configuration`
- Restart Notepad++ after adding the script

### Console window doesn't appear
- The console should auto-show, but you can manually open it via `Plugins` → `Python Script` → `Show Console`

## Limitations

- The script modifies the document directly (no undo for the entire operation)
- Page number removal might be overly aggressive in some cases
- Linting only reports issues, it doesn't auto-fix them

## Version Info

- Compatible with Notepad++ Python Script plugin (Python 2.7)
- Last updated: 2024