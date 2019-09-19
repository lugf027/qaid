package model

import (
	"CitiProject/util"
	"strconv"
)

type Analysis struct {
	Id          int64  `json:"id"`
	CompanyId   string `json:"company_id"`
	CompanyName string `json:"company_name"`
	CreatedAt   string `json:"created_at"`
	State       string `json:"state"`
	Digit       string `json:"digit"`
	Stock       string `json:"stock"`
	Result      string `json:"result"`
}

/**
 * 获取用户的分析列表
 */
func (*Analysis) List(userId int, page string) (int, []Analysis) {
	var analyses []Analysis
	total := 0
	offsets, err := strconv.Atoi(page)
	// 判断页码是否为合法的数字
	if err != nil {
		return total, analyses
	}
	err = util.Mysql.QueryRow("SELECT count(*) FROM analysis WHERE user_id = ? GROUP BY user_id", userId).Scan(&total)
	if err != nil {
		util.HandleError(err)
		return total, analyses
	}
	// 校正offsets值
	offsets = (offsets - 1) * 9
	rows, err := util.Mysql.Query("SELECT analysis.analysis_id, analysis.company_id, company.name, analysis.created_at, analysis.state FROM analysis, company WHERE analysis.user_id = ? AND analysis.company_id = company.company_id ORDER BY analysis.created_at DESC LIMIT ?, 9", userId, offsets)
	if err != nil {
		util.HandleError(err)
	}
	defer rows.Close()
	for rows.Next() {
		var analysis Analysis
		_ = rows.Scan(&analysis.Id, &analysis.CompanyId, &analysis.CompanyName, &analysis.CreatedAt, &analysis.State)
		analyses = append(analyses, analysis)
	}
	return total, analyses
}

/**
 * 添加一项分析请求
 */
func (analysis *Analysis) Add(userId int, companyId string) bool {
	result, err := util.Mysql.Exec(
		"INSERT INTO analysis (user_id, company_id) VALUES (?, ?)",
		userId, companyId)
	if err != nil {
		util.HandleError(err)
		return false
	} else {
		analysis.Id, _ = result.LastInsertId()
		return true
	}
}

func (analysis *Analysis) Get(id int) error {
	err := util.Mysql.QueryRow("SELECT analysis.company_id, company.name, analysis.company_digit, analysis.company_stock, analysis.company_result FROM analysis, company WHERE analysis.company_id = company.company_id AND analysis.analysis_id = ?", id).Scan(&analysis.CompanyId, &analysis.CompanyName, &analysis.Digit, &analysis.Stock, &analysis.Result)
	return err
}
