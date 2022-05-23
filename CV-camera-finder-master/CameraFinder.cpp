#include <iostream>
#include <vector>
#include <mfplay.h>
#include <python.h>
#include "capture.h"

using namespace std;

vector< string > _get_devices() {
	vector< string > result;
	DeviceList  g_devices;
	HRESULT hr = S_OK;

	WCHAR* szFriendlyName = NULL;
	g_devices.Clear();

	hr = g_devices.EnumerateDevices();

	if (FAILED(hr)) {
		return result;
	}

	for (UINT32 iDevice = 0; iDevice < g_devices.Count(); iDevice++)
	{

		hr = g_devices.GetDeviceName(iDevice, &szFriendlyName);

		if (FAILED(hr)) { return result; }
		wstring ws(szFriendlyName);
		string szFriendlyNameStr(ws.begin(), ws.end());
		result.push_back(szFriendlyNameStr);
		CoTaskMemFree(szFriendlyName);
		szFriendlyName = NULL;
	}
	return result;
}

PyObject* GetDevices(PyObject* self, PyObject* args) {
	vector< string > devices = _get_devices();
	PyObject* result = PyList_New(devices.size());
	for (int i = 0; i < devices.size(); ++i) {
		PyObject* pytmp = Py_BuildValue("s", devices[i].c_str());
		PyList_SetItem(result, i, pytmp);
	}
	return result;
}

static PyMethodDef CameraFinder_methods[] = {
	// The first property is the name exposed to Python, fast_tanh, the second is the C++
	// function name that contains the implementation.
	{ "GetDevices", (PyCFunction)GetDevices, METH_NOARGS, nullptr },

	// Terminate the array with an object containing nulls.
	{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef CameraFinder_module = {
	PyModuleDef_HEAD_INIT,
	"CameraFinder",                        // Module name to use with Python import statements
	"MSMF tool",                    // Module description
	0,
	CameraFinder_methods                   // Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_CameraFinder() {
	return PyModule_Create(&CameraFinder_module);
}
