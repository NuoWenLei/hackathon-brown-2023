from firestore import get_all_locations
from collage_in_location import create_collage_in_location

def main():
	locs = get_all_locations()
	for loc in locs:
		if loc["num_images"] >= 3:
			create_collage_in_location(loc["_id"])

if __name__ == "__main__":
	main()