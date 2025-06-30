# dsniff Suite: Command Reference
This document provides detailed information on each tool in the dsniff suite: purpose, synopsis, options, examples, and common use cases.

---

## dsniff
**Purpose:** Sniff and decode clear-text credentials and other application-level data across various protocols (FTP, Telnet, HTTP, SMTP, IMAP, etc.).
**Synopsis:**
```
dsniff [options] [expression]
```
**Options:**
- `-i <iface>`: capture interface
- `-p <pcapfile>`: read from pcap file
- `-f <services>`: comma-separated list of services
- `-s <snaplen>`: snapshot length (default 1024)
- `-t <trigger1,...>`: trigger packet types
- `-r <file>`: read saved DB file
- `-w <file>`: write records to DB file
- `-c`, `-m`, `-n`, `-V`: flags for client-only, magic, no DNS, version
**Example:**
```bash
dsniff -i eth0 tcp port ftp or tcp port telnet
```

## arpspoof
**Purpose:** Forge ARP replies to intercept and relay LAN traffic (ARP poisoning).
**Synopsis:**
```
arpspoof [options] <target-ip> <gateway-ip>
```
**Options:**
- `-i <iface>`: interface
- `-r`: relay traffic
- `-t <host>`: target one host
**Example:**
```bash
arpspoof -i eth0 192.168.1.10 192.168.1.1
```

## dnsspoof
**Purpose:** Spoof DNS responses using hosts file mappings.
**Synopsis:**
```
dnsspoof [options] <hostsfile>
```
**Options:**
-- `-i <iface>`: interface
**Example:**
```bash
dnsspoof -i eth0 hosts.txt
```
  
## filesnarf
**Purpose:** Capture and dump NFS file reads.
**Synopsis:**
```
filesnarf [options] [expression]
```
**Options:**
- `-i <iface>`: network interface
**Example:**
```bash
filesnarf -i eth0 tcp port 2049
```
  
## mailsnarf
**Purpose:** Capture SMTP sessions and print mail bodies.
**Synopsis:**
```
mailsnarf [options] [expression]
```
**Options:**
- `-i <iface>`: network interface
**Example:**
```bash
mailsnarf -i eth0 tcp port 25
```
  
## msgsnarf
**Purpose:** Intercept IRC and messaging protocols (ICQ, AIM, MSN).
**Synopsis:**
```
msgsnarf [options] [expression]
```
**Options:**
- `-i <iface>`: interface
**Example:**
```bash
msgsnarf -i eth0 tcp port 6667
```
  
## urlsnarf
**Purpose:** Extract and display URLs from HTTP GET requests.
**Synopsis:**
```
urlsnarf [options] [expression]
```
**Options:**
- `-i <iface>`: interface
**Example:**
```bash
urlsnarf -i eth0 tcp port 80
```
  
## macof
**Purpose:** Flood a switch MAC table with random source addresses.
**Synopsis:**
```
macof [options]
```
**Options:**
- `-i <iface>`: interface
**Example:**
```bash
macof -i eth0
```
  
## sshow
**Purpose:** Display active sniffing sessions (tracked credentials).
**Synopsis:**
```
sshow
```
**Example:**
```bash
sshow
```
  
## sshmitm
**Purpose:** Man-in-the-middle SSH v1 sessions to capture credentials.
**Synopsis:**
```
sshmitm [options] <server>
```
**Options:**
- `-i <iface>`: interface
- `-l <keyfile>`: local private key
**Example:**
```bash
sshmitm -i eth0 victim.example.com
```
  
## webmitm
**Purpose:** HTTPS man-in-the-middle using forged certificates.
**Synopsis:**
```
webmitm [options] <server>
```
**Options:**
- `-i <iface>`: interface
- `-k <certfile>`: certificate file
**Example:**
```bash
webmitm -i eth0 secure.example.com
```
  
## webspy
**Purpose:** Passive HTTP sniffer; prints full requests and responses.
**Synopsis:**
```
webspy [options] [expression]
```
**Options:**
- `-i <iface>`: interface
**Example:**
```bash
webspy -i eth0 tcp port 80
```
  
## tcpkill
**Purpose:** Terminate TCP connections by injecting RST packets.
**Synopsis:**
```
tcpkill [options] [expression]
```
**Options:**
- `-i <iface>`: interface
- `-9`: single termination packet
**Example:**
```bash
tcpkill -i eth0 port 80
```
  
## tcpnice
**Purpose:** Throttle TCP flows by advertising small window sizes.
**Synopsis:**
```
tcpnice [options] [expression]
```
**Options:**
- `-i <iface>`: interface
- `-s <size>`: window size
**Example:**
```bash
tcpnice -i eth0 -s 64 port 80
```