package util

import (
	"github.com/go-redis/redis"
)

var Redis *redis.Client

/**
 * 连接缓存
 */
func ConnectCache() {
	Redis = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})
	_, err := Redis.Ping().Result()
	if err != nil {
		panic(err)
	}
}
