package model

import "CitiProject/util"

type Company struct {
	Id       string `json:"id"`
	Name     string `json:"name"`
	ListedOn string `json:"listed_on"`
}

func (*Company) SearchByName(keyword string) []Company {
	var companies []Company
	rows, err := util.Mysql.Query("SELECT * FROM company WHERE name LIKE ? LIMIT 9", "%"+keyword+"%")
	if err != nil {
		util.HandleError(err)
	}
	defer rows.Close()
	for rows.Next() {
		var company Company
		_ = rows.Scan(&company.Id, &company.Name, &company.ListedOn)
		companies = append(companies, company)
	}
	return companies
}

func (*Company) SearchByCode(code string) []Company {
	var companies []Company
	var company Company
	err := util.Mysql.QueryRow("SELECT * FROM company WHERE company_id = ? LIMIT 1", code).Scan(&company.Id, &company.Name, &company.ListedOn)
	if err == nil {
		companies = append(companies, company)
	}
	return companies
}
