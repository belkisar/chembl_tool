import pandas as pd
import requests
import json
import time

# CSV'den ChEMBL ID'leri oku
df = pd.read_csv("chembl_ids.csv")
chembl_ids = df["chembl_id"].tolist()

# Sonuçları burada toplayacağız
results = []

# Her ChEMBL ID için veri çek
for chembl_id in chembl_ids:
    print(f"Processing: {chembl_id}")
    
    # Molekül bilgisi (SMILES, isim)
    url_mol = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
    res_mol = requests.get(url_mol)
    mol_data = res_mol.json()
    
    # Bazı moleküllerde 'molecule_structures' olmayabilir
    structure_data = mol_data.get("molecule_structures")
    smiles = structure_data.get("canonical_smiles") if structure_data else "Not found"
    name = mol_data.get("pref_name", "Unknown")
    
    # IC50 ve hedef bilgisi
    url_ic50 = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?molecule_chembl_id={chembl_id}&standard_type=IC50"
    res_ic50 = requests.get(url_ic50)
    act_data = res_ic50.json().get("activities", [])
    
    ic50_values = []
    targets = []
    for act in act_data:
        try:
            ic50_values.append(float(act["standard_value"]))
            targets.append(act["target_chembl_id"])
        except:
            continue

    # Sonuçları ekle
    results.append({
        "chembl_id": chembl_id,
        "name": name,
        "smiles": smiles,
        "ic50": ic50_values[:5],
        "targets": targets[:3]
    })
    
    time.sleep(1)  # API'yi çok hızlı çağırmamak için

# JSON dosyasına kaydet
with open("chembl_results.json", "w", encoding='utf-8') as f:
    json.dump(results, f, indent=4)

print("✅ Tüm veriler başarıyla çekildi ve 'chembl_results.json' dosyasına kaydedildi.")
