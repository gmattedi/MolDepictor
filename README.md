# MolDepictor

Minimal Flask app for depicting the molecules in a user-provided dataset.

The input is a .csv/.csv.gz file with containing a SMILES and identifier column.  
The app exposes a landing page and three endpoints:

- `/image`: Returns the image of the molecule given a compound ID
- `/smiles`: Returns the SMILES string of the molecule given its ID
- `/depict`: Produces an image for an arbitrary SMILES string

### Requirements

- `flask`
- `rdkit`
- `pandas`