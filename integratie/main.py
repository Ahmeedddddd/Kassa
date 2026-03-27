import time
import sys
from odoo_client import odoo

def main():
    print("Kassa Integration Service Gestart.", flush=True)
    
    # Odoo doet er soms eventjes over om op te starten in Docker
    retries = 5
    while not odoo.uid and retries > 0:
        time.sleep(3)
        odoo._connect()
        retries -= 1
        
    if odoo.uid:
        print(f"✅ API connectie met Odoo ({odoo.url}) succesvol opgezet!", flush=True)
    else:
        print("❌ Kon geen verbinding maken met de Odoo API.", flush=True)
        
    print("Wachtend op verdere code van het team. Container blijft actief...", flush=True)
    
    # Simpele keep-alive loop
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Service wordt afgesloten...")
        sys.exit(0)

if __name__ == "__main__":
    main()
