-- MySQL Workbench Synchronization
-- Generated: 2017-10-04 01:10
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: jacobteves

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE TABLE IF NOT EXISTS `mudima_db`.`Article` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `link` VARCHAR(45) NULL DEFAULT NULL,
  `Summary` MEDIUMBLOB NULL DEFAULT NULL,
  `addDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualDate` DATETIME NULL DEFAULT NULL,
  `Cluster_id` INT(11) NOT NULL,
  `Topic_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `Topic_id`),
  UNIQUE INDEX `idArticle_UNIQUE` (`id` ASC),
  INDEX `fk_Article_Cluster_idx` (`Cluster_id` ASC),
  INDEX `fk_Article_Topic1_idx` (`Topic_id` ASC),
  CONSTRAINT `fk_Article_Cluster`
    FOREIGN KEY (`Cluster_id`)
    REFERENCES `mudima_db`.`Cluster` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Article_Topic1`
    FOREIGN KEY (`Topic_id`)
    REFERENCES `mudima_db`.`Topic` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mudima_db`.`Topic` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL COMMENT 'Name of cluster',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mudima_db`.`Cluster` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mudima_db`.`Keyword` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `word` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mudima_db`.`Topic_has_Cluster` (
  `Topic_id` INT(11) NOT NULL,
  `Cluster_id` INT(11) NOT NULL,
  PRIMARY KEY (`Topic_id`, `Cluster_id`),
  INDEX `fk_Topic_has_Cluster_Cluster1_idx` (`Cluster_id` ASC),
  INDEX `fk_Topic_has_Cluster_Topic1_idx` (`Topic_id` ASC),
  CONSTRAINT `fk_Topic_has_Cluster_Topic1`
    FOREIGN KEY (`Topic_id`)
    REFERENCES `mudima_db`.`Topic` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Topic_has_Cluster_Cluster1`
    FOREIGN KEY (`Cluster_id`)
    REFERENCES `mudima_db`.`Cluster` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `mudima_db`.`Cluster_has_Keyword` (
  `Cluster_id` INT(11) NOT NULL,
  `Keyword_id` INT(11) NOT NULL,
  PRIMARY KEY (`Cluster_id`, `Keyword_id`),
  INDEX `fk_Cluster_has_Keyword_Keyword1_idx` (`Keyword_id` ASC),
  INDEX `fk_Cluster_has_Keyword_Cluster1_idx` (`Cluster_id` ASC),
  CONSTRAINT `fk_Cluster_has_Keyword_Cluster1`
    FOREIGN KEY (`Cluster_id`)
    REFERENCES `mudima_db`.`Cluster` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cluster_has_Keyword_Keyword1`
    FOREIGN KEY (`Keyword_id`)
    REFERENCES `mudima_db`.`Keyword` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
