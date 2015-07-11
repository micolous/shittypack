#!/usr/bin/env python
"""
shittypack.py - Repacks GTFS data so that it is more compact.

Copyright 2014-2015 Michael Farrell <http://micolous.id.au/>;

BSD 3-clause license, see COPYING.

"""

import argparse, csv, hashlib, itertools, os, zipfile

try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

# These substrings, if they appear in filenames, will not be modified by
# shittypack.  All values must be lowercase (and it is checked case insensitive)
BLACKLIST_NAMES = [
	'license',
	'notes',
	'licence',
]

def swallow_windows_unicode(fileobj, rewind=True):
	"""
	Windows programs put '\xef\xbb\xbf' at the start of a Unicode text file.
	This is used to handle "utf-8-sig" files.

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

def try_index(array, value, default=None):
	"""
	Tries to get the index of value in array, otherwise returns default (None).
	"""
	try:
		return array.index(value)
	except ValueError:
		return default


def blacklisted_file(fn):
	"""
	Checks if shittypack shouldn't touch a given filename.
	"""
	fnl = fn.lower()
	if not fnl.endswith('.txt'):
		return True

	for x in BLACKLIST_NAMES:
		if x in fnl:
			return True

	return False

class GtfsDialect(csv.excel):
	lineterminator = '\n'


class ShittyPacker(object):

	def __init__(self, input_zip, output_zip):
		SPECIAL_NAMES = [
			('agency.txt', self._f_agency, True),
			('routes.txt', self._f_routes, True),
			('trips.txt', self._f_trips, True),
			('shapes.txt', self._f_shapes, False),
			('stop_times.txt', self._f_stop_times, True),
			('stops.txt', self._f_stops, True),
			('transfers.txt', self._f_transfers, False),
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

		self.stop_id_map = {}
		self.last_stop_id = 0

		self.agency_map = {}
		self.last_agency_id = 0
		self.one_agency = False

		self.zip = zipfile.ZipFile(input_zip, 'r')
		self.out = zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED)
		names = set(self.zip.namelist())

		# Preprocess calendar entries.
		cal_c, cal_header = self._open_csv('calendar.txt')
		date_c, date_header = self._open_csv('calendar_dates.txt')
		cal_header, cal_c, date_header, date_c = self._process_calendar(cal_header, cal_c, date_header, date_c)

		# Write calendar.txt
		outf = StringIO.StringIO()
		oc = csv.writer(outf, dialect=GtfsDialect)
		oc.writerow(cal_header)
		[oc.writerow(x) for x in cal_c]
		self.out.writestr('calendar.txt', outf.getvalue())
		del cal_c

		# Write calendar_dates.txt
		outf = StringIO.StringIO()
		oc = csv.writer(outf, dialect=GtfsDialect)
		oc.writerow(date_header)
		[oc.writerow(x) for x in date_c]
		self.out.writestr('calendar_dates.txt', outf.getvalue())
		del date_c

		# Process other special files
		for fn, processor, required in SPECIAL_NAMES:
			if fn not in names:
				if required:
					print "WARNING: Could not find %r" % fn
				continue

			outf = StringIO.StringIO()
			oc = csv.writer(outf, dialect=GtfsDialect)
			c, header = self._open_csv(fn)
			oc.writerow(header)
			processor(header, c, oc)
			self.out.writestr(fn, outf.getvalue())

		# Now work out what's left
		for fn in (names - set((x[0] for x in SPECIAL_NAMES))) - set(SKIP_NAMES):
			if blacklisted_file(fn):
				# This is a metadata file, just copy it.
				datafile_content = self.zip.open(fn, 'r').read()
				self.out.writestr(fn, datafile_content)
			else:
				# This is probably some unknown datafile, try to handle it by
				# rewriting what we may have broken.
				outf = StringIO.StringIO()
				oc = csv.writer(outf, dialect=GtfsDialect)
				c, header = self._open_csv(fn)
				oc.writerow(header)
				self._f_generic(header, c, oc)
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


	def _f_agency(self, header, c, oc):
		"""
		Rewrite agency.txt
		"""
		agency_id = try_index(header, 'agency_id')
		if agency_id is None:
			self.one_agency = True

		# Convert to list so we can peek
		c = list(c)
		if len(c) <= 1:
			self.one_agency = True
		elif self.one_agency:
			# > 1 agency exists, but we were already in one_agency mode
			# This is a fault
			raise Exception, 'agency_id field missing from agency.txt, and more than one agency exists.'

		for row in c:
			if self.one_agency:
				if agency_id is not None:
					# Only one agency, we can blank the ID
					row[agency_id] = ''
			else:
				if row[agency_id] in self.agency_map:
					raise Exception, 'Duplicated agency_id in use!'

				self.agency_map[row[agency_id]] = str(self.last_agency_id)
				row[agency_id] = self.agency_map[row[agency_id]]
				self.last_agency_id += 1

			oc.writerow(row)

	def _f_shapes(self, header, c, oc):
		"""
		Rewrite shapes.txt.
		"""
		# Clamp lat/long to 6 decimal places
		# Clamp trip distance to 1 decimal place
		id = header.index('shape_id')
		lat = header.index('shape_pt_lat')
		lng = header.index('shape_pt_lon')
		dst = try_index(header, 'shape_dist_traveled')

		for row in c:
			# remap shapes to numbers, and skip any that aren't used by any trip
			if row[id] not in self.shape_map:
				continue

			row[id] = self.shape_map[row[id]]

			# clamp decimal places
			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]
			if dst is not None and '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			oc.writerow(row)


	def _f_routes(self, header, c, oc):
		"""
		Rewrite routes.txt
		"""
		id = header.index('route_id')
		agency_id = try_index(header, 'agency_id')

		for row in c:
			# remap routes to numbers

			if row[id] not in self.route_map:
				self.route_map[row[id]] = str(self.last_route_id)
				self.last_route_id += 1

			row[id] = self.route_map[row[id]]

			if agency_id is not None:
				if self.one_agency:
					row[agency_id] = ''
				else:
					row[agency_id] = self.agency_map[row[agency_id]]

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
			if row[hid] != '':
				# Including a shape is optional
				# Some Victorian services lack shapes
				if row[hid] not in self.shape_map:
					self.shape_map[row[hid]] = str(self.last_shape_id)
					self.last_shape_id += 1

				row[hid] = self.shape_map[row[hid]]

			oc.writerow(row)

	def _f_stop_times(self, header, c, oc):
		"""
		Rewrite stop_times.txt.
		"""
		# Clamp trip distance to 1 decimal place
		dst = try_index(header, 'shape_dist_traveled')

		trip_id = header.index('trip_id')
		stop_id = header.index('stop_id')

		for row in c:
			if row[trip_id] in self.null_trips:
				# This is a trip that is never taken, junk it
				continue

			if dst is not None and '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			# Rewrite stop id
			if row[stop_id] not in self.stop_id_map:
				self.stop_id_map[row[stop_id]] = str(self.last_stop_id)
				self.last_stop_id += 1

			row[stop_id] = self.stop_id_map[row[stop_id]]
			row[trip_id] = self.trip_map[row[trip_id]]

			oc.writerow(row)


	def _f_transfers(self, header, c, oc):
		"""
		Rewrite transfers.txt
		"""
		from_stop_id = header.index('from_stop_id')
		to_stop_id = header.index('to_stop_id')
		transfer_type = header.index('transfer_type')
		min_transfer_time = try_index(header, 'min_transfer_time')

		for row in c:
			if row[from_stop_id] not in self.stop_id_map or row[to_stop_id] not in self.stop_id_map:
				# Nuked stop, skip
				continue

			row[from_stop_id] = self.stop_id_map[row[from_stop_id]]
			row[to_stop_id] = self.stop_id_map[row[to_stop_id]]

			if row[transfer_type] != '':
				# May be non-integer, force to integer
				row[transfer_type] = str(int(row[transfer_type]))
				if row[transfer_type] == '0':
					row[transfer_type] = ''

			if min_transfer_time is not None and row[min_transfer_time] != '':
				# Force to integer
				row[min_transfer_time] = str(int(row[min_transfer_time]))

			oc.writerow(row)

	def _f_stops(self, header, c, oc):
		"""
		Rewrite stops.txt.
		"""
		# Clamp stop lat/long to 6 decimal places
		lat = header.index('stop_lat')
		lng = header.index('stop_lon')
		stop_id = header.index('stop_id')
		location_type = try_index(header, 'location_type')
		parent_station = try_index(header, 'parent_station')

		for row in c:
			# Determine if the stop is unused and we should remove it
			if row[stop_id] not in self.stop_id_map:
				if location_type is None or row[location_type] in ('', '0'):
					# This is a regular stop, and not a station, so is not referenced
					# Skip!
					continue

				elif row[location_type] == '1':
					# This is a parent station, we should register our number
					self.stop_id_map[row[stop_id]] = str(self.last_stop_id)
					self.last_stop_id += 1
				else:
					raise Exception, 'unknown location type = %r' % (row[location_type],)

			# Mapping should exist by this point
			row[stop_id] = self.stop_id_map[row[stop_id]]

			# See if we can assign a number for the parent station
			# Stations can't contain other stations, so we don't accept this if
			# location_type != 0 or blank
			if parent_station is not None and location_type is not None and row[parent_station] != '' and row[location_type] in ('', '0'):
				if row[parent_station] not in self.stop_id_map:
					self.stop_id_map[row[parent_station]] = str(self.last_stop_id)
					self.last_stop_id += 1

				row[parent_station] = self.stop_id_map[row[parent_station]]

			if location_type is not None and row[location_type] == '0':
				# We can shorten this to just blank
				row[location_type] = ''

			if '.' in row[lat]:
				row[lat] = row[lat][:row[lat].index('.')+7]
			if '.' in row[lng]:
				row[lng] = row[lng][:row[lng].index('.')+7]

			oc.writerow(row)

	def _f_generic(self, header, c, oc):
		"""
		Generic rewriter for unknown file types.
		"""

		agency_id = try_index(header, 'agency_id')
		route_id = try_index(header, 'route_id')
		shape_id = try_index(header, 'shape_id')
		stop_id = try_index(header, 'stop_id')
		trip_id = try_index(header, 'trip_id')
		service_id = try_index(header, 'service_id')

		for row in c:
			if agency_id is not None:
				row[agency_id] = self.agency_map[row[agency_id]]
			if route_id is not None:
				row[route_id] = self.route_map[row[route_id]]
			if shape_id is not None:
				row[shape_id] = self.shape_map[row[shape_id]]
			if stop_id is not None:
				row[stop_id] = self.stop_map[row[stop_id]]
			if trip_id is not None:
				row[trip_id] = self.trip_map[row[trip_id]]
			if service_id is not None:
				row[service_id] = self.service_map[row[service_id]]

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
		header = [x.strip() for x in c.next()]

		# Filter empty rows
		c = itertools.ifilter(lambda x: len(x) > 0, c)
		return c, header


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('zip', nargs=1)
	parser.add_argument('-o', '--output-zip', required=True)

	options = parser.parse_args()
	packer = ShittyPacker(options.zip[0], options.output_zip)


if __name__ == '__main__':
	main()

