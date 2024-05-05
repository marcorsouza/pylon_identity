/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 8.3.0 : Database - meudb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`meudb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `meudb`;

/*Data for the table `actions` */

insert  into `actions`(`id`,`name`,`task_id`) values 
(11,'CREATE',2),
(12,'READ',2),
(13,'UPDATE',2),
(14,'DELETE',2),
(20,'CREATE',4),
(21,'READ',4),
(22,'UPDATE',4),
(23,'DELETE',4),
(24,'CREATE_ACTIONS',4),
(25,'DELETE_ACTIONS',4),
(26,'CREATE',5),
(27,'READ',5),
(28,'UPDATE',5),
(29,'DELETE',5),
(30,'CREATE_ACTIONS',5),
(31,'DELETE_ACTIONS',5),
(34,'CREATE',6),
(35,'READ',6),
(36,'UPDATE',6),
(37,'DELETE',6),
(38,'CREATE_ROLES',6),
(39,'DELETE_ROLES',6);

/*Data for the table `alembic_version` */

insert  into `alembic_version`(`version_num`) values 
('8f36ed25393d');

/*Data for the table `applications` */

insert  into `applications`(`id`,`name`,`acronym`,`creation_date`) values 
(1,'Pylon Admin','PADM','2024-04-26 21:38:23');

/*Data for the table `role_action` */

insert  into `role_action`(`role_id`,`action_id`) values 
(1,12),
(1,14),
(1,13),
(1,11),
(1,20),
(1,21),
(1,22),
(1,23),
(1,24),
(1,25),
(1,26),
(1,27),
(1,28),
(1,29),
(1,30),
(1,31),
(1,34),
(1,35),
(1,36),
(1,37),
(1,38),
(1,39);

/*Data for the table `roles` */

insert  into `roles`(`id`,`name`,`application_id`) values 
(1,'Admin',1);

/*Data for the table `tasks` */

insert  into `tasks`(`id`,`name`,`tag_name`,`icon`,`show_in_menu`,`menu_title`) values 
(2,'Módulo de Aplicações','APPLICATIONS','',0,''),
(4,'Módulo de Regras','ROLES','',0,''),
(5,'Módulo de Tarefas','TASKS','',0,''),
(6,'Módulo de Usuários','USERS','',0,'');

/*Data for the table `user_role` */

insert  into `user_role`(`user_id`,`role_id`) values 
(2,1);

/*Data for the table `users` */

insert  into `users`(`id`,`name`,`username`,`password`,`email`,`is_locked_out`,`failed_pass_att_count`,`creation_date`,`last_login_date`,`last_change`,`temporary_password`,`temporary_password_expiration`) values 
(1,'Administrador','admin','$2b$12$1wLu1URoy8rrgfVyiqJd3ePZulBkjdiiP84IJMB4iHymFMSpeJjea','marco.souza@wilsonsons.com.br',0,0,'2024-04-27 12:15:16','2024-04-27 12:41:29',NULL,NULL,NULL),
(2,'Teste','manz','$2b$12$KS1q9v9zNgY5uWO7.VFjceQnSrJoDYd0MjsgNnJKgHO.fMaKsxlmq','marco.rsouza@gmail.com',0,0,'2024-04-27 12:20:47','2024-05-05 08:55:23',NULL,NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
