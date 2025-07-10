import gradio as gr
import pandas as pd
import json
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw

# JSON dosyasından veriyi yükle
with open("chembl_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Tüm ChEMBL ID'leri listesi
chembl_id_list = df["chembl_id"].tolist()

# Ana fonksiyon
def show_info(chembl_id):
    row = df[df["chembl_id"] == chembl_id].iloc[0]

    # 📈 IC50 grafiği
    plt.figure(figsize=(5,3))
    plt.plot(row["ic50"], marker='o')
    plt.title(f"IC50 Values - {chembl_id}")
    plt.xlabel("Measurement Index")
    plt.ylabel("IC50 (nM)")
    plt.grid(True)
    plt.tight_layout()
    ic50_plot_path = "ic50_plot.png"
    plt.savefig(ic50_plot_path)
    plt.close()

    # 🧪 SMILES molekül görseli
    mol = Chem.MolFromSmiles(row["smiles"])
    mol_img = Draw.MolToImage(mol)
    smiles_path = "smiles.png"
    mol_img.save(smiles_path)

    # ℹ️ Metinsel bilgi
    info_text = f"Name: {row['name']}\nChEMBL ID: {chembl_id}\nSMILES: {row['smiles']}\nTargets: {row['targets']}\n"

    return info_text, smiles_path, ic50_plot_path, "chembl_results.json"

# Gradio arayüzü
iface = gr.Interface(
    fn=show_info,
    inputs=gr.Dropdown(choices=chembl_id_list, label="Select ChEMBL ID"),
    outputs=[
        gr.Textbox(label="Molecule Info"),
        gr.Image(label="SMILES Structure"),
        gr.Image(label="IC50 Plot"),
        gr.File(label="Download JSON")
    ],
    title="ChEMBL Molecule Viewer with SMILES & IC50"
)

iface.launch()
