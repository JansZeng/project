/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50726
Source Host           : 127.0.0.1:3306
Source Database       : cn357

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2020-07-23 19:53:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cndatebase
-- ----------------------------
DROP TABLE IF EXISTS `cndatebase`;
CREATE TABLE `cndatebase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producer` varchar(255) DEFAULT NULL COMMENT '生产企业',
  `vehicle_model_code` varchar(255) DEFAULT NULL COMMENT '公告型号',
  `batch` varchar(255) DEFAULT NULL COMMENT '公告批次',
  `brand_name` varchar(255) DEFAULT NULL COMMENT '品牌',
  `vehicle_type` varchar(255) DEFAULT NULL COMMENT '类型',
  `fuel_type` varchar(255) DEFAULT NULL COMMENT '燃料种类',
  `axes_num` varchar(255) DEFAULT NULL COMMENT 'axes_num',
  `wheel_base` varchar(255) DEFAULT NULL COMMENT '轴距',
  `vin` varchar(255) DEFAULT NULL COMMENT '识别代号',
  `vehicle_length` varchar(255) DEFAULT NULL COMMENT '整车长',
  `vehicle_wide` varchar(255) DEFAULT NULL COMMENT '整车长',
  `vehicle_high` varchar(255) DEFAULT NULL COMMENT '整车高',
  `engine_type` varchar(255) DEFAULT NULL COMMENT '发动机型号',
  `md5` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cnial
-- ----------------------------
DROP TABLE IF EXISTS `cnial`;
CREATE TABLE `cnial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(255) DEFAULT NULL,
  `initial` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;
