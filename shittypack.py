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

import argparse, csv, hashlib, os, zipfile

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

# Special files that need to be processed first.


def swallow_windows_unicode(fileobj, rewind=True):
	"""
	Windows programs (specifically, Notepad) puts '\xef\xbb\xbf' at the start of
	a Unicode text file.  This is used to handle "utf-8-sig" files.

	This function looks for those bytes and advances the stream past them if
	they are present.

	Returns True if the characters were present.
	"""
	if rewind:
		pos = fileobj.tell()

	try:
		bom = fileobj.read(3)
	except:
		# End of file, revert!
		fileobj.seek(pos)
	if bom == '\xef\xbb\xbf':
		return True

	# Bytes not present, rewind the stream
	if rewind:
		fileobj.seek(pos)
	return False


class ShittyPacker(object):

	def __init__(self, input_zip, output_zip):
		SPECIAL_NAMES = [
			('shapes.txt', self._f_shapes),
			('routes.txt', self._f_routes),
			('trips.txt', self._f_trips),
			('stop_times.txt', self._f_stop_times),
			('stops.txt', self._f_stops),
		]
		SKIP_NAMES = ['calendar.txt', 'calendar_dates.txt']

		# Remap the shape, route, service and trip IDs to simple numbers.
		# This is a very simple algo, it could do Hoffman encoding to make it
		# better, but it's probably not worth it.
		self.shape_map = {}
		self.last_shape_id = 0

		self.route_map = {}
		self.last_route_id = 0

		self.service_map = {}
		self.last_service_id = 0
		self.null_services = set()

		self.trip_map = {}
		self.last_trip_id = 0
		self.null_trips = set()

		self.zip = zipfile.ZipFile(input_zip, 'r')
		self.out = zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED)
		names = set(self.zip.namelist())

		# Preprocess calendar entries.
		cal_c, cal_header = self._open_csv('calendar.txt')
		date_c, date_header = self._open_csv('calendar_dates.txt')
		cal_header, cal_c, date_header, date_c = self._process_calendar(cal_header, cal_c, date_header, date_c)

		# Write calendar.txt
		outf = StringIO.StringIO()
		oc = csv.writer(outf)
		oc.writerow(cal_header)
		[oc.writerow(x) for x in cal_c]
		self.out.writestr('calendar.txt', outf.getvalue())
		del cal_c

		# Write calendar_dates.txt
		outf = StringIO.StringIO()
		oc = csv.writer(outf)
		oc.writerow(date_header)
		[oc.writerow(x) for x in date_c]
		self.out.writestr('calendar_dates.txt', outf.getvalue())
		del date_c

		# Process other special files
		for fn, processor in SPECIAL_NAMES:
			if fn not in names:
				print "WARNING: Could not find %r" % fn
				continue

			outf = StringIO.StringIO()
			oc = csv.writer(outf)
			c, header = self._open_csv(fn)
			oc.writerow(header)
			processor(header, c, oc)
			self.out.writestr(fn, outf.getvalue())

		# Now work out what's left
		for fn in (names - set((x[0] for x in SPECIAL_NAMES))) - set(SKIP_NAMES):
			outf = StringIO.StringIO()
			oc = csv.writer(outf)
			c, header = self._open_csv(fn)
			oc.writerow(header)
			for r in c:
				oc.writerow(r)
			self.out.writestr(fn, outf.getvalue())

	def _process_calendar(self, cal_header, cal_c, date_header, date_c):
		raw_trip_data = {}
		
		service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date = [cal_header.index(x) for x in 'service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date'.split(',')]
		
		# Collect all the data into a dict
		for r in cal_c:
			days_mask = r[monday] + r[tuesday] + r[wednesday] + r[thursday] + r[friday] + r[saturday] + r[sunday]
			assert len(days_mask) == 7, 'days mask must be of length 7'

			raw_trip_data[r[service_id]] = dict(
				days=days_mask,
				start_date=r[start_date],
				end_date=r[end_date],
				add=set(),
				exclude=set()
			)

		d_service_id,d_date,d_exception_type = [date_header.index(x) for x in 'service_id,date,exception_type'.split(',')]
		for r in date_c:
			assert r[d_exception_type] in '12', 'exception_type must be 1 or 2'
			raw_trip_data[r[d_service_id]]['add' if r[d_exception_type] == '1' else 'exclude'].add(r[d_date])

		# Junk useless trips and replace all the route_ids with a hash composed of
		# - the calendar bits
		# - any holiday exclusions or inclusions
		trip_data_map = {}
		trip_hashes = {}
		for service_id in raw_trip_data.keys():
			if raw_trip_data[service_id]['days'] == '0000000' and len(raw_trip_data[service_id]['add']) == 0:
				# Trip never used!  Junk!
				#print 'junking trip: %r' % service_id
				self.null_services.add(service_id)
				del raw_trip_data[service_id]
			else:
				# Hash the trip info
				# This is ugly, yes.
				raw_trip_data[service_id]['add'] = list(raw_trip_data[service_id]['add'])
				raw_trip_data[service_id]['exclude'] = list(raw_trip_data[service_id]['exclude'])
				raw_trip_data[service_id]['add'].sort()
				raw_trip_data[service_id]['exclude'].sort()

				trip_hash = hashlib.sha1(repr(raw_trip_data[service_id])).hexdigest()
				trip_data_map[service_id] = trip_hash
				if trip_hash not in trip_hashes:
					trip_hashes[trip_hash] = set()
				trip_hashes[trip_hash].add(service_id)

		# From the single set of data, merge!
		cal_c = []
		date_c = []
		cal_header = 'service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date'.split(',')
		date_header = 'service_id,date,exception_type'.split(',')
		trip_num = 1
		for trip_hash, service_ids in trip_hashes.iteritems():
			#if len(service_ids) > 1:
			#	print 'TripHash %r used %d times!' % (trip_hash, len(service_ids))
			for service_id in service_ids:
				trip_data_map[service_id] = str(trip_num)
			trip_data = raw_trip_data[next(iter(service_ids))]
			cal_c.append([
				str(trip_num),
			] + [x for x in trip_data['days']] + [
				trip_data['start_date'],
				trip_data['end_date'],
			])
			for d in trip_data['add']:
				date_c.append([trip_num, d, '1'])
			for d in trip_data['exclude']:
				date_c.append([trip_num, d, '2'])
			trip_num += 1

		# And we're done!
		self.service_map = trip_data_map
		return cal_header, cal_c, date_header, date_c

	def _f_shapes(self, header, c, oc):
		"""
		Rewrite shapes.txt.
		"""
		# Clamp lat/long to 6 decimal places
		# Clamp trip distance to 1 decimal place
		id = header.index('shape_id')
		lat = header.index('shape_pt_lat')
		lng = header.index('shape_pt_lon')
		if 'shape_dist_traveled' in header:
			dst = header.index('shape_dist_traveled')
		else:
			dst = None

		for row in c:
			# clamp decimal places
			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]
			if dst is not None and '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			# remap shapes to numbers
			if row[id] not in self.shape_map:
				self.shape_map[row[id]] = str(self.last_shape_id)
				self.last_shape_id += 1

			row[id] = self.shape_map[row[id]]

			oc.writerow(row)


	def _f_routes(self, header, c, oc):
		"""
		Rewrite routes.txt
		"""
		id = header.index('route_id')
		for row in c:
			# remap routes to numbers

			if row[id] not in self.route_map:
				self.route_map[row[id]] = str(self.last_route_id)
				self.last_route_id += 1

			row[id] = self.route_map[row[id]]

			oc.writerow(row)


	def _f_trips(self, header, c, oc):
		"""
		Rewrite trips.txt.
		"""
		rid = header.index('route_id')
		eid = header.index('service_id')
		tid = header.index('trip_id') # PK
		hid = header.index('shape_id')
		for row in c:
			if row[eid] in self.null_services:
				# Junked service_id that is never used, drop!
				self.null_trips.add(row[tid])
				continue

			# remap services to numbers
			if row[tid] not in self.trip_map:
				self.trip_map[row[tid]] = str(self.last_trip_id)
				self.last_trip_id += 1

			row[tid] = self.trip_map[row[tid]]
			row[rid] = self.route_map[row[rid]]
			row[eid] = self.service_map[row[eid]]
			row[hid] = self.shape_map[row[hid]]

			oc.writerow(row)

	def _f_stop_times(self, header, c, oc):
		"""
		Rewrite stop_times.txt.
		"""
		# Clamp trip distance to 1 decimal place
		if 'shape_dist_traveled' in header:
			dst = header.index('shape_dist_traveled')
		else:
			dst = None
		trip_id = header.index('trip_id')
		for row in c:
			if row[trip_id] in self.null_trips:
				#print 'null trip! %r' % row[trip_id]
				continue

			if dst is not None and '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]


			row[trip_id] = self.trip_map[row[trip_id]]

			oc.writerow(row)


	def _f_stops(self, header, c, oc):
		"""
		Rewrite stops.txt.
		"""
		# Clamp stop lat/long to 6 decimal places
		lat = header.index('stop_lat')
		lng = header.index('stop_lon')

		for row in c:
			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]

			oc.writerow(row)


	def _open_csv(self, filename):
		"""
		Opens a given CSV file in the archive.
		Returns tuple of (csvobj, header)
		"""
		input_f = self.zip.open(filename, 'r')
		swallowed = swallow_windows_unicode(input_f, False)
		if not swallowed:
			# We need to manually reset the file.
			input_f = self.zip.open(filename, 'r')
		c = csv.reader(input_f)
		header = c.next()
		return c, header

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('zip', nargs=1)
	parser.add_argument('-o', '--output-zip', required=True)

	options = parser.parse_args()
	packer = ShittyPacker(options.zip[0], options.output_zip)
	



if __name__ == '__main__':
	main()
