/**********************************************************************
History:
	<author>	<time>		<desc>
	闫少伟		2013-12		创建文件
	郭文强		2015-03		添加PCBU显示函数；根据第一个有效字节，对第二个有效字节进行运算函数
************************************************************************/
#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE

#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include "formula_comply.h"
#include "../formula_parse/interface.h"
#include "formula.h"
#include "../command/command.h"
#include "../public/public.h"
#include "../InitConfigFromXml/init_config_from_xml_lib.h"
#include "../SpecialFunction/special_function.h"

//故障码各状态位为1的显示
byte *DTCStatusBitTrueArry[] =
{
	"ID_STR_DTC_STATUS00",
	"ID_STR_DTC_STATUS01",
	"ID_STR_DTC_STATUS02",
	"ID_STR_DTC_STATUS03",
	"ID_STR_DTC_STATUS04",
	"ID_STR_DTC_STATUS05",
	"ID_STR_DTC_STATUS06",
	"ID_STR_DTC_STATUS07",

};
//故障码各状态位为0的显示
byte *DTCStatusBitFalseArry[] =
{
	"ID_STR_DTC_STATUS08",
	"ID_STR_DTC_STATUS09",
	"ID_STR_DTC_STATUS10",
	"ID_STR_DTC_STATUS11",
	"ID_STR_DTC_STATUS12",
	"ID_STR_DTC_STATUS13",
	"ID_STR_DTC_STATUS14",
	"ID_STR_DTC_STATUS15",
};
/*************************************************
Description:	获得故障码状态
Input:	
	cDctStatusData	故障码状态字节
	cDtcMask		故障码mask值

Output:	pcOut	结果输出地址
Return:	int		该故障码支持的状态个数
Others:
*************************************************/

int get_Dtc_status( byte cDctStatusData, byte *pcOut, byte cDtcMask )
{
	int i = 0;
	int iSupportStatusCounter = 0;//支持的状态计数
	byte temp_Status = 0;
	byte temp_SupportStatus = 0;
	bool bFirst = true;

	while( i < 8 )
	{
		temp_SupportStatus = ( ( cDtcMask >> i ) & 0x01 );
		temp_Status = ( ( cDctStatusData >> i ) & 0x01 );

		if( 0x01 == temp_SupportStatus )//位为1
		{

			if( i > 0 && !bFirst)
			{
				*pcOut = ',';
				pcOut++;
			}

			bFirst = true;//第一次进来置为真

			if( 0x01 == temp_Status )
			{

				memcpy( pcOut, DTCStatusBitTrueArry[i], strlen( DTCStatusBitTrueArry[i] ) );
				pcOut += strlen( DTCStatusBitTrueArry[i] );

			}
			else//位为0
			{
				memcpy( pcOut, DTCStatusBitFalseArry[i], strlen( DTCStatusBitFalseArry[i] ) );
				pcOut += strlen( DTCStatusBitFalseArry[i] );

			}


			iSupportStatusCounter++;
		}

		i++;

	}

	*pcOut = '\0';

	return iSupportStatusCounter;
}

//大众故障码状态显示
byte *VWDTCStatusBitFalseArry[] =
{
	"ID_STR_VW_DTC_STATUS00",//偶发
	"ID_STR_VW_DTC_STATUS01",//非偶发

};
/*************************************************
Description:	获得大众故障码状态
Input:	
	cDctStatusData	故障码状态字节
	cDtcMask		故障码mask值

Output:	pcOut	结果输出地址
Return:	int		该故障码支持的状态个数
Others:
*************************************************/

int get_VW_Dtc_status( byte cDctStatusData, byte *pcOut, byte cDtcMask )
{
	if( (cDctStatusData & 0x80) == 0x80 )
	{

		memcpy( pcOut, VWDTCStatusBitFalseArry[0], strlen( VWDTCStatusBitFalseArry[0] ) );
		pcOut += strlen( VWDTCStatusBitFalseArry[0] );

	}
	else
	{
		memcpy( pcOut, VWDTCStatusBitFalseArry[1], strlen( VWDTCStatusBitFalseArry[1] ) );
		pcOut += strlen( VWDTCStatusBitFalseArry[1] );

	}

	*pcOut = '\0';

	return 1;
}


/*************************************************
Description:	处理版本信息显示格式
Input:	
	pcSource	取值地址
	cIvalidLen	有效长度
	cStyle		显示方式

Output:	pcOut	结果输出地址
Return:	void
Others:
*************************************************/

void process_inform_format( const byte* pcSource, byte cIvalidLen, byte cStyle, byte* pcOut )
{
	switch( cStyle )
	{
	case 'A'://ASCII码方式处理
		DisASCII( pcSource, cIvalidLen, pcOut );
		break;

	case 'H':
	case 'B':
		DisHex( pcSource, cIvalidLen, pcOut );
		break;

	case 'D':
		break;

	default:
		break;
	}
}


/*************************************************
Description:	根据数据流处理方式处理数据流
Input:	
	iDsId		数据流项ID
	pcDsSource	取值地址

Output:	pcDsValueOut	结果输出地址
Return:	void
Others: 
DisplayString(pcDsSource,stDisStringArraypcDsSource,stDisStringArray,0,0xff,0,pcDsValueOut);
*************************************************/
void process_normal_ds_calculate( uint8 * pcFormula, const uint8* pcDsSource,const uint8* pcFormat, uint8* pcDsValueOut )
{
	uint32 iRule[2] = {0};
	double dData[20] = {0.0};
	uint32 iFormulaType = 0;
	uint32 iEndian = 0;
	uint8 u8counter = 0;	//计数器，相当于平时用的i

	get_protocol_fomula_content( dData, iRule, pcFormula, (uint32)strlen(pcFormula) );

	iFormulaType = iRule[0];
	iEndian = iRule[1];

	switch(iFormulaType)
	{
	case 0://A [00-7F]   B [80-FF]
		{
			if (*pcDsSource < 0x80)
			{
				OneByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], pcFormat, pcDsValueOut ); //[00-7F]
			}
			else
			{
				OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], pcFormat, pcDsValueOut ); //[80-FF]
			}
		}
		break;
	case 1://当XY<=7FFF时,A .当XY>7FFF,B
		{
			uint16 twobyte = 0;

			if( iEndian == 0 ) //小端，高位在高地址xy
			{
				twobyte = ( uint16 )pcDsSource[1]<< 8;
				twobyte |= ( uint8 )pcDsSource[0];
			}
			else if( iEndian == 1 )//yx
			{
				twobyte = ( uint16 )pcDsSource[0] << 8;
				twobyte |= ( uint8 )pcDsSource[1];
			}

			if (twobyte <= 0x7fff)
			{
				TwoByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); // xy/10
			}
			else
			{
				TwoByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], iEndian, pcFormat, pcDsValueOut ); // xy/10 - 6553.6
			}
		}
		break;
	case 2://[0,7FFFFFFF] X*A/B+C-D ；             [80000000,FFFFFFFF]X*A/B+C-D
		{
			uint8 u8head = 0;

			if( iEndian == 1 ) //
			{
				u8head = ( uint8 )pcDsSource[3] << 24;
			}
			else if( iEndian == 0 )//
			{
				u8head = ( uint8 )pcDsSource[0];
			}

			if (u8head <= 0x7f)
			{
				FourByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); //
			}
			else
			{
				FourByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], iEndian, pcFormat, pcDsValueOut ); //
			}
		}
		break;

	case 3://当XY<=A7AF时,A .当XY>A7AF,B
		{
			uint16 twobyte = 0;

			if( iEndian == 0 ) //YX
			{
				twobyte = ( uint16 )pcDsSource[1]<< 8;
				twobyte |= ( uint8 )pcDsSource[0];
			}
			else if( iEndian == 1 )//XY
			{
				twobyte = ( uint16 )pcDsSource[0] << 8;
				twobyte |= ( uint8 )pcDsSource[1];
			}

			if (twobyte <= 0xA7AF)
			{
				TwoByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut );
			}
			else
			{
				Displayonebyte( pcDsSource,dData[4], dData[5], dData[6], dData[7],  pcFormat, pcDsValueOut ); 
			}
		}
		break;

	case 4://当XY<=A7B4时,A .当XY>A7B4,B
		{
			uint16 twobyte = 0;

			if( iEndian == 0 ) //YX
			{
				twobyte = ( uint16 )pcDsSource[1]<< 8;
				twobyte |= ( uint8 )pcDsSource[0];
			}
			else if( iEndian == 1 )//XY
			{
				twobyte = ( uint16 )pcDsSource[0] << 8;
				twobyte |= ( uint8 )pcDsSource[1];
			}

			if (twobyte <= 0xA7B4)
			{
				TwoByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); 
			}
			else
			{
				Displayonebyte( pcDsSource,dData[4], dData[5], dData[6], dData[7],  pcFormat, pcDsValueOut ); 
			}
		}
		break;


	case 5://当XY<=dData[5]时,TwoByteOperation .当XY>dData[5],显示dData[4]
		{
			uint16 twobyte = 0;

			if( iEndian == 0 ) //YX
			{
				twobyte = ( uint16 )pcDsSource[1]<< 8;
				twobyte |= ( uint8 )pcDsSource[0];
			}
			else if( iEndian == 1 )//XY
			{
				twobyte = ( uint16 )pcDsSource[0] << 8;
				twobyte |= ( uint8 )pcDsSource[1];
			}

			if ( twobyte <= (dData[5]))
			{
				TwoByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); 
			}
			else
			{
				Displayonebyte( pcDsSource,dData[4], dData[5], dData[6], dData[7],  pcFormat, pcDsValueOut ); 
			}
		}
		break;

	case 6://当XYZW<=dData[5]时,TwoByteOperation .当XYZW>dData[5],显示dData[4]
		{
			uint32 fourbyte = 0;

			if( iEndian == 1 ) //YX
			{
				fourbyte = ( uint32 )pcDsSource[3] << 24;
				fourbyte |= ( uint32 )pcDsSource[2]<<16;
				fourbyte |= ( uint32 )pcDsSource[1]<<8;
				fourbyte |= ( uint32 )pcDsSource[0];
			}
			else if( iEndian == 0 )//XY
			{
				fourbyte = ( uint32 )pcDsSource[0] << 24;
				fourbyte |= ( uint32 )pcDsSource[1]<<16;
				fourbyte |= ( uint32 )pcDsSource[2]<<8;
				fourbyte |= ( uint32 )pcDsSource[3];
			}

			if (fourbyte <= (dData[5]))
			{
				FourByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); //
			}
			else
			{
				Displayonebyte( pcDsSource,dData[4], dData[5], dData[6], dData[7],  pcFormat, pcDsValueOut ); 
			}
		}
		break;

	case 7://当XYZ<=dData[5]时,TwoByteOperation .当XYZ>dData[5],显示dData[4]
		{
			uint32 threebyte = 0;

			if( iEndian == 1 ) //YX
			{
				threebyte |= ( uint32 )pcDsSource[2]<<16;
				threebyte |= ( uint32 )pcDsSource[1]<<8;
				threebyte |= ( uint32 )pcDsSource[0];
			}
			else if( iEndian == 0 )//XY
			{
				threebyte |= ( uint32 )pcDsSource[0]<<16;
				threebyte |= ( uint32 )pcDsSource[1]<<8;
				threebyte |= ( uint32 )pcDsSource[2];
			}

			if (threebyte <= (dData[5]))
			{
				ThreeByteOperationd( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); //
			}
			else
			{
				Displayonebyte( pcDsSource,dData[4], dData[5], dData[6], dData[7],  pcFormat, pcDsValueOut ); 
			}
		}
		break;		

	case 11://一个字节的按高到低位优先控制
		{
			uint8 u8DisplayBuff[8][25] = {0};   //输出字符串参数
			uint8 u8StringValue[5] = {0};	  //字符串后缀

			for ( u8counter = 0; u8counter < 8; u8counter++ )
			{
				memcpy( u8DisplayBuff[u8counter], "ID_STR_DS_VALUE_", 16 );
				sprintf( u8StringValue, "%.0f", dData[u8counter] );
				memcpy( u8DisplayBuff[u8counter] + 16, u8StringValue, sizeof(u8StringValue) );
			}
			
			if ( 0x80 == (*pcDsSource & 0x80) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[0], strlen(u8DisplayBuff[0]) + 1 );
			}
			else if ( 0x40 == (*pcDsSource & 0x40) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[1], strlen(u8DisplayBuff[1]) + 1 );
			}
			else if ( 0x20 == (*pcDsSource & 0x20) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[2], strlen(u8DisplayBuff[2]) + 1 );
			}
			else if ( 0x10 == (*pcDsSource & 0x10) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[3], strlen(u8DisplayBuff[3]) + 1 );
			}
			else if ( 0x08 == (*pcDsSource & 0x08) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[4], strlen(u8DisplayBuff[4]) + 1 );
			}
			else if ( 0x04 == (*pcDsSource & 0x04) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[5], strlen(u8DisplayBuff[5]) + 1 );
			}
			else if ( 0x02 == (*pcDsSource & 0x02) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[6], strlen(u8DisplayBuff[6]) + 1 );
			}
			else
			{
				memcpy(pcDsValueOut, u8DisplayBuff[7], strlen(u8DisplayBuff[7]) + 1 );
			}
		}
		break;


	case 12://一个字节8个bit哪个位优先级最高就先传那位，
		{
			uint8 u8DisplayBuff[10][25] = {0};   //输出字符串参数
			uint8 u8StringValue[5] = {0};	    //字符串后缀
			uint8 u8PriorityByte[8] = {0};	    //依次存放优先级从高到低的位
			uint8 u8counter = 0;                //计数器

			for ( u8counter = 0; u8counter < 8; u8counter++ )
			{
				u8PriorityByte[u8counter] = (uint8)dData[u8counter] ;
			}

			for ( u8counter = 0; u8counter < 9; u8counter++ )
			{
				memcpy( u8DisplayBuff[u8counter], "ID_STR_DS_VALUE_", 16 );
				sprintf( u8StringValue, "%.0f", dData[u8counter+8] );
				memcpy( u8DisplayBuff[u8counter] + 16, u8StringValue, sizeof(u8StringValue) );
			}

			if ( (*pcDsSource >> u8PriorityByte[0]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[0], strlen(u8DisplayBuff[0]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[1]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[1], strlen(u8DisplayBuff[1]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[2]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[2], strlen(u8DisplayBuff[2]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[3]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[3], strlen(u8DisplayBuff[3]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[4]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[4], strlen(u8DisplayBuff[4]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[5]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[5], strlen(u8DisplayBuff[5]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[6]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[6], strlen(u8DisplayBuff[6]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[7]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[7], strlen(u8DisplayBuff[7]) + 1 );
			}
			else
			{
				memcpy(pcDsValueOut, u8DisplayBuff[8], strlen(u8DisplayBuff[8]) + 1 );
			}
		}
		break;

	case 13://A [00-66]   B [66-FF]
		{
			if (pcDsSource[1] < 0x66)
			{
				OneByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], pcFormat, pcDsValueOut ); //[00-66]
			}
			else
			{
				OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], pcFormat, pcDsValueOut ); //[66-FF]
			}
		}
		break;
	case 14:// X*7.47/254 [00-fe]		N/A ff
		{
			uint8 u8StringValue[4] = {0};

			if(dData[0] == 0)		//关键字节属于某个范围输出字符串不属于运算
			{
				if( pcDsSource[0] > dData[1] && pcDsSource[0] < dData[2] )
				{
					memcpy( pcDsValueOut, "ID_STR_DS_VALUE_", 16 );
					sprintf( u8StringValue, "%.0f", dData[3] );
					memcpy( pcDsValueOut + 16, u8StringValue, sizeof(u8StringValue) );
				}
				else
				{
					OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], "%.2f", pcDsValueOut );
				}
			}
			else	//关键字节属于某个范围运算不属于输出字符串
			{
				if( pcDsSource[0] > dData[1] && pcDsSource[0] < dData[2] )
				{
					OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], "%.2f", pcDsValueOut );
				}
				else
				{
					memcpy( pcDsValueOut, "ID_STR_DS_VALUE_", 16 );
					sprintf( u8StringValue, "%.0f", dData[3] );
					memcpy( pcDsValueOut + 16, u8StringValue, sizeof(u8StringValue) );
				}

			}
		}
		break;
	case 15:// X1*273.84/19+X2*14.36/255 结果大于274.97后显示--
		{
			double dResultOperation = 0.00;
			dResultOperation = pcDsSource[0] * 273.84 / 19 + pcDsSource[1] * 14.36 / 255;
			if(dResultOperation > 274.97)
			{
				memcpy( pcDsValueOut, "--", 3 );
			}
			else
			{
				sprintf(pcDsValueOut, "%.2f", dResultOperation);
			}
		}
		break;

	case PCBU_DISPLAY_DS://将输入按PCBU码显示
		{
			PCBU_display( pcDsSource, pcDsValueOut );
		}
		break;

	case OPERATE_BY_CONDITION://	条件运算
		{
			operate_by_condition(dData, pcDsSource, pcDsValueOut, pcFormat );
		}
		break;

	default:
		break;
	}
}

/*************************************************
Description:	根据识别规则处理数据流计算公式
Input:
	pcFormula		识别部分公式内容
	pcDsSource		取值地址
	pcFormat		数据输出格式

Output:	pcDsValueOut	结果输出地址
Return:	void
Others:
在xml中配置数据的顺序为：公式号、大小端标志
被加数、被减数、被乘数、被除数。。。。
*************************************************/
void process_normal_info_calculate( uint8 * pcFormula, const uint8* pcDsSource,const uint8* pcFormat, uint8* pcDsValueOut )
{
	uint32 iRule[2] = {0};
	double dData[20] = {0.0};
	uint32 iFormulaType = 0;
	uint32 iEndian = 0;
	uint32 Result = 0;
	uint8 u8counter = 0;	//计数器，相当于平时用的i

	get_protocol_fomula_content( dData, iRule, pcFormula, (int)strlen(pcFormula) );

	iFormulaType = iRule[0];
	iEndian = iRule[1];

	switch(iFormulaType)
	{
	case 0://A [00-7F]   B [80-FF]
		{
			if (*pcDsSource < 0x80)
			{
				OneByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], pcFormat, pcDsValueOut ); //[00-7F]
			}
			else
			{
				OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], pcFormat, pcDsValueOut ); //[80-FF]
			}
		}
		break;

	case 2://[0,7FFFFFFF] X*A/B+C-D ；             [80000000,FFFFFFFF]X*A/B+C-D
		{
			uint8 u8head = 0;

			if( iEndian == 1 ) //
			{
				u8head = ( uint8 )pcDsSource[3] << 24;
			}
			else if( iEndian == 0 )//
			{
				u8head = ( uint8 )pcDsSource[0];
			}

			if (u8head <= 0x7f)
			{
				FourByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], iEndian, pcFormat, pcDsValueOut ); //
			}
			else
			{
				FourByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], iEndian, pcFormat, pcDsValueOut ); //
			}
		}
		break;

	case 3:		//XXXX-XX-XX
		{
			uint8 u8Scaler = 0;
			sprintf( pcDsValueOut, "%02X%02X", pcDsSource[0],pcDsSource[1] );					

			for( u8counter = 4, u8Scaler = 2; u8Scaler < 4; u8counter += 3, u8Scaler++ )
			{
				pcDsValueOut[u8counter] = '-';				
				sprintf( pcDsValueOut+u8counter + 1, "%02X", pcDsSource[u8Scaler]);					
			}	
		}
		break;

	case 4://前两个字节为0，则显示后两位的十六进制，否则显示00，且00FF也显示0000
		{
			uint8 u8Scaler = 0;
			if ((pcDsSource[0]== 0x00)&&(pcDsSource[1]== 0x00)&&((pcDsSource[2]&pcDsSource[3])!= 0xFF))
			{			
				sprintf( pcDsValueOut, "%X%X", pcDsSource[2],pcDsSource[3] );					
			}
			else
			{
				memcpy( pcDsValueOut, "0000" , 4 );								
			}
		}
		break;

	case 5:		//VIN固定显示一个L,后面再加16位
		{
			int i = 0;
			uint8 u8Scaler = 0;
			memcpy( pcDsValueOut, "L" , 1 );			
			for( i = 0; i < 16; i++)
			{

				sprintf( pcDsValueOut+i+1, "%c", pcDsSource[i] );
			}

		}
		break;



	case 11:
		{
			uint8 u8DisplayBuff[3][30] = {0};   //输出字符串参数
			uint8 u8StringValue[5] = {0};	    //字符串后缀

			for ( u8counter = 0; u8counter < 3; u8counter++ )
			{
				memcpy( u8DisplayBuff[u8counter], "ID_STR_INTER_CON_STRING_0", 25 );
				sprintf( u8StringValue, "%.0f", dData[u8counter] );
				memcpy( u8DisplayBuff[u8counter] + 25, u8StringValue, sizeof(u8StringValue) );
			}

			if(((pcDsSource[0] < 0x40) && (pcDsSource[0] > 0x1f)) || ((pcDsSource[0] < 0xc0) && (pcDsSource[0] > 0x9f)))
			{
				memcpy( pcDsValueOut,u8DisplayBuff[0], strlen(u8DisplayBuff[0])+1 );
			}
			else if(((pcDsSource[0] < 0x60) && (pcDsSource[0] > 0x3f)) || ((pcDsSource[0] < 0xe0) && (pcDsSource[0] > 0xbf)))
			{
				memcpy( pcDsValueOut,u8DisplayBuff[1], strlen(u8DisplayBuff[1])+1 );
			}
			else
			{
				memcpy( pcDsValueOut,u8DisplayBuff[2], strlen(u8DisplayBuff[2])+1 );
			}
		}
		break;
	case 12:		//BB3132
		{
			uint8 u8Scaler = 0;

			memcpy( pcDsValueOut, "BB" , 3 );
			for( u8counter = 0, u8Scaler = 0; u8Scaler < 3; u8counter += 2, u8Scaler++ )
			{
				pcDsValueOut[u8counter + 2] = pcDsSource[u8Scaler] / 16 + 0x30;
				pcDsValueOut[u8counter + 3] = pcDsSource[u8Scaler] % 16 + 0x30;
			}	
		}
		break;
	case 13:		//31.32.33.34
		{
			uint8 u8Scaler = 0;

			pcDsValueOut[0] = pcDsSource[0] / 16 + 0x30;
			pcDsValueOut[1] = pcDsSource[0] % 16 + 0x30;

			for( u8counter = 2, u8Scaler = 1; u8Scaler < 4; u8counter += 3, u8Scaler++ )
			{
				pcDsValueOut[u8counter] = '.';
				pcDsValueOut[u8counter + 1] = pcDsSource[u8Scaler] / 16 + 0x30;
				pcDsValueOut[u8counter + 2] = pcDsSource[u8Scaler] % 16 + 0x30;
			}	
		}
		break;
	default:
		break;
	}
}


/*************************************************
Description:	根据冻结帧数据流方式处理数据流
Input:	
	pcFormula	数据流配置公式
	pcDsSource	取值地址

Output:	pcDsValueOut	结果输出地址
Return:	void
Others:
*************************************************/
void process_freeze_ds_calculate( byte * pcFormula, const byte* pcDsSource,const byte* pcFormat, byte* pcDsValueOut )
{
	uint32 iRule[2] = {0};
	double dData[20] = {0.0};
	uint32 iFormulaType = 0;
	uint32 iEndian = 0;
	uint32 Result = 0;
	uint8 u8counter = 0;	//计数器，相当于平时用的i

	get_protocol_fomula_content( dData, iRule, pcFormula, (int)strlen(pcFormula) );

	iFormulaType = iRule[0];
	iEndian = iRule[1];

	switch(iFormulaType)
	{
	case 0://A [00-7F]   B [80-FF]
		{
			if (*pcDsSource < 0x80)
			{
				OneByteOperation( pcDsSource, dData[0], dData[1], dData[2], dData[3], pcFormat, pcDsValueOut ); //[00-7F]
			}
			else
			{
				OneByteOperation( pcDsSource, dData[4], dData[5], dData[6], dData[7], pcFormat, pcDsValueOut ); //[80-FF]
			}
		}
		break;
	case 11://一个字节相与后按高到低位优先控制
		{
			uint8 u8DisplayBuff[8][25] = {0};   //输出字符串参数
			uint8 u8StringValue[5] = {0};	  //字符串后缀
			uint8 u8OpreateValue = 0;

			u8OpreateValue = *pcDsSource & 0x3F;

			for ( u8counter = 0; u8counter < 6; u8counter++ )
			{
				memcpy( u8DisplayBuff[u8counter], "ID_STR_FREEZE_VALUE_", 20 );
				sprintf( u8StringValue, "%.0f", dData[u8counter] );
				memcpy( u8DisplayBuff[u8counter] + 20, u8StringValue, sizeof(u8StringValue) );
			}

			if ( 0x20 == (u8OpreateValue & 0x20) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[1], strlen(u8DisplayBuff[1]) + 1 );
			}
			else if ( 0x10 == (u8OpreateValue & 0x10) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[2], strlen(u8DisplayBuff[2]) + 1 );
			}
			else if ( 0x08 == (u8OpreateValue & 0x08) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[3], strlen(u8DisplayBuff[3]) + 1 );
			}
			else if ( 0x04 == (u8OpreateValue & 0x04) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[4], strlen(u8DisplayBuff[4]) + 1 );
			}
			else if ( 0x02 == (u8OpreateValue & 0x02) )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[5], strlen(u8DisplayBuff[5]) + 1 );
			}
			else
			{
				memcpy(pcDsValueOut, u8DisplayBuff[0], strlen(u8DisplayBuff[0]) + 1 );
			}
		}
		break;

	case 12://一个字节8个bit哪个位优先级最高就先传那位，
		{
			uint8 u8DisplayBuff[10][25] = {0};   //输出字符串参数
			uint8 u8StringValue[5] = {0};	    //字符串后缀
			uint8 u8PriorityByte[8] = {0};	    //依次存放优先级从高到低的位
			uint8 u8counter = 0;                //计数器

			for ( u8counter = 0; u8counter < 8; u8counter++ )
			{
				u8PriorityByte[u8counter] = (uint8)dData[u8counter] ;
			}

			for ( u8counter = 0; u8counter < 9; u8counter++ )
			{
				memcpy( u8DisplayBuff[u8counter], "ID_STR_DS_VALUE_", 16 );
				sprintf( u8StringValue, "%.0f", dData[u8counter+8] );
				memcpy( u8DisplayBuff[u8counter] + 16, u8StringValue, sizeof(u8StringValue) );
			}

			if ( (*pcDsSource >> u8PriorityByte[0]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[0], strlen(u8DisplayBuff[0]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[1]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[1], strlen(u8DisplayBuff[1]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[2]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[2], strlen(u8DisplayBuff[2]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[3]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[3], strlen(u8DisplayBuff[3]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[4]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[4], strlen(u8DisplayBuff[4]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[5]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[5], strlen(u8DisplayBuff[5]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[6]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[6], strlen(u8DisplayBuff[6]) + 1 );
			}
			else if ( (*pcDsSource >> u8PriorityByte[7]) & 1 )
			{
				memcpy(pcDsValueOut, u8DisplayBuff[7], strlen(u8DisplayBuff[7]) + 1 );
			}
			else
			{
				memcpy(pcDsValueOut, u8DisplayBuff[8], strlen(u8DisplayBuff[8]) + 1 );
			}
		}
		break;
	case 13:
		{
			uint8 u8Ctemp[3] = {0};

			if(pcDsSource[0] == 1)
			{
				if(pcDsSource[1] < 11)
				{
					memcpy( pcDsValueOut, "ID_STR_FREEZE_VALUE_", 20 );
					sprintf(u8Ctemp, "%.0f", (double)(pcDsSource[1] + 1) );
					memcpy( pcDsValueOut+20, u8Ctemp, sizeof(u8Ctemp) );
				}
				else
				{
					memcpy( pcDsValueOut, "ID_STR_FREEZE_VALUE_0", 21 );
				}
			}
			else
			{
				memcpy( pcDsValueOut, "ID_STR_FREEZE_VALUE_0", 21 );
			}
		}
		break;
	case PCBU_DISPLAY_FZDS://将输入按PCBU码显示
		{
			PCBU_display( pcDsSource, pcDsValueOut );
		}
		break;

	default:
		break;
	}
}

/************************************************************************/
/* 下面是安全进入计算公式                                               */
/************************************************************************/

/*************************************************
  Description:	计算安全算法
  Calls:	seedToKey;
  Called By:	process_security_access_algorithm;

  Input:	Group	保存ECU回复seed的首地址

  Output:	Group	结果输出地址
  Return:	byte	key占用字节数
  Others:	函数定义会随系统而异
*************************************************/
byte security_calculate( byte *Group )
{
	uint32 Learmask = 0;
	UNN_2WORD_4BYTE Seed;
	uint8 Cnt = 0;
	Learmask = 0x5827A3B6;//0XA2159E16		

	for ( ; Cnt < 4; ++Cnt )
	{
		Seed.u8Bit[3-Cnt]	= *( Group + Cnt );
	}
	if ( Seed.u32Bit != 0)
	{
		for ( Cnt = 0; Cnt < 35; ++Cnt )
		{
			if ( Seed.u32Bit & 0x80000000 )
			{
				Seed.u32Bit <<= 1;
				Seed.u32Bit ^= Learmask;
			}
			else
			{
				Seed.u32Bit <<= 1;
			}
		}
	}
	for ( Cnt = 0; Cnt < 4; ++Cnt )
	{
		*(Group + Cnt) = Seed.u8Bit[3-Cnt];
	}
	return 4;

}
/*************************************************
Description:	根据安全等级处理安全算法
Input:	cAccessLevel	安全等级

Output:	pOut	结果输出地址
Return:	bool	算法执行状态（成功、失败）
Others:	函数具体实现会因系统而异
*************************************************/

bool process_security_access_algorithm( byte cAccessLevel, void* pOut )
{
	bool bProcessSingleCmdStatus = false;
	byte cBufferOffset = 0;//缓存偏移
	byte cRequestSeedCmdOffset = 0;
	byte cSendKeyCmdOffset = 0;

	byte cDataArray[10] = {0};
	byte cNeedBytes = 0;

	//根据安全等级确定命令偏移
	switch( cAccessLevel )
	{
	case 0:
		cRequestSeedCmdOffset	= g_iRequestSeedCmdIndex[1];
		cSendKeyCmdOffset		= g_iSendKeyCmdIndex[1];
		break;

	default:
		break;
	}

	cBufferOffset = g_stInitXmlGobalVariable.m_p_stCmdList[ cRequestSeedCmdOffset ].cBufferOffset;

	bProcessSingleCmdStatus = process_single_cmd_without_subsequent_processing( cRequestSeedCmdOffset, pOut );

	if( !bProcessSingleCmdStatus )
	{
		return false;
	}

	memcpy( cDataArray, ( g_stBufferGroup[cBufferOffset].cBuffer + 2 ), 4 );

	//根据安全等级确定计算公式
	switch( cAccessLevel )
	{
	case 0://安全等级为0
	{

		cNeedBytes = security_calculate( cDataArray );
	}
	break;

	default:
		break;
	}

	memcpy( ( g_stInitXmlGobalVariable.m_p_stCmdList[cSendKeyCmdOffset].pcCmd + 5 ), cDataArray, cNeedBytes );

	bProcessSingleCmdStatus = process_single_cmd_without_subsequent_processing( cSendKeyCmdOffset, pOut );

	if( !bProcessSingleCmdStatus )
	{
		return false;
	}

	return true;

}

/*************************************************
Description:	处理版本信息显示格式
Input:
pcSource	取值地址

Output:
pbCmdData	结果输出地址，结果为double型数据
piRlue		输出公式号和大小端标志
Return:	int		返回用于计算的数据个数
Others:
*************************************************/
int get_protocol_fomula_content(double* pbCmdData, int *piRlue, const char* pcSource, const int iMaxLen)
{
	char cTemp[20] = {0};
	int i=0,k=0,m=0;
	int iRlueByteCount = 0;

	if(0 == iMaxLen)
		return iMaxLen;

	while(1)
	{
		if( isspace(pcSource[iRlueByteCount]) )//处理空格、换行、制表符等
		{
			iRlueByteCount += 1;
			continue;
		}

		if(',' == pcSource[iRlueByteCount])
		{
			cTemp[k] = '\0';
			piRlue[m] = (int)atoi(cTemp);//(byte)strtol(cTemp,NULL,iScale);

			iRlueByteCount += 1;
			if(m == 1)//取到第2个数则跳出
				break;

			m += 1;
			k = 0;

			continue;
		}

		cTemp[k] = pcSource[iRlueByteCount];

		k += 1;

		iRlueByteCount += 1;
	}

	i = 0;
	k = 0;
	m = 0;

	pcSource += iRlueByteCount;

	while(i != iMaxLen - iRlueByteCount + 1)
	{
		if( isspace(pcSource[i]) )//处理空格、换行、制表符等
		{
			i += 1;
			continue;
		}

		if(',' == pcSource[i])
		{
			cTemp[k] = '\0';
			if( cTemp[0] == '-' )
			{
				pbCmdData[m] = atof(cTemp + 1) * -1;
			}
			else
			{
				pbCmdData[m] = atof(cTemp);//(byte)strtol(cTemp,NULL,iScale);
			}
			m += 1;
			k = 0;
			i += 1;
			continue;
		}
		else if(i == iMaxLen - iRlueByteCount)
		{
			cTemp[k] = '\0';
			pbCmdData[m] = atof(cTemp);
			m += 1;
			break;
		}

		cTemp[k] = pcSource[i];

		k += 1;

		i += 1;
	}

	return m;
}
/*************************************************
Description:	将传入内容用PCBU码表示
Input:			pcSource			传入内容
Output:			pcDsValueOut		转换好的PCBU码
Return:	无
Others:
*************************************************/
void PCBU_display(const byte *pcDsSource, byte *pcDsValueOut)
{
	uint8 u8ValueOprea[5] = {0};
	//将输入字符转化为字符
	sprintf( u8ValueOprea, "%02x", pcDsSource[0] );
	sprintf( u8ValueOprea + 2, "%02x", pcDsSource[1] );

	if( ( u8ValueOprea[0] >= '0') && ( u8ValueOprea[0] <= '3') )
	{
		pcDsValueOut[0] = 'p';
		pcDsValueOut[1] = u8ValueOprea[0];
	}
	else if( ( u8ValueOprea[0] >= '4') && ( u8ValueOprea[0] <= '7') )
	{
		pcDsValueOut[0] = 'c';
		pcDsValueOut[1] = u8ValueOprea[0] - 4;
	}
	else if( ( u8ValueOprea[0] >= '8') && ( u8ValueOprea[0] <= '9') )
	{
		pcDsValueOut[0] = 'b';
		pcDsValueOut[1] = u8ValueOprea[0] - 8;
	}
	else if( u8ValueOprea[0] == 'a' || u8ValueOprea[0] == 'b')
	{
		pcDsValueOut[0] = 'b';
		pcDsValueOut[1] = u8ValueOprea[0] - 'a' + '2';
	}
	else if( ( u8ValueOprea[0] >= 'c') && ( u8ValueOprea[0] <= 'f') )
	{
		pcDsValueOut[0] = 'u';
		pcDsValueOut[1] = u8ValueOprea[0] - 'c' + '0';
	}
	//处理其余字节
	memcpy(pcDsValueOut + 2, u8ValueOprea + 1, 4);

}
/*************************************************
Description:	第一个关键字节属于不同范围第二个关键字节进行不同运算，
                dData               参数
Input:			pcSource			传入内容
Output:			pcDsValueOut		计算结果
Return:	无
Others:
*************************************************/
void operate_by_condition( double *dData, const byte *pcDsSource, byte *pcDsValueOut, const uint8* pcFormat )
{
	//在[ dData[0] , dData[1] ]进行上边运算
	if ( (pcDsSource[0] >= dData[0]) && (pcDsSource[0] <= dData[1]) )
	{
		OneByteOperation( pcDsSource + 1, dData[2], dData[3], dData[4], dData[5], pcFormat, pcDsValueOut ); 
	}
	else
	{
		OneByteOperation( pcDsSource + 1, dData[6], dData[7], dData[8], dData[9], pcFormat, pcDsValueOut ); 
	}
}
/*************************************************
Description:	根据数据流处理方式处理数据流
Input:	
	iDsId		数据流项ID
	pcDsSource	取值地址

Output:	pcDsValueOut	结果输出地址
Return:	void
Others: 
DisplayString(pcDsSource,stDisStringArraypcDsSource,stDisStringArray,0,0xff,0,pcDsValueOut);
*************************************************/
void process_LJ_ds_calculate(  const char* pcDsSource, const int nDataSourceLen, const char * pcFormula, const int nFormulaLen, char* pcFormat, char* pcDsValueOut )
{
	double dData[2] ={0};
	uint32 iFormulaType = 0;
	uint32 iEndian = 0,fourbyte = 0;
	uint16 u8counter = 0;	//计数器，相当于平时用的i
	char len = 0;
	uint8 u8StringValue[4] = {0};
	STRUCT_STRING_NONE dStringTempData[300];  //保存要显示的字符串

	len = get_string_type_to_string_arr(dStringTempData, pcFormula, nFormulaLen);

	iEndian = (uint32)atoi(dStringTempData[0].m_strTemp) * 10 + (uint32)atoi(dStringTempData[1].m_strTemp);

	if(iEndian /10 == 1)
	{
		fourbyte = (( uint32 )pcDsSource[0]) & 0x000000ff;
	}
	else if(iEndian == 20) //yx
	{
		fourbyte = (( uint32 )pcDsSource[1] << 8) & 0x0000ff00;
		fourbyte |= (( uint32 )pcDsSource[0]) & 0x000000ff;
	}
	else if( iEndian == 21 )//xy
	{
		fourbyte = (( uint32 )pcDsSource[0] << 8) & 0x0000ff00;
		fourbyte |= (( uint32 )pcDsSource[1]) & 0x000000ff;
	}
	else if(iEndian == 30)//小端，高位在高地址zyx
	{
		fourbyte = (( uint32 )pcDsSource[2] << 16) & 0x00ff0000;
		fourbyte |= (( uint32 )pcDsSource[1] << 8) & 0x0000ff00;
 		fourbyte |= (( uint32 )pcDsSource[0]) & 0x000000ff;
	}
	else if( iEndian == 31 )//xyz
	{
		fourbyte = (( uint32 )pcDsSource[0] << 16) & 0x00ff0000;
		fourbyte |= (( uint32 )pcDsSource[1] << 8) & 0x0000ff00;
		fourbyte |= (( uint32 )pcDsSource[2]) & 0x000000ff;
	}
	else if(iEndian == 40) //小端，高位在高地址kzyx
	{
		fourbyte = (( uint32 )pcDsSource[3] << 24) & 0xff000000;
		fourbyte |= (( uint32 )pcDsSource[2] << 16) & 0x00ff0000;
		fourbyte |= (( uint32 )pcDsSource[1] << 8) & 0x0000ff00;
		fourbyte |= (( uint32 )pcDsSource[0]) & 0x000000ff;
	}
	else if( iEndian == 41 )//xykz
	{
		fourbyte = (( uint32 )pcDsSource[0] << 24) & 0xff000000;
		fourbyte |= (( uint32 )pcDsSource[1] << 16) & 0x00ff0000;
		fourbyte |= (( uint32 )pcDsSource[2] << 8) & 0x0000ff00;
		fourbyte |= (( uint32 )pcDsSource[3]) & 0x000000ff;
	}

	for(u8counter = 2; u8counter< len; u8counter = u8counter + 3)
	{
		if(u8counter+1 == len)
		{
			if(dStringTempData[u8counter].m_strTemp[0] == '@')
			{
				memcpy( pcDsValueOut, "ID_STR_DS_VALUE_", 16 );
				sprintf( u8StringValue, "%s", dStringTempData[u8counter].m_strTemp + 1 );
				memcpy( pcDsValueOut + 16, u8StringValue, sizeof(u8StringValue) );
			}
			else
			{
				calculate(pcDsSource, nDataSourceLen, dStringTempData[u8counter].m_strTemp, sizeof(dStringTempData[u8counter].m_strTemp), pcFormat, pcDsValueOut);
			}
			break;
		}
		else
		{
			if(dStringTempData[u8counter].m_strTemp[0] == '0' && dStringTempData[u8counter].m_strTemp[1] =='x' || dStringTempData[u8counter].m_strTemp[1] == 'X')
				dData[0] = (uint32)strtoul( dStringTempData[u8counter].m_strTemp, NULL, 16 );
			else
				dData[0] = atoi(dStringTempData[u8counter].m_strTemp);
			if(dStringTempData[u8counter + 1].m_strTemp[0] == '0' && dStringTempData[u8counter + 1].m_strTemp[1] =='x' || dStringTempData[u8counter + 1].m_strTemp[1] == 'X')
				dData[1] = (uint32)strtoul( dStringTempData[u8counter + 1].m_strTemp, NULL, 16 );
			else
				dData[1] = atoi(dStringTempData[u8counter + 1].m_strTemp);

			if (fourbyte >= (uint32)dData[0] && fourbyte <= (uint32)dData[1])
			{
				if(dStringTempData[u8counter + 2].m_strTemp[0] == '@')
				{
					memcpy( pcDsValueOut, "ID_STR_DS_VALUE_", 16 );
					sprintf( u8StringValue, "%s", dStringTempData[u8counter + 2].m_strTemp + 1 );
					memcpy( pcDsValueOut + 16, u8StringValue, sizeof(u8StringValue) );
				}
				else
				{
					calculate(pcDsSource, nDataSourceLen, dStringTempData[u8counter + 2].m_strTemp, sizeof(dStringTempData[u8counter + 2].m_strTemp), pcFormat, pcDsValueOut);
				}
				break;
			}
		}
	}
}
