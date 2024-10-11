-- Script that creates database WordFlow and user wordflow_dev

CREATE DATABASE IF NOT EXISTS WordFlow;

CREATE USER IF NOT EXISTS 'wordflow_dev' @'localhost' IDENTIFIED BY 'wordflow_dev_pwd';

GRANT ALL ON WordFlow.* TO 'wordflow_dev' @'localhost';

GRANT SELECT ON performance_schema.* TO 'wordflow_dev' @'localhost';