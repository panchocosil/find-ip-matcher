import argparse
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def fetch_ip_for_host(host, ip, output_file, match_word=None, csv_mode=False, csv_writer=None):
    """
    Tries to fetch the domain using the given IP and Host header.
    Logs and outputs real-time results for matching responses.
    """
    cmd = f'curl --max-time 5 -i -s -k -X GET -H "Host: {host}" -H "User-Agent: Mozilla/5.0" "https://{ip}/"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        response = result.stdout

        if match_word:  # Match based on word/phrase
            if match_word in response:
                status = "MATCH FOUND"
                response_length = len(response)
                output = (
                    f"{Fore.GREEN}IP: {Fore.CYAN}{ip}\n"
                    f"{Fore.GREEN}Domain: {Fore.CYAN}{host}\n"
                    f"{Fore.GREEN}Status: {Fore.CYAN}{status} for '{match_word}'\n"
                    f"{Fore.GREEN}Response Received: {Fore.CYAN}{response[:100]}...\n"
                    f"{Fore.GREEN}Curl Command: {Fore.MAGENTA}{cmd}\n"
                    f"{Style.BRIGHT}{'-' * 50}{Style.RESET_ALL}\n"
                )
                print(output, end="")  # Print to terminal
                if csv_mode:
                    csv_writer.writerow([host, ip, status, response[:100], response_length, cmd])
                else:
                    with open(output_file, "a") as of:
                        of.write(output)  # Append to output file
        else:  # Match based on HTTP 200 response
            status_line = next((line for line in response.splitlines() if line.startswith("HTTP/")), None)
            if status_line and "200 OK" in status_line:
                status = "200 OK"
                response_length = len(response)
                output = (
                    f"{Fore.GREEN}IP: {Fore.CYAN}{ip}\n"
                    f"{Fore.GREEN}Domain: {Fore.CYAN}{host}\n"
                    f"{Fore.GREEN}Status: {Fore.CYAN}{status}\n"
                    f"{Fore.GREEN}Response Received: {Fore.CYAN}{response[:100]}...\n"
                    f"{Fore.GREEN}Curl Command: {Fore.MAGENTA}{cmd}\n"
                    f"{Style.BRIGHT}{'-' * 50}{Style.RESET_ALL}\n"
                )
                print(output, end="")  # Print to terminal
                if csv_mode:
                    csv_writer.writerow([host, ip, status, response[:100], response_length, cmd])
                else:
                    with open(output_file, "a") as of:
                        of.write(output)  # Append to output file
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}Timeout: {cmd}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}\nCurl Command: {cmd}")

def find_correct_ips(domains_file, ips_file, output_file, match_word=None, csv_mode=False):
    """
    Reads domain names and IP addresses, checks which IPs match which domains,
    and outputs results in real time.
    """
    with open(domains_file, "r") as df, open(ips_file, "r") as ipf:
        domains = [line.strip() for line in df if line.strip()]
        ips = [line.strip() for line in ipf if line.strip()]

    # Prepare CSV file if in CSV mode
    csv_writer = None
    csv_file = None
    if csv_mode:
        csv_file = open(output_file, "w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Domain", "IP", "Status", "Response Preview", "Response Length", "Curl Command"])

    def check_domain_ip_pair(domain):
        for ip in ips:
            fetch_ip_for_host(domain, ip, output_file, match_word, csv_mode, csv_writer)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_domain_ip_pair, domains)

    # Close the CSV file if in CSV mode
    if csv_mode and csv_file:
        csv_file.close()

def main():
    parser = argparse.ArgumentParser(description="Find correct IPs for domains.")
    parser.add_argument("-d", "--domains", required=True, help="Path to domains list file.")
    parser.add_argument("-ip", "--ips", required=True, help="Path to IPs list file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output file.")
    parser.add_argument("-match", "--match", help="Optional: Word or phrase to match in the response.")
    parser.add_argument("-csv", "--csv", action="store_true", help="Optional: Save output in CSV format.")
    args = parser.parse_args()

    # Clear the output file if not in CSV mode
    if not args.csv:
        with open(args.output, "w") as of:
            of.write("")

    find_correct_ips(args.domains, args.ips, args.output, args.match, args.csv)

if __name__ == "__main__":
    main()
