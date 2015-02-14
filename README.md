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
- Rewrites `calendar.txt` and `calendar_dates.txt` to remove unused and duplicate records.
- Removes entries from `trips.txt` and `stop_times.txt` for trips that are never taken (because of the calendar).

This makes the file size of the GTFS data about **less than 40% of the original** (for Sydney, _see results below_).

There are some other features [which are planned](https://github.com/micolous/shittypack/issues) to reduce the file size further.

## Usage ##

This requires you pass in the `google_transit.zip` file, and it will return a new version of that archive, repacked.

```console
$ python shittypack.py google_transit.zip -o google_transit_packed.zip
```

The output file (`-o`) will be created, and will update an existing archive if present.  Any files with the same name inside the archive will be overwritten.

This tool is pretty unforgiving about problems (and shit).  It will probably give you bad output if it fails, and not complain about it.

## Results -- Transport NSW "full Greater Sydney data", 2015-01-04. ##

### Source data ###

- Uncompressed: 1.16 GiB
- Compressed ZIP (as supplied): 261 MiB

```
   Length      Date    Time    Name
 ---------  ---------- -----   ----
      4329  2015-01-01 23:09   agency.txt
     49408  2015-01-01 23:09   calendar.txt
    122369  2015-01-01 23:09   calendar_dates.txt
    124288  2015-01-01 23:09   routes.txt
 317571979  2015-01-01 23:09   shapes.txt
 899601310  2015-01-01 23:09   stop_times.txt
   3458772  2015-01-01 23:04   stops.txt
  25273020  2015-01-01 23:09   trips.txt
 ---------                     -------
1246205475                     8 files
```

### Shitty-packed data ###

- Uncompressed: 467 MiB (39% of original)
- Compressed ZIP: 115 MiB (44% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     3788  2015-02-15 01:15   agency.txt
     8935  2015-02-15 01:14   calendar.txt
    17694  2015-02-15 01:14   calendar_dates.txt
    98360  2015-02-15 01:14   routes.txt
151615306  2015-02-15 01:14   shapes.txt
328181393  2015-02-15 01:15   stop_times.txt
  2449603  2015-02-15 01:15   stops.txt
  7112780  2015-02-15 01:14   trips.txt
---------                     -------
489487859                     8 files
```

