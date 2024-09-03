package common

import "github.com/spf13/viper"

type Config struct {
	Debug        bool   `mapstructure:"DEBUG"`
	Port         int    `mapstructure:"PORT"`
	Host         string `mapstructure:"HOST"`
	DatabaseUrl  string `mapstructure:"DATABASE_URL"`
	MediaDir     string `mapstructure:"MEDIA_DIR"`
	KafkaBootStr string `mapstructure:"KAFKA_BOOTSTRAP_SERVER"`
}

func LoadConfig(path string) (*Config, error) {
	viper.AddConfigPath(path)
	viper.SetConfigName("app")
	viper.SetConfigType("env")

	// Override configs when environment variables occure
	viper.AutomaticEnv()

	err := viper.ReadInConfig()
	if err != nil {
		return nil, err
	}

	var config Config

	err = viper.Unmarshal(&config)

	if err != nil {
		return nil, err
	}
	return &config, nil
}
