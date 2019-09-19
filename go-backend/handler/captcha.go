package handler

import (
	"CitiProject/model"
	"CitiProject/util"
	"github.com/gin-gonic/gin"
	"time"
)

/**
 * 发送注册验证码
 */
type SendCaptchaParam struct {
	Email string `json:"email" binding:"required"`
}

func SendSignUpCaptcha(c *gin.Context) {
	var param SendCaptchaParam
	if c.BindJSON(&param) != nil {
		BadRequest(c)
		return
	}
	// 检查该邮箱是否已注册
	if (&model.User{}).HasUser(param.Email) {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "该邮箱已被注册，请更换邮箱。",
		})
		return
	}
	// 生成并发送
	captcha, flag := util.SendCaptcha(param.Email, "用户注册验证码")
	if flag {
		// 将验证码存入缓存
		util.Redis.Set(param.Email, captcha, 10*time.Minute)
		c.JSON(200, gin.H{
			"state": true,
		})
	} else {
		c.JSON(200, gin.H{
			"state":   false,
			"message": "邮件发送异常，请稍后重试。",
		})
	}
}
