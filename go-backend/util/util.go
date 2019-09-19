package util

import (
	"crypto/md5"
	"encoding/hex"
	"log"
	"math/rand"
	"net/smtp"
	"strconv"
	"time"
)

/**
 * 发送邮件
 */
func SendEmail(to string, subject string, message string) bool {
	from := "renjiangdu@qq.com"
	auth := smtp.PlainAuth("", from, "vyripiqndyqybdbh", "smtp.qq.com")
	nickname := "test"
	content := []byte("To: " + to + "\r\n" +
		"From: " + nickname + "<" + from + ">" + "\r\n" +
		"Subject: " + subject + "\r\n" +
		"Content-Type: text/plain; charset=UTF-8" +
		"\r\n\r\n" +
		message)
	err := smtp.SendMail("smtp.qq.com:25", auth, from, []string{to}, content)
	if err != nil {
		HandleError(err)
		return false
	} else {
		return true
	}
}

/**
 * 生成验证码
 */
func MakeCaptcha() string {
	rand.Seed(time.Now().Unix())
	captcha := 100000 + rand.Intn(900000)
	return strconv.Itoa(captcha)
}

/**
 * 发送验证码邮件
 */
func SendCaptcha(email string, subject string) (string, bool) {
	captcha := MakeCaptcha()
	// 发送给注册邮箱
	if SendEmail(email, subject, "您的验证码为："+captcha+"。") {
		return captcha, true
	} else {
		return "", false
	}
}

/**
 * MD5加密封装
 */
func MD5(plain string) string {
	ctx := md5.New()
	ctx.Write([]byte(plain))
	return hex.EncodeToString(ctx.Sum(nil))
}

/**
 * 生成登录验证Token
 */
func MakeAuthToken(email string) string {
	timestamp := strconv.FormatInt(time.Now().Unix(), 10)
	auth := MD5(email + timestamp)
	return auth
}

/**
 * 处理错误
 */
func HandleError(err error) {
	log.Println(err)
}
