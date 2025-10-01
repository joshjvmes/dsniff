import os
import sys
import subprocess

def setup_config_files():
    """Setup dsniff configuration files by creating symlinks or copies."""
    pkg_dir = os.path.dirname(__file__)

    # Try multiple possible config locations
    # The binaries may be compiled with different paths
    config_dirs = [
        '/usr/local/share/dsniff',
        '/usr/share/dsniff',
        os.path.join(os.path.expanduser('~'), 'Downloads/prime_dsniff/build/share/dsniff'),
    ]

    success = False
    for config_dir in config_dirs:
        try:
            # Check if config directory exists
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)

            # Try to create symlinks or copy config files
            for config_file in ['dsniff.services', 'dsniff.magic']:
                config_path = os.path.join(config_dir, config_file)
                pkg_config = os.path.join(pkg_dir, config_file)

                if not os.path.exists(config_path) and os.path.exists(pkg_config):
                    try:
                        os.symlink(pkg_config, config_path)
                        success = True
                    except (OSError, PermissionError):
                        try:
                            import shutil
                            shutil.copy2(pkg_config, config_path)
                            success = True
                        except (OSError, PermissionError):
                            pass
        except (OSError, PermissionError):
            continue

    return success

def main():
    """Wrapper entry point to invoke dsniff C binaries."""
    bin_name = os.path.basename(sys.argv[0])
    pkg_dir = os.path.dirname(__file__)
    exe_path = os.path.join(pkg_dir, 'bin', bin_name)

    if not os.path.isfile(exe_path):
        sys.stderr.write(f"Executable {bin_name} not found at {exe_path}\n")
        return 1

    # Try to setup config files automatically
    setup_config_files()

    args = [exe_path] + sys.argv[1:]
    return subprocess.call(args)

if __name__ == "__main__":
    sys.exit(main())