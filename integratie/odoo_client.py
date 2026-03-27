import os
import xmlrpc.client

# Lees de configuratie in vanuit de environment variabelen (.env)
ODOO_URL = os.environ.get("ODOO_URL")
ODOO_DB = os.environ.get("ODOO_DB")
ODOO_USER = os.environ.get("ODOO_USER")
ODOO_PASS = os.environ.get("ODOO_PASS")

if not all([ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASS]):
    print("[Waarschuwing] Niet alle Odoo environment variabelen zijn ingesteld!")

class OdooClient:
    """
    Simpele wrapper rond de XML-RPC API van Odoo.
    Geeft developers direct een '.execute()' methode zonder de uid/pass logica te moeten herhalen.
    """
    def __init__(self):
        self.url = ODOO_URL
        self.db = ODOO_DB
        self.user = ODOO_USER
        self.password = ODOO_PASS
        self.uid = None
        self.models = None
        self._connect()

    def _connect(self):
        try:
            # Stap 1: Authenticatie
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.user, self.password, {})
            
            if not self.uid:
                print(f"[Odoo API] Authenticatie mislukt voor user '{self.user}'.")
                return
            
            # Stap 2: Model object opzetten voor API calls
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
            
        except Exception as e:
            print(f"[Odoo API] Fout bij verbinden met Odoo: {e}")

    def execute(self, model, method, *args, **kwargs):
        """
        Voert een methode uit op een specifiek Odoo model via XML-RPC.
        
        Voorbeeld - Zoek een klant:
        klant = odoo.execute('res.partner', 'search_read', [[['x_user_id', '=', '123']]], {'fields': ['name'], 'limit': 1})
        """
        if not self.uid or not self.models:
            print("[Odoo API] Niet verbonden, probeer opnieuw te verbinden...")
            self._connect()
            if not self.uid:
                raise ConnectionError("Odoo DB is momenteel niet bereikbaar.")
                
        try:
            return self.models.execute_kw(
                self.db, 
                self.uid, 
                self.password, 
                model, 
                method, 
                args, 
                kwargs
            )
        except Exception as e:
            print(f"[Odoo API] Fout tijdens API call {method} op model {model}: {e}")
            raise

# Meteen een connectie pre-loaden voor makkelijke import
# Devs kunnen dit via: 'from odoo_client import odoo' gebruiken
odoo = OdooClient()
