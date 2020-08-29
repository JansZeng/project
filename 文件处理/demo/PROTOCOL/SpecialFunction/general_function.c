/**********************************************************************
Copyright:		JBT AUTO S&T Co., Ltd.
Description:	定义特殊功能处理函数和通用的相关函数
History:
	<author>	<time>		<desc>
	闫少伟		2014-01		创建文件
************************************************************************/
#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/*#define NDEBUG*/
#include <assert.h>
#include "special_function.h"
#include "../InitConfigFromXml/init_config_from_xml_lib.h"
#include "../function/quit_system_lib.h"
#include "../function/active_ecu_lib.h"
#include "../function/idle_link_lib.h"

/*************************************************
Description:	特殊功能处理函数
Input:	
	pIn		输入与特殊功能有关的命令数据
			和从UI输入的内容
Output:	pOut	输出数据地址
Return:	void
Others:	根据第一个命令数据执行不同的功能函数
*************************************************/
void process_special_function( void* pIn, void* pOut )
{
	int iIndexSum = 0;
	int iProcessStatus = FAILE;
	byte cSpecialCmdData[128] = {0};//存放特殊功能命令数据
	STRUCT_CHAIN_DATA_INPUT* pstParam = ( STRUCT_CHAIN_DATA_INPUT* )pIn;
	bool bStatus = false;

	assert(pstParam->pcData);
	assert(pstParam->iLen != 0);

	if( ( pstParam->pcData == NULL ) || ( pstParam->iLen == 0 ) )
	{
		general_return_status( INVALID_INPUT, NULL, 0, pOut ); //提示无效输入
		return;
	}

	iIndexSum =get_string_type_data_to_byte(cSpecialCmdData, pstParam->pcData, pstParam->iLen);
	//指向下一个结点
	pstParam = pstParam->pNextNode;

	switch(cSpecialCmdData[0])
	{
	case 0:
		{
			bStatus = write_ECU_VIN(cSpecialCmdData,pstParam,pOut);

			if(bStatus)
			{
				//提示写入成功
				special_return_status(PROCESS_OK|NO_JUMP|HAVE_TIP,NULL,"ID_STR_WRITE_SUCCESS",NULL,0,0,NULL,pOut);
			}
		}

		break;
	case 1:
		{
			bStatus = write_VehicleDefinition(cSpecialCmdData,pstParam,pOut);

			if(bStatus)
			{
				//提示写入成功
				special_return_status(PROCESS_OK|NO_JUMP|HAVE_TIP,NULL,"ID_STR_WRITE_SUCCESS",NULL,0,0,NULL,pOut);
			}
		}
		break;
	case 2:
		{
			read_EOLConfig(cSpecialCmdData,pstParam,pOut);

		}
		break;
	case 3:
		{
			bStatus = write_EOLConfig(cSpecialCmdData,pstParam,pOut);

			if(bStatus)
			{
				//提示写入成功
				special_return_status(PROCESS_OK|NO_JUMP|HAVE_TIP,NULL,"ID_STR_WRITE_SUCCESS",NULL,0,0,NULL,pOut);
			}
		}
	case 4:
		{
			int i = 0;

			while(i++ < 0xfffffff)
				;
			//提示写入成功
			special_return_status(PROCESS_OK|NO_JUMP|NO_TIP,NULL,"ID_STR_WRITE_SUCCESS",NULL,0,0,NULL,pOut);
		}
		break;
	
	case 5:
		break;
	//重新激活系统
	case 6:
		{
			reavtive_system(pstParam,pOut);
		}
		break;
	//发送退出系统命令
	case 7:
		{
			sp_quit_system(pstParam,pOut);
		}
		break;
	default:
		break;
	}

}

/*************************************************
Description:	获得特殊功能的命令数据
Input:	
	pcSource	存放命令数据的地址（字符串）
	iMaxLen	命令数据长度（字符串）

Output:	pcCmdData	存放命令数据地址
Return:	int		命令数据个数
Others:	直接从xml获取的命令数据是string类型的，
		且格式类似"00,10,00,01,01,25,07,11"
*************************************************/
int get_string_type_data_to_byte(byte* pcCmdData, const byte* pcSource, const int iMaxLen)
{
	byte cTemp[15] = {0};
	int i=0,k=0,m=0;
	int iScale = 16;

	if(0 == iMaxLen)
		return iMaxLen;

	while(i != iMaxLen + 1)
	{
		if(0 == k)
			iScale = 10;

		if( isspace(pcSource[i]) )//处理空格、换行、制表符等
		{
			i += 1;
			continue;
		}

		if(',' == pcSource[i])
		{
			cTemp[k] = '\0';
			pcCmdData[m] = (byte)strtol(cTemp,NULL,iScale);
			m += 1;
			k = 0;
			i += 1;
			continue;
		}
		else if(i == iMaxLen)
		{
			cTemp[k] = '\0';
			pcCmdData[m] = (byte)strtol(cTemp,NULL,iScale);
			m += 1;
			break;
		}

		cTemp[k] = pcSource[i];

		if(1 == k)//在xml中0和x中间有空格其实是错误的，这里添加这种容错
		{
			if(cTemp[k] == 'x' || cTemp[k] == 'X')
				iScale = 16;
		}

		k += 1;

		i += 1;
	}

	return m;
}


/*************************************************
Description:	获得设码功能XML中类型为STRING的第一个字符串
Input:	
pcSource	存放命令数据的地址（字符串）
iMaxLen	命令数据长度（字符串）

Output:	pcCmdData	存放命令数据地址
Return:	int		命令数据个数
Others:	例如<param type="string" value="COMBOX_READ_00,01,03,00,0x60,00"/>
其获取的是COMBOX_READ_00,以","作为字符串的结束
*************************************************/
int get_string_type_first_value_string(uint8* u8pcCmdData, const uint8* u8pcSource, const uint32 u32MaxLen)
{
	uint32 u32Count = 0;
	uint32 u32IndexSum = 0;

	if(0 == u32MaxLen)
		return u32MaxLen;

	while(',' != u8pcSource[u32Count])
	{
		u8pcCmdData[u32Count+1] = u8pcSource[u32Count];
		u32Count += 1;
	}

	u8pcCmdData[0] = u32Count;

	u8pcCmdData[u32Count+1] = '\0';

	return u32Count+1;
}

/*************************************************
Description:	获得设码功能XML中类型为STRING的几个字符串，用结构体数组存储
Input:	
u8pcSource	存放数据的地址（字符串）
u32MaxLen	数据长度（字符串）
Output:	pcCmdData	存放命令数据地址
Return:	int		字符串的个数
Others:	例如<param type="string" value="COMBOX_READ_00,COMBOX_READ_01,"/>
其获取的是u8pcCmdData[0] = "COMBOX_READ_00",u8pcCmdData[1] = "COMBOX_READ_00",以","作为字符串的结束
*************************************************/
int get_string_type_to_string_arr(STRUCT_STRING_NONE* u8pcCmdData, const uint8* u8pcSource, const uint32 u32MaxLen)
{
	uint16  u8Count = 0;			//计算器，对整个传入的字符串进行遍历
	uint16  u8StrCount = 0;		//循环计算器，记录每个字符串
	uint16  u8StrNum = 0;		//递增记录字符串的总数	
	uint8  u8StrTemp[300] = {0};	//保存临时字符串

	if(0 == u32MaxLen)
		return u32MaxLen;

	while( u8Count != u32MaxLen + 1 )
	{
		if ( ',' == u8pcSource[u8Count] || '\0' == u8pcSource[u8Count] )
		{
			u8StrTemp[u8StrCount] = '\0';
			u8pcCmdData[u8StrNum].m_strID = u8StrNum;
			strcpy( u8pcCmdData[u8StrNum].m_strTemp, u8StrTemp );

			memset( u8StrTemp, 0, u8StrCount );

			u8StrNum += 1;
			u8StrCount = 0;
			u8Count += 1;
			continue;
		}

		u8StrTemp[u8StrCount] = u8pcSource[u8Count];

		u8StrCount += 1;
		u8Count += 1;
	}

	return u8StrNum;

}


/*************************************************
Description:	获得类型为string的命令数据
Input:	
	pcSource	存放命令数据的地址（字符串）
	iMaxLen		命令数据长度（字符串）

Output:	pu32Dest	存放命令数据地址
Return:	int		命令数据个数
Others:	直接从xml获取的命令数据是string类型的，
		且格式类似"00,10,0x00,01,01,25,07,11"
		把结果保存在uint32型地址中
*************************************************/
int get_string_type_data_to_uint32(uint32 *pu32Dest, const byte* pcSource, const int iMaxLen)
{
	byte cTemp[15] = {0};
	int i=0,k=0,m=0;
	int iScale = 16;

	if(0 == iMaxLen)
		return iMaxLen;

	while(i != iMaxLen + 1)
	{
		if(0 == k)
			iScale = 10;

		if( isspace(pcSource[i]) )//处理空格、换行、制表符等
		{
			i += 1;
			continue;
		}

		if(',' == pcSource[i])
		{
			cTemp[k] = '\0';
			pu32Dest[m] = strtol(cTemp,NULL,iScale);
			m += 1;
			k = 0;
			i += 1;
			continue;
		}
		else if(i == iMaxLen)
		{
			cTemp[k] = '\0';
			pu32Dest[m] = strtol(cTemp,NULL,iScale);
			m += 1;
			break;
		}

		cTemp[k] = pcSource[i];

		if(1 == k)//在xml中0和x中间有空格其实是错误的，这里添加这种容错
		{
			if(cTemp[k] == 'x' || cTemp[k] == 'X')
				iScale = 16;
		}

		k += 1;

		i += 1;
	}

	return m;

}

/*************************************************
Description:	获得类型为string的命令数据，存入double型数组中
Input:	
pcSource	存放命令数据的地址（字符串）
iMaxLen		命令数据长度（字符串）

Output:	pu32Dest	存放命令数据地址
Return:	int		命令数据个数
Others:	直接从xml获取的命令数据是string类型的，
且格式类似"00,10,0x00,01,01,12.75,07,11"
把结果保存在int型地址中
*************************************************/
int get_string_type_data_to_double(double *pu32Dest, const byte* pcSource, const int iMaxLen)
{
	byte cTemp[300] = {0};
	int i=0,k=0,m=0;
	int iScale = 16;
	double doutemp = 0;

	if(0 == iMaxLen)
	{
		return iMaxLen;
	}

	iScale = 10;

	while(i != iMaxLen + 1)
	{
		if(0 == k)
			iScale = 10;

		if( isspace(pcSource[i]) )//处理空格、换行、制表符等
		{
			i += 1;
			continue;
		}

		if(',' == pcSource[i])
		{
			cTemp[k] = '\0';
			if ( iScale == 10 && k <= 20 )
			{
				doutemp = atof(cTemp);
			}
			else if ( iScale == 16 && k <= 18 )
			{
				doutemp = strtol(cTemp,NULL,iScale);
			}

			pu32Dest[m] = doutemp;
			doutemp = 0;
			m += 1;
			k = 0;
			i += 1;
			continue;
		}
		else if(i == iMaxLen)
		{
			cTemp[k] = '\0';
			if ( iScale == 10 && k <= 20 )
			{
				doutemp = atof(cTemp);
			}
			else if ( iScale == 16 && k <= 18 )
			{
				doutemp = strtol(cTemp,NULL,iScale);
			}

			pu32Dest[m] = doutemp;
			doutemp = 0;
			m += 1;
			break;
		}

		cTemp[k] = pcSource[i];

		if(1 == k)//在xml中0和x中间有空格其实是错误的，这里添加这种容错
		{
			if(cTemp[k] == 'x' || cTemp[k] == 'X')
				iScale = 16;
			else
				iScale = 10;
		}

		k += 1;

		i += 1;
	}

	return m;

}


/*************************************************
Description:	通用向ECU写入数据函数
Input:	
	pcCmdData	存放命令数据的地址
	pcSource	存放要写入数据的地址

Output:	pOut	输出数据地址
Return:	bool	功能执行状态 true:成功 false:失败
Others:	pcCmdData中各字节含义如下：
pcCmdData[0]：协议类型（0x00:CAN、0x01:KWP）
pcCmdData[1]：单/多帧（0x00:单帧、0x01:多帧）
pcCmdData[2]：安全进入（0x00:无、0x01:有）
pcCmdData[3]：写入命令的偏移
pcCmdData[4]：写入起始字节
pcCmdData[5]：写入字节总数
*************************************************/
bool write_data_to_ECU(const byte* pcCmdData, const byte* pcSource, void* pOut)
{
	byte cWriteECUCmdOffset = 0;//写入命令偏移
	byte cStartOffset = 0;//写入的起始字节
	byte cByteSum = 0;//要写入的字节总数
	bool bProcessStatus = false;
	int  iCmdLen = 0;

	//得到写入命令偏移
	cWriteECUCmdOffset =pcCmdData[3];
	//得到写入的起始字节
	cStartOffset = pcCmdData[4];
	//得到写入字节总数
	cByteSum = pcCmdData[5];
	//第1步装配命令
	do
	{
		//如果是UDS协议或KWP协议
		if( 0x00 == pcCmdData[0] || 0x01 == pcCmdData[0])
		{
			memcpy
				(
					g_stInitXmlGobalVariable.m_p_stCmdList[cWriteECUCmdOffset].pcCmd + cStartOffset,/*目标地址*/
					pcSource,/*源地址*/
					cByteSum/*存储几个字节*/
				);
			break;							
		}
	
	}
	while(0);

	//下面是操作步骤，部分步骤可选
	do
	{
		//第2步 进入扩展层
		bProcessStatus = process_single_cmd_without_subsequent_processing( g_iExtendSessionCmdIndex[1], pOut );

		if( !bProcessStatus )
		{
			return false;
		}
		//第3步安全进入，可选
		if(0x01 == pcCmdData[2])
		{
			bProcessStatus = process_security_access_algorithm( 0, pOut );

			if( !bProcessStatus )
			{
				process_single_cmd_without_subsequent_processing( g_iDefaultSessionCmdIndex[1], pOut );
				return false;
			}	
		}

		//第4步	发送写入命令
		bProcessStatus = process_single_cmd_without_subsequent_processing( cWriteECUCmdOffset, pOut );

		if( !bProcessStatus )
		{
			return false;
		}
	}
	while(0);

	//第5步 进入默认层

	bProcessStatus = process_single_cmd_without_subsequent_processing( g_iDefaultSessionCmdIndex[1], pOut );

	if( !bProcessStatus )
	{
		return false;
	}

	return true;
}

/*************************************************
Description:	返回状态信息函数
Input:	
	cTipMode		状态信息类型，可取下列3种值的或
						功能执行的结果:
								COMM_INTERRUPT(0X02)
								PROCESS_OK(0X01)
								PROCESS_FAIL(0X00)
						是否跳步:
								HAVE_JUMP(0X04)
								NO_JUMP(0X00)
						是否弹出提示框:
								HAVE_TIP_DATA(0X10)
								HAVE_TIP(0X08)
								NO_TIP(0X00)

	pcLable			要跳转的lable
	pcTipContent	提示信息内容
	pcData			数据存放地址
	cDataLen		数据长度
	iUploadDataType	上传数据类型(HEX_PRINT,DEC_PRINT,ORIGINAL)
	pcControlsID	控件ID

Output:	pOut	输出数据地址
Return:	int		输出地址中存放数据长度
Others:该函数目前支持上传一组数据和与之相关的控件ID
*************************************************/
int special_return_status( const byte cTipMode,const byte* pcLable,const byte* pcTipContent, const byte* pcData, 
							const byte cDataLen, const int iUploadDataType,const byte* pcControlsID,void* pOut )
{
	byte *pOutTemp = ( byte* )pOut;
	byte cProcessValue	= (cTipMode >> 0) & 0x03;
	byte cJumpValue		= (cTipMode >> 2) & 0x01;
	byte cTipValue		= (cTipMode >> 3) & 0x03;

	byte cTipConentOffset	= 0;//提示内容保存偏移
	byte cAppendDataOffset	= 0;//附加数据保存偏移

	int i = 0;
	int iDataLen = 0;

	pOutTemp[0] = cProcessValue;
	pOutTemp[1] = cJumpValue;
	pOutTemp[2] = cTipValue;

	pOutTemp[3] = 0;
	pOutTemp[4] = 0;
	pOutTemp[5] = 0;
	pOutTemp[6] = 0;

	//装载Lable
	pOutTemp[7] = 0;//跳转Lable长度高字节
	pOutTemp[8] = (pcLable == NULL)? 0 : (byte)strlen(pcLable);//跳转Lable长度低字节

	memcpy(&pOutTemp[9],pcLable,pOutTemp[8]);

	//装载提示信息
	cTipConentOffset = 9 + pOutTemp[8];

	pOutTemp[ cTipConentOffset ] = 0;//提示信息长度高字节
	pOutTemp[ cTipConentOffset  + 1] = (pcTipContent == NULL)? 0 : (byte)strlen(pcTipContent);//提示信息长度低字节

	memcpy( &pOutTemp[ cTipConentOffset + 2 ], pcTipContent, pOutTemp[ cTipConentOffset + 1] );


	//装载附加数据
	cAppendDataOffset = cTipConentOffset + 2 + pOutTemp[cTipConentOffset +1];

	iDataLen = add_data_and_controlsID(cAppendDataOffset,pcData, cDataLen, 
		iUploadDataType,pcControlsID,pOut);

	return iDataLen;

}
/*************************************************
Description:	追加数据和控件ID
Input:	
	iAppendDataOffset	存放附加数据的偏移，
							与输出总长度相同
	pcData				数据存放地址
	cDataLen			数据长度
	iUploadDataType		上传数据类型(HEX_PRINT,DEC_PRINT,ORIGINAL)
	pcControlsID		控件ID

Output:	pOut	输出数据地址
Return:	int		输出地址中存放数据长度
Others:第一次使用本函数前需先调用special_return_status
函数，本函数会修改输出数据总数字节
*************************************************/
int add_data_and_controlsID(const int iAppendDataOffset,const byte* pcData, const byte cDataLen, 
							const int iUploadDataType,const byte* pcControlsID,void* pOut)
{
	byte *pOutTemp = ( byte* )pOut;
	int i = 0;

	int iControlsIDOffset	= 0;//控件ID保存偏移
	byte cDecDataLen		= 0;//10进制数据长度

	UNN_2WORD_4BYTE uuControlsIDLen;

	UNN_2WORD_4BYTE DataLen;

	DataLen.u32Bit = 0;
	uuControlsIDLen.u32Bit = 0;

	DataLen.u32Bit += iAppendDataOffset;//获取之前输出总长度

	switch(iUploadDataType)
	{
	case HEX_PRINT://按16进制打印成字符的
		{
			pOutTemp[iAppendDataOffset] = 0;
			pOutTemp[iAppendDataOffset + 1] = cDataLen * 2;

			for( i = 0; i < cDataLen; i++ )
			{
				/*sprintf_s( &pOutTemp[iAppendDataOffset + 1 + i * 2], ( cDataLen * 2 + 1 - i * 2 ), "%02X", pcData[i] );*/
				sprintf( &pOutTemp[iAppendDataOffset + 2 + i * 2], "%02X", pcData[i] );
			}
		}
		break;
	case DEC_PRINT://按10进制打印成字符的
		{
			cDecDataLen = 0;

			for( i = 0; i < cDataLen; i++ )
			{
				cDecDataLen += sprintf( &pOutTemp[iAppendDataOffset + 2 + cDecDataLen], "%d", pcData[i] );
			}

			pOutTemp[iAppendDataOffset] = 0; 
			pOutTemp[iAppendDataOffset + 1] = cDecDataLen;
		}
		break;
	case ORIGINAL:
	default://其他情况按原样拷贝
		{
			pOutTemp[iAppendDataOffset] = 0;
			pOutTemp[iAppendDataOffset + 1] = cDataLen;

			memcpy(&pOutTemp[iAppendDataOffset + 2],pcData,cDataLen);
		}
		break;
	}

	DataLen.u32Bit += 2 + pOutTemp[iAppendDataOffset + 1];

	//装载controlsID
	iControlsIDOffset = iAppendDataOffset + 2 + pOutTemp[iAppendDataOffset + 1];

	uuControlsIDLen.u32Bit = (pcControlsID == NULL)? 0 : (uint32)strlen(pcControlsID);

	pOutTemp[iControlsIDOffset] = uuControlsIDLen.u8Bit[1];
	pOutTemp[iControlsIDOffset + 1] = uuControlsIDLen.u8Bit[0];

	memcpy(&pOutTemp[iControlsIDOffset + 2],pcControlsID,uuControlsIDLen.u32Bit);

	DataLen.u32Bit += 2 + uuControlsIDLen.u32Bit;

	//装载总数
	pOutTemp[3] = DataLen.u8Bit[3];
	pOutTemp[4] = DataLen.u8Bit[2];
	pOutTemp[5] = DataLen.u8Bit[1];
	pOutTemp[6] = DataLen.u8Bit[0];

	return (int)DataLen.u32Bit;
}

/*************************************************
Description:	将一个byte型数据拆分成两个字符存放到字符数组中
Input:	
cByteValue:	输入数据存放地址
iLen:		真实数据的长度
Output:	
cMatchTEMP3:输出数据存放地址,其中第一个字节存放数据长度。
Return:	void
Others:	
*************************************************/
void hex_value_to_byte_string( uint8 *u8ByteOutput, uint8 iLen,const uint8 *u8ByteSource )
{
	uint8 u8Count;
	for ( u8Count=0; u8Count < iLen; u8Count++ )
	{
		u8ByteOutput[2*u8Count + 1]  = u8ByteSource[u8Count] >> 4;
		u8ByteOutput[2*u8Count + 1] += (u8ByteOutput[2*u8Count + 2] >= 0xA ? 0x37: 0x30);
		u8ByteOutput[2*u8Count + 2]  = u8ByteSource[u8Count] & 0x0f ;
		u8ByteOutput[2*u8Count + 2] += (u8ByteOutput[2*u8Count + 3] >= 0xA ? 0x37: 0x30);
	}

	u8ByteOutput[0] = u8Count*2;

	return ;
}

/*************************************************
Description:	将字符串按byte位拆分
Input:	
u8Source	存放命令数据的地址（字符串）
iMaxLen	命令数据长度（字符串）
Output:	u8pcData	存放命令数据地址
Return:	int		命令数据个数
Others:	直接从xml获取的命令数据是string类型的，
如格式类似"98CCC000000000005C000000004800000064"
拆分成一个个byte位数据"98 CC C0 00 00 00 00 00 5C 00 00 00 00 48 00 00 00 64"
*************************************************/
int get_string_to_byte_arr( uint8* u8pcData, const uint8* u8Source, const uint32 u32MaxLen)
{
	uint8 u8Temp[3] = {0};
	uint8 u8Count = 0;
	uint8 u8ArrNum = 0;

	if(0 == u32MaxLen)
	{
		return u32MaxLen;
	}

	if ( u32MaxLen % 2 !=0 )
	{	
		u8Temp[0] = u8Source[0];
		u8Temp[1] = '\0';
		u8pcData[u8ArrNum] = (byte)strtol(u8Temp,NULL,16);
		u8ArrNum++;
		u8Count++;
	}

	for ( u8Count; u8Count < u32MaxLen; u8Count += 2 )
	{
		u8Temp[0] = u8Source[u8Count];
		u8Temp[1] = u8Source[u8Count + 1];
		u8Temp[2] = '\0';
		u8pcData[u8ArrNum] = (byte)strtol(u8Temp,NULL,16);
		u8ArrNum += 1;
	}

	return u8ArrNum;
}
/************************************************************************
 Description:   某功能执行完成之后需重新激活系统
 
************************************************************************/
bool reavtive_system( void* pIn, void* pOut)
{
	bool iReceiveResult = false;
	int iIndexSum;
	int i;
	int cSpecialCmdData[128],cSpecialCmdDataTemp[128];
	STRUCT_CHAIN_DATA_INPUT* pstParam = ( STRUCT_CHAIN_DATA_INPUT* )pIn;

	package_and_send_active_config();
	iIndexSum = get_string_type_data_to_uint32(cSpecialCmdDataTemp, pstParam->pcData, pstParam->iLen);
	cSpecialCmdData[0] = iIndexSum;
	for( i = 0; i < iIndexSum; i++)
	{
		cSpecialCmdData[i+1] = cSpecialCmdDataTemp[i];
	}
	iReceiveResult = send_receive_and_process_7f( cSpecialCmdData );
	if( iReceiveResult != 0)
		return false;
	return true;
}

/*
Description:发送退出命令但不退出系统。

*/
void sp_quit_system( void* pIn, void* pOut)
{
	pf_general_function pFun = NULL;

	if(g_iActiveECUStatus == ACTIVE_ECU_SUCCESS)//激活成功后才执行退出动作
	{
		pFun = get_quit_system_fun(g_p_stProcessFunConfig->cQuitSystemFunOffset);
		assert(pFun);
		pFun(pIn,pOut);

		set_idle_link(0);//
	}

}