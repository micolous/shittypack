# shittypack #

Repacks verbose GTFS feeds so that they consume less disk space.

Created for [Transport for NSW's GTFS feeds](https://tdx.transportnsw.info/) which are lazily converted from TransXchange format, and needlessly verbose.  It is currently in the process of being adapted to suit other transit networks' shitty files.

The root cause of these issues is some badly written transit network management software.  These software packages will just output a dump of their internal data structures, and make no regard for optimising the file.

With Transport NSW's dataset, this reduces the files to half of their original size, while being well-formed GTFS.  It doesn't yet do all possible optimisations, but still achieves [good results](#results).

I'm aware you could do better with some binary format like `protobuf`, but we actually care about it still being GTFS.

## What it does ##

- Removes Unicode byte order markers.
- Removes unneeded quotation characters on CSV fields.
- Removes padding on field names.
- Rounds shape and stop latitude and longitude to 6 decimal places (11cm [accuracy at the equator](https://en.wikipedia.org/wiki/Decimal_degrees)).
- Rounds trip distances (`shape_dist_traveled`) to 1 decimal place.  Specification does not define units, as this is only used for drawing parts of a shape between two stops.  Commonly this is in metres or kilometres.
- Rewrites the `agency_id`, `route_id`, `service_id`, `shape_id`, `stop_id` and `trip_id` fields so that they use incremental numeric values, instead of `1.TA.12-556-sj2-1.1.R`.
- Deletes `agency_id` entirely for feeds that have only one agency.
- Rewrites `calendar.txt` and `calendar_dates.txt` to remove unused and duplicate records.
- Removes entries from `trips.txt` and `stop_times.txt` for trips that are never taken (because of the calendar).
- Removes unused shapes, stops and transfers (because there are no trips that follow the route or stop there).

This makes the file size of [most data sets tested less than 70% of their original size](#results).

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

Agency (District)         | Location | Date       | Source   | Packed   | %   | CSP?
------------------------- | -------- | ---------- | -------- | -------- | --- | ----
Public Transport Victoria | VIC, AU  | 2015-03-30 | 0.98 GiB | 334 MiB  | 33% | Yes
Transport for NSW         | NSW, AU  | 2015-01-01 | 1.16 GiB | 457 MiB  | 38% | Yes
Transport for NSW         | NSW, AU  | 2015-04-02 | 0.94 GiB | 456 MiB  | 47% | Yes
MetroTAS (Hobart)         | TAS, AU  | 2015-03-18 | 23.5 MiB | 13.3 MiB | 56% | No
qConnect (Sunshine Coast) | QLD, AU  | 2014-11-24 | 145 KiB  | 83 KiB   | 57% | No
Translink (Brisbane)      | QLD, AU  | 2015-03-25 | 220 MiB  | 132 MiB  | 60% | No
ACTION                    | ACT, AU  | 2015-04-01 | 41.4 MiB | 25.4 MiB | 61% | No
Auckland Transit          | AUK, NZ  | 2015-02-13 | 47.3 MiB | 32.5 MiB | 69% | No
Wellington Metlink        | WGN, NZ  | 2015-01-14 | 34.1 MiB | 28.6 MiB | 84% | No
Adelaide Metro            | SA, AU   | 2015-02-12 | 56.1 MiB | 48.6 MiB | 87% | Yes
Transperth                | WA, AU   | 2015-04-01 | 90.9 MiB | 82.7 MiB | 91% | No
Metro Canterbury          | CAN, NZ  | 2015-04-05 | 12.7 MiB | 12.1 MiB | 96% | Yes

`CSP` = Current Shittypack version.  Newer versions of shittypack have better results, but testing is slow.  Results will be updated *in due course*.

More details on the testing methods, data quality notes and specific improvements are detailed in [results.md](https://github.com/micolous/shittypack/blob/master/results.md).

## Utility ###

This tool gets used to pack my mirrors of the [New South Welsh](https://bitbucket.org/micolous/transportnsw-gtfs), [Queenslander](https://bitbucket.org/micolous/queensland-gtfs) and [Victorian](https://bitbucket.org/micolous/ptvictoria-gtfs) public transit data feeds to more manageable sizes for revision control systems.

