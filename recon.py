import subprocess
import sys


def check_host(target):
    result = subprocess.run(
        ["nmap", "-sn", target],
        capture_output=True,
        text=True
    )

    return "Host is up" in result.stdout


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 recon.py <target>")
        sys.exit(1)

    target = sys.argv[1]

    print("=" * 40)
    print("   NETWORK RECON TOOL v0.2")
    print("=" * 40)

    print(f"\nTarget: {target}")
    print("[+] Performing Nmap host discovery...")

    if check_host(target):
        print("[+] Host is reachable")
    else:
        print("[-] Host appears unreachable")


if __name__ == "__main__":
    main()
