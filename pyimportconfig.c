#include "Python.h"

extern PyAPI_FUNC(PyObject*) _PyWarnings_Init(void);
extern PyMODINIT_FUNC PyMarshal_Init(void);
extern PyMODINIT_FUNC PyInit_array(void);
extern PyMODINIT_FUNC PyInit_imp(void);
extern PyMODINIT_FUNC PyInit__io(void);
extern PyMODINIT_FUNC PyInit__csv(void);
extern PyMODINIT_FUNC PyInit_itertools(void);
extern PyMODINIT_FUNC PyInit__collections(void);
extern PyMODINIT_FUNC PyInit__heapq(void);
extern PyMODINIT_FUNC PyInit__operator(void);
extern PyMODINIT_FUNC PyInit_math(void);
extern PyMODINIT_FUNC PyInit_errno(void);
extern PyMODINIT_FUNC PyInit_gc(void);
extern PyMODINIT_FUNC PyInit_posix(void);
extern PyMODINIT_FUNC PyInit__weakref(void);
extern PyMODINIT_FUNC PyInit__sre(void);
extern PyMODINIT_FUNC PyInit__codecs(void);
extern PyMODINIT_FUNC PyInit__string(void);
extern PyMODINIT_FUNC PyInit_time(void);
extern PyMODINIT_FUNC PyInit__datetime(void);
extern PyMODINIT_FUNC PyInit__sha1(void);
extern PyMODINIT_FUNC PyInit__sha256(void);
extern PyMODINIT_FUNC PyInit__sha512(void);
extern PyMODINIT_FUNC PyInit__md5(void);
extern PyMODINIT_FUNC PyInit__json(void);
extern PyMODINIT_FUNC PyInit_zlib(void);
extern PyMODINIT_FUNC PyInit__struct(void);
extern PyMODINIT_FUNC PyInit__functools(void);
#ifdef WITH_THREAD
extern PyMODINIT_FUNC PyInit__thread(void);
#endif
extern PyMODINIT_FUNC PyInit_binascii(void);
extern PyMODINIT_FUNC PyInit__random(void);
extern PyMODINIT_FUNC PyInit__socket(void);
//extern PyMODINIT_FUNC PyInit__ssl(void);
//extern PyMODINIT_FUNC PyInit_zlib(void);
extern PyMODINIT_FUNC PyInit_select(void);
extern PyMODINIT_FUNC PyInit_signal(void);
extern PyMODINIT_FUNC PyInit_fcntl(void);
extern PyMODINIT_FUNC PyInit__locale(void);
extern PyMODINIT_FUNC PyInit__pickle(void);
extern PyMODINIT_FUNC PyInit__stat(void);
extern PyMODINIT_FUNC PyInit_cmath(void);
extern PyMODINIT_FUNC PyInit_fpectl(void);
extern PyMODINIT_FUNC PyInit_unicodedata(void);

#ifdef WITH_PYCRYPTO
extern PyMODINIT_FUNC PyInit__PyCrypto(void);
#endif

struct _inittab _PyImport_Inittab[] = {
	
    {"array", PyInit_array},
    {"_csv", PyInit__csv},
    {"itertools", PyInit_itertools},
    {"_collections", PyInit__collections},
    {"_heapq", PyInit__heapq},
    {"_operator", PyInit__operator},
    {"math", PyInit_math},
    {"errno", PyInit_errno},
    {"gc", PyInit_gc},
    {"posix", PyInit_posix},
    {"_weakref", PyInit__weakref},
    {"_sre", PyInit__sre},
    {"_codecs", PyInit__codecs},
    {"_string", PyInit__string},
    {"time", PyInit_time},
    {"_datetime", PyInit__datetime},
    {"_sha1", PyInit__sha1},
    {"_sha256", PyInit__sha256},
    {"_sha512", PyInit__sha512},
    {"_md5", PyInit__md5},
    {"_json", PyInit__json},
    {"_struct", PyInit__struct},
    {"_functools", PyInit__functools},
#ifdef WITH_THREAD
    {"_thread", PyInit__thread},
#endif
	{"binascii", PyInit_binascii},
	{"_random", PyInit__random},
	{"_socket", PyInit__socket},
	//{"_ssl", PyInit__ssl},
	//{"zlib", PyInit_zlib},
	{"select", PyInit_select},
	{"signal", PyInit_signal},
	{"fcntl", PyInit_fcntl},
	{"_locale", PyInit__locale},
	{"_pickle", PyInit__pickle},
	{"_stat", PyInit__stat},
	{"cmath", PyInit_cmath},
	{"fpectl", PyInit_fpectl},
	{"unicodedata", PyInit_unicodedata},


/*
    {"_ast", PyInit__ast},
    {"future_builtins", PyInit_future_builtins},
    {"strop", PyInit_strop},
    {"cPickle", PyInit_cPickle},
    {"_subprocess", PyInit__subprocess},
	
    {"_hotshot", PyInit__hotshot},
    {"_bisect", PyInit__bisect},
    {"_lsprof", PyInit__lsprof},
    {"_symtable", PyInit__symtable},
    {"mmap", PyInit_mmap},
    {"parser", PyInit_parser},
    {"_winreg", PyInit__winreg},
	
    {"xxsubtype", PyInit_xxsubtype},
    {"zipimport", PyInit_zipimport},
	
    {"_multibytecodec", PyInit__multibytecodec},
    {"_codecs_cn", PyInit__codecs_cn},
    {"_codecs_hk", PyInit__codecs_hk},
    {"_codecs_iso2022", PyInit__codecs_iso2022},
    {"_codecs_jp", PyInit__codecs_jp},
    {"_codecs_kr", PyInit__codecs_kr},
    {"_codecs_tw", PyInit__codecs_tw},
*/
	
    /* This module "lives in" with marshal.c */
    {"marshal", PyMarshal_Init},
	
    /* This lives it with import.c */
    {"imp", PyInit_imp},
	
    /* These entries are here for sys.builtin_module_names */
    {"__main__", NULL},
    {"__builtin__", NULL},
    {"sys", NULL},
    {"exceptions", NULL},
    {"_warnings", _PyWarnings_Init},
	
    {"_io", PyInit__io},

#ifdef WITH_PYCRYPTO
	{"Crypto", PyInit__PyCrypto},
#endif
	
    /* Sentinel */
    {0, 0}
};
