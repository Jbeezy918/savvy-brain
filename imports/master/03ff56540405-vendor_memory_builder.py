from pathlib import Path
import csv

ROOT = Path.home() / "AI_SYSTEM" / "govcon_ops"
VENDORS = ROOT / "vendors"
VENDORS.mkdir(exist_ok=True)

files = {
    "container_vendors.csv": [
        ["Category","Vendor","Contact","Email","Phone","Website","Notes","Status"],
        ["Container Supplier","","","","","","","NEW"],
        ["Container Supplier","","","","","","","NEW"],
        ["Container Supplier","","","","","","","NEW"],
    ],
    "freight_vendors.csv": [
        ["Category","Vendor","Contact","Email","Phone","Website","Notes","Status"],
        ["Heavy Freight","","","","","","","NEW"],
        ["Heavy Freight","","","","","","","NEW"],
        ["Heavy Freight","","","","","","","NEW"],
    ],
    "rf_amplifier_vendors.csv": [
        ["Category","Vendor","Contact","Email","Phone","Website","Notes","Status"],
        ["RF Amplifier","ATEC","","","","","RFQ #13288 submitted","ACTIVE"],
        ["RF Amplifier","AMETEK / AR","","ari-sales@ametek.com","","","Pending","ACTIVE"],
        ["RF Amplifier","Richardson / Quantic PMI","","","","PA-2G18G-43-5-40-SFF","Research","ACTIVE"],
        ["RF Amplifier","Qualwave","","","","QPAS-2000-18000-40-40S","Research","ACTIVE"],
    ],
    "filter_vendors.csv": [
        ["Category","Vendor","Contact","Email","Phone","Website","Notes","Status"],
        ["Filter","CIS / Marla Montgomery","Marla Montgomery","","","","Eaton 300368 $322.80, 132 in stock, 3-4 weeks remainder","QUOTED"],
    ],
}

for name, rows in files.items():
    path = VENDORS / name
    if not path.exists():
        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"Created {path}")
    else:
        print(f"Exists, skipped {path}")

print("Vendor memory initialized.")
