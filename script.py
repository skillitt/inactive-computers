from ldap3 import Server, Connection, ALL, SUBTREE
import datetime

def convert_ad_timestamp_to_datetime(ad_timestamp):
    epoch_start = datetime.datetime(year=1601, month=1, day=1)
    seconds_since_epoch = ad_timestamp / 10**7
    return epoch_start + datetime.timedelta(seconds=seconds_since_epoch)

def get_last_logon(computer_name, server_address, user, password):
    # Define the server and connection
    server = Server(server_address, get_info=ALL)
    conn = Connection(server, user, password, auto_bind=True)

    # Construct the LDAP filter
    ldap_filter = f"(&(objectClass=computer)(name={computer_name}))"

    # Define the search base and attributes you want to retrieve
    search_base = "DC=yourdomain,DC=com"
    attributes = ['name', 'lastLogonTimestamp']

    # Perform the search
    conn.search(search_base, ldap_filter, SUBTREE, attributes=attributes)

    if conn.entries:
        computer = conn.entries[0]
        last_logon_timestamp = computer.lastLogonTimestamp.value
        last_logon_datetime = convert_ad_timestamp_to_datetime(last_logon_timestamp)
        print(f"Last logon for {computer_name}: {last_logon_datetime}")
    else:
        print(f"Computer {computer_name} not found.")

# Example usage
server_address = "your_ldap_server"
user = "your_username"
password = "your_password"
computer_name = "ExampleComputer"
get_last_logon(computer_name, server_address, user, password)

