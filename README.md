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


This script categorizes files based on their extensions and moves them to specific directories:

    Image files (e.g., JPG, PNG, GIF) are placed in the image directory.
    Document files (e.g., DOC, PDF, XLS) are placed in the document directory.
    Ebook files (e.g., EPUB, MOBI, AZW) are placed in the ebook directory.
    Substance files (e.g., SBSAR, SBS) are placed in the substance directory.
    Brush files (e.g., ABR, BRUSH) are placed in the brush directory.
    Font files (e.g., TTF, OTF) are placed in the font directory.
    3D model files (e.g., FBX, OBJ, STL) are placed in the 3D model directory.
    Executable files (e.g., EXE, MSI, BAT) are placed in the executable directory.
    DaVinci Resolve files (e.g., SETTING) are placed in the DaVinci Resolve directory.
    After Effects files (e.g., AEP, JSX) are placed in the After Effects directory.
    Unity package files (e.g., UNITYPACKAGE) are placed in the Unity directory.
    ZBrush files (e.g., ZMT, ZPR) are placed in the ZBrush directory.
    Unreal Engine assets (e.g., UASSET, UPLUGIN) are placed in the Unreal Engine directory.
    Mockup files (PSD and TXT) are placed in the mockup directory.
