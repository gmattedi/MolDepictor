from io import BytesIO

import pandas as pd
from flask import Flask, send_file, request, render_template
from rdkit import Chem
from rdkit.Chem import Draw, rdDepictor

"""
Small Flask REST api for depicting and returning SMILES of molecules in a CSV file.
The `depict` route is a bonus endpoint for depicting arbitrary SMILES
"""

rdDepictor.SetPreferCoordGen(True)

app = Flask(__name__)


def serve_pil_image(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/image')
def get_image():
    idx = request.args.get('id')
    if idx is None:
        return 'Provide an identifier string ["id" argument]', 400
    elif idx not in data:
        return f'{idx} not found', 400

    smiles = data[idx]
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return 'Invalid SMILES', 400

    img = Draw.MolToImage(mol)

    return serve_pil_image(img)


@app.route('/smiles')
def get_smiles():
    idx = request.args.get('id')
    if idx is None:
        return 'Provide an identifier string ["id" argument]', 400
    elif idx not in data:
        return f'{idx} not found', 400

    smiles = data[idx]
    return smiles


@app.route('/depict')
def depictor():
    smiles = request.args.get('smiles')
    if smiles is None:
        return 'Provide a SMILES string ["smiles" argument]', 400

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return 'Invalid SMILES', 400
    img = Draw.MolToImage(mol)
    return serve_pil_image(img)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Flask depictor')
    parser.add_argument('-i', '--input_csv', help='Input CSV file', required=True)
    parser.add_argument('-s', '--smiles_col', help='SMILES column (default: %(default)s)', default='SMILES')
    parser.add_argument('-n', '--name_col', help='Identifier column (default: %(default)s)')
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    data = df.set_index(args.name_col)[args.smiles_col].to_dict()

    app.run(debug=True)
