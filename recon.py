import subprocess
import sys


def check_host(target):
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", target],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return result.returncode == 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 recon.py <target>")
        sys.exit(1)

    target = sys.argv[1]

    print("=" * 40)
    print("   NETWORK RECON TOOL v0.1")
    print("=" * 40)

    print(f"\nTarget: {target}")
    print("[+] Checking host availability...")

    if check_host(target):
        print("[+] Host is reachable")
    else:
        print("[-] Host appears unreachable")


if __name__ == "__main__":
    main()
