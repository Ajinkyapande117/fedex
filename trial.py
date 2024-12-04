import pandas as pd

# ULD data
uld_data = [
    ("U1", 224, 150, 162, 2500),
    ("U2", 224, 318, 162, 2500),
    ("U3", 244, 318, 244, 2800),
    ("U4", 244, 318, 244, 2800),
    ("U5", 244, 318, 285, 3500),
    ("U6", 244, 31, 28, 3500)
]

# Package data (add more packages as needed)
package_data = [
     ("P-1", 99, 53, 55, 61, False, 176),
("P-2", 56, 99, 81, 53, True, None),
("P-3", 42, 101, 51, 17, True, None),
("P-4", 108, 75, 56, 73, False, 138),
("P-5", 88, 58, 64, 93, False, 139),
("P-6", 91, 56, 84, 47, True, None),
("P-7", 88, 78, 93, 117, False, 102),
("P-8", 108, 105, 76, 142, False, 108),
("P-9", 73, 71, 88, 50, True, None),
("P-10", 88, 70, 85, 81, True, None),
("P-11", 55, 80, 81, 23, False, 96),
("P-12", 48, 80, 88, 27, False, 117),
("P-13", 55, 94, 87, 41, False, 73),
("P-14", 45, 46, 81, 27, False, 68),
("P-15", 84, 49, 60, 57, True, None),
("P-16", 48, 93, 63, 82, True, None),
("P-17", 83, 63, 57, 29, True, None),
("P-18", 68, 101, 95, 96, False, 65),
("P-19", 51, 87, 69, 73, False, 107),
("P-20", 88, 106, 56, 71, True, None),
("P-21", 105, 71, 105, 223, False, 116),
("P-22", 100, 92, 99, 191, False, 86),
("P-23", 51, 50, 110, 59, True, None),
("P-24", 81, 109, 55, 123, False, 69),
("P-25", 44, 77, 53, 37, False, 108),
("P-26", 69, 56, 73, 56, False, 130),
("P-27", 93, 62, 49, 18, False, 122),
("P-28", 81, 64, 95, 70, False, 139),
("P-29", 62, 86, 53, 23, False, 122),
("P-30", 88, 85, 102, 164, False, 70),
("P-31", 71, 49, 76, 67, False, 76),
("P-32", 70, 44, 98, 53, False, 124),
("P-33", 90, 89, 73, 132, False, 136),
("P-34", 87, 45, 81, 45, False, 77),
("P-35", 83, 72, 63, 96, False, 103),
("P-36", 86, 80, 78, 146, True, None),
("P-37", 59, 76, 51, 33, False, 131),
("P-38", 84, 96, 48, 21, False, 60),
("P-39", 96, 64, 61, 61, False, 111),
("P-40", 70, 45, 90, 78, False, 106)
]

K = 40 # Delay for spreading priority packages into multiple ULDs

uld_df = pd.DataFrame(uld_data, columns=["ULD_ID", "Length", "Width", "Height", "Weight_Limit"])
package_df = pd.DataFrame(package_data,
                          columns=["Package_ID", "Length", "Width", "Height", "Weight", "Type", "Cost_of_Delay"])

def rotate_package(package):
    # Generate all possible rotations of the package
    rotations = [
        (package["Length"], package["Width"], package["Height"]),
        (package["Length"], package["Height"], package["Width"]),
        (package["Width"], package["Length"], package["Height"]),
        (package["Width"], package["Height"], package["Length"]),
        (package["Height"], package["Length"], package["Width"]),
        (package["Height"], package["Width"], package["Length"])
    ]
    return rotations

def fit_packages_to_uld(uld_df, package_df):
    allocations = {uld: [] for uld in uld_df["ULD_ID"]}
    positions = {uld: [] for uld in uld_df["ULD_ID"]}
    
    remaining_space = {
        uld: {
            "Length": uld_df.loc[uld_df["ULD_ID"] == uld, "Length"].values[0],
            "Width": uld_df.loc[uld_df["ULD_ID"] == uld, "Width"].values[0],
            "Height": uld_df.loc[uld_df["ULD_ID"] == uld, "Height"].values[0],
            "Volume": uld_df.loc[uld_df["ULD_ID"] == uld, "Length"].values[0] * 
                      uld_df.loc[uld_df["ULD_ID"] == uld, "Width"].values[0] * 
                      uld_df.loc[uld_df["ULD_ID"] == uld, "Height"].values[0],
            "Weight": uld_df.loc[uld_df["ULD_ID"] == uld, "Weight_Limit"].values[0]
        } for uld in uld_df["ULD_ID"]
    }

    occupied_positions = {uld: [] for uld in uld_df["ULD_ID"]}
    
    # Sort packages by size (volume), weight and type for better packing
    package_df["Volume"] = package_df["Length"] * package_df["Width"] * package_df["Height"]
    package_df = package_df.sort_values(by=["Type", "Volume", "Weight"], ascending=[False, False, False])
    
    allocations_result = []

    for _, package in package_df.iterrows():
        package_volume = package["Volume"]
        package_weight = package["Weight"]
        package_rotations = rotate_package(package)
        
        allocated = False
        best_uld = None
        best_position = None
        
        # Try to allocate the package
        for uld in sorted(allocations.keys(), key=lambda x: remaining_space[x]["Volume"], reverse=True):
            if remaining_space[uld]["Weight"] >= package_weight and remaining_space[uld]["Volume"] >= package_volume:
                for rotation in package_rotations:
                    p_length, p_width, p_height = rotation
                    
                    # Check potential positions within the ULD dimensions
                    for x in range(remaining_space[uld]["Length"] - p_length + 1):
                        for y in range(remaining_space[uld]["Width"] - p_width + 1):
                            for z in range(remaining_space[uld]["Height"] - p_height + 1):
                                # Check overlap using spatial partitioning
                                overlap = False
                                for pos in occupied_positions[uld]:
                                    if is_overlapping((x,y,z), (x+p_length,y+p_width,z+p_height), pos):
                                        overlap = True
                                        break
                                if not overlap:
                                    best_uld = uld
                                    best_position = (x,y,z)
                                    allocated = True
                                    break
                            if allocated:
                                break
                        if allocated:
                            break
            
            if allocated:
                break
        
        if best_uld is not None:
            allocations[best_uld].append(package["Package_ID"])
            remaining_space[best_uld]["Volume"] -= package_volume
            remaining_space[best_uld]["Weight"] -= package_weight
            
            occupied_positions[best_uld].append((best_position,(p_length,p_width,p_height)))
            
            allocations_result.append((package["Package_ID"], best_uld, best_position))
    
    return allocations_result

def is_overlapping(new_pos_start, new_pos_end, existing_pos):
    existing_start = existing_pos[0]
    existing_end = (existing_start[0] + existing_pos[1][0], 
                    existing_start[1] + existing_pos[1][1], 
                    existing_start[2] + existing_pos[1][2])
    
    overlap_x = not (new_pos_end[0] <= existing_start[0] or new_pos_start[0] >= existing_end[0])
    overlap_y = not (new_pos_end[1] <= existing_start[1] or new_pos_start[1] >= existing_end[1])
    overlap_z = not (new_pos_end[2] <= existing_start[2] or new_pos_start[2] >= existing_end[2])
    
    return overlap_x and overlap_y and overlap_z

allocations_result = fit_packages_to_uld(uld_df, package_df)

# Count priority ULDs
priority_package_ids = package_df[package_df['Type'] == True]['Package_ID'].tolist()
priority_uld_count = len(set([uld_id for pkg_id, uld_id, _ in allocations_result if pkg_id in priority_package_ids and uld_id is not None]))

print(f"Number of ULDs with priority packages: {priority_uld_count}")
print(f"Cost Delay: {K * priority_uld_count}")
print("Package Allocations to ULDs and Positions:")
for result in allocations_result:
    print(f"Package {result[0]} allocated to ULD {result[1]} at position {result[2]}.")
