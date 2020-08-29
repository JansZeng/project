#ifndef _INTERFACE_H
#define _INTERFACE_H


#include "protocol_define.h"

#ifdef __cplusplus
extern "C" {
#endif


#ifdef PROTOCOL_DLL_EXPORTS
#	define PROTOCOL_API __declspec(dllexport)
#else
#	define PROTOCOL_API __declspec(dllimport)
#endif
#else
#	define PROTOCOL_API
#endif