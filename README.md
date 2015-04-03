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

## Results ##

Benefits are stated in the percentage of the size of the original uncompressed data vs. the shitty-packed data.

As a result, lower percentages mean that shittypack was able to make big improvements, and indicates cities with poor quality data sources.

Conversely, higher percentages mean that shittypack was not able to make big improvements, and may indicate cities with good quality data sources.  Or that they have issues which shittypack doesn't know how to sort out just yet.

Agency / Location              | Date       | Source   | Packed   | Percent
------------------------------ | ---------- | -------- | -------- | -------
Public Transport Victoria (AU) | 2015-03-30 | 0.98 GiB | 345 MiB  | 34%
Transport for NSW (AU)         | 2015-01-04 | 1.16 GiB | 467 MiB  | 39%
Auckland Transit (NZ)          | 2015-02-13 | 47.3 MiB | 32.5 MiB | 69%
Adelaide Metro (AU)            | 2015-02-12 | 56.1 MiB | 48.9 MiB | 87%

More details on the testing methods, data quality notes and specific improvements are detailed in [results.md](https://github.com/micolous/shittypack/blob/master/results.md).

