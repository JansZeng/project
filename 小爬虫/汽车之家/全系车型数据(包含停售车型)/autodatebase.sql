/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50726
Source Host           : 127.0.0.1:3306
Source Database       : autodatebase

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2020-07-23 18:03:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for autodatebase
-- ----------------------------
DROP TABLE IF EXISTS `autodatebase`;
CREATE TABLE `autodatebase` (
  `首字母` text COLLATE utf8_unicode_ci,
  `车型名称` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `厂商指导价(元)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `厂商` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `级别` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `能源类型` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `环保标准` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `上市时间` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `工信部纯电续航里程(km)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `快充时间(小时)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `慢充时间(小时)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `快充电量百分比` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `最大功率(kW)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `最大扭矩(N·m)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `发动机` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `变速箱` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `长*宽*高(mm)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `车身结构` text COLLATE utf8_unicode_ci,
  `最高车速(km/h)` text COLLATE utf8_unicode_ci,
  `官方0-100km/h加速(s)` text COLLATE utf8_unicode_ci,
  `实测0-100km/h加速(s)` text COLLATE utf8_unicode_ci,
  `实测100-0km/h制动(m)` text COLLATE utf8_unicode_ci,
  `实测续航里程(km)` text COLLATE utf8_unicode_ci,
  `工信部综合油耗(L/100km)` text COLLATE utf8_unicode_ci,
  `实测油耗(L/100km)` text COLLATE utf8_unicode_ci,
  `整车质保` text COLLATE utf8_unicode_ci,
  `长度(mm)` text COLLATE utf8_unicode_ci,
  `宽度(mm)` text COLLATE utf8_unicode_ci,
  `高度(mm)` text COLLATE utf8_unicode_ci,
  `轴距(mm)` text COLLATE utf8_unicode_ci,
  `前轮距(mm)` text COLLATE utf8_unicode_ci,
  `后轮距(mm)` text COLLATE utf8_unicode_ci,
  `最小离地间隙(mm)` text COLLATE utf8_unicode_ci,
  `车门数(个)` text COLLATE utf8_unicode_ci,
  `座位数(个)` text COLLATE utf8_unicode_ci,
  `油箱容积(L)` text COLLATE utf8_unicode_ci,
  `行李厢容积(L)` text COLLATE utf8_unicode_ci,
  `整备质量(kg)` text COLLATE utf8_unicode_ci,
  `发动机型号` text COLLATE utf8_unicode_ci,
  `排量(mL)` text COLLATE utf8_unicode_ci,
  `排量(L)` text COLLATE utf8_unicode_ci,
  `进气形式` text COLLATE utf8_unicode_ci,
  `气缸排列形式` text COLLATE utf8_unicode_ci,
  `气缸数(个)` text COLLATE utf8_unicode_ci,
  `每缸气门数(个)` text COLLATE utf8_unicode_ci,
  `压缩比` text COLLATE utf8_unicode_ci,
  `配气机构` text COLLATE utf8_unicode_ci,
  `缸径(mm)` text COLLATE utf8_unicode_ci,
  `行程(mm)` text COLLATE utf8_unicode_ci,
  `最大马力(Ps)` text COLLATE utf8_unicode_ci,
  `最大功率转速(rpm)` text COLLATE utf8_unicode_ci,
  `最大扭矩转速(rpm)` text COLLATE utf8_unicode_ci,
  `发动机特有技术` text COLLATE utf8_unicode_ci,
  `燃料形式` text COLLATE utf8_unicode_ci,
  `燃油标号` text COLLATE utf8_unicode_ci,
  `供油方式` text COLLATE utf8_unicode_ci,
  `缸盖材料` text COLLATE utf8_unicode_ci,
  `缸体材料` text COLLATE utf8_unicode_ci,
  `电机类型` text COLLATE utf8_unicode_ci,
  `电动机总功率(kW)` text COLLATE utf8_unicode_ci,
  `电动机总扭矩(N·m)` text COLLATE utf8_unicode_ci,
  `前电动机最大功率(kW)` text COLLATE utf8_unicode_ci,
  `前电动机最大扭矩(N·m)` text COLLATE utf8_unicode_ci,
  `后电动机最大功率(kW)` text COLLATE utf8_unicode_ci,
  `后电动机最大扭矩(N·m)` text COLLATE utf8_unicode_ci,
  `系统综合功率(kW)` text COLLATE utf8_unicode_ci,
  `系统综合扭矩(N·m)` text COLLATE utf8_unicode_ci,
  `驱动电机数` text COLLATE utf8_unicode_ci,
  `电机布局` text COLLATE utf8_unicode_ci,
  `电池类型` text COLLATE utf8_unicode_ci,
  `电池能量(kWh)` text COLLATE utf8_unicode_ci,
  `百公里耗电量(kWh/100km)` text COLLATE utf8_unicode_ci,
  `电池组质保` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `快充电量(%)` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `挡位个数` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `变速箱类型` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `简称` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `驱动方式` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `前悬架类型` text COLLATE utf8_unicode_ci,
  `后悬架类型` text COLLATE utf8_unicode_ci,
  `助力类型` text COLLATE utf8_unicode_ci,
  `车体结构` text COLLATE utf8_unicode_ci,
  `前制动器类型` text COLLATE utf8_unicode_ci,
  `后制动器类型` text COLLATE utf8_unicode_ci,
  `驻车制动类型` text COLLATE utf8_unicode_ci,
  `前轮胎规格` text COLLATE utf8_unicode_ci,
  `后轮胎规格` text COLLATE utf8_unicode_ci,
  `备胎规格` text COLLATE utf8_unicode_ci,
  `主/副驾驶座安全气囊` text COLLATE utf8_unicode_ci,
  `前/后排侧气囊` text COLLATE utf8_unicode_ci,
  `前/后排头部气囊(气帘)` text COLLATE utf8_unicode_ci,
  `膝部气囊` text COLLATE utf8_unicode_ci,
  `后排安全带式气囊` text COLLATE utf8_unicode_ci,
  `后排中央安全气囊` text COLLATE utf8_unicode_ci,
  `被动行人保护` text COLLATE utf8_unicode_ci,
  `胎压监测功能` text COLLATE utf8_unicode_ci,
  `零胎压继续行驶` text COLLATE utf8_unicode_ci,
  `安全带未系提醒` text COLLATE utf8_unicode_ci,
  `ISOFIX儿童座椅接口` text COLLATE utf8_unicode_ci,
  `ABS防抱死` text COLLATE utf8_unicode_ci,
  `制动力分配(EBD/CBC等)` text COLLATE utf8_unicode_ci,
  `刹车辅助(EBA/BAS/BA等)` text COLLATE utf8_unicode_ci,
  `牵引力控制(ASR/TCS/TRC等)` text COLLATE utf8_unicode_ci,
  `车身稳定控制(ESC/ESP/DSC等)` text COLLATE utf8_unicode_ci,
  `并线辅助` text COLLATE utf8_unicode_ci,
  `车道偏离预警系统` text COLLATE utf8_unicode_ci,
  `车道保持辅助系统` text COLLATE utf8_unicode_ci,
  `道路交通标识识别` text COLLATE utf8_unicode_ci,
  `主动刹车/主动安全系统` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `夜视系统` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `疲劳驾驶提示` text COLLATE utf8_unicode_ci,
  `前/后驻车雷达` text COLLATE utf8_unicode_ci,
  `驾驶辅助影像` text COLLATE utf8_unicode_ci,
  `倒车车侧预警系统` text COLLATE utf8_unicode_ci,
  `巡航系统` text COLLATE utf8_unicode_ci,
  `驾驶模式切换` text COLLATE utf8_unicode_ci,
  `自动泊车入位` text COLLATE utf8_unicode_ci,
  `发动机启停技术` text COLLATE utf8_unicode_ci,
  `自动驻车` text COLLATE utf8_unicode_ci,
  `上坡辅助` text COLLATE utf8_unicode_ci,
  `陡坡缓降` text COLLATE utf8_unicode_ci,
  `可变悬架功能` text COLLATE utf8_unicode_ci,
  `空气悬架` text COLLATE utf8_unicode_ci,
  `电磁感应悬架` text COLLATE utf8_unicode_ci,
  `可变转向比` text COLLATE utf8_unicode_ci,
  `中央差速器锁止功能` text COLLATE utf8_unicode_ci,
  `整体主动转向系统` text COLLATE utf8_unicode_ci,
  `限滑差速器/差速锁` text COLLATE utf8_unicode_ci,
  `涉水感应系统` text COLLATE utf8_unicode_ci,
  `天窗类型` text COLLATE utf8_unicode_ci,
  `运动外观套件` text COLLATE utf8_unicode_ci,
  `轮圈材质` text COLLATE utf8_unicode_ci,
  `电动吸合车门` text COLLATE utf8_unicode_ci,
  `侧滑门形式` text COLLATE utf8_unicode_ci,
  `电动后备厢` text COLLATE utf8_unicode_ci,
  `感应后备厢` text COLLATE utf8_unicode_ci,
  `电动后备厢位置记忆` text COLLATE utf8_unicode_ci,
  `尾门玻璃独立开启` text COLLATE utf8_unicode_ci,
  `车顶行李架` text COLLATE utf8_unicode_ci,
  `发动机电子防盗` text COLLATE utf8_unicode_ci,
  `车内中控锁` text COLLATE utf8_unicode_ci,
  `钥匙类型` text COLLATE utf8_unicode_ci,
  `无钥匙启动系统` text COLLATE utf8_unicode_ci,
  `无钥匙进入功能` text COLLATE utf8_unicode_ci,
  `主动闭合式进气格栅` text COLLATE utf8_unicode_ci,
  `远程启动功能` text COLLATE utf8_unicode_ci,
  `车侧脚踏板` text COLLATE utf8_unicode_ci,
  `电池预加热` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `方向盘材质` text COLLATE utf8_unicode_ci,
  `方向盘位置调节` text COLLATE utf8_unicode_ci,
  `多功能方向盘` text COLLATE utf8_unicode_ci,
  `方向盘换挡` text COLLATE utf8_unicode_ci,
  `方向盘加热` text COLLATE utf8_unicode_ci,
  `方向盘记忆` text COLLATE utf8_unicode_ci,
  `行车电脑显示屏幕` text COLLATE utf8_unicode_ci,
  `全液晶仪表盘` text COLLATE utf8_unicode_ci,
  `液晶仪表尺寸` text COLLATE utf8_unicode_ci,
  `HUD抬头数字显示` text COLLATE utf8_unicode_ci,
  `内置行车记录仪` text COLLATE utf8_unicode_ci,
  `主动降噪` text COLLATE utf8_unicode_ci,
  `手机无线充电功能` text COLLATE utf8_unicode_ci,
  `电动可调踏板` text COLLATE utf8_unicode_ci,
  `座椅材质` text COLLATE utf8_unicode_ci,
  `运动风格座椅` text COLLATE utf8_unicode_ci,
  `主座椅调节方式` text COLLATE utf8_unicode_ci,
  `副座椅调节方式` text COLLATE utf8_unicode_ci,
  `主/副驾驶座电动调节` text COLLATE utf8_unicode_ci,
  `前排座椅功能` text COLLATE utf8_unicode_ci,
  `电动座椅记忆功能` text COLLATE utf8_unicode_ci,
  `副驾驶位后排可调节按钮` text COLLATE utf8_unicode_ci,
  `第二排座椅调节` text COLLATE utf8_unicode_ci,
  `后排座椅电动调节` text COLLATE utf8_unicode_ci,
  `后排座椅功能` text COLLATE utf8_unicode_ci,
  `后排小桌板` text COLLATE utf8_unicode_ci,
  `第二排独立座椅` text COLLATE utf8_unicode_ci,
  `座椅布局` text COLLATE utf8_unicode_ci,
  `后排座椅放倒形式` text COLLATE utf8_unicode_ci,
  `后排座椅电动放倒` text COLLATE utf8_unicode_ci,
  `前/后中央扶手` text COLLATE utf8_unicode_ci,
  `后排杯架` text COLLATE utf8_unicode_ci,
  `加热/制冷杯架` text COLLATE utf8_unicode_ci,
  `中控彩色液晶屏幕` text COLLATE utf8_unicode_ci,
  `中控液晶屏尺寸` text COLLATE utf8_unicode_ci,
  `GPS导航系统` text COLLATE utf8_unicode_ci,
  `导航路况信息显示` text COLLATE utf8_unicode_ci,
  `道路救援呼叫` text COLLATE utf8_unicode_ci,
  `中控液晶屏分屏显示` text COLLATE utf8_unicode_ci,
  `蓝牙/车载电话` text COLLATE utf8_unicode_ci,
  `手机互联/映射` text COLLATE utf8_unicode_ci,
  `语音识别控制系统` text COLLATE utf8_unicode_ci,
  `手势控制` text COLLATE utf8_unicode_ci,
  `车联网` text COLLATE utf8_unicode_ci,
  `车载电视` text COLLATE utf8_unicode_ci,
  `后排液晶屏幕` text COLLATE utf8_unicode_ci,
  `后排控制多媒体` text COLLATE utf8_unicode_ci,
  `外接音源接口类型` text COLLATE utf8_unicode_ci,
  `USB/Type-C接口数量` text COLLATE utf8_unicode_ci,
  `车载CD/DVD` text COLLATE utf8_unicode_ci,
  `220V/230V电源` text COLLATE utf8_unicode_ci,
  `行李厢12V电源接口` text COLLATE utf8_unicode_ci,
  `扬声器品牌名称` text COLLATE utf8_unicode_ci,
  `扬声器数量` text COLLATE utf8_unicode_ci,
  `近光灯光源` text COLLATE utf8_unicode_ci,
  `远光灯光源` text COLLATE utf8_unicode_ci,
  `灯光特色功能` text COLLATE utf8_unicode_ci,
  `LED日间行车灯` text COLLATE utf8_unicode_ci,
  `自适应远近光` text COLLATE utf8_unicode_ci,
  `自动头灯` text COLLATE utf8_unicode_ci,
  `转向辅助灯` text COLLATE utf8_unicode_ci,
  `转向头灯` text COLLATE utf8_unicode_ci,
  `车前雾灯` text COLLATE utf8_unicode_ci,
  `前大灯雨雾模式` text COLLATE utf8_unicode_ci,
  `大灯高度可调` text COLLATE utf8_unicode_ci,
  `大灯清洗装置` text COLLATE utf8_unicode_ci,
  `大灯延时关闭` text COLLATE utf8_unicode_ci,
  `触摸式阅读灯` text COLLATE utf8_unicode_ci,
  `车内环境氛围灯` text COLLATE utf8_unicode_ci,
  `前/后电动车窗` text COLLATE utf8_unicode_ci,
  `车窗一键升降功能` text COLLATE utf8_unicode_ci,
  `车窗防夹手功能` text COLLATE utf8_unicode_ci,
  `多层隔音玻璃` text COLLATE utf8_unicode_ci,
  `外后视镜功能` text COLLATE utf8_unicode_ci,
  `内后视镜功能` text COLLATE utf8_unicode_ci,
  `后风挡遮阳帘` text COLLATE utf8_unicode_ci,
  `后排侧窗遮阳帘` text COLLATE utf8_unicode_ci,
  `后排侧隐私玻璃` text COLLATE utf8_unicode_ci,
  `车内化妆镜` text COLLATE utf8_unicode_ci,
  `后雨刷` text COLLATE utf8_unicode_ci,
  `感应雨刷功能` text COLLATE utf8_unicode_ci,
  `可加热喷水嘴` text COLLATE utf8_unicode_ci,
  `空调温度控制方式` text COLLATE utf8_unicode_ci,
  `后排独立空调` text COLLATE utf8_unicode_ci,
  `后座出风口` text COLLATE utf8_unicode_ci,
  `温度分区控制` text COLLATE utf8_unicode_ci,
  `车载空气净化器` text COLLATE utf8_unicode_ci,
  `车内PM2.5过滤装置` text COLLATE utf8_unicode_ci,
  `负离子发生器` text COLLATE utf8_unicode_ci,
  `车内香氛装置` text COLLATE utf8_unicode_ci,
  `车载冰箱` text COLLATE utf8_unicode_ci,
  `面部识别` text COLLATE utf8_unicode_ci,
  `OTA升级` text COLLATE utf8_unicode_ci,
  `四驱形式` text COLLATE utf8_unicode_ci,
  `后排车门开启方式` text COLLATE utf8_unicode_ci,
  `货箱尺寸(mm)` text COLLATE utf8_unicode_ci,
  `中央差速器结构` text COLLATE utf8_unicode_ci,
  `实测快充时间(小时)` text COLLATE utf8_unicode_ci,
  `实测慢充时间(小时)` text COLLATE utf8_unicode_ci,
  `电动机` text COLLATE utf8_unicode_ci,
  `最大载重质量(kg)` text COLLATE utf8_unicode_ci,
  `工信部续航里程(km)` text COLLATE utf8_unicode_ci,
  `品牌ID` text COLLATE utf8_unicode_ci,
  `品牌名称` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `厂商ID` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `厂商名称` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `车系ID` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `车系名称` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `车型ID` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `选装包` text COLLATE utf8_unicode_ci,
  `外观颜色` text COLLATE utf8_unicode_ci,
  `内饰颜色` text COLLATE utf8_unicode_ci,
  `-` text COLLATE utf8_unicode_ci,
  `MD5` text COLLATE utf8_unicode_ci
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
