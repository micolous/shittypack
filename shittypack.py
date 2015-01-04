#!/usr/bin/env python
"""
shittypack.py - Repacks GTFS data so that it is more compact.

Transport NSW's dataset is so verbose because it is converted from TransExchange.

Copyright 2014 Michael Farrell <http://micolous.id.au/>; BSD 3-clause

File order (as files must be in the correct order else this will break!)

shapes.txt
routes.txt
calendar.txt
calendar_dates.txt
trips.txt
stop_times.txt
other files


eg:
python repack.py shapes.txt routes.txt calendar.txt calendar_dates.txt trips.txt stop_times.txt agency.txt stops.txt -o output/

"""

import argparse, csv, os

parser = argparse.ArgumentParser()

parser.add_argument('csv', nargs='+')
parser.add_argument('-o', '--output-dir', required=True)

options = parser.parse_args()

os.mkdir(options.output_dir)

# Remap the shape, route, service and trip IDs to simple numbers.
# This is a very simple algo, it could do Hoffman encoding to make it better, but it's
# probably not worth it.
shape_map = {}
last_shape_id = 0

route_map = {}
last_route_id = 0

service_map = {}
last_service_id = 0

trip_map = {}
last_trip_id = 0

def swallow_windows_unicode(fileobj):
	"""
	Windows programs (specifically, Notepad) puts '\xef\xbb\xbf' at the start of
	a Unicode text file.  This is used to handle "utf-8-sig" files.

	This function looks for those bytes and advances the stream past them if
	they are present.

	Returns True if the characters were present.
	"""
	pos = fileobj.tell()
	try:
		bom = fileobj.read(3)
	except:
		# End of file, revert!
		fileobj.seek(pos)
	if bom == '\xef\xbb\xbf':
		return True

	# Bytes not present, rewind the stream
	fileobj.seek(pos)
	return False


for fn in options.csv:
	# Windows puts in Unicode BOM.  This will swallow it if it is present.
	#input_f = io.open(fn, 'r', encoding='utf-8-sig')
	input_f = open(fn, 'rb')
	swallow_windows_unicode(input_f)
	output_f = open(os.path.join(options.output_dir, fn), 'wb')

	c = csv.reader(input_f)
	oc = csv.writer(output_f)

	header = c.next()
	oc.writerow(header)

	if fn.lower().endswith('shapes.txt'):
		# shapes.txt
		# Clamp lat/long to 6 decimal places
		# Clamp trip distance to 1 decimal place
		id = header.index('shape_id')
		lat = header.index('shape_pt_lat')
		lng = header.index('shape_pt_lon')
		dst = header.index('shape_dist_traveled')

		for row in c:
			# clamp decimal places
			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]
			if '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			# remap shapes to numbers
			if row[id] not in shape_map:
				shape_map[row[id]] = str(last_shape_id)
				last_shape_id += 1

			row[id] = shape_map[row[id]]

			oc.writerow(row)
	elif fn.lower().endswith('routes.txt'):
		id = header.index('route_id')
		for row in c:
			# remap routes to numbers

			if row[id] not in route_map:
				route_map[row[id]] = str(last_route_id)
				last_route_id += 1

			row[id] = route_map[row[id]]

			oc.writerow(row)
			
	elif fn.lower().endswith('calendar.txt'):
		id = header.index('service_id')
		for row in c:
			# remap services to numbers

			if row[id] not in service_map:
				service_map[row[id]] = str(last_service_id)
				last_service_id += 1

			row[id] = service_map[row[id]]

			oc.writerow(row)

	elif fn.lower().endswith('calendar_dates.txt'):
		id = header.index('service_id')
		for row in c:
			# remap services to numbers
			row[id] = service_map[row[id]]

			oc.writerow(row)

	elif fn.lower().endswith('trips.txt'):
		rid = header.index('route_id')
		eid = header.index('service_id')
		tid = header.index('trip_id')
		hid = header.index('shape_id')
		for row in c:
			# remap services to numbers

			if row[tid] not in trip_map:
				trip_map[row[tid]] = str(last_trip_id)
				last_trip_id += 1

			row[tid] = trip_map[row[tid]]
			row[rid] = route_map[row[rid]]
			row[eid] = service_map[row[eid]]
			row[hid] = shape_map[row[hid]]

			oc.writerow(row)


	elif fn.lower().endswith('stop_times.txt'):
		# stop_times.txt
		# Clamp trip distance to 1 decimal place
		dst = header.index('shape_dist_traveled')
		id = header.index('trip_id')
		for row in c:
			if '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			row[id] = trip_map[row[id]]

			oc.writerow(row)

	elif fn.lower().endswith('stops.txt'):
		# stops.txt
		# Clamp stop lat/long to 6 decimal places
		lat = header.index('stop_lat')
		lng = header.index('stop_lon')

		for row in c:
			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]

			oc.writerow(row)


	else:
		# Other files -- this normally just removes un-needed quotation characters from the
		# CSV file
		for row in c:
			oc.writerow(row)

	output_f.close()
	input_f.close()
