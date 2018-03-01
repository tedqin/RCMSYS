/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50718
Source Host           : localhost:3306
Source Database       : scrcmsys

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-04-12 20:58:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `books`
-- ----------------------------
DROP TABLE IF EXISTS `books`;
CREATE TABLE `books` (
  `bid` varchar(64) NOT NULL,
  `bname` varchar(64) NOT NULL,
  `bpopularity` int(11) NOT NULL,
  PRIMARY KEY (`bid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of books
-- ----------------------------

-- ----------------------------
-- Table structure for `records`
-- ----------------------------
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records` (
  `rid` varchar(64) NOT NULL,
  `ruid` varchar(64) DEFAULT NULL,
  `rbid` varchar(64) DEFAULT NULL,
  `rlendtime` time NOT NULL,
  `rreturntime` time NOT NULL,
  PRIMARY KEY (`rid`),
  KEY `ruid` (`ruid`),
  KEY `rbid` (`rbid`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`ruid`) REFERENCES `users` (`uid`),
  CONSTRAINT `records_ibfk_2` FOREIGN KEY (`rbid`) REFERENCES `books` (`bid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of records
-- ----------------------------

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` varchar(64) NOT NULL,
  `udepartment` varchar(64) NOT NULL,
  `urecord` int(11) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
