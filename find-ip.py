import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def fetch_ip_for_host(host, ip, output_file):
    """
    Tries to fetch the domain using the given IP and Host header.
    Logs and outputs real-time results for successful (200 OK) responses.
    """
    cmd = f'curl --max-time 5 -i -s -k -X GET -H "Host: {host}" -H "User-Agent: Mozilla/5.0" "https://{ip}/"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        response = result.stdout
        status_line = next((line for line in response.splitlines() if line.startswith("HTTP/")), None)

        if status_line and "200 OK" in status_line:
            status_code = "200"
            response_length = len(response)
            output = (
                f"{Fore.GREEN}IP: {Fore.CYAN}{ip}\n"
                f"{Fore.GREEN}Domain: {Fore.CYAN}{host}\n"
                f"{Fore.GREEN}Status Code: {Fore.CYAN}{status_code}\n"
                f"{Fore.GREEN}Response Received: {Fore.CYAN}{response[:100]}...\n"
                f"{Fore.GREEN}Length: {Fore.CYAN}{response_length}\n"
                f"{Fore.GREEN}Curl Command: {Fore.MAGENTA}{cmd}\n"
                f"{Style.BRIGHT}{'-' * 50}{Style.RESET_ALL}\n"
            )
            print(output, end="")  # Print to terminal
            with open(output_file, "a") as of:
                of.write(output)  # Append to output file
        elif not status_line:
            print(f"{Fore.YELLOW}Error: No status line received for {host} with IP {ip}")
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}Timeout: {cmd}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}\nCurl Command: {cmd}")

def find_correct_ips(domains_file, ips_file, output_file):
    """
    Reads domain names and IP addresses, checks which IPs match which domains,
    and outputs results in real time.
    """
    with open(domains_file, "r") as df, open(ips_file, "r") as ipf:
        domains = [line.strip() for line in df if line.strip()]
        ips = [line.strip() for line in ipf if line.strip()]

    def check_domain_ip_pair(domain):
        for ip in ips:
            fetch_ip_for_host(domain, ip, output_file)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_domain_ip_pair, domains)

def main():
    parser = argparse.ArgumentParser(description="Find correct IPs for domains.")
    parser.add_argument("-d", "--domains", required=True, help="Path to domains list file.")
    parser.add_argument("-ip", "--ips", required=True, help="Path to IPs list file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output file.")
    args = parser.parse_args()

    # Clear the output file
    with open(args.output, "w") as of:
        of.write("")

    find_correct_ips(args.domains, args.ips, args.output)

if __name__ == "__main__":
    main()
