# TilesetParser

find single tile image in folder full of tilesets. It's very common that many tilesets are unorganized and contains unrecognaizable names. With TileParser you can take one tile (for example screenshot from web) and find whitch tileset contains that tile.
To parse large amount of files TilesetParser uses AI (openCV)

---

## Instalation

```
pip install TilesetParser
```

## How to use?

```
tilesetparser /path/to/source/image.bmp /path/to/folder_with_tilesets
```

Program takes a few arguments:

### positional arguments:

- source_image_path
  > Path to single source tile you need to find
- tiles_folder
  > Path to tileset folder you want to parse

### options:

- -h, --help
  > Show help message and exit
- -s, --size
  > Size of a tile (default: 32)
- -q, --similarity
  > Similarity level for openCV (default: 0.8)
- -e, --extension
  > Extension of the files (default: bmp)
