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

# File Categorization and Destination Directories

This script organizes files based on their extensions and moves them to specific directories.

## Categories and Destinations

- **Image Files** (`.jpg`, `.png`, `.gif`, etc.) → `images/`
- **Document Files** (`.doc`, `.pdf`, `.xls`, etc.) → `documents/`
- **Ebook Files** (`.epub`, `.mobi`, `.azw`, etc.) → `ebooks/`
- **Substance Files** (`.sbsar`, `.sbs`, etc.) → `substance/`
- **Brush Files** (`.abr`, `.brush`, etc.) → `brushes/`
- **Font Files** (`.ttf`, `.otf`, `.woff`, etc.) → `fonts/`
- **3D Model Files** (`.fbx`, `.obj`, `.stl`, etc.) → `3d_models/`
- **Executable Files** (`.exe`, `.msi`, `.bat`, etc.) → `executables/`
- **DaVinci Resolve Files** (`.setting`) → `davinci_resolve/`
- **After Effects Files** (`.aep`, `.jsx`, etc.) → `after_effects/`
- **Unity Package Files** (`.unitypackage`) → `unity/`
- **ZBrush Files** (`.zmt`, `.zpr`, etc.) → `zbrush/`
- **Unreal Engine Assets** (`.uasset`, `.umap`, etc.) → `unreal_engine/`
- **Mockup Files** (`.psd`, `.txt`) → `mockups/`
