#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by: python.exe -m py2exe -W winbuild.py pylotro

import os
import PyLotROLauncher.Information
from distutils.core import setup
import py2exe

class Target(object):
	'''Target is the baseclass for all executables that are created.
	It defines properties that are shared by all of them.
	'''
	def __init__(self, **kw):
		self.__dict__.update(kw)

		# the VersionInfo resource, uncomment and fill in those items
		# that make sense:

		# The 'version' attribute MUST be defined, otherwise no versioninfo will be built:
		# self.version = "1.0"

		# self.company_name = "Company Name"
		# self.copyright = "James Potts © 2016"
		# self.legal_copyright = "James Potts © 2016"
		# self.legal_trademark = ""
		# self.product_version = "0.0.2.2"
		# self.product_name = "PyLotRO"

		# self.private_build = "foo"
		# self.special_build = "bar"

	def copy(self):
		return Target(**self.__dict__)

	def __setitem__(self, name, value):
		self.__dict__[name] = value

RT_BITMAP = 2
RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6

manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
	version="5.0.0.0"
	processorArchitecture="*"
	name="%(prog)s"
	type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
	<security>
	  <requestedPrivileges>
		<requestedExecutionLevel
			level="%(level)s"
			uiAccess="false">
		</requestedExecutionLevel>
	  </requestedPrivileges>
	</security>
  </trustInfo>
  <dependency>
	<dependentAssembly>
		<assemblyIdentity
			type="win32"
			name="Microsoft.Windows.Common-Controls"
			version="6.0.0.0"
			processorArchitecture="*"
			publicKeyToken="6595b64144ccf1df"
			language="*"
		/>
	</dependentAssembly>
  </dependency>
</assembly>
'''



pylotro = Target(
	# We can extend or override the VersionInfo of the base class:
	# version = "1.0",
	# file_description = "File Description",
	# comments = "Some Comments",
	# internal_name = "spam",

	script="pylotro", # path of the main script

	# Allows to specify the basename of the executable, if different from 'pylotro'
	# dest_base = "pylotro",

	# Icon resources:[(resource_id, path to .ico file), ...]
	# icon_resources=[(1, r"pylotro.ico")]

	other_resources = [(RT_MANIFEST, 1, (manifest_template % dict(prog="pylotro", level="asInvoker")).encode("utf-8")),
	# for bitmap resources, the first 14 bytes must be skipped when reading the file:
	#                    (RT_BITMAP, 1, open("bitmap.bmp", "rb").read()[14:]),
					  ]
	)


# ``zipfile`` and ``bundle_files`` options explained:
# ===================================================
#
# zipfile is the Python runtime library for your exe/dll-files; it
# contains in a ziparchive the modules needed as compiled bytecode.
#
# If 'zipfile=None' is used, the runtime library is appended to the
# exe/dll-files (which will then grow quite large), otherwise the
# zipfile option should be set to a pathname relative to the exe/dll
# files, and a library-file shared by all executables will be created.
#
# The py2exe runtime *can* use extension module by directly importing
# the from a zip-archive - without the need to unpack them to the file
# system.  The bundle_files option specifies where the extension modules,
# the python dll itself, and other needed dlls are put.
#
# bundle_files == 3:
#     Extension modules, the Python dll and other needed dlls are
#     copied into the directory where the zipfile or the exe/dll files
#     are created, and loaded in the normal way.
#
# bundle_files == 2:
#     Extension modules are put into the library ziparchive and loaded
#     from it directly.
#     The Python dll and any other needed dlls are copied into the
#     directory where the zipfile or the exe/dll files are created,
#     and loaded in the normal way.
#
# bundle_files == 1:
#     Extension modules and the Python dll are put into the zipfile or
#     the exe/dll files, and everything is loaded without unpacking to
#     the file system.  This does not work for some dlls, so use with
#     caution.
#
# bundle_files == 0:
#     Extension modules, the Python dll, and other needed dlls are put
#     into the zipfile or the exe/dll files, and everything is loaded
#     without unpacking to the file system.  This does not work for
#     some dlls, so use with caution.


py2exe_options = dict(
	packages = [],
##	excludes = "tof_specials Tkinter".split(),
##	ignores = "dotblas gnosis.xml.pickle.parsers._cexpat mx.DateTime".split(),
	includes = ["sip"],
	dll_excludes = "MSVCP90.dll mswsock.dll powrprof.dll HID.DLL w9xpopen.exe".split(),
	optimize=0,
	compressed=True, # uncompressed may or may not have a faster startup
	bundle_files=2, # PyQT doesn't like 0.  1 works but only packs the python dll.
	dist_dir='dist'
	)


# Some options can be overridden by command line options...

dataFiles = []
for files in os.listdir('PyLotroLauncher/images/'):
	f1 = 'PyLotroLauncher/images/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'images', [f1]
		dataFiles.append(f2)
for files in os.listdir('PyLotroLauncher/ui/'):
	f1 = 'PyLotroLauncher/ui/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'ui', [f1]
		dataFiles.append(f2)
for files in os.listdir('PyLotroLauncher/certificates/'):
	f1 = 'PyLotroLauncher/certificates/' + files
	if os.path.isfile(f1): # skip directories
		f2 = 'certificates', [f1]
		dataFiles.append(f2)
if os.path.isfile("COPYING"):
	dataFiles.append(("", ["COPYING"]))
else:
	print("COPYING not found, skipping")
if os.path.isfile("README.windows"):
	dataFiles.append(("", ["README.windows"]))
else:
	print("README.windows not found, skipping")
if os.path.isfile("README.wine"):
	dataFiles.append(("", ["README.wine"]))
else:
	print("README.wine not found, skipping")
if os.path.isfile("source.zip"):
	dataFiles.append(("", ["source.zip"]))
else:
	print("source.zip not found, skipping")

setup(name = "PyLotROLauncher",
	version = PyLotROLauncher.Information.Version,
	description = PyLotROLauncher.Information.Description,
	author = PyLotROLauncher.Information.Author,
	author_email = PyLotROLauncher.Information.Email,
	url = PyLotROLauncher.Information.WebSite,
	packages = ['PyLotROLauncher'],
	scripts = ["pylotro"],
	data_files = dataFiles,
	package_data = {'PyLotROLauncher' : ["*.png", "ui/*", "images/*", "certificates/*.pem"] },
	long_description = PyLotROLauncher.Information.LongDescription,
	zipfile=None,
	options={"py2exe": py2exe_options},
	windows = ["pylotro"]

#	This is commented until I figure out how to make py2exe embed an icon.
#	windows = [
#		{
#			"script": "pylotro",
#			"icon_resources": [(1, "")]
#		}
#	]
)

