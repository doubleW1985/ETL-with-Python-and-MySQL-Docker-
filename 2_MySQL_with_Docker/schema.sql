-- create DB
create database `MySQL57_in_Docker`;
 
use MySQL57_in_Docker;
 
-- create Tables
DROP TABLE IF EXISTS `sku_head`;
DROP TABLE IF EXISTS `brand`;
DROP TABLE IF EXISTS `model`;
DROP TABLE IF EXISTS `sku_tail`;
DROP TABLE IF EXISTS `tt_sku`;
DROP TABLE IF EXISTS `sales_quantity_by_brand`;
DROP TABLE IF EXISTS `sales_quantity_by_created_date`;

CREATE TABLE `sku_head` (
  `id` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Type` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `product` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `brand` (
  `id` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `brand` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
CREATE TABLE `model` (
  `id` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sku_tail` (
  `id` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sku_tail` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `tt_sku` (
  `sku_id` int(10) NOT NULL,
  `sku` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantity` int(10) DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `sku_noplus` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sku1` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sku2` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nchar` int(10) DEFAULT NULL,
  `sku_num` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ndigit` int(10) DEFAULT NULL,
  `sku_head` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sku_tail_id` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `brand_id` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `model_id` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `design_id` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`sku_id`),
  CONSTRAINT fk_sku_head FOREIGN KEY(`sku_head`) REFERENCES sku_head(`id`),
  CONSTRAINT fk_brand_id FOREIGN KEY(`brand_id`) REFERENCES brand(`id`),
  CONSTRAINT fk_model_id FOREIGN KEY(`model_id`) REFERENCES model(`id`),
  CONSTRAINT fk_sku_tail_id FOREIGN KEY(`sku_tail_id`) REFERENCES sku_tail(`id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sales_quantity_by_brand` (
  `brand` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int(10) DEFAULT NULL,
  PRIMARY KEY (`brand`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sales_quantity_by_created_date` (
  `created_date` date NOT NULL,
  `quantity` int(10) DEFAULT NULL,
  PRIMARY KEY (`created_date`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
