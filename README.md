# downloads-organizer
Categorizes files by type and moves them to relevant directories

1. Categorizes files by type and moves them to relevant directories
2. Identifies and moves ALL empty directories in the working folder to the recycle bin
3. Supports multiple archive formats (ZIP, RAR, 7z) and analyzes their contents
4. Detects specialized file types including fonts, ZBrush files, ZMT files, etc.

Required Libraries:
- rarfile: For opening RAR archives ('pip install rarfile')
- py7zr: For opening 7z archives ('pip install py7zr')
- send2trash: For moving empty folders to recycle bin ('pip install send2trash')

Note: If send2trash is not available, empty folders will be deleted directly.

usage: copy py file in downloads directory. and run it.
