package middleware

import (
	"CitiProject/util"
	"github.com/gin-gonic/gin"
)

/**
 * 登录验证中间件
 */
func Auth(c *gin.Context) {
	auth := c.GetHeader("Auth")
	id, _ := util.Redis.Get(auth).Int()
	// 判断是否存在匹配的Token
	if id == 0 {
		c.JSON(200, gin.H{
			"state": false,
			"code":  401,
		})
		c.Abort()
	} else {
		c.Set("id", id)
		c.Next()
	}
}
