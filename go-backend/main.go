package main

import (
	"CitiProject/handler"
	"CitiProject/middleware"
	"CitiProject/util"
	"github.com/gin-gonic/gin"
	"log"
)

func main() {
	// gin.SetMode(gin.ReleaseMode)

	log.SetFlags(log.Ldate | log.Ltime)

	util.ConnectDB()
	defer util.Mysql.Close()
	util.ConnectCache()
	defer util.Redis.Close()

	app := gin.New()

	app.POST("/captcha/sign", handler.SendSignUpCaptcha)             // 发送注册验证码
	app.POST("/user", handler.AddUser)                               // 注册用户
	app.POST("/sign", handler.SignIn)                                // 用户登录
	app.GET("/companies", middleware.Auth, handler.SearchCompany)    // 查询公司
	app.GET("/analyses/:page", middleware.Auth, handler.GetAnalyses) // 获取分析请求列表
	app.POST("/analysis", middleware.Auth, handler.AddAnalysis)      // 创建一个分析请求
	app.GET("/analysis/:id", handler.GetAnalysis)

	// _ = exec.Command("cmd", "/C", "start http://localhost").Run()
	_ = app.Run("127.0.0.1:8001")
}
