/**********************************************************************
Copyright:		JBT AUTO S&T Co., Ltd.
Description:	定义与命令或具体功能配置相关的全局或局部变量
History:
	<author>	<time>		<desc>
	闫少伟		2013-12		创建文件
************************************************************************/

#include "../interface/protocol_define.h"
#include "command.h"
#include <stdio.h>

#define CAN_H_ID 0x07
#define CAN_L_ID 0X25
#define CAN_D_ID 0xDF

#define FMT_BYTE 0X80
#define TGT_BYTE 0X59
#define SRC_BYTE 0XF1