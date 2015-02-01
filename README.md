# shittypack #

Repacks verbose GTFS feeds so that they consume less disk space.

Created for [Transport NSW's GTFS feeds](https://tdx.transportnsw.info/) which are lazily converted from TransXchange format, and needlessly verbose.  It is currently in the process of being adapted to suit other transit networks' shitty files.

The root cause of these issues is some badly written transit network management software.  These software packages will just output a dump of their internal data structures, and make no regard for optimising the file.

With Transport NSW's dataset, this reduces the files to about half of their original size, while being well-formed GTFS.  I'm aware you could do better with some binary format like `protobuf`, but we actually care about it still being GTFS.

## What it does ##

- Removes Unicode byte order markers.
- Removes unneeded quotation characters on CSV fields.
- Rounds shape and stop latitude and longitude to 6 decimal places.
- Rounds trip distances to 1 decimal place.
- Rewrites the `shape_id`, `route_id`, `trip_id` and `service_id` fields so that they use incremental numeric values, instead of `1.TA.12-556-sj2-1.1.R`.
- **WIP:** [Rewriting `calendar.txt` to eliminate identical records.](https://github.com/micolous/shittypack/issues/3)

## Usage ##

This requires you pass in the `google_transit.zip` file, and it will return a new version of that archive, repacked.

```console
$ python shittypack.py google_transit.zip -o google_transit_packed.zip
```

The output directory (`-o`) will be created, and this tool will not run if the output directory already exists.  This is a safety mechanism so it doesn't overwrite files.

This tool is pretty unforgiving about problems (and shit).  It will probably give you bad output if it fails, and not complain about it.

## Results -- Transport NSW "full Greater Sydney data", 2015-01-04. ##

### Source data ###

- Uncompressed: 1.16 GiB
- Compressed ZIP (as supplied): 261 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     4329  2015-01-01 23:09   agency.txt
  3458772  2015-01-01 23:04   stops.txt
   124288  2015-01-01 23:09   routes.txt
    49408  2015-01-01 23:09   calendar.txt
   122369  2015-01-01 23:09   calendar_dates.txt
317571979  2015-01-01 23:09   shapes.txt
 25273020  2015-01-01 23:09   trips.txt
899601310  2015-01-01 23:09   stop_times.txt
---------                     -------
1246205475                     8 files
```

### Shitty-packed data ###

- Uncompressed: 579 MiB (49% of original)
- Compressed ZIP: 144 MiB (55% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
    28580  2015-02-01 23:36   calendar.txt
    67999  2015-02-01 23:36   calendar_dates.txt
151615306  2015-02-01 23:37   shapes.txt
    98360  2015-02-01 23:37   routes.txt
  9645885  2015-02-01 23:37   trips.txt
443701997  2015-02-01 23:37   stop_times.txt
  2449603  2015-02-01 23:37   stops.txt
     3788  2015-02-01 23:37   agency.txt
---------                     -------
607611518                     8 files

```
