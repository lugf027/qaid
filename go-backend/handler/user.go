package handler

import (
	"CitiProject/model"
	"CitiProject/util"
	"github.com/gin-gonic/gin"
	"time"
)

/**
 * 检验验证码并新增用户
 */
type AddUserParam struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
	Captcha  string `json:"captcha" binding:"required"`
}

func AddUser(c *gin.Context) {
	var param AddUserParam
	if c.BindJSON(&param) != nil {
		BadRequest(c)
		return
	}
	captcha := util.Redis.Get(param.Email).Val()
	if captcha == "" {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "验证码已过期，请重新获取。"})
		return
	} else if captcha != param.Captcha {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "验证码错误，请重新输入。"})
		return
	}
	user := &model.User{}
	flag := user.Add(param.Email, param.Password)
	if flag {
		// 将验证码从缓存中删除
		util.Redis.Del(param.Email)
		c.JSON(200, gin.H{
			"state": true,
			"data": gin.H{
				"auth": util.MakeAuthToken(user.Email),
				"user": user,
			},
		})
	} else {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "注册失败，请稍后重试。",
		})
	}
}

/**
 * 用户登录
 */
type SignInParam struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func SignIn(c *gin.Context) {
	var param SignInParam
	if c.BindJSON(&param) != nil {
		BadRequest(c)
		return
	}
	user := &model.User{}
	flag := user.SignIn(param.Email, util.MD5(param.Password))
	if flag {
		// 生成登录验证Token
		auth := util.MakeAuthToken(param.Email)
		// 存入缓存，有效期24小时
		util.Redis.Set(auth, user.Id, 24*time.Hour)
		c.JSON(200, gin.H{
			"state": true,
			"data": gin.H{
				"auth": auth,
				"user": user,
			},
		})
	} else {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "登录失败，用户名或密码错误。",
		})
	}
}
