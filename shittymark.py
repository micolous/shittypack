#!/usr/bin/env python
"""
shittymark.py - Generates reports of the size difference from shittypacked
files.

Copyright 2015 Michael Farrell <http://micolous.id.au/>;

BSD 3-clause license, see COPYING.
"""

import argparse, zipfile
from collections import OrderedDict
from shittypack import blacklisted_file

def pretty_bytes(b):
	"""
	Format a value of bytes to something sensible.
	"""

	if b >= 10 * (1024**3): # 10 GiB
		return '%0.0f GiB' % (float(b) / (1024**3))
	elif b >= (1024**3): # 1 GiB
		return '%0.1f GiB' % (float(b) / (1024**3))
	elif b >= 10 * (1024**2): # 10 MiB
		return '%0.0f MiB' % (float(b) / (1024**2))
	elif b >= (1024**2): # 1 MiB
		return '%0.1f MiB' % (float(b) / (1024**2))
	elif b >= 1024: # 1 KiB
		return '%0.0f KiB' % (float(b) / 1024)
	else:
		return '%d B' % b

def compare_packed(source, packed):
	"""
	Compares two given ZIP archives size by their contents.

	Assumes these both have the same content.
	"""
	source_zip = zipfile.ZipFile(source, 'r')
	packed_zip = zipfile.ZipFile(packed, 'r')

	source_names = set(filter(lambda x: not blacklisted_file(x), source_zip.namelist()))
	packed_names = set(filter(lambda x: not blacklisted_file(x), packed_zip.namelist()))

	assert source_names == packed_names, 'Source and packed files need identical file list.'
	source_names = list(source_names)
	source_names.sort()

	sizes = OrderedDict()
	source_size = 0
	packed_size = 0
	for name in source_names:
		size = source_zip.getinfo(name).file_size
		assert name not in sizes
		sizes[name] = [size]
		source_size += size

	for name in source_names:
		size = packed_zip.getinfo(name).file_size
		sizes[name].append(size)
		assert len(sizes[name]) == 2
		packed_size += size

	# build a report
	report = '''\
- Original size: %(source_size)s
- Packed size: %(packed_size)s (%(percent)d%% of original)

Original size | Packed size | Percent | Filename
-------------:|------------:|--------:|---------
''' % dict(source_size=pretty_bytes(source_size), packed_size=pretty_bytes(packed_size), percent=(float(packed_size) / float(source_size)) * 100)

	for name, size in sizes.iteritems():
		report += '%s | %s | %s%% | %s\n' % (pretty_bytes(size[0]).rjust(13), pretty_bytes(size[1]).rjust(11), str(int((float(size[1]) / float(size[0]))*100)).rjust(6), name)

	return report

def main():
	parser = argparse.ArgumentParser()

	group = parser.add_argument_group('Single-file mode')

	group.add_argument('-s', '--source-file',
		help='Source, non-packed file to compare from')

	group.add_argument('-p', '--packed-file',
		help='New, Shittypacked file to compare to')


	# TODO: Implement multi-file support
	options = parser.parse_args()
	print compare_packed(options.source_file, options.packed_file),


if __name__ == '__main__':
	main()

