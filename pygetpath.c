
#include "Python.h"
#include "osdefs.h"
#include <sys/types.h>
#include <string.h>

extern PyAPI_FUNC(wchar_t *) Py_GetProgramName(void);

static int pathCalculated = 0; 
static wchar_t progPath[MAXPATHLEN+1];
static wchar_t modulePathes[4*MAXPATHLEN+1];
static wchar_t execPrefixPath[2*MAXPATHLEN+1];

static void calcPathes() {
	if(pathCalculated) return;

	wchar_t* p = wcpcpy(progPath, Py_GetProgramName());
	while(--p > progPath) {
		if(*p == '/') {
			*p = 0;
			break;
		}
	}
	
	wcscpy(modulePathes, progPath);
	wcscat(modulePathes, L"/pylib/lib:");
	wcscat(modulePathes, progPath);
	wcscat(modulePathes, L"/pylib/sitepkgs");
	wcscpy(execPrefixPath, progPath);
	wcscat(execPrefixPath, L"/pylib/exec");
	
	pathCalculated = 1;
}

/* External interface */

wchar_t *
Py_GetPath(void)
{
	calcPathes();
	return modulePathes;
}

wchar_t *
Py_GetPrefix(void)
{
	calcPathes();
	return L"pygetpath.c-PYPREFIX-NOT-SET";
}

wchar_t *
Py_GetExecPrefix(void)
{
	calcPathes();
	return execPrefixPath;
}

wchar_t *
Py_GetProgramFullPath(void)
{
	calcPathes();
	return progPath;
}
