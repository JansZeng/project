/**********************************************************************
Copyright:		JBT AUTO S&T Co., Ltd.
Description:	声明特殊功能函数、定义相关宏和数据类型
History:
	<author>	<time>		<desc>
	闫少伟		2014-01		创建文件
************************************************************************/
#ifndef _SPECIAL_FUNCTION
#define _SPECIAL_FUNCTION

#include "../interface/protocol_define.h"
#include "../command/command.h"
#include "../public/public.h"
#include "../public/protocol_config.h"
#include "../protocol/iso_14230.h"
#include "../protocol/iso_15765.h"
#include "../formula/formula.h"
#include "../formula/formula_comply.h"

#define COMM_INTERRUPT	0X02
#define PROCESS_OK		0X01
#define PROCESS_FAIL	0X00

#define HAVE_JUMP		0X04
#define NO_JUMP			0X00

#define HAVE_TIP_DATA	0X10 //提示的时候把数据域的数据显示出来
#define HAVE_TIP		0X08
#define NO_TIP			0X00