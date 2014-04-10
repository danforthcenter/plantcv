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
  `run_id` INTEGER NOT NULL,
  `snapshot_id` INTEGER NOT NULL,
  `plant_id` TEXT NOT NULL,
  `datetime` INTEGER NOT NULL,
  `camera` TEXT NOT NULL,
  `frame` INTEGER NOT NULL,
  `zoom` INTEGER NOT NULL,
  `image_path` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `vis_shapes` (
  `image_id` INTEGER PRIMARY KEY,
  `area_raw` REAL NOT NULL,
  `area_corrected` REAL NOT NULL,
  `hull_area` REAL NOT NULL,
  `solidity` REAL NOT NULL,
  `perimeter` REAL NOT NULL,
  `extent_x` INTEGER NOT NULL,
  `extent_y` INTEGER NOT NULL,
  `centroid_x` REAL NOT NULL,
  `centroid_y` REAL NOT NULL,
  `longest_axis` REAL NOT NULL,
  `in_bounds` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `vis_colors` (
  `image_id` INTEGER PRIMARY KEY,
  `bins` INTEGER NOT NULL,
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
  `bins` INTEGER NOT NULL,
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
  `bins` INTEGER NOT NULL,
  `fvfm` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `analysis_images` (
  `image_id` INTEGER NOT NULL,
  `type` TEXT NOT NULL,
  `image_path` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `boundary_data` (
  `image_id` INTEGER NOT NULL,
  `x_position` INTEGER NOT NULL,
  `height_above_bound` INTEGER NOT NULL,
  `height_below_bound` INTEGER NOT NULL,
  `above_bound_area` INTEGER NOT NULL,
  `percent_above_bound_area` REAL NOT NULL,
  `below_bound_area` INTEGER NOT NULL,
  `percent_below_bound_area` REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS `snapshot_id` ON `snapshots` (`snapshot_id`);
CREATE INDEX IF NOT EXISTS `plant_id` ON `snapshots` (`plant_id`);
CREATE INDEX IF NOT EXISTS `image_id` ON `analysis_images` (`image_id`);
CREATE INDEX IF NOT EXISTS `type` ON `analysis_images` (`type`);
CREATE INDEX IF NOT EXISTS `image_id` ON `boundary_data` (`image_id`);
