# dsniff Python Package

This package provides a Python wrapper for the **dsniff** network sniffer suite (originally by Dug Song), allowing you to install and use dsniff tools via `pip`.

pip install .

## Installation

Ensure you have the required dependencies:

- `berkeley-db` (optional; support is disabled by default)
- `libnet`
- `libnids`
- `libpcap`
- `openssl`

On macOS with Homebrew:
```bash
brew install berkeley-db libnet libnids libpcap openssl
```

### Enable Berkeley DB support (optional)
By default, Berkeley DB compatibility is disabled. To enable support with a newer
Berkeley DB installation, set the `DSNIFF_DB_PATH` environment variable to your
Berkeley DB prefix and install:
pip install .
```bash
DSNIFF_DB_PATH=/opt/homebrew/opt/berkeley-db@4 \
pip install .
```

> On macOS, the installer will attempt to auto-detect a Homebrew keg-only
> Berkeley DB under `/usr/local/opt` or `/opt/homebrew/opt`. If found, you
> do **not** need to set `DSNIFF_DB_PATH` manually. Manual setting is only
> required for non-standard installation paths.

Install via `pip`:
```bash
pip install .
```

To specify custom library paths (e.g., Homebrew on Apple Silicon):
```bash
DSNIFF_LIBPCAP=/opt/homebrew/opt/libpcap \
DSNIFF_LIBNET=/opt/homebrew/opt/libnet \
DSNIFF_LIBNIDS=/opt/homebrew/opt/libnids \
DSNIFF_OPENSSL=/opt/homebrew/opt/openssl \
pip install .
```

## Usage

After installation, the following commands are available:

- `dsniff`
- `arpspoof`
- `dnsspoof`
- `filesnarf`
- `mailsnarf`
- `msgsnarf`
- `urlsnarf`
- `macof`
- `sshow`
- `sshmitm`
- `webmitm`
- `webspy`
- `tcpkill`
- `tcpnice`

## Commands & Examples

Below are common usage patterns and examples for each tool. Replace `-i eth0` with your network interface and adjust filters as needed.

- **dsniff**: sniff credentials on the network (FTP, Telnet, SMTP, HTTP, etc.)
  ```bash
  dsniff -i eth0 tcp port ftp or tcp port telnet
  ```
- **arpspoof**: perform ARP spoofing to man-in-the-middle two hosts
  ```bash
  arpspoof -i eth0 TARGET_IP GATEWAY_IP
  ```
- **dnsspoof**: spoof DNS responses based on a hosts file
  ```bash
  dnsspoof -i eth0 hosts.txt
  ```
- **filesnarf**: capture NFS file reads
  ```bash
  filesnarf -i eth0 tcp port nfs
  ```
- **mailsnarf**: capture SMTP mail traffic
  ```bash
  mailsnarf -i eth0 tcp port 25
  ```
- **msgsnarf**: capture IRC, IM, and messaging traffic
  ```bash
  msgsnarf -i eth0 tcp port 6667 or tcp port 5190
  ```
- **urlsnarf**: capture URLs from HTTP traffic
  ```bash
  urlsnarf -i eth0 tcp port 80
  ```
- **macof**: flood a switch by generating random MAC traffic
  ```bash
  macof -i eth0
  ```
- **sshow**: display active sniffer sessions
  ```bash
  sshow
  ```
- **sshmitm**: perform SSH v1 man-in-the-middle attack
  ```bash
  sshmitm -i eth0 REMOTE_HOST
  ```
- **webmitm**: HTTPS man-in-the-middle (requires appropriate certs)
  ```bash
  webmitm -i eth0 SERVER_IP
  ```
- **webspy**: passive HTTP snooping
  ```bash
  webspy -i eth0 tcp port 80
  ```
- **tcpkill**: kill TCP connections matching a filter
  ```bash
  tcpkill -i eth0 port 80
  ```
- **tcpnice**: throttle TCP connections (window-nice)
  ```bash
  tcpnice -i eth0 port 80
  ```

For detailed help on each tool, run:
```bash
<tool-name> -h
```

## Notes

- Original documentation and license can be found in the `dsniff-old` directory.
- Binaries are built and installed into the Python package during installation.
- This wrapper invokes the compiled executables under the hood.