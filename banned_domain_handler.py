from urllib.parse import urlparse
import os

BANNED_DOMAINS_FILE = "banned_domains.txt"

def ensure_file_exists(filename):
    if not os.path.exists(filename):
        try:
            with open(filename, "w") as file:
                pass  # Create an empty file
        except IOError as e:
            print(f"Error creating file {filename}: {e}")
            raise

def add_to_banned_domains(domain):
    try:
        parsed_domain = urlparse(domain).netloc.split('www.')[-1].lower()
        if not parsed_domain:
            raise ValueError("Invalid domain")

        ensure_file_exists(BANNED_DOMAINS_FILE)
        
        with open(BANNED_DOMAINS_FILE, "r+") as file:
            existing_domains = set(line.strip().lower() for line in file)
            if parsed_domain not in existing_domains:
                file.write(parsed_domain + '\n')
                print(f"Domain '{parsed_domain}' added to banned list.")
            else:
                print(f"Domain '{parsed_domain}' already in banned list.")
    except Exception as e:
        print(f"Error adding domain to banned list: {e}")

def is_domain_banned(domain):
    try:
        parsed_domain = urlparse(domain).netloc.split('www.')[-1].lower()
        if not parsed_domain:
            raise ValueError("Invalid domain")

        ensure_file_exists(BANNED_DOMAINS_FILE)
        
        with open(BANNED_DOMAINS_FILE, "r") as file:
            for line in file:
                banned_domain = line.strip().lower()
                if parsed_domain == banned_domain or domain.lower().startswith(banned_domain):
                    return True
        return False
    except Exception as e:
        print(f"Error checking if domain is banned: {e}")
        return False