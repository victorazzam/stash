#!/usr/bin/env python3

import os
import sys
import time
import json
import socket
import urllib3
import requests
import dns.resolver
from typing import List

# We want to explicitly ignore certificate verification. So shush!
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Pre-load list of (sub)domains that would normally be reported as problematic.
# They should state a valid reason for being kept.
try:
    with open('allowed.json') as f:
        ALLOW_LIST = json.load(f)
except:
    ALLOW_LIST = {}

def stylize(text: str, style: str) -> str:
    '''
    Stylize text.
    '''
    styles = {
        'off':   '\x1b[m',
        'bold':  '\x1b[1m',
        'red':   '\x1b[91m',
        'green': '\x1b[92m'
    }
    return styles.get(style, styles['off']) + text + styles['off']

def style_http(code: int, suffix: str = '', justify: int = 7) -> str:
    '''
    Stylize HTTP status codes.
    '''
    styles = (
        '\x1b[38;2;120;200;255m', # 1xx
        '\x1b[38;2;100;255;150m', # 2xx
        '\x1b[38;2;255;255;100m', # 3xx
        '\x1b[38;2;255;200;100m', # 4xx
        '\x1b[38;2;255;100;100m'  # 5xx
    )
    return styles[code // 100 - 1] + (str(code) + suffix).ljust(justify) + '\x1b[m'

def valid_domain(domain) -> bool:
    '''
    Validate domain according to permitted DNS characters.
    '''
    domain_chars = 'abcdefghijklmnopqrstuvwxyz0123456789.-'
    return all(char in domain_chars for char in domain)

def recent(file: str) -> bool:
    '''
    Test if a file exists and is less than a week old.
    '''
    return os.path.isfile(file) and os.stat(file).st_mtime > time.time() - 60*60*24*7

def fetch_data(domain: str, domain_data: dict, session: requests.Session) -> int:
    '''
    Aquire certificate data and enumerate subdomains via public APIs, or use cache if recent enough.
    '''
    max_length = 0

    print(f'\nGetting certificate data for {domain}')
    try:
        try:
            fname = f'{domain}.crt.json'
            if recent(fname):
                raise Exception
            url = f'https://crt.sh/?output=json&q={domain}'
            response = session.get(url).json()
            with open(fname, 'w') as f:
                json.dump(response, f)
        except Exception:
            with open(fname) as f:
                response = json.load(f)

        response.sort(key=lambda x: x['not_after'], reverse=True)
        for entry in response:

            # Each domain has 2 possible fields
            for meta in ('common_name', 'name_value'):
                sub = entry.get(meta, '').lower()

                # Has to end with the main domain
                if sub and sub.endswith(domain):

                    # Make sure fields conform to DNS standards
                    if valid_domain(sub):

                        # Add domain, specifying certificate validity
                        today = time.strftime('%FT%T')
                        domain_data[domain].setdefault(sub, {
                            'cert': 'expired' if entry['not_after'] < today else 'valid'
                        })

                        # Update the domains table column length
                        if len(sub) > max_length:
                            max_length = len(sub)
        failed = False
    except Exception:
        print(f'Failed to parse certificate data for {domain}')
        failed = True

    print(f'Getting subdomains for {domain}')
    try:
        try:
            fname = f'{domain}.ht.json'
            if recent(fname):
                raise Exception
            url = f'https://api.hackertarget.com/hostsearch/?q={domain}'
            response = session.get(url)
            subdomains = response.text.split()
            with open(f'{domain}.ht.json', 'w') as f:
                json.dump(subdomains, f)
        except Exception:
            with open(f'{domain}.ht.json') as f:
                subdomains = json.load(f)

        for subdomain in subdomains:
            sub, ip = subdomain.split(',')
            if sub.count('.') > 1:
                domain_data[domain].setdefault(sub, {'cert': 'missing'})
        failed = False
    except Exception:
        print(f'Failed subdomain enumeration for {domain}') # Tends to happen... rate limiting

    if failed:
        try:
            print('Using saved data.')
            with open(f'{domain}.json') as f:
                domain_data[domain].update(json.load(f))
            max_length = len(max(domain_data[domain], key=len))
        except (IOError, OSError):
            print('No saved data found. Skipping domain.')

    return max_length

def save_results(results: List[List], filename: str = 'results-table.txt'):
    '''
    Save domains with potential issues to a file.
    '''
    with open(filename, 'w') as f:

        # Adjust domains column length
        length = max(len(row[0]) for row in results)

        # Write column headers
        f.write(f'{"Domain":<{length}}  {"DNS":<15}  Cert     HTTP     HTTPS    Remarks\n')
        f.write(f'{"------":<{length}}  {"---":<15}  ----     ----     -----    -------\n')

        # Sort by certificate validity, then HTTP status
        results.sort(key=lambda x: x[-2:])

        for line in results:
            line[0] = line[0].ljust(length)
            f.write('  '.join(line) + '\n')

        print(f'\nSaved to {filename}\n')

def main(domains: List[str]):
    '''
    Gather and report on subdomain data for each domain in the list.
    '''
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'}
    domain_data = {}
    out = []

    for domain in domains:

        # Retrieve subdomains and cert info
        domain_data[domain] = {}
        max_length = fetch_data(domain, domain_data, session)
        subdomains = domain_data[domain]

        if not subdomains:
            continue

        i = 0
        lines = [
            f'#    {"Domain":<{max_length}}  {"DNS":<15}  Cert     HTTP     HTTPS    Remarks',
            f'-    {"------":<{max_length}}  {"---":<15}  ----     ----     -----    -------'
        ]
        print(''.join('\n' + stylize(line, 'bold') for line in lines))

        for name in sorted(subdomains):
            sub = subdomains[name]

            # Gather DNS records
            sub['dns'] = []
            for qtype in 'A MX NS SOA TXT'.split():
                try:
                    dig = dns.resolver.resolve(name, qtype)
                    if len(dig.response.answer[0]):
                        sub['dns'].append(qtype)
                except Exception:
                    pass

            # Skip domain if no DNS records were found
            if not sub['dns']:
                continue

            i += 1
            line = [
                f'{i:<4} {name:<{max_length}}', # Current index and domain
                ' '.join(sub['dns']).ljust(15)  # DNS record types the domain has
            ]

            # Visually represent HTTP redirect to HTTPS (None = to a different domain)
            arrow = {True: ' ->', None: ' >?', False: ''}

            # If record type A is present, test TLS and HTTP
            if 'A' in sub['dns']:

                # Single out expired certificates
                cert = sub['cert']
                style = {'valid': 'green', 'expired': 'red'}.get(cert, 'off')
                line.append(stylize(cert.ljust(7), style))

                # Contact domain and show response code, ignoring wildcard subdomains
                if name.startswith('*.'):
                    line.append('wildcard    ')
                else:
                    # HTTP
                    try:
                        r = session.get('http://' + name, allow_redirects=False, timeout=3)
                        answer = r.status_code

                        # Check if HTTP redirects to HTTPS
                        location = r.headers.get('location', '')
                        redirect = location.startswith('https://')
                        if redirect and not location.startswith('https://' + name):
                            redirect = None

                        line.append(style_http(answer, suffix=arrow.get(redirect)))
                        http = sub['http'] = answer
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        line.append(stylize('-'.ljust(7), 'red'))
                        http = sub['http'] = None

                    # HTTPS
                    try:
                        r = session.get('https://' + name, verify=False, timeout=3)
                        answer = r.status_code
                        line.append(style_http(answer))
                        https = sub['https'] = answer
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        line.append(stylize('-'.ljust(7), 'red'))
                        https = sub['https'] = None
            else:
                cert = http = https = sub['cert'] = sub['http'] = sub['https'] = 'inappl.'
                line.extend([cert] * 3)

            # Add quick and actionable notes
            remarks = []
            if name in ALLOW_LIST:
                remarks.append(ALLOW_LIST[name])
            elif cert == 'inappl.':
                pass
            else:
                # Abandoned service or different port
                if http == https == None:
                    if cert == 'valid':
                        remarks.append('Why no HTTP(S)? Perhaps another port/service is used?')
                    else:
                        remarks.append('If unused, remove DNS data.')
                # No HTTPS service
                elif https == None:
                    remarks.append('Why only HTTP and no HTTPS?')
                else:
                    # HTTP(S) stuff
                    if http // 100 != 3:
                        remarks.append('Add a redirect from HTTP to HTTPS.')
                    elif https // 100 == 5:
                        remarks.append('Verify that the server can handle requests.')

                    # Cert stuff
                    if cert == 'expired':
                        remarks.append('Renew the TLS certificate.')
                    elif cert == 'missing':
                        remarks.append('Add a TLS certificate.')

            if remarks:
                line.append(' '.join(remarks))

                # Add to output file if unchecked
                if name not in ALLOW_LIST:
                    out.append([
                        name,
                        line[1],
                        cert.ljust(7),
                        (str(http) + arrow.get(redirect)).ljust(7),
                        str(https).ljust(7),
                        line[-1]
                    ])

            # Print domain row
            print('  '.join(line))

        # Cache collected domain data
        with open(f'{domain}.json', 'w') as f:
            json.dump(domain_data[domain], f)

    # Write problematic domains to a file
    if out:
        save_results(out)
    else:
        print('\nCongrats! No issues found.\n')

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            sys.exit(f'Usage: {sys.argv[0]} domain-1.com [domain-2.net ...]')

        domains = []
        for domain in sys.argv[1:]:
            try:
                socket.gethostbyname(domain) # Will raise error on failure.
                domains.append(domain)
            except Except:
                print(f'Unknown host: {domain}')

        if not domains:
            sys.exit('No valid domains provided.')

        main(domains)
    except (KeyboardInterrupt, EOFError):
        print('\nInterrupt received, exiting.')
