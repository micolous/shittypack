# The Results #

Benefits are stated in the percentage of the size of the original uncompressed data vs. the shitty-packed data.

As a result, lower percentages mean that shittypack was able to make big improvements, and indicates cities with poor quality data sources.

Conversely, higher percentages mean that shittypack was not able to make big improvements, and may indicate cities with good quality data sources.  Or that they have issues which shittypack doesn't know how to sort out just yet.

For all the tests, we only compare the **uncompressed** size of the data files.  While there is a corresponding improvement on filesizes of the resulting ZIP file, it does not accurately convey how much data is eliminated.

# Public Transport Victoria, 2015-03-30 #

PTV's data has similar problems to TfNSW, being converted from another format.  Source data is supplied as a ZIP file containing 10 more ZIP files, one for each mode/region of the transit network.

Percentage of original size: 34%

- Source uncompressed: 0.98GB
- Shitty-packed uncompressed: 334 MiB

# TfNSW "full Greater Sydney data", 2015-01-01 #

Transport for NSW is large dataset, and an example of a really bad feed (as it is converted from TransXchange), so sees significant improvements after being shitty-packed.

Percentage of original size: 38%

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

- Uncompressed: 457 MiB (38% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     8935  2015-04-05 22:03   calendar.txt
    17694  2015-04-05 22:03   calendar_dates.txt
     3753  2015-04-05 22:03   agency.txt
    96855  2015-04-05 22:03   routes.txt
  7094463  2015-04-05 22:03   trips.txt
142093381  2015-04-05 22:04   shapes.txt
317094960  2015-04-05 22:04   stop_times.txt
  2374179  2015-04-05 22:04   stops.txt
---------                     -------
468784220                     8 files
```

# TfNSW "full Greater Sydney data", 2015-04-02 #

Converted from TransXchange, but shows less improvements due to less train-replacement services (back in 2015-01-04).

Percentage of original size: 47%

## Source data ##

- Uncompressed: 0.94 GiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     4327  2015-04-02 23:03   agency.txt
    44807  2015-04-02 23:03   calendar.txt
   190877  2015-04-02 23:03   calendar_dates.txt
   133263  2015-04-02 23:03   routes.txt
319311697  2015-04-02 23:03   shapes.txt
  3485436  2015-04-02 22:56   stops.txt
675450832  2015-04-02 23:03   stop_times.txt
 19980917  2015-04-02 23:03   trips.txt
---------                     -------
1018602156                     8 files
```

## Shitty-packed data ##

- Uncompressed: 470 MiB (46% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     9196  2015-04-06 00:24   calendar.txt
    31221  2015-04-06 00:24   calendar_dates.txt
     3698  2015-04-06 00:24   agency.txt
   103058  2015-04-06 00:24   routes.txt
  7194343  2015-04-06 00:24   trips.txt
146037827  2015-04-06 00:25   shapes.txt
312048064  2015-04-06 00:25   stop_times.txt
  2370809  2015-04-06 00:25   stops.txt
---------                     -------
467798216                     8 files
```

# MetroTAS Hobart, 2015-03-18 #

http://www.metrotas.com.au/community/gtfs/

Percentage of original size: 56%

## Source data ##

- Uncompressed: 23.5 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      151  2015-03-18 16:06   agency.txt
     1599  2015-03-18 16:06   calendar.txt
    80563  2015-03-18 16:06   calendar_dates.txt
     7507  2015-03-18 16:06   routes.txt
 16767392  2015-03-18 16:07   shapes.txt
   202353  2015-03-18 16:07   stops.txt
  7392790  2015-03-18 16:07   stop_times.txt
       57  2015-03-18 16:07   transfers.txt
   224402  2015-03-18 16:07   trips.txt
---------                     -------
 24676814                     9 files
```

## Shitty-packed data ##

- Uncompressed: 13.3 MiB (56% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      151  2015-04-03 22:09   agency.txt
     1268  2015-04-03 22:09   calendar.txt
    45207  2015-04-03 22:09   calendar_dates.txt
     7094  2015-04-03 22:09   routes.txt
  9776894  2015-04-03 22:09   shapes.txt
  3806662  2015-04-03 22:09   stop_times.txt
   175919  2015-04-03 22:09   stops.txt
       57  2015-04-03 22:09   transfers.txt
    85693  2015-04-03 22:09   trips.txt
---------                     -------
 13898945                     9 files
```

# Translink (South-East Queensland), 2015-03-25 #

For this test, only [the data for South-East Queensland](https://data.qld.gov.au/dataset/general-transit-feed-specification-gtfs-seq/resource/be7f19e5-3ee8-4396-b9eb-46f6b4ce8039) was used.

Percentage of original size: 60%

## Source data ##

- Uncompressed: 219.5 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      135  2015-03-25 10:36   agency.txt
     7061  2015-03-25 10:36   calendar.txt
   236289  2015-03-25 10:37   calendar_dates.txt
      191  2015-03-25 10:38   feed_info.txt
    70011  2015-03-25 10:20   routes.txt
 28227137  2015-03-25 10:20   shapes.txt
  1536016  2015-03-25 10:21   stops.txt
189296806  2015-03-25 10:18   stop_times.txt
 10802005  2015-03-25 10:20   trips.txt
---------                     -------
230175651                     9 files
```

## Shitty-packed data ##

- Uncompressed: 132.1 MiB (60% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      135  2015-04-03 17:23   agency.txt
     2456  2015-04-03 17:23   calendar.txt
    40703  2015-04-03 17:23   calendar_dates.txt
      191  2015-04-03 17:23   feed_info.txt
    67044  2015-04-03 17:23   routes.txt
107269047  2015-04-03 17:23   stop_times.txt
 25268621  2015-04-03 17:23   shapes.txt
  1536016  2015-04-03 17:23   stops.txt
  4396289  2015-04-03 17:23   trips.txt
---------                     -------
138580502                     9 files
```

# qConnect, Sunshine Coast (Maleny-Landsborough), 2014-11-24 #

This is a very small [data file](https://data.qld.gov.au/dataset/general-transit-feed-specification-gtfs-seq/resource/e725929f-7c51-4eb8-be1d-4d162010cb98), but still shows there is room for improvement on small files.

Percentage of original size: 57%

## Source data ##

- Uncompressed: 145 KiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      222  2014-11-24 13:32   agency.txt
      449  2014-11-24 13:33   calendar.txt
      494  2014-11-24 13:33   calendar_dates.txt
      191  2014-11-24 10:53   feed_info.txt
      213  2014-11-24 13:52   routes.txt
    31945  2014-11-24 09:26   shapes.txt
     3169  2014-11-24 13:52   stops.txt
    96799  2014-11-24 13:34   stop_times.txt
    15180  2014-11-24 13:35   trips.txt
---------                     -------
   148662                     9 files
```

## Shitty-packed data ##

- Uncompressed: 83 KiB (57% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      220  2015-04-03 18:06   agency.txt
      299  2015-04-03 18:06   calendar.txt
      200  2015-04-03 18:06   calendar_dates.txt
      191  2015-04-03 18:06   feed_info.txt
      197  2015-04-03 18:06   routes.txt
    26785  2015-04-03 18:06   shapes.txt
    49674  2015-04-03 18:06   stop_times.txt
     3169  2015-04-03 18:06   stops.txt
     4570  2015-04-03 18:06   trips.txt
---------                     -------
    85305                     9 files
```

# ACTION, 2015-04-01 #

https://data.gov.au/dataset/action-bus-service-gtfs-feed-act

Percentage of original size: 61%

## Source data ##

- Uncompressed: 41.4 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      131  2015-04-01 14:45   agency.txt
      378  2015-04-01 14:45   calendar.txt
      733  2015-04-01 14:45   calendar_dates.txt
    16200  2015-04-01 14:45   routes.txt
 13096106  2015-04-01 14:47   shapes.txt
 29128302  2015-04-01 14:46   stop_times.txt
   194796  2015-04-01 14:45   stops.txt
  1023723  2015-04-01 14:45   trips.txt
---------                     -------
 43460369                     8 files
```

## Shitty-packed data ##

- Uncompressed: 25.4 MiB (61% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      129  2015-04-03 21:20   agency.txt
      264  2015-04-03 21:20   calendar.txt
      298  2015-04-03 21:20   calendar_dates.txt
    13380  2015-04-03 21:20   routes.txt
  9959572  2015-04-03 21:20   shapes.txt
 16155946  2015-04-03 21:20   stop_times.txt
   189154  2015-04-03 21:20   stops.txt
   299505  2015-04-03 21:20   trips.txt
---------                     -------
 26618248                     8 files
```

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

# Wellington Metlink, 2015-01-14 #

http://www.metlink.org.nz/customer-services/general-transit-feed-specification/

Percentage of original size: 84%

## Source data ##

- Uncompressed: 34.1 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      956  2015-01-14 11:08   agency.txt
     6801  2015-01-14 11:08   calendar.txt
   273320  2015-01-14 11:08   calendar_dates.txt
      164  2015-01-14 11:08   feed_info.txt
    11122  2015-01-14 11:08   routes.txt
 22683796  2015-01-14 11:08   shapes.txt
 12240734  2015-01-14 11:08   stop_times.txt
   280821  2015-01-14 11:08   stops.txt
   273954  2015-01-14 11:08   trips.txt
---------                     -------
 35771668                     9 files
```

## Shitty-packed data ##

- Uncompressed: 28.6 MiB (84% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      956  2015-04-05 18:36   agency.txt
     3140  2015-04-05 18:36   calendar.txt
    44179  2015-04-05 18:36   calendar_dates.txt
      164  2015-04-05 18:36   feed_info.txt
     9766  2015-04-05 18:36   routes.txt
 12240582  2015-04-05 18:36   stop_times.txt
 17269576  2015-04-05 18:36   shapes.txt
   261071  2015-04-05 18:36   stops.txt
   162517  2015-04-05 18:36   trips.txt
---------                     -------
 29991951                     9 files
```


# Adelaide Metro, 2015-02-12 #

[Adelaide Metro's feed](http://www.adelaidemetro.com.au/Developer-Information) is fairly clean, and has not a large amount of services.  As a result it only sees small improvements with shittypack.  It also has some additional metadata in the file which shittypack handles.

Percentage of original size: 87%

## Source data ##

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

- Uncompressed: 48.6 MiB (87% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     1700  2015-04-05 22:13   calendar.txt
      343  2015-04-05 22:13   calendar_dates.txt
      778  2015-04-05 22:13   agency.txt
    79537  2015-04-05 22:13   routes.txt
   802562  2015-04-05 22:13   trips.txt
 12189272  2015-04-05 22:13   shapes.txt
 36944055  2015-04-05 22:13   stop_times.txt
   919614  2015-04-05 22:13   stops.txt
     8483  2015-04-05 22:13   transfers.txt
      167  2015-04-05 22:13   feed_info.txt
     1103  2015-04-05 22:13   Release Notes.txt
---------                     -------
 50947614                     11 files
```

# Transperth, 2015-04-01 #

Transperth's data has only minor improvements that can be made to it, only floating-point error on geospatial co-ordinates causing excessive decimal points to be used, removal of redundant calendar entries, and un-needed quotation marks in CSV files.

Percentage of original size: 91%

## Source data ##

- Uncompressed: 90.9 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     1807  2015-04-01 12:46   agency.txt
    23739  2015-04-01 12:48   calendar.txt
    47577  2015-04-01 12:48   calendar_dates.txt
    28727  2015-04-01 12:46   routes.txt
 46340022  2015-04-01 12:47   shapes.txt
  1233541  2015-04-01 12:48   stops.txt
 46296933  2015-04-01 12:50   stop_times.txt
      166  2015-04-01 12:50   transfers.txt
  1309921  2015-04-01 12:47   trips.txt
---------                     -------
 95282433                     9 files
```

## Shitty-packed data ##

- Uncompressed: 82.7 MiB (91% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     1807  2015-04-03 23:05   agency.txt
     4495  2015-04-03 23:05   calendar.txt
    13226  2015-04-03 23:05   calendar_dates.txt
    28322  2015-04-03 23:05   routes.txt
 39795135  2015-04-03 23:05   shapes.txt
  1004177  2015-04-03 23:05   stops.txt
 44755831  2015-04-03 23:05   stop_times.txt
      163  2015-04-03 23:05   transfers.txt
  1151377  2015-04-03 23:05   trips.txt
---------                     -------
 86754533                     9 files
```

# Metro Canterbury, 2015-04-05 #

This is a very [small datafile](http://data.ecan.govt.nz/Catalogue/Method?MethodId=65#tab-data) which has very clean data, very few improvements can be made.

Percentage of original size: 96%

## Source data ##

- Uncompressed: 12.7 MiB

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      163  2015-04-05 07:04   agency.txt
      267  2015-04-05 07:04   calendar.txt
      245  2015-04-05 07:04   calendar_dates.txt
     2943  2015-04-05 07:04   routes.txt
   854241  2015-04-05 07:04   shapes.txt
 11913832  2015-04-05 07:04   stop_times.txt
   282541  2015-04-05 07:04   stops.txt
   233308  2015-04-05 07:04   trips.txt
---------                     -------
 13287540                     8 files
```

## Shitty-packed data ##

- Uncompressed: 12.1 MiB (96% of original)

```
  Length      Date    Time    Name
---------  ---------- -----   ----
      264  2015-04-05 22:18   calendar.txt
      242  2015-04-05 22:18   calendar_dates.txt
      149  2015-04-05 22:18   agency.txt
     2669  2015-04-05 22:18   routes.txt
   206321  2015-04-05 22:18   trips.txt
   824105  2015-04-05 22:18   shapes.txt
 11401737  2015-04-05 22:18   stop_times.txt
   274208  2015-04-05 22:18   stops.txt
---------                     -------
 12709695                     8 files
```
