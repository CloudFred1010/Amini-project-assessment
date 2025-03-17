import h5py

# Define the path to an example HDF5 file
input_file = "data/raw/SMAP_L2_SM_P_NRT_53836_A_20250228T150011_N17701_001.h5"

# Open the HDF5 file and explore its contents
with h5py.File(input_file, "r") as h5f:
    print("HDF5 File Structure:\n")
    
    def print_structure(name, obj):
        print(name, ":", type(obj))
    
    h5f.visititems(print_structure)

