package model

import (
	"CitiProject/util"
	"database/sql"
)

type User struct {
	Id    int64  `json:"id"`
	Email string `json:"email"`
}

/**
 * 检查邮箱是否已被注册
 */
func (*User) HasUser(email string) bool {
	err := util.Mysql.QueryRow("SELECT user_id FROM user WHERE email = ?", email).Scan()
	return err != sql.ErrNoRows
}

/**
 * 添加一个用户
 */
func (user *User) Add(email string, password string) bool {
	result, err := util.Mysql.Exec(
		"INSERT INTO user (email, password) VALUES (?, ?)",
		email, util.MD5(password))
	if err != nil {
		util.HandleError(err)
		return false
	} else {
		id, _ := result.LastInsertId()
		user.Id = id
		user.Email = email
		return true
	}
}

/**
 * 用户登录
 */
func (user *User) SignIn(email string, password string) bool {
	user.Email = email
	err := util.Mysql.QueryRow("SELECT user_id FROM user WHERE email = ? AND password = ?", email, password).Scan(&user.Id)
	return err == nil
}
