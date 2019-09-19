package handler

import (
	"CitiProject/model"
	"CitiProject/util"
	"github.com/gin-gonic/gin"
	"net/http"
	"net/url"
	"strconv"
)

/**
 * 获取用户的分析请求
 */
func GetAnalyses(c *gin.Context) {
	page := c.Param("page")
	total, analyses := (&model.Analysis{}).List(c.GetInt("id"), page)
	c.JSON(200, gin.H{
		"state": true,
		"data": gin.H{
			"total":    total,
			"analyses": analyses,
		},
	})
}

/**
 * 添加一条分析需求
 */
type AddAnalysisParam struct {
	CompanyId string `json:"company_id" binding:"required"`
}

func AddAnalysis(c *gin.Context) {
	var param AddAnalysisParam
	if c.BindJSON(&param) != nil {
		BadRequest(c)
		return
	}
	var analysis model.Analysis
	flag := analysis.Add(c.GetInt("id"), param.CompanyId)
	if flag {
		// 通知中控服务器
		_, err := http.PostForm("http://localhost:8888/new", url.Values{"analysis_id": {strconv.FormatInt(analysis.Id, 10)}, "company_id": {param.CompanyId}})
		if err != nil {
			util.HandleError(err)
			c.JSON(200, gin.H{
				"state":   false,
				"message": "创建分析请求失败，请稍后重试。",
			})
		} else {
			c.JSON(200, gin.H{
				"state": true,
			})
		}
	}
}

func GetAnalysis(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		BadRequest(c)
		return
	}
	var analysis model.Analysis
	err = analysis.Get(id)
	if err != nil {
		c.Status(404)
		return
	}
	c.JSON(200, gin.H{
		"state": true,
		"data":  analysis,
	})
}
