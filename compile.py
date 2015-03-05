#!/usr/bin/python
import os, sys
os.chdir(os.path.dirname(__file__) or os.getcwd())
import better_exchook
better_exchook.install()

CC = "gcc"
LD = "ld"
LIBTOOL = "libtool"
CFLAGS = []
LDFLAGS = []

buildExec = False

def selectNewestDir(dirpattern):
	from glob import glob
	dirs = glob(dirpattern)
	assert dirs
	return dirs[-1]

platform = 'iPhoneSimulator' if 'simulator' in sys.argv else 'iPhoneOS'
platext  = '_sim' if 'simulator' in sys.argv else ''
archs    = ['-arch', 'i386'] if 'simulator' in sys.argv else ['-arch', 'armv7', '-arch', 'arm64']

DEVROOT = "/Developer/Platforms/%s.platform/Developer" % platform
SDKROOT = selectNewestDir("/Applications/Xcode.app/Contents/Developer/Platforms/%s.platform/Developer/SDKs/%s*.sdk" % (platform,platform))
SDKROOT2 = "/Applications/Xcode.app/Contents/Developer/Platforms/%s.platform/Developer/SDKs/%s.sdk" % (platform,platform)
assert os.path.exists(DEVROOT)
assert os.path.exists(SDKROOT)
assert os.path.exists(SDKROOT2)

CC = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
LD = DEVROOT + "/usr/bin/ld"
LIBTOOL = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/libtool"
assert os.path.exists(CC)
assert os.path.exists(LD)
assert os.path.exists(LIBTOOL)

CFLAGS += [
	"-isysroot", SDKROOT,
	"-I%s/usr/include/" % SDKROOT,
	"-pipe"] + \
	archs + \
	["-miphoneos-version-min=6.0",
	"-O2",
	"-DNDEBUG",	# To remove asserts.
	]
LDFLAGS += archs + [
	"-ios_version_min=6.0",
	"-L%s/usr/lib" % SDKROOT,
	"-L%s/usr/lib/system" % SDKROOT,
	"-lc",
	SDKROOT2 + "/usr/lib/crt1.3.1.o",
	"-lgcc_s.1",
	]

PythonDir = "CPython"
assert os.path.exists(PythonDir)

from glob import glob as pyglob
from pprint import pprint
try: os.mkdir("build%s"%platext)
except: pass

def glob(pattern):
	def glob_(baseDir, patternList):
		if not patternList:
			yield baseDir
			return
		head = patternList[0]
		if head == "**":
			for f in glob_(baseDir, patternList[1:]): yield f
			for d in pyglob(baseDir + "/*/"):
				for f in glob_(d, patternList): yield f
			return
		for m in pyglob(baseDir + "/" + head):
			for f in glob_(m, patternList[1:]): yield f
	parts = pattern.split("/")
	if not parts: return
	if parts[0] == "": # start in root
		for f in glob_("/", parts[1:]): yield os.path.normpath(f)
		return
	for f in glob_(".", parts): yield os.path.normpath(f)

baseFiles = \
	set(glob(PythonDir + "/Python/*.c")) - \
	set(glob(PythonDir + "/Python/dynload_*.c")) - \
	set(glob(PythonDir + "/Python/mactoolboxglue.c")) - \
	set(glob(PythonDir + "/Python/sigcheck.c"))
baseFiles |= \
	set(glob(PythonDir + "/Python/dynload_stub.c")) | \
	set(glob("pyimportconfig.c")) | \
	set(glob("pygetpath.c"))

# via blacklist
modFiles = \
	set(glob(PythonDir + "/Modules/**/*.c")) - \
	set(glob(PythonDir + "/Modules/**/testsuite/**/*.c")) - \
	set(glob(PythonDir + "/Modules/_sqlite/**/*.c")) - \
	set(glob(PythonDir + "/Modules/_bsddb.c")) - \
	set(glob(PythonDir + "/Modules/expat/**/*.c")) - \
	set(glob(PythonDir + "/Modules/imgfile.c")) - \
	set(glob(PythonDir + "/Modules/_ctypes/**/*.c")) - \
	set(glob(PythonDir + "/Modules/glmodule.c"))
	# ...
	
# via whitelist
# Add the init reference also to pyimportconfig.c.
# For hacking builtin submodules, see pycryptoutils/cryptomodule.c.
modFiles = \
	set(map(lambda f: PythonDir + "/Modules/" + f,
		[
			"main.c",
			"python.c",
			"getbuildinfo.c",
			"posixmodule.c",
			"arraymodule.c",
			"gcmodule.c",
			"faulthandler.c",
			"_tracemalloc.c",
			"hashtable.c",
			"_csv.c",
			"_collectionsmodule.c",
			"_heapqmodule.c",
			"itertoolsmodule.c",
			"_localemodule.c",
			"_operator.c",
			"_pickle.c",
			"_stat.c",
			"cmathmodule.c",
			"fpectlmodule.c",
			"_math.c",
			"mathmodule.c",
			"errnomodule.c",
			"_weakref.c",
			"_sre.c",
			"_codecsmodule.c",
			"unicodedata.c",
			"timemodule.c",
			"_datetimemodule.c",
			"sha1module.c",
			"sha256module.c",
			"sha512module.c",
			"md5module.c",
			"_json.c",
			"_struct.c",
			"_functoolsmodule.c",
			"_threadmodule.c",
			"binascii.c",
			"_randommodule.c",
			"socketmodule.c",
			#"_ssl.c",
			#"zlibmodule.c",
			"selectmodule.c",
			"signalmodule.c",
			"fcntlmodule.c",
			])) | \
	set(glob(PythonDir + "/Modules/_io/*.c"))

# remove main.c/python.c if we dont want an executable
if not buildExec:
	modFiles -= set([PythonDir + "/Modules/python.c"])

objFiles = \
	set(glob(PythonDir + "/Objects/*.c"))

parserFiles = \
	set(glob(PythonDir + "/Parser/*.c")) - \
	set(glob(PythonDir + "/Parser/*pgen*.c"))

pycryptoFiles = \
	set(glob("pycrypto/src/*.c")) - \
	set(glob("pycrypto/src/*template.c")) - \
	set(glob("pycrypto/src/cast*.c")) - \
	set(glob("pycrypto/src/_fastmath.c")) # for now. it needs libgmp

pycryptoFiles = map(lambda f: "pycrypto/src/" + f,
	[
		"_counter.c",
		"AES.c",
		"strxor.c",
	]) + \
	["pycryptoutils/cryptomodule.c"]

compileOpts = CFLAGS + [
	"-Ipylib",
	"-I" + PythonDir + "/Include",
	#"-DWITH_PYCRYPTO",
]

compilePycryptoOpts = compileOpts + [
	"-Ipycryptoutils",
	"-Ipycrypto/src/libtom",
	"-std=c99",
]

def execCmd(cmd):
	cmdFlat = " ".join(cmd)
	print cmdFlat
	return os.system(cmdFlat)
	
def compilePyFile(f, compileOpts):
	if not os.path.exists(f):
		print('%s does not exist' % f)
		sys.exit(1)
	ofile = os.path.splitext(os.path.basename(f))[0] + ".o"
	try:
		if os.stat(f).st_mtime < os.stat(("build%s/"%platext) + ofile).st_mtime:
			return [ofile]
	except: pass
	cmd = [CC] + compileOpts + ["-c", f, "-o", ("build%s/"%platext) + ofile]
	if execCmd(cmd) != 0:
		sys.exit(1)
	return [ofile]

def compilePycryptoFile(fn):
	return compilePyFile(fn, compilePycryptoOpts)
	
def compile():
	ofiles = []
	for f in list(baseFiles) + list(modFiles) + list(objFiles) + list(parserFiles):
		ofiles += compilePyFile(f, compileOpts)
	#for f in list(pycryptoFiles):
	#	ofiles += compilePycryptoFile(f)
	
	if buildExec:
		execCmd([CC] + LDFLAGS + map(lambda f: ("build%s/"%platext) + f, ofiles) + ["-o", "python%s"%platext])
	else:
		execCmd(
			[LIBTOOL, "-static", "-syslibroot", SDKROOT, "-o", "libpython%s.a"%platext] +
			map(lambda f: ("build%s/"%platext) + f, ofiles)
			)

if __name__ == '__main__':
	compile()

