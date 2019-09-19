// This file is auto-generated by taxi v1.0.2, DO NOT EDIT!

package config

import (
	"encoding/csv"
	"io"
	"strings"
)

var (
	_ = io.EOF
	_ = strings.Compare
)

const (
	KeyGlobalPropertyDefineName = "global_property_define"
)

// 全局数值配置, 全局变量表.xlsx
type GlobalPropertyDefine struct {
	GoldExchangeTimeFactor1    float32        // 金币兑换时间参数1
	GoldExchangeTimeFactor2    float32        // 金币兑换时间参数2
	GoldExchangeTimeFactor3    float32        // 金币兑换时间参数3
	GoldExchangeResource1Price uint32         // 金币兑换资源1价格
	GoldExchangeResource2Price uint32         // 金币兑换资源2价格
	GoldExchangeResource3Price uint32         // 金币兑换资源3价格
	GoldExchangeResource4Price uint32         // 金币兑换资源4价格
	FreeCompleteSeconds        uint32         // 免费立即完成时间
	CancelBuildReturnPercent   uint32         // 取消建造后返还资源比例
	SpawnLevelLimit            []int          // 最大刷新个数显示
	FirstRechargeReward        map[string]int // 首充奖励
}

func (p *GlobalPropertyDefine) ParseFromRows(rows [][]string) error {
	if len(rows) < 11 {
		log.Panicf("GlobalPropertyDefine:row length out of index, %d < 11", len(rows))
	}
	if rows[0][3] != "" {
		var value = MustParseTextValue("float32", rows[0][3], 0)
		p.GoldExchangeTimeFactor1 = value.(float32)
	}
	if rows[1][3] != "" {
		var value = MustParseTextValue("float32", rows[1][3], 1)
		p.GoldExchangeTimeFactor2 = value.(float32)
	}
	if rows[2][3] != "" {
		var value = MustParseTextValue("float32", rows[2][3], 2)
		p.GoldExchangeTimeFactor3 = value.(float32)
	}
	if rows[3][3] != "" {
		var value = MustParseTextValue("uint32", rows[3][3], 3)
		p.GoldExchangeResource1Price = value.(uint32)
	}
	if rows[4][3] != "" {
		var value = MustParseTextValue("uint32", rows[4][3], 4)
		p.GoldExchangeResource2Price = value.(uint32)
	}
	if rows[5][3] != "" {
		var value = MustParseTextValue("uint32", rows[5][3], 5)
		p.GoldExchangeResource3Price = value.(uint32)
	}
	if rows[6][3] != "" {
		var value = MustParseTextValue("uint32", rows[6][3], 6)
		p.GoldExchangeResource4Price = value.(uint32)
	}
	if rows[7][3] != "" {
		var value = MustParseTextValue("uint32", rows[7][3], 7)
		p.FreeCompleteSeconds = value.(uint32)
	}
	if rows[8][3] != "" {
		var value = MustParseTextValue("uint32", rows[8][3], 8)
		p.CancelBuildReturnPercent = value.(uint32)
	}
	if rows[9][3] != "" {
		for _, item := range strings.Split(rows[9][3], "|") {
			var value = MustParseTextValue("int", item, rows[9][3])
			p.SpawnLevelLimit = append(p.SpawnLevelLimit, value.(int))
		}
	}
	if rows[10][3] != "" {
		p.FirstRechargeReward = map[string]int{}
		for _, text := range strings.Split(rows[10][3], "|") {
			if text == "" {
				continue
			}
			var items = strings.Split(text, "=")
			var value = MustParseTextValue("string", items[0], rows[10][3])
			var key = value.(string)
			value = MustParseTextValue("int", items[1], rows[10][3])
			var val = value.(int)
			p.FirstRechargeReward[key] = val
		}
	}
	return nil
}

func LoadGlobalPropertyDefine(loader DataSourceLoader) (*GlobalPropertyDefine, error) {
	buf, err := loader.LoadDataByKey(KeyGlobalPropertyDefineName)
	if err != nil {
		return nil, err
	}
	r := csv.NewReader(buf)
	rows, err := r.ReadAll()
	if err != nil {
		log.Errorf("GlobalPropertyDefine: csv read all, %v", err)
		return nil, err
	}
	var item GlobalPropertyDefine
	if err := item.ParseFromRows(rows); err != nil {
		log.Errorf("GlobalPropertyDefine: parse row %d, %v", len(rows), err)
		return nil, err
	}
	return &item, nil
}
