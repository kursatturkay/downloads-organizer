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

- **Image Files** (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`, `.psd`, `.ico`, `.raw`, `.cr2`, `.nef`, `.heic`, `.heif`, `.ai`, `.eps`, `.dds`, `.tga`, `.exr`) → `__images__`
- **Document Files** (`.doc`, `.docx`, `.pdf`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.txt`, `.rtf`) → `__documents__`
- **Ebook Files** (`.epub`, `.mobi`, `.azw`, `.azw3`, `.fb2`, `.lrf`, `.tcr`, `.lit`) → `__ebooks__`
- **Substance Files** (`.sbsar`, `.sbs`, `.sbsprs`, `.sbsasm`, `.sbsm`, `.spsm`) → `__substance__`
- **Brush Files** (`.abr`, `.tpl`, `.brushset`, `.brush`, `.atn`) → `__brushes__`
- **Font Files** (`.ttf`, `.otf`, `.woff`, `.woff2`, `.eot`) → `__fonts__`
- **3D Model Files** (`.fbx`, `.obj`, `.3ds`, `.dae`, `.stl`, `.ply`, `.glb`, `.gltf`, `.abc`, `.usd`, `.usda`, `.usdc`, `.x3d`) → `__3d_models__`
- **Executable Files** (`.exe`, `.msi`, `.app`, `.bat`, `.cmd`) → `__executables__`
- **DaVinci Resolve Files** (`.setting`) → `__davinci_resolve__`
- **After Effects Files** (`.aep`, `.aepx`, `.aet`, `.ffx`, `.jsx`, `.jsxbin`) → `__after_effects__`
- **Unity Package Files** (`.unitypackage`) → `__unity__`
- **ZBrush Files** (`.zmt`, `.zsc`, `.zpr`, `.zbr`, `.ztl`, `.zb`, `.zpz`, `.zpk`, `.zprj`, `.zdl`) → `__zbrush__`
- **Unreal Engine Assets** (`.uasset`, `.uplugin`, `.umap`, `.uproject`) → `__unreal_engine__`
- **Mockup Files** (`.psd`, `.txt`) → `__mockups__`

