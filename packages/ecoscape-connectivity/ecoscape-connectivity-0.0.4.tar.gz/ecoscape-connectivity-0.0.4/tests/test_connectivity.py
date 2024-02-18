import os
import sys
sys.path.append("..")
import ecoscape_connectivity
from ecoscape_connectivity.util import read_transmission_csv

DATA_PATH="../../ecoscape-layers/"

HABITAT_PATH = os.path.join(DATA_PATH, "tests/outputs/acowoo/habitat.tif")
TERRAIN_PATH = os.path.join(DATA_PATH, "tests/inputs/test_terrain_300_near_cropped.tif")
PERMEABILITY_PATH = os.path.join(DATA_PATH, "outputs/acowoo/transmission_refined_1.csv")

CONNECTIVITY_PATH = os.path.join(DATA_PATH, "connectivity.tif")
FLOW_PATH = os.path.join(DATA_PATH, "flow.tif")

p_dict = read_transmission_csv(PERMEABILITY_PATH)

def test_connectivity():
    ecoscape_connectivity.compute_connectivity(
        habitat_fn=HABITAT_PATH,
        terrain_fn=TERRAIN_PATH,
        permeability_dict=p_dict,
        connectivity_fn=CONNECTIVITY_PATH,
        flow_fn=FLOW_PATH,
        num_simulations=20
    )

test_connectivity()