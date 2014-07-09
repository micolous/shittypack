# shittypack #

Repacks verbose GTFS feeds so that they consume less disk space.

Created for [Transport NSW's GTFS feeds](https://tdx.transportnsw.info/) which are lazily converted from TransXchange format, and needlessly verbose.

With Transport NSW's dataset, this reduces the files to about half of their original size, while being well-formed GTFS.  I'm aware you could do better with some binary format like `protobuf`, but we actually care about it still being GTFS.

## What it does ##

- Removes Unicode byte order markers.
- Removes unneeded quotation characters on CSV fields.
- Rounds shape and stop latitude and longitude to 6 decimal places.
- Rounds trip distances to 1 decimal place.
- Rewrites the `shape_id`, `route_id`, `trip_id` and `service_id` fields so that they use incremental numeric values, instead of `1.TA.12-556-sj2-1.1.R`.
- Blows up or gives bad data if you don't run it properly.

## Usage ##

This requires that you pass the files in this order:

1. `shapes.txt`
2. `routes.txt`
3. `calendar.txt`
4. `calendar_dates.txt` (if present)
5. `trips.txt`
6. `stop_times.txt`
7. `stops.txt`
8. All other files.

They need to be done all in one shot, as existing IDs need to be remapped on the fly.  For example:

```console
$ python shittypack.py shapes.txt routes.txt calendar.txt calendar_dates.txt trips.txt stop_times.txt agency.txt stops.txt -o output/
```

The output directory (`-o`) will be created, and this tool will not run if the output directory already exists.  This is a safety mechanism so it doesn't overwrite files.

This tool is pretty unforgiving about problems (and shit).  It will probably give you bad output if it fails, and not complain about it.

If you don't specify the files in the correct order, you're going to have a bad time.

## Results -- Transport NSW "full Greater Sydney data", 2014-07-07. ##

### Source data ###

- Uncompressed: 938 MiB
- Compressed ZIP (as supplied): 206 MiB

```
-rw-rw-rw-@ 1 michael  staff       4320  7 Jul 11:51 agency.txt
-rw-rw-rw-@ 1 michael  staff      46436  7 Jul 11:51 calendar.txt
-rw-rw-rw-@ 1 michael  staff     102093  7 Jul 11:51 calendar_dates.txt
-rw-rw-rw-@ 1 michael  staff     153752  7 Jul 11:51 routes.txt
-rw-rw-rw-@ 1 michael  staff  289544136  7 Jul 11:51 shapes.txt
-rw-rw-rw-@ 1 michael  staff  671119136  7 Jul 11:51 stop_times.txt
-rw-rw-rw-@ 1 michael  staff    3475362  7 Jul 11:51 stops.txt
-rw-rw-rw-@ 1 michael  staff   18790239  7 Jul 11:51 trips.txt
```

### Shitty-packed data ###

- Uncompressed: 458 MiB (49% of original)
- Compressed ZIP (zip -9): 111 MiB (54% of original)

```
-rw-r--r--+ 1 michael  staff       3779  9 Jul 23:37 agency.txt
-rw-r--r--+ 1 michael  staff      26804  9 Jul 23:36 calendar.txt
-rw-r--r--+ 1 michael  staff      56381  9 Jul 23:36 calendar_dates.txt
-rw-r--r--+ 1 michael  staff     121597  9 Jul 23:36 routes.txt
-rw-r--r--+ 1 michael  staff  137854807  9 Jul 23:36 shapes.txt
-rw-r--r--+ 1 michael  staff  332237581  9 Jul 23:37 stop_times.txt
-rw-r--r--+ 1 michael  staff    2460802  9 Jul 23:37 stops.txt
-rw-r--r--+ 1 michael  staff    7211783  9 Jul 23:36 trips.txt
```