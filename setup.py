import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Custom install command to build and install dsniff C binaries."""
    def run(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Directories for build
        tmp_dir = os.path.join(cwd, 'tmp')
        build_dir = os.path.join(cwd, 'build')
        c_src_dir = os.path.join(cwd, 'dsniff-old')

        # Create directories
        os.makedirs(tmp_dir, exist_ok=True)
        os.makedirs(build_dir, exist_ok=True)

        # Environment for build
        env = os.environ.copy()
        env['TMPDIR'] = tmp_dir

        # Configure library paths (override via environment)
        libpcap = env.get('DSNIFF_LIBPCAP', '/usr/local/opt/libpcap')
        libnet = env.get('DSNIFF_LIBNET', '/usr/local/opt/libnet')
        libnids = env.get('DSNIFF_LIBNIDS', '/usr/local/opt/libnids')
        openssl = env.get('DSNIFF_OPENSSL', '/usr/local/opt/openssl')

        # ✅ Always skip Berkeley DB if we're in CI (e.g., GitHub Actions)
        if os.getenv('CI'):
            db_path = None
        else:
            # Auto-detect Berkeley DB include/lib paths if provided or on macOS Homebrew
            db_path = env.get('DSNIFF_DB_PATH')
            if db_path:
                inc = os.path.join(db_path, 'include', 'db.h')
                libdir = os.path.join(db_path, 'lib')
                if not (os.path.isfile(inc) and os.path.isdir(libdir)):
                    db_path = None  # Invalid override

            if not db_path and sys.platform == 'darwin':
                for base in ('/opt/homebrew/opt', '/usr/local/opt'):
                    if os.path.isdir(base):
                        for d in os.listdir(base):
                            if d.startswith('berkeley-db'):
                                cand = os.path.join(base, d)
                                inc = os.path.join(cand, 'include', 'db.h')
                                libdir = os.path.join(cand, 'lib')
                                if os.path.isfile(inc) and os.path.isdir(libdir):
                                    db_path = cand
                                    break
                        if db_path:
                            break

        if db_path:
            # inject compiler flags for DB include and lib
            env['CPPFLAGS'] = env.get('CPPFLAGS', '') + f' -I{db_path}/include'
            env['LDFLAGS'] = env.get('LDFLAGS', '') + f' -L{db_path}/lib'

        # Make sure we're in the right directory when running configure
        old_cwd = os.getcwd()
        os.chdir(c_src_dir)

        try:
            # Configure C build
            config_cmd = [
                './configure',
                f'--with-libpcap={libpcap}',
                f'--with-libnet={libnet}',
                f'--with-libnids={libnids}',
                f'--with-openssl={openssl}',
                '--without-x',
                f'--sbindir={os.path.join(build_dir, "bin")}',
                f'--prefix={build_dir}',
            ]

            # ✅ Always disable Berkeley DB in CI
            if os.getenv('CI'):
                config_cmd.insert(1, '--with-db=no')
                print("Forcing --with-db=no in CI")
            elif db_path:
                config_cmd.insert(1, f'--with-db={db_path}')
            elif sys.platform == 'darwin':
                config_cmd.insert(1, '--with-db=no')

            print(f"Running configure in {c_src_dir}")
            subprocess.check_call(config_cmd, env=env)

            # Build and install
            subprocess.check_call(['make'], env=env)
            subprocess.check_call(['make', 'install'], env=env)

        finally:
            # Always go back to original working directory
            os.chdir(old_cwd)

        # Copy binaries to Python package
        dest_bin = os.path.join(cwd, 'dsniff_py', 'bin')
        if os.path.exists(dest_bin):
            shutil.rmtree(dest_bin)
        shutil.copytree(os.path.join(build_dir, 'bin'), dest_bin)

        # Run standard install
        super().run()

long_description = ''
if os.path.exists('README.md'):
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='dsniff',
    version='0.1.0',
    author='Modified dsniff',
    author_email='',
    description='Python wrapper for dsniff network utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'arpspoof=dsniff_py.cli:main',
            'dnsspoof=dsniff_py.cli:main',
            'dsniff=dsniff_py.cli:main',
            'filesnarf=dsniff_py.cli:main',
            'mailsnarf=dsniff_py.cli:main',
            'msgsnarf=dsniff_py.cli:main',
            'urlsnarf=dsniff_py.cli:main',
            'macof=dsniff_py.cli:main',
            'sshow=dsniff_py.cli:main',
            'sshmitm=dsniff_py.cli:main',
            'webmitm=dsniff_py.cli:main',
            'webspy=dsniff_py.cli:main',
            'tcpkill=dsniff_py.cli:main',
            'tcpnice=dsniff_py.cli:main',
            'dsniff-menu=dsniff_py.menu:main',
        ]
    },
    cmdclass={'install': PostInstallCommand},
    python_requires='>=3.6',
)