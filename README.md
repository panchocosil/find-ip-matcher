# Find IP Matcher

A Python tool to match domains with their correct IP addresses by sending HTTP requests using `curl`. The script provides real-time feedback on the terminal and logs results to a file, supporting both plain text and CSV formats.

---

## Features:
- Identifies matching IPs for a list of domains.
- Real-time terminal output with color-coded details:
  - **IP**: The tested IP address.
  - **Domain**: The tested domain name.
  - **Status Code**: Displays successful (`200 OK`) responses.
  - **Optional Matching**: Search for a specific word or phrase in the response content.
  - **Response Preview**: Shows the first 100 characters of the response.
  - **Error/Timeouts**: Logs issues in real-time.
  - **Curl Command**: Displays the `curl` command executed.
- Save results as:
  - **Plain text** (default).
  - **CSV** format (optional).

---

## Requirements:
- Python 3.6 or higher
- `colorama` for colored terminal output:
  ```bash
  pip install colorama
  ```

---

## Usage:

### 1. Prepare the input files:
- **Domains List**: A file (`domains-list.txt`) containing one domain per line.
  ```text
  example.com
  test.com
  ```
- **IP List**: A file (`ip-list.txt`) containing one IP per line.
  ```text
  192.168.1.1
  10.0.0.2
  ```

  To obtain the IPs, the script can make use of resources like https://search.censys.io/. Subdomains can be gathered using tools like https://github.com/owasp-amass/amass or similar.

### 2. Run the script:
#### Default Mode (Text Output):
```bash
python3 find-ip.py -d domains-list.txt -ip ip-list.txt -o output.txt
```

#### Match a Word/Phrase in Responses:
```bash
python3 find-ip.py -d domains-list.txt -ip ip-list.txt -o output.txt -match "Welcome"
```

#### Save Output in CSV Format:
```bash
python3 find-ip.py -d domains-list.txt -ip ip-list.txt -o output.csv -csv
```

#### Match a Word/Phrase and Save as CSV:
```bash
python3 find-ip.py -d domains-list.txt -ip ip-list.txt -o output.csv -match "Welcome" -csv
```

---

## Output Examples:

### Terminal Output (Real-time):
#### Match Mode (`-match "Welcome"`):
```
IP: 192.168.1.1
Domain: example.com
Status: MATCH FOUND: 'Welcome'
Response Received: Welcome to Example.com! Please enjoy your visit. HTTP/1.1 200 OK
...
Curl Command: curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://192.168.1.1/"
--------------------------------------------------
```

#### Default Mode (HTTP 200):
```
IP: 192.168.1.1
Domain: example.com
Status Code: 200
Response Received: HTTP/1.1 200 OK
Date: Tue, 09 Dec 2024 12:34:56 GMT
...
Curl Command: curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://192.168.1.1/"
--------------------------------------------------
```

---

### CSV Output (`output.csv`):
#### Example:
```csv
Domain,IP,Status,Response Preview,Response Length,Curl Command
example.com,192.168.1.1,200 OK,HTTP/1.1 200 OK Date: Tue, 09 Dec 2024 ...,12345,curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://192.168.1.1/"
example.com,10.0.0.2,MATCH FOUND,Welcome to Example.com! ...,5678,curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://10.0.0.2/"
```

---

## Notes:
- **Plain Text vs. CSV**: Use the `-csv` option to save the output in a structured CSV format.
- **Custom Matching**: Use `-match <word>` to search for a specific word or phrase in the response instead of relying on HTTP status codes.
- **Parallel Processing**: The script uses multithreading for faster execution.
