/**********************************************************************
Description:	声明与命令或具体功能配置相关的全局或局部变量
History:
	<author>	<time>		<desc>
	闫少伟		2013-12		创建文件
************************************************************************/

#ifndef _PROTOCOL_CMD_H
#define _PROTOCOL_CMD_H
#include "../interface/protocol_define.h"

extern  STRUCT_CMD g_stCmdList[];
extern  int	g_iDefaultSessionCmdIndex[];
extern  int	g_iExtendSessionCmdIndex[];

extern	int	g_iRequestSeedCmdIndex[];
extern	int	g_iSendKeyCmdIndex[];
extern  int	g_iQuitActuatorTestCmdIndex[];

extern  int	g_iReadVWDSCmdIndex[];


#endif