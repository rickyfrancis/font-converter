#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path


def convert_with_fontforge_script(otf_file, ttf_output):
    """Convert using a FontForge script file"""
    script_content = f"""
Open("{otf_file}")
Generate("{ttf_output}")
"""
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ff", delete=False) as f:
        f.write(script_content)
        script_path = f.name
    
    try:
        result = subprocess.run([
            "fontforge", "-script", script_path
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and Path(ttf_output).exists():
            return True
        else:
            print(f"    FontForge error: {result.stderr}")
            return False
    except Exception as e:
        print(f"    FontForge exception: {e}")
        return False
    finally:
        try:
            os.unlink(script_path)
        except:
            pass


def convert_with_fonttools_direct(otf_file, output_dir):
    """Try direct conversion using fonttools for all formats"""
    base_name = Path(otf_file).stem
    success = {"ttf": False, "woff": False, "woff2": False}
    
    # Try TTF conversion with fonttools ttx
    ttf_output = Path(output_dir) / "ttf" / f"{base_name}.ttf"
    try:
        result = subprocess.run([
            "fonttools", "ttLib.woff2", "decompress", str(otf_file), "-o", str(ttf_output)
        ], capture_output=True, text=True, timeout=60)
        if ttf_output.exists():
            print(f"  ✓ TTF: {ttf_output.name}")
            success["ttf"] = True
    except:
        pass
    
    # Try direct WOFF conversion
    woff_output = Path(output_dir) / "woff" / f"{base_name}.woff"
    try:
        result = subprocess.run([
            "pyftsubset", str(otf_file),
            "--flavor=woff",
            "--output-file=" + str(woff_output),
            "--unicodes=*"
        ], capture_output=True, text=True, timeout=60)
        if woff_output.exists():
            print(f"  ✓ WOFF: {woff_output.name}")
            success["woff"] = True
    except:
        pass
    
    # Try direct WOFF2 conversion
    woff2_output = Path(output_dir) / "woff2" / f"{base_name}.woff2"
    try:
        result = subprocess.run([
            "pyftsubset", str(otf_file),
            "--flavor=woff2",
            "--output-file=" + str(woff2_output),
            "--unicodes=*"
        ], capture_output=True, text=True, timeout=60)
        if woff2_output.exists():
            print(f"  ✓ WOFF2: {woff2_output.name}")
            success["woff2"] = True
    except:
        pass
    
    return success


def convert_otf_to_web_fonts(input_dir, output_dir):
    """Convert OTF fonts to web-supported formats using multiple methods"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    otf_files = list(input_path.glob("*.otf"))
    
    if not otf_files:
        print("No OTF files found in input directory")
        return
    
    print(f"Found {len(otf_files)} OTF files to convert")
    
    total_converted = {"ttf": 0, "woff": 0, "woff2": 0}
    
    for otf_file in otf_files:
        base_name = otf_file.stem
        print(f"Converting {otf_file.name}...")
        
        # Try direct conversion with fonttools first (often works for OTF)
        success = convert_with_fonttools_direct(str(otf_file), str(output_path))
        
        # If TTF conversion failed, try FontForge
        if not success["ttf"]:
            ttf_output = output_path / "ttf" / f"{base_name}.ttf"
            if convert_with_fontforge_script(str(otf_file), str(ttf_output)):
                print(f"  ✓ TTF: {ttf_output.name} (via FontForge)")
                success["ttf"] = True
                
                # Now try WOFF/WOFF2 from the TTF
                if not success["woff"]:
                    woff_output = output_path / "woff" / f"{base_name}.woff"
                    try:
                        subprocess.run([
                            "pyftsubset", str(ttf_output),
                            "--flavor=woff",
                            "--output-file=" + str(woff_output),
                            "--unicodes=*"
                        ], check=True, capture_output=True, timeout=60)
                        print(f"  ✓ WOFF: {woff_output.name}")
                        success["woff"] = True
                    except:
                        pass
                
                if not success["woff2"]:
                    woff2_output = output_path / "woff2" / f"{base_name}.woff2"
                    try:
                        subprocess.run([
                            "pyftsubset", str(ttf_output),
                            "--flavor=woff2",
                            "--output-file=" + str(woff2_output),
                            "--unicodes=*"
                        ], check=True, capture_output=True, timeout=60)
                        print(f"  ✓ WOFF2: {woff2_output.name}")
                        success["woff2"] = True
                    except:
                        pass
        
        # Count successful conversions
        for format_type, succeeded in success.items():
            if succeeded:
                total_converted[format_type] += 1
        
        # Show failures
        failures = [fmt for fmt, succeeded in success.items() if not succeeded]
        if failures:
            failed_str = ", ".join(failures)
            print(f"  ✗ Failed: {failed_str}")
    
    print("\nConversion Summary:")
    ttf_count = total_converted["ttf"]
    woff_count = total_converted["woff"]
    woff2_count = total_converted["woff2"]
    total_files = len(otf_files)
    print(f"  TTF: {ttf_count}/{total_files} successful")
    print(f"  WOFF: {woff_count}/{total_files} successful")
    print(f"  WOFF2: {woff2_count}/{total_files} successful")


if __name__ == "__main__":
    convert_otf_to_web_fonts("/fonts/input", "/fonts/output")
    print("\nConversion complete! Check /fonts/output for converted fonts.")
    
    # List the output files
    output_path = Path("/fonts/output")
    for format_dir in ["ttf", "woff", "woff2"]:
        format_path = output_path / format_dir
        if format_path.exists():
            files = list(format_path.glob("*"))
            format_upper = format_dir.upper()
            file_count = len(files)
            print(f"\n{format_upper} files ({file_count}):")
            for file in sorted(files):
                print(f"  {file.name}")