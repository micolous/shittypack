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

import argparse, csv, os, zipfile

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
			('calendar.txt', self._f_calendar),
			('calendar_dates.txt', self._f_calendar_dates),
			('trips.txt', self._f_trips),
			('stop_times.txt', self._f_stop_times),
			('stops.txt', self._f_stops),
		]

		# Remap the shape, route, service and trip IDs to simple numbers.
		# This is a very simple algo, it could do Hoffman encoding to make it
		# better, but it's probably not worth it.
		self.shape_map = {}
		self.last_shape_id = 0

		self.route_map = {}
		self.last_route_id = 0

		self.service_map = {}
		self.last_service_id = 0

		self.trip_map = {}
		self.last_trip_id = 0

		self.zip = zipfile.ZipFile(input_zip, 'r')
		self.out = zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED)
		names = set(self.zip.namelist())

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
		for fn in names - set((x[0] for x in SPECIAL_NAMES)):
			outf = StringIO.StringIO()
			oc = csv.writer(outf)
			c, header = self._open_csv(fn)
			oc.writerow(header)
			for r in c:
				oc.writerow(r)
			self.out.writestr(fn, outf.getvalue())

	def _f_shapes(self, header, c, oc):
		"""
		Rewrite shapes.txt.
		"""
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

	def _f_calendar(self, header, c, oc):
		"""
		Rewrite calendar.txt.
		"""
		id = header.index('service_id')
		for row in c:
			# remap services to numbers

			if row[id] not in self.service_map:
				self.service_map[row[id]] = str(self.last_service_id)
				self.last_service_id += 1

			row[id] = self.service_map[row[id]]

			oc.writerow(row)

	def _f_calendar_dates(self, header, c, oc):
		"""
		Rewrite calendar_dates.txt.
		"""
		id = header.index('service_id')
		for row in c:
			# remap services to numbers
			row[id] = self.service_map[row[id]]
			oc.writerow(row)


	def _f_trips(self, header, c, oc):
		"""
		Rewrite trips.txt.
		"""
		rid = header.index('route_id')
		eid = header.index('service_id')
		tid = header.index('trip_id')
		hid = header.index('shape_id')
		for row in c:
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
		dst = header.index('shape_dist_traveled')
		id = header.index('trip_id')
		for row in c:
			if '.' in row[dst]:
				row[dst] = row[dst][:row[dst].index('.')+2]

			row[id] = self.trip_map[row[id]]

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
