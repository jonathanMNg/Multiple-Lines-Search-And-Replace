# Multiple-Lines-Search-And-Replace

## Introduction
This is a python program that can search and replace string in one or more files in a target file or location.
It can also make a backup before modify the file(s)
## Requirements
- `python3.6`

## Installation
Clone or download this repository

## Usage
In your terminal or command-line, type:
```
python3 search_and_replace.py target_location search_string[file] replace_string[file] target_file_extension[php|txt|html|...]
```
Then follow the prompt and enter your choice
## Example

- `target_location`: `tmp/`
- `search_string`: `old_string.txt`
- `replace_string`: `new_string.txt`
- `target_file_extension`: `php`

### Run:
```
python3 search_and_replace3.py tmp/ old_string.txt new_string.txt php
```
### Output:
```
- - - - - - - - - - - - - - - - - - - - -
Old string:
<script>
$.example('testing')
</script>
- - - - - - - - - - - - - - - - - - - - -
New string:
<?php require_once('../footer.php');?>
- - - - - - - - - - - - - - - - - - - - -
Target files:
tmp/index.php
tmp/non-effected-file.php
tmp/index2.php
Are these information all correct? (y/N) y
Do you want to create a backup for your modified files? (y/N) y
Modified files:
tmp/index.php
tmp/index2.php
```
**Original `index.php`**
```
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Sample</title>
</head>
<body>

</body>
</html>
<script>
$.example('testing')
</script>
<p></p>

```
**Modified `index.php`***
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Sample</title>
</head>
<body>
</body>
</html>
<?php require_once('../footer.php');?>
<p></p>
```
