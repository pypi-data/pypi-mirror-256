import cv2
import os


def compare_images(img1, img2):
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return score


def split_into_tiles(image, tile_size=(32, 32)):
    tiles = []
    for y in range(0, image.shape[0], tile_size[1]):
        for x in range(0, image.shape[1], tile_size[0]):
            tile = image[y:y+tile_size[1], x:x+tile_size[0]]
            tiles.append(tile)
    return tiles


def find_matching_tile(source_image_path, tiles_folder, tile_size, similarity, extension, tiles_per_tileset):
    source_image = cv2.imread(source_image_path, cv2.IMREAD_COLOR)
    assert source_image.shape[:2] == (
        tile_size, tile_size), f"Source image must be {tile_size}px x {tile_size}px"

    for root, dirs, files in os.walk(tiles_folder):
        for file in files:
            if file.endswith(f".{extension}"):
                tile_path = os.path.join(root, file)
                tile_image = cv2.imread(tile_path, cv2.IMREAD_COLOR)

                tiles = split_into_tiles(
                    tile_image, tile_size=(tile_size, tile_size))

                for i, tile in enumerate(tiles):
                    if tile.shape[:2] == (tile_size, tile_size):
                        row = i // tiles_per_tileset
                        col = i % tiles_per_tileset
                        print(
                            f" Current file: {file} | Current row: {row} | Current column: {col}")
                        score = compare_images(source_image, tile)
                        if score > similarity:

                            print(
                                f"Tile was found at: {tile_path} | position: (row: {row}, col: {col}) | Similarity level: {'{:.2f}'.format(score * 100)}%")
                            return tile_path, (row, col)

    print("Tile not found.")
    return None, None
