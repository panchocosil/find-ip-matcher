# Find IP Matcher

A Python tool to match domains with their correct IP addresses by sending HTTP requests using `curl`. The script provides real-time feedback on the terminal and logs results to an output file.

---

## Features:
- Identifies matching IPs for a list of domains.
- Real-time terminal output with color-coded details:
  - **IP**: The tested IP address.
  - **Domain**: The tested domain name.
  - **Status Code**: Only displays successful (200 OK) responses.
  - **Response Preview**: Shows the first 100 characters of the response.
  - **Error/Timeouts**: Logs issues in real-time.
  - **Curl Command**: Displays the `curl` command executed.
- Parallel processing for faster execution.
- Saves results to a specified output file.

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
```bash
python3 find-ip.py -d domains-list.txt -ip ip-list.txt -o output.txt
```

### 3. View results:
- **Terminal**: Real-time, color-coded output.
- **Output File**: Results saved in `output.txt` in plain text format.

---

## Output Example:
### Terminal:
```
IP: 192.168.1.1
Domain: example.com
Status Code: 200
Response Received: HTTP/1.1 200 OK
Date: Tue, 09 Dec 2024 12:34:56 GMT
Content-Type: text/html; charset=UTF-8
...
Length: 12345
Curl Command: curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://192.168.1.1/"
--------------------------------------------------
```

### Output File (`output.txt`):
```text
IP: 192.168.1.1
Domain: example.com
Status Code: 200
Response Received: HTTP/1.1 200 OK
Date: Tue, 09 Dec 2024 12:34:56 GMT
Content-Type: text/html; charset=UTF-8
...
Length: 12345
Curl Command: curl --max-time 5 -i -s -k -X GET -H "Host: example.com" -H "User-Agent: Mozilla/5.0" "https://192.168.1.1/"
--------------------------------------------------
```

---

## Notes:
- Adjust the `max_workers` parameter in the script to control the level of parallelism.
- Ensure your system has `curl` installed and accessible via the terminal.
- The output file does not include color formatting for better compatibility.

