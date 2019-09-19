package util

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

var Mysql *sql.DB

/**
 * 连接数据库
 */
func ConnectDB() {
	var err error
	Mysql, err = sql.Open("mysql", "citi:ELYJelyj2019@tcp(rm-uf68k4dqap4q24x88ho.mysql.rds.aliyuncs.com:3306)/citi")
	if err != nil {
		panic(err)
	}
}
