# The Results #

Benefits are stated in the percentage of the size of the original uncompressed data vs. the shitty-packed data.

As a result, lower percentages mean that shittypack was able to make big improvements, and indicates cities with poor quality data sources.

Conversely, higher percentages mean that shittypack was not able to make big improvements, and may indicate cities with good quality data sources.  Or that they have issues which shittypack doesn't know how to sort out just yet.

# TfNSW "full Greater Sydney data", 2015-01-04 #

Transport for NSW is large dataset, and an example of a really bad feed (as it is converted from TransXchange), so sees significant improvements after being shitty-packed.

Percentage of original size: 39%

## Source data ##

- Uncompressed: 1.16 GiB

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

## Shitty-packed data ##

- Uncompressed: 467 MiB (39% of original)

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

# Public Transport Victoria, 2015-03-30 #

PTV's data has similar problems to TfNSW, being converted from another format.  Source data is supplied as a ZIP file containing 10 more ZIP files, one for each mode/region of the transit network.

Percentage of original size: 34%

- Source uncompressed: 0.98GB
- Shitty-packed uncompressed: 345 MiB

# Auckland Transit, 2015-02-13 #

Auckland Transit's feed is mediocre, but is very verbose about calendar entries.  It doesn't have a large amount of services or accurate shape data (it doesn't follow roads or rail), which means the problems with the feed don't balloon out as much as larger networks.

Percentage of original size: 69%

## Source data ##

- Uncompressed: 47.3 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      153  2015-02-13 06:27   agency.txt
  1092156  2015-02-13 06:28   calendar.txt
   429821  2015-02-13 06:29   calendar_dates.txt
    95061  2015-02-13 06:27   routes.txt
  2395801  2015-02-13 06:29   shapes.txt
 43844232  2015-02-13 06:32   stop_times.txt
   307535  2015-02-13 06:27   stops.txt
  1454830  2015-02-13 06:28   trips.txt
---------                     -------
 49619589                     8 files
```

## Shitty-packed data ##

- Uncompressed: 32.5 MiB (69% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      153  2015-02-15 02:00   agency.txt
     1736  2015-02-15 02:00   calendar.txt
     4238  2015-02-15 02:00   calendar_dates.txt
    84787  2015-02-15 02:00   routes.txt
  2289702  2015-02-15 02:00   shapes.txt
 30756607  2015-02-15 02:00   stop_times.txt
   307535  2015-02-15 02:00   stops.txt
   599894  2015-02-15 02:00   trips.txt
---------                     -------
 34044652                     8 files
```

# Adelaide Metro, 2015-02-12 #

Adelaide Metro's feed is very clean, and has not a large amount of services.  As a result it only sees small improvements with shittypack.  It also has some additional metadata in the file which shittypack handles.

Percentage of original size: 87%

## Source Data ##

- Uncompressed: 56.1 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      778  2015-02-12 10:32   agency.txt
     2113  2015-02-12 10:32   calendar.txt
      461  2015-02-12 10:32   calendar_dates.txt
      165  2015-02-12 09:51   feed_info.txt
     1101  2015-02-12 09:50   Release Notes.txt
    80413  2015-02-12 10:32   routes.txt
 14378603  2015-02-12 10:32   shapes.txt
 42558114  2015-02-12 10:32   stop_times.txt
   969757  2015-02-12 10:32   stops.txt
     9953  2015-02-12 10:32   transfers.txt
   873208  2015-02-12 10:32   trips.txt
---------                     -------
 58874666                     11 files
```

## Shitty-packed data ##

- Uncompressed: 48.9 MiB (87% of original)

```
Archive:  packed_adl.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      778  2015-02-15 01:39   agency.txt
     1700  2015-02-15 01:39   calendar.txt
      343  2015-02-15 01:39   calendar_dates.txt
      167  2015-02-15 01:39   feed_info.txt
     1103  2015-02-15 01:39   Release Notes.txt
    79537  2015-02-15 01:39   routes.txt
 12194668  2015-02-15 01:39   shapes.txt
 37239230  2015-02-15 01:39   stop_times.txt
   922242  2015-02-15 01:39   stops.txt
     9953  2015-02-15 01:39   transfers.txt
   803735  2015-02-15 01:39   trips.txt
---------                     -------
 51253456                     11 files
```

