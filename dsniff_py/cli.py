import os
import sys
import subprocess

def setup_config_files():
    """Setup dsniff configuration files by creating symlinks."""
    pkg_dir = os.path.dirname(__file__)
    config_dir = '/usr/local/share/dsniff'

    # Check if config directory exists
    if not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir, exist_ok=True)
        except (OSError, PermissionError):
            return False

    # Try to create symlinks or copy config files
    for config_file in ['dsniff.services', 'dsniff.magic']:
        config_path = os.path.join(config_dir, config_file)
        pkg_config = os.path.join(pkg_dir, config_file)

        if not os.path.exists(config_path) and os.path.exists(pkg_config):
            try:
                os.symlink(pkg_config, config_path)
            except (OSError, PermissionError):
                try:
                    import shutil
                    shutil.copy2(pkg_config, config_path)
                except (OSError, PermissionError):
                    return False
    return True

def main():
    """Wrapper entry point to invoke dsniff C binaries."""
    bin_name = os.path.basename(sys.argv[0])
    pkg_dir = os.path.dirname(__file__)
    exe_path = os.path.join(pkg_dir, 'bin', bin_name)

    if not os.path.isfile(exe_path):
        sys.stderr.write(f"Executable {bin_name} not found at {exe_path}\n")
        return 1

    # Try to setup config files
    config_check = '/usr/local/share/dsniff/dsniff.services'
    if not os.path.exists(config_check):
        if not setup_config_files():
            # Print helpful error message
            sys.stderr.write(f"\nError: dsniff configuration files not found.\n")
            sys.stderr.write(f"Please run the following commands to set them up:\n\n")
            sys.stderr.write(f"  mkdir -p /usr/local/share/dsniff\n")
            sys.stderr.write(f"  cp {pkg_dir}/dsniff.services /usr/local/share/dsniff/\n")
            sys.stderr.write(f"  cp {pkg_dir}/dsniff.magic /usr/local/share/dsniff/\n\n")
            return 1

    args = [exe_path] + sys.argv[1:]
    return subprocess.call(args)

if __name__ == "__main__":
    sys.exit(main())