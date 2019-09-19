package handler

import (
	"CitiProject/model"
	"github.com/gin-gonic/gin"
)

/**
 * 搜索公司
 */
type SearchCompanyParam struct {
	Type    string `form:"type" binding:"required"`
	Keyword string `form:"keyword" binding:"required"`
}

func SearchCompany(c *gin.Context) {
	var param SearchCompanyParam
	if c.BindQuery(&param) != nil {
		BadRequest(c)
		return
	}
	var companies []model.Company
	if param.Type == "code" {
		// 通过公司代码搜索
		companies = (&model.Company{}).SearchByCode(param.Keyword)
	} else if param.Type == "name" {
		// 通过公司名称搜索
		companies = (&model.Company{}).SearchByName(param.Keyword)
	} else {
		// 异常处理
		BadRequest(c)
		return
	}
	c.JSON(200, gin.H{
		"state": true,
		"data": gin.H{
			"companies": companies,
		},
	})
}
