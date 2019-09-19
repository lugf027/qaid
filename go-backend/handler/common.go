package handler

import "github.com/gin-gonic/gin"

func BadRequest(c *gin.Context) {
	c.JSON(400, gin.H{
		"state":   false,
		"message": "请求失败，参数错误或缺少必要的参数。",
	})
	c.Abort()
}
