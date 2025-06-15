# 🟣 Purpleprint Bridge

**Purpleprint Bridge** is a Blender add-on designed to export scene object data into a format compatible with [Purpleprint Placer](https://github.com/Hevedy/Purpleprint-Core) and other Unreal Engine-based tools.

This tool enables quick and structured transfer of level design data from Blender to Unreal Engine pipelines, making it ideal for prototyping, layout planning, and mass placement of entities in-game.

---

## ✨ Features

- Exports only objects marked as **visible for render**.
- Ignores all `EMPTY` objects, but **applies their transformations to their children**.
- Outputs to Unreal Engine–compatible `.csv` files with the following structure:
  ```csv
  Row,"Name","Type","(X=0,Y=0,Z=0)","(Pitch=0,Yaw=0,Roll=0)","(X=1,Y=1,Z=1)"


## Links
[Purpleprint](https://www.hevedy.com/purpleprint/)
[Purpleprint Core](https://github.com/Hevedy/Purpleprint-Core)