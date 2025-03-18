"""
File Organization and Directory Cleanup Script
--------------------------

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


    
This script:
1. Categorizes files by type and moves them to relevant directories
2. Identifies and moves ALL empty directories in the working folder to the recycle bin
3. Supports multiple archive formats (ZIP, RAR, 7z) and analyzes their contents
4. Detects specialized file types including fonts, ZBrush files, ZMT files, etc.

Required Libraries:
- rarfile: For opening RAR archives ('pip install rarfile')
- py7zr: For opening 7z archives ('pip install py7zr')
- send2trash: For moving empty folders to recycle bin ('pip install send2trash')

Note: If send2trash is not available, empty folders will be deleted directly.
"""
import os
import zipfile
import rarfile
import shutil
import tempfile
import sys

# Set terminal output to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Get the directory where the script is located (instead of os.getcwd())
script_directory = os.path.dirname(os.path.abspath(__file__))

# Check if py7zr is available for 7z support
try:
    import py7zr
    SUPPORT_7Z = True
    print("py7zr library found. 7z archives will be processed.")
except ImportError:
    SUPPORT_7Z = False
    print("Note: Install 'py7zr' library to process 7z archives.")
    print("To install: pip install py7zr")


def create_target_directory(directory):
    """Create the target directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created: {directory}")


def debug_archive(archive_path):
    """Thoroughly debug an archive by extracting and listing all files."""
    print(f"\n--- DEBUGGING ARCHIVE: {archive_path} ---")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract archive based on type
        try:
            if archive_path.lower().endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.rar'):
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    rar_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.7z') and SUPPORT_7Z:
                with py7zr.SevenZipFile(archive_path, mode='r') as sz_ref:
                    sz_ref.extractall(temp_dir)
                    
            # List all files recursively
            print("Full listing of extracted contents:")
            for root, dirs, files in os.walk(temp_dir):
                rel_path = os.path.relpath(root, temp_dir)
                if rel_path == '.':
                    path_prefix = ""
                else:
                    path_prefix = rel_path + "/"
                    
                for file in files:
                    print(f"  {path_prefix}{file}")
                    
            print("--- END DEBUG ---\n")
        except Exception as e:
            print(f"Error debugging archive: {e}")


def contains_file_in_archive_zip(archive_path, file_extensions, archive_extensions):
    """Check if a ZIP archive contains files with specific extensions, including in subdirectories."""
    try:
        print(f"Examining zip archive: {archive_path}")
        with zipfile.ZipFile(archive_path, 'r') as archive_file:
            file_list = archive_file.namelist()
            
            # Log file list information
            print(f"Archive contains {len(file_list)} files/directories")
            for i, name in enumerate(file_list):
                if i < 20:  # Print first 20 items for debugging
                    print(f"  {name}")
                elif i == 20:
                    print(f"  ... and {len(file_list) - 20} more items")
            
            # Extract all contents to check subdirectories properly
            with tempfile.TemporaryDirectory() as temp_dir:
                archive_file.extractall(temp_dir)
                
                # Walk through all extracted content
                for root, dirs, files in os.walk(temp_dir):
                    for file_name in files:
                        lower_file_name = file_name.lower()
                        
                        # Check if file matches target extensions
                        if any(ext.lower() in lower_file_name for ext in file_extensions):
                            rel_path = os.path.relpath(os.path.join(root, file_name), temp_dir)
                            print(f"Found match in subdirectory: {rel_path}")
                            return True
                            
                        # Check for nested archives
                        if any(lower_file_name.endswith(ext.lower()) for ext in archive_extensions):
                            nested_path = os.path.join(root, file_name)
                            try:
                                if nested_path.lower().endswith('.zip'):
                                    if contains_file_in_archive_zip(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.rar'):
                                    if contains_file_in_archive_rar(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.7z') and SUPPORT_7Z:
                                    if contains_file_in_archive_7z(nested_path, file_extensions, archive_extensions):
                                        return True
                            except Exception as nested_error:
                                print(f"Error with nested archive {file_name}: {nested_error}")
    except Exception as e:
        print(f"Error opening or processing zip archive: {archive_path} - {e}")
    
    print(f"No matching files found in {archive_path}")
    return False


def contains_file_in_archive_rar(archive_path, file_extensions, archive_extensions):
    """Check if a RAR archive contains files with specific extensions."""
    try:
        print(f"Examining RAR archive: {archive_path}")
        with rarfile.RarFile(archive_path, 'r') as archive_file:
            file_list = archive_file.namelist()
            
            # Log a sample of files
            sample_size = min(5, len(file_list))
            if sample_size > 0:
                print(f"Sample of {sample_size} files from {len(file_list)} total:")
                for i in range(sample_size):
                    print(f"  {file_list[i]}")
            
            # Check all files in the archive
            for file_name in file_list:
                lower_file_name = file_name.lower()
                if any(ext.lower() in lower_file_name for ext in file_extensions):

                    print(f"Found match in RAR: {file_name}")
                    return True
                elif any(lower_file_name.endswith(ext.lower()) for ext in archive_extensions):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        nested_path = os.path.join(temp_dir, file_name)
                        try:
                            archive_file.extract(file_name, temp_dir)
                            if os.path.isfile(nested_path):
                                if nested_path.lower().endswith('.zip'):
                                    if contains_file_in_archive_zip(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.rar'):
                                    if contains_file_in_archive_rar(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.7z') and SUPPORT_7Z:
                                    if contains_file_in_archive_7z(nested_path, file_extensions, archive_extensions):
                                        return True
                        except Exception as nested_error:
                            print(f"Error with nested archive {file_name}: {nested_error}")
    except Exception as e:
        print(f"Error opening RAR archive: {archive_path} - {e}")
    return False

def contains_file_in_archive_7z(archive_path, file_extensions, archive_extensions):
    """Check if a 7z archive contains files with specific extensions."""
    if not SUPPORT_7Z:
        return False

    try:
        print(f"Examining 7z archive: {archive_path}")
        with py7zr.SevenZipFile(archive_path, mode='r') as archive_file:
            # Get the list of files without extracting
            file_list = archive_file.getnames()
            
            # Log all file names for debugging
            print(f"Files in archive ({len(file_list)} total files):")
            for i, name in enumerate(file_list):
                if i < 10 or any(name.lower().endswith(ext.lower()) for ext in file_extensions):
                    print(f"  {name}")
                if i == 10 and len(file_list) > 10:
                    print(f"  ... and {len(file_list) - 10} more files")
            
            # First, do a quick check of file names
            for file_name in file_list:
                lower_file_name = file_name.lower()
                if any(ext.lower() in lower_file_name for ext in file_extensions):

                    print(f"Found match in 7z: {file_name} matches {file_extensions}")
                    return True
            
            # Extract all files to a temporary directory for deeper inspection
            print("No matches found in file names, extracting for deeper inspection...")
            with tempfile.TemporaryDirectory() as temp_dir:
                archive_file.extractall(path=temp_dir)
                file_count = 0
                matches_found = 0
                
                # Walk through the extracted directory and check files
                for root, dirs, files in os.walk(temp_dir):
                    file_count += len(files)
                    for file_name in files:
                        lower_file_name = file_name.lower()
                        # Check for target file extensions
                        if any(ext.lower() in lower_file_name for ext in file_extensions):

                            matches_found += 1
                            print(f"Found match in extracted content: {os.path.join(root, file_name)}")
                            if matches_found >= 3:  # Limit log output
                                print(f"Found {matches_found} matches, stopping search.")
                                return True
                            
                        # Check for nested archives
                        if any(lower_file_name.endswith(ext.lower()) for ext in archive_extensions):
                            nested_path = os.path.join(root, file_name)
                            try:
                                if nested_path.lower().endswith('.zip'):
                                    if contains_file_in_archive_zip(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.rar'):
                                    if contains_file_in_archive_rar(nested_path, file_extensions, archive_extensions):
                                        return True
                                elif nested_path.lower().endswith('.7z'):
                                    if contains_file_in_archive_7z(nested_path, file_extensions, archive_extensions):
                                        return True
                            except Exception as nested_error:
                                print(f"Error with nested archive {file_name}: {nested_error}")
                
                print(f"Examined {file_count} extracted files, found {matches_found} matches.")
                if matches_found > 0:
                    return True
                
    except Exception as e:
        print(f"Error opening 7z archive: {archive_path} - {e}")
    
    print(f"No matching files found in {archive_path}")
    return False


def contains_file_in_archive(archive_path, file_extensions, archive_extensions):
    """
    Check if the archive (zip/rar/7z) or its nested archives contain any files matching the given extensions.
    Delegates to format-specific functions.
    
    :param archive_path: Path to the archive file (zip/rar/7z)
    :param file_extensions: File extensions to search for (e.g., .py, .uasset)
    :param archive_extensions: Archive extensions to search for (e.g., .zip, .rar, .7z)
    """
    # Ensure file_extensions is a tuple
    if isinstance(file_extensions, str):
        file_extensions = (file_extensions,)
    
    print(f"Checking archive {archive_path} for {file_extensions}")
    
    # Handle different archive types
    if archive_path.lower().endswith('.zip'):
        return contains_file_in_archive_zip(archive_path, file_extensions, archive_extensions)
    elif archive_path.lower().endswith('.rar'):
        return contains_file_in_archive_rar(archive_path, file_extensions, archive_extensions)
    elif archive_path.lower().endswith('.7z') and SUPPORT_7Z:
        return contains_file_in_archive_7z(archive_path, file_extensions, archive_extensions)
    
    return False


def contains_only_specific_files_in_archive(archive_path, extensions_to_check):
    """Check if an archive contains ONLY files with specific extensions."""
    try:
        print(f"Checking if archive contains only specific file types: {archive_path}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract archive based on its type
            if archive_path.lower().endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.rar'):
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    rar_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.7z') and SUPPORT_7Z:
                with py7zr.SevenZipFile(archive_path, mode='r') as sz_ref:
                    sz_ref.extractall(temp_dir)
            else:
                return False  # Unsupported archive type
            
            # Check if all files have the specified extensions
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if not any(file.lower().endswith(ext.lower()) for ext in extensions_to_check):
                        print(f"Found non-matching file: {file}")
                        return False
            
            # If we got here, all files matched the specified extensions
            return True
            
    except Exception as e:
        print(f"Error checking file types in archive {archive_path}: {e}")
        return False


def move_file(source, target_directory):
    """Move the file to the target directory."""
    try:
        destination = os.path.join(target_directory, os.path.basename(source))
        shutil.move(source, destination)
        print(f"Moved: {source} -> {destination}")
        return True
    except Exception as e:
        print(f"Error moving file {source}: {e}")
        return False


def is_directory_empty(directory):
    """
    Check if a directory is completely empty by recursively checking for files.
    A directory is considered empty if it contains no files in itself or its subdirectories.
    """
    # Skip non-existent directories
    if not os.path.exists(directory):
        return True
    
    # Check all files and subdirectories
    for root, dirs, files in os.walk(directory):
        # If there are any files, the directory is not empty
        if files:
            return False
    
    # If we got here, no files were found
    return True


def safe_delete_directory(directory, send2trash_available):
    """Safely delete or move a directory to the recycle bin."""
    try:
        if send2trash_available:
            import send2trash
            send2trash.send2trash(directory)
            print(f"Directory moved to recycle bin: {directory}")
        else:
            shutil.rmtree(directory)
            print(f"Directory deleted: {directory}")
        return True
    except Exception as e:
        print(f"Error removing directory {directory}: {e}")
        return False
    

def handle_mockup_files(file_name, file_path, mockups_directory, directories_used):
    """Check if 'mockup' is in the file name and move it to mockups directory if true."""
    if "mockup" in file_name.lower():
        create_target_directory(mockups_directory)
        if move_file(file_path, mockups_directory):
            directories_used.add(mockups_directory)
            print(f"File/archive with 'mockup' in name moved to mockups directory: {file_path}")
            return True  # Indicates the file was handled
    return False  # Indicates the file was not handled

def handle_audio_files(file_name, file_path, sfx_directory, directories_used):
    """Check if the file is an audio file and move it to sfx directory if true."""
    audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma', '.aiff', '.mid', '.midi')
    if file_name.lower().endswith(audio_extensions):
        create_target_directory(sfx_directory)
        if move_file(file_path, sfx_directory):
            directories_used.add(sfx_directory)
            print(f"Audio file moved to sfx directory: {file_path}")
            return True  # Indicates the file was handled
    return False  # Indicates the file was not handled


def check_audio_archive(archive_path, archive_extensions):
    """Check if an archive contains only audio files or audio files plus .txt files."""
    audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma', '.aiff', '.mid', '.midi')
    allowed_extensions = audio_extensions + ('.txt',)  # Only audio and .txt allowed
    
    try:
        print(f"Checking archive for audio content: {archive_path}")
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract archive based on its type
            if archive_path.lower().endswith('.zip'):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.rar'):
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    rar_ref.extractall(temp_dir)
            elif archive_path.lower().endswith('.7z') and SUPPORT_7Z:
                with py7zr.SevenZipFile(archive_path, mode='r') as sz_ref:
                    sz_ref.extractall(temp_dir)
            else:
                return False  # Unsupported archive type
            
            # Check all files in the extracted directory
            has_audio = False
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_lower = file.lower()
                    # Check if it's an audio file
                    if file_lower.endswith(audio_extensions):
                        has_audio = True
                    # If it's not an allowed extension (audio or .txt), fail
                    elif not any(file_lower.endswith(ext) for ext in allowed_extensions):
                        print(f"Found non-audio/non-txt file: {file}")
                        return False
            
            # Return True only if at least one audio file was found
            if has_audio:
                print(f"Archive contains only audio files (and possibly .txt): {archive_path}")
                return True
            else:
                print(f"No audio files found in archive: {archive_path}")
                return False
            
    except Exception as e:
        print(f"Error checking archive {archive_path}: {e}")
        return False
    

def check_davinci_archive(archive_path, archive_extensions):
    try:
        print(f"Checking archive for DaVinci Resolve project file: {archive_path}")
        
        if archive_path.lower().endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as archive_file:
                file_list = archive_file.namelist()
                for file_name in file_list:
                    base_name = os.path.basename(file_name).lower()
                    if base_name == "project.drp" or file_name.lower().endswith('.dra'):
                        print(f"Found 'project.drp' or '.dra' in zip archive: {file_name}")
                        return True
        
        elif archive_path.lower().endswith('.rar'):
            with rarfile.RarFile(archive_path, 'r') as archive_file:
                file_list = archive_file.namelist()
                for file_name in file_list:
                    base_name = os.path.basename(file_name).lower()
                    if base_name == "project.drp" or file_name.lower().endswith('.dra'):
                        print(f"Found 'project.drp' or '.dra' in rar archive: {file_name}")
                        return True
        
        elif archive_path.lower().endswith('.7z') and SUPPORT_7Z:
            with py7zr.SevenZipFile(archive_path, mode='r') as archive_file:
                file_list = archive_file.getnames()
                for file_name in file_list:
                    base_name = os.path.basename(file_name).lower()
                    if base_name == "project.drp" or file_name.lower().endswith('.dra'):
                        print(f"Found 'project.drp' or '.dra' in 7z archive: {file_name}")
                        return True
        
        print(f"No 'project.drp' found in archive: {archive_path}")
        return False
    
    except Exception as e:
        print(f"Error checking archive {archive_path}: {e}")
        return False
        
def main():
    # Use script directory (instead of os.getcwd())
    current_directory = script_directory
    
    # Define target directories
    mockups_directory = os.path.join(current_directory, "__mockups__")
    sfx_directory = os.path.join(current_directory, "__sfx__")  # New audio directory
    target_directory = os.path.join(current_directory, "__blenderaddons__")
    ue_directory = os.path.join(current_directory, "__ue__")
    blendfiles_directory = os.path.join(current_directory, "__blendfiles__")
    img_directory = os.path.join(current_directory, "__img__images__")
    docs_directory = os.path.join(current_directory, "__docs__")
    sbsar_directory = os.path.join(current_directory, "__sbsar__")
    brushset_directory = os.path.join(current_directory, "__brushset_abr__")
    py_directory = os.path.join(current_directory, "__py__")
    font_directory = os.path.join(current_directory, "__ttf__")
    threed_directory = os.path.join(current_directory, "__3dfiles__")
    exe_directory = os.path.join(current_directory, "__exe__")
    ebook_directory = os.path.join(current_directory, "__ebooks__")
    davinci_directory = os.path.join(current_directory, "__davinci__")
    aep_directory = os.path.join(current_directory, "__aep__")
    unity_directory = os.path.join(current_directory, "__unitypackage__")
    zbrush_directory = os.path.join(current_directory, "__zbrush__")
    
    # Check for send2trash library
    try:
        import send2trash
        print("send2trash library found. Empty folders will be moved to recycle bin.")
        send2trash_available = True
    except ImportError:
        print("Note: Install 'send2trash' library to move empty folders to recycle bin.")
        print("To install: pip install send2trash")
        print("Without this library, empty folders will be directly deleted.\n")
        send2trash_available = False
    
    # Define file extensions
    # Image file extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.psd', 
                        '.ico', '.raw', '.cr2', '.nef', '.heic', '.heif', '.ai', '.eps', '.dds', '.tga','.exr')
    
    # Document file extensions
    doc_extensions = ('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf')
    
    # Ebook file extensions
    ebook_extensions = ('.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lrf', '.tcr', '.lit')
    
    # Substance file extensions
    substance_extensions = ('.sbsar', '.sbs', '.sbsprs', '.sbsasm', '.sbsm', '.spsm')
    
    # Brush file extensions
    brush_extensions = ('.abr', '.tpl', '.brushset', '.brush','atn')
    
    # Font file extensions
    font_extensions = ('.ttf', '.otf', '.woff', '.woff2', '.eot')
    
    # 3D model file extensions
    threed_extensions = ('.fbx', '.obj', '.3ds', '.dae', '.stl', '.ply', '.glb', '.gltf', '.abc', '.usd', '.usda', '.usdc', '.x3d')
    
    # Executable file extensions
    exe_extensions = ('.exe', '.msi', '.app', '.bat', '.cmd')
    
    # Davinci Resolve file extensions
    davinci_extensions = ('.setting',)
    
    # After Effects file extensions
    aep_extensions = ('.aep', '.aepx', '.aet', '.ffx', '.jsx', '.jsxbin')
    
    # Unity package extensions
    unity_extensions = ('.unitypackage',)
    
    # ZBrush file extensions (including ZMT files)
    zbrush_extensions = ('.zmt', '.zsc', '.zpr', '.zbr', '.ztl', '.zb', '.zpz', '.zpk', '.zprj', '.zdl')
    
    # Unreal Engine asset extensions
    ue_extensions = ('.uasset', '.uplugin', '.umap', '.uproject')
    
    # Mockup file extensions (PSD and TXT only)
    mockup_extensions = ('.psd', '.txt')
    
    # Archive extensions
    archive_extensions = ('.zip', '.rar')
    if SUPPORT_7Z:
        archive_extensions = ('.zip', '.rar', '.7z')
    
    # Track directories that have files moved to them in this run
    directories_used = set()
    
    # Process all files in the root directory
    for file_name in os.listdir(current_directory):
        file_path = os.path.join(current_directory, file_name)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        try:

            # Check for "mockup" in file name first
            if handle_mockup_files(file_name, file_path, mockups_directory, directories_used):
                continue  # Skip to next file if handled

            # Check for audio files
            if handle_audio_files(file_name, file_path, sfx_directory, directories_used):
                continue  # Skip to next file if handled

            # Process Font files
            if file_name.lower().endswith(font_extensions):
                create_target_directory(font_directory)
                if move_file(file_path, font_directory):
                    directories_used.add(font_directory)
            
            # Process ZBrush files (including ZMT)
            elif file_name.lower().endswith(zbrush_extensions):
                create_target_directory(zbrush_directory)
                if move_file(file_path, zbrush_directory):
                    directories_used.add(zbrush_directory)
            
            # Process Unity package files
            elif file_name.lower().endswith(unity_extensions):
                create_target_directory(unity_directory)
                if move_file(file_path, unity_directory):
                    directories_used.add(unity_directory)
            
            # Process Blend files and their backups (.blend, .blend1, .blend2, etc.)
            elif '.blend' in file_name.lower():
                create_target_directory(blendfiles_directory)
                if move_file(file_path, blendfiles_directory):
                    directories_used.add(blendfiles_directory)
            
            # Process Python files
            elif file_name.lower().endswith('.py'):
                # Don't move the currently running script
                if file_path != os.path.abspath(__file__):
                    create_target_directory(py_directory)
                    if move_file(file_path, py_directory):
                        directories_used.add(py_directory)
                else:
                    print(f"This script file was not moved (currently running): {file_path}")
            
            # Process image files
            elif file_name.lower().endswith(image_extensions):
                create_target_directory(img_directory)
                if move_file(file_path, img_directory):
                    directories_used.add(img_directory)
            
            # Process document files
            elif file_name.lower().endswith(doc_extensions):
                create_target_directory(docs_directory)
                if move_file(file_path, docs_directory):
                    directories_used.add(docs_directory)
            
            # Process ebook files
            elif file_name.lower().endswith(ebook_extensions):
                create_target_directory(ebook_directory)
                if move_file(file_path, ebook_directory):
                    directories_used.add(ebook_directory)
            
            # Process Substance files
            elif file_name.lower().endswith(substance_extensions):
                create_target_directory(sbsar_directory)
                if move_file(file_path, sbsar_directory):
                    directories_used.add(sbsar_directory)
            
            # Process brush files
            elif file_name.lower().endswith(brush_extensions):
                create_target_directory(brushset_directory)
                if move_file(file_path, brushset_directory):
                    directories_used.add(brushset_directory)
            
            # Process 3D model files
            elif file_name.lower().endswith(threed_extensions):
                create_target_directory(threed_directory)
                if move_file(file_path, threed_directory):
                    directories_used.add(threed_directory)
            
            # Process executable files
            elif file_name.lower().endswith(exe_extensions):
                create_target_directory(exe_directory)
                if move_file(file_path, exe_directory):
                    directories_used.add(exe_directory)
                    
            # Process Davinci Resolve setting files
            elif file_name.lower().endswith(davinci_extensions):
                create_target_directory(davinci_directory)
                if move_file(file_path, davinci_directory):
                    directories_used.add(davinci_directory)
                    
            # Process After Effects files
            elif file_name.lower().endswith(aep_extensions):
                create_target_directory(aep_directory)
                if move_file(file_path, aep_directory):
                    directories_used.add(aep_directory)
                    
            # Process Unreal Engine asset files
            elif file_name.lower().endswith(ue_extensions):
                create_target_directory(ue_directory)
                if move_file(file_path, ue_directory):
                    directories_used.add(ue_directory)
            
            # Classify archives based on their contents
            elif file_name.lower().endswith(archive_extensions):
                # Special test for chrisRoseman_stylizedGrass.zip
                if file_name == "chrisRoseman_stylizedGrass.zip":
                    debug_archive(file_path)
                
                # Special test for 7z archives containing UE assets
                if file_name.lower().endswith('.7z') and SUPPORT_7Z:
                    print(f"Testing 7z archive for special content: {file_name}")
                
                # Check for archives with only PSD and TXT files (mockups)
                if contains_file_in_archive(file_path, mockup_extensions, archive_extensions):
                    # Additional check to ensure it ONLY contains PSD and TXT files
                    if contains_only_specific_files_in_archive(file_path, mockup_extensions):
                        create_target_directory(mockups_directory)
                        if move_file(file_path, mockups_directory):
                            directories_used.add(mockups_directory)
                            print(f"Archive containing only PSD and TXT files moved to mockups directory: {file_path}")
                            # Continue to next file since we've already moved this archive
                            continue
                
                # Check for Substance files in archives
                if contains_file_in_archive(file_path, substance_extensions, archive_extensions):
                    create_target_directory(sbsar_directory)
                    if move_file(file_path, sbsar_directory):
                        directories_used.add(sbsar_directory)
                        print(f"Archive containing Substance files moved to sbsar directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for archives with only audio files or audio + .txt files
                if check_audio_archive(file_path, archive_extensions):
                    create_target_directory(sfx_directory)
                    if move_file(file_path, sfx_directory):
                        directories_used.add(sfx_directory)
                        print(f"Archive containing only audio files (and possibly .txt) moved to sfx directory: {file_path}")
                        continue

                # Check for archives with 'project.drp' file
                if check_davinci_archive(file_path, archive_extensions):
                    create_target_directory(davinci_directory)
                    if move_file(file_path, davinci_directory):
                        directories_used.add(davinci_directory)
                        print(f"Archive containing 'project.drp' moved to davinci directory: {file_path}")
                        continue

                # Check for Font files in archives
                if contains_file_in_archive(file_path, font_extensions, archive_extensions):
                    create_target_directory(font_directory)
                    if move_file(file_path, font_directory):
                        directories_used.add(font_directory)
                        print(f"Archive containing font files moved to font directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for ZBrush files in archives (including ZMT)
                if contains_file_in_archive(file_path, zbrush_extensions, archive_extensions):
                    create_target_directory(zbrush_directory)
                    if move_file(file_path, zbrush_directory):
                        directories_used.add(zbrush_directory)
                        print(f"Archive containing ZBrush files moved to ZBrush directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for Unity package files in archives
                if contains_file_in_archive(file_path, unity_extensions, archive_extensions):
                    create_target_directory(unity_directory)
                    if move_file(file_path, unity_directory):
                        directories_used.add(unity_directory)
                        print(f"Archive containing Unity packages moved to Unity directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for After Effects files in archives
                if contains_file_in_archive(file_path, aep_extensions, archive_extensions):
                    create_target_directory(aep_directory)
                    if move_file(file_path, aep_directory):
                        directories_used.add(aep_directory)
                        print(f"Archive containing After Effects files moved to AEP directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for Davinci Resolve setting files in archives
                if contains_file_in_archive(file_path, davinci_extensions, archive_extensions):
                    create_target_directory(davinci_directory)
                    if move_file(file_path, davinci_directory):
                        directories_used.add(davinci_directory)
                        print(f"Archive containing Davinci Resolve settings moved to davinci directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue

                # Check for brush files in archives
                if contains_file_in_archive(file_path, brush_extensions, archive_extensions):
                    create_target_directory(brushset_directory)
                    if move_file(file_path, brushset_directory):
                        directories_used.add(brushset_directory)
                        print(f"Archive containing brush files moved to brushset directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue

                # Check for Unreal Engine assets in archives
                if contains_file_in_archive(file_path, ue_extensions, archive_extensions):
                    create_target_directory(ue_directory)
                    if move_file(file_path, ue_directory):
                        directories_used.add(ue_directory)
                        print(f"Archive containing Unreal Engine assets moved to UE directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for executables in archives (including subdirectories)
                if contains_file_in_archive(file_path, exe_extensions, archive_extensions):
                    create_target_directory(exe_directory)
                    if move_file(file_path, exe_directory):
                        directories_used.add(exe_directory)
                        print(f"Archive containing executables moved to exe directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for 3D files in archives
                if contains_file_in_archive(file_path, threed_extensions, archive_extensions):
                    create_target_directory(threed_directory)
                    if move_file(file_path, threed_directory):
                        directories_used.add(threed_directory)
                        print(f"Archive containing 3D files moved to 3D files directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Check for ebooks in archives
                if contains_file_in_archive(file_path, ebook_extensions, archive_extensions):
                    create_target_directory(ebook_directory)
                    if move_file(file_path, ebook_directory):
                        directories_used.add(ebook_directory)
                        print(f"Archive containing ebooks moved to ebook directory: {file_path}")
                        # Continue to next file since we've already moved this archive
                        continue
                
                # Archives containing Blender Python code or blend files
                if contains_file_in_archive(file_path, ('.py', '.blend'), archive_extensions):
                    create_target_directory(target_directory)
                    if move_file(file_path, target_directory):
                        directories_used.add(target_directory)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    main()                    
