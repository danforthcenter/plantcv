CREATE TABLE IF NOT EXISTS `runinfo` (
  `run_id` INTEGER PRIMARY KEY,
  `datetime` INTEGER NOT NULL,
  `pipeline` TEXT NOT NULL,
  `outlier_version` TEXT NOT NULL
);

--snapshots table
--Stores data on individual images and image groups (snapshots)
CREATE TABLE IF NOT EXISTS `snapshots` (
  `image_id` INTEGER PRIMARY KEY,
  `snapshot_id` INTEGER NOT NULL,
  `plant_id` TEXT NOT NULL,
  `datetime` INTEGER NOT NULL,
  `camera` TEXT NOT NULL,
  `frame` TEXT NOT NULL,
  `zoom` INTEGER NOT NULL,
  `image_path` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `vis_shapes` (
  `image_id` INTEGER PRIMARY KEY,
  `area_raw` REAL NOT NULL,
  `hull_area` REAL NOT NULL,
  `solidity` REAL NOT NULL,
  `perimeter` REAL NOT NULL,
  `extent_x` INTEGER NOT NULL,
  `extent_y` INTEGER NOT NULL,
  `centroid_x` REAL NOT NULL,
  `centroid_y` REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS `vis_colors` (
  `image_id` INTEGER PRIMARY KEY,
  `blue` TEXT NOT NULL,
  `green` TEXT NOT NULL,
  `red` TEXT NOT NULL,
  `lightness` TEXT NOT NULL,
  `green-magenta` TEXT NOT NULL,
  `blue-yellow` TEXT NOT NULL,
  `hue` TEXT NOT NULL,
  `saturation` TEXT NOT NULL,
  `value` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `nir_shapes` (
  `image_id` INTEGER PRIMARY KEY,
  `area_raw` REAL NOT NULL,
  `hull_area` REAL NOT NULL,
  `solidity` REAL NOT NULL,
  `perimeter` REAL NOT NULL,
  `extent_x` INTEGER NOT NULL,
  `extent_y` INTEGER NOT NULL,
  `centroid_x` REAL NOT NULL,
  `centroid_y` REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS `nir_signal` (
  `image_id` INTEGER PRIMARY KEY,
  `signal` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `flu_shapes` (
  `image_id` INTEGER PRIMARY KEY,
  `area_raw` REAL NOT NULL,
  `hull_area` REAL NOT NULL,
  `solidity` REAL NOT NULL,
  `perimeter` REAL NOT NULL,
  `extent_x` INTEGER NOT NULL,
  `extent_y` INTEGER NOT NULL,
  `centroid_x` REAL NOT NULL,
  `centroid_y` REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS `flu_fvfm` (
  `image_id` INTEGER PRIMARY KEY,
  `fvfm` TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS `snapshot_id` ON `snapshots` (`snapshot_id`);
CREATE INDEX IF NOT EXISTS `plant_id` ON `snapshots` (`plant_id`);
