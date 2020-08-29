#define _CRT_SECURE_NO_WARNINGS
#include "stdio.h"
#include <string.h>
#include <stdlib.h>
//#include <fcntl.h>
//#include <unistd.h>

//--------------------------------------------
//其他的头文件
#include "../InitConfigFromXml/init_config_from_xml_lib.h"
//--------------------------------------------

#ifdef WIN32
#define DEBUGFILE_PATH 0
#else
#define DEBUGFILE_PATH 1 
#endif

#define int_number  1
#define string_src  2
#define Ayyay_type  3
#define Ayyay_type1 4

#define unsigned_int_type  1
#define unsigned_char_type 2
#define int_type		   3


