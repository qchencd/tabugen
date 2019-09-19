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
	KeySoldierPropertyDefineName = "soldier_property_define"
)

// 兵种属性配置, 兵种.xlsx
type SoldierPropertyDefine struct {
	Name               string  // 士兵ID
	Level              int     // 士兵等级
	NameID             string  // 名字
	Description        string  // 描述
	BuildingName       string  // 所属建筑
	BuildingLevel      uint32  // 建筑等级
	RequireSpace       uint32  // 登陆艇占用空间
	Volume             uint32  // 体积
	UpgradeTime        uint32  // 升级消耗的时间(秒）
	UpgradeMaterialID  string  // 升级消耗的材料
	UpgradeMaterialNum int     // 升级消耗的数量
	ConsumeMaterial    string  // 生产消耗的材料
	ConsumeMaterialNum int     // 生产消耗的数量
	ConsumeTime        int     // 生产消耗的时间（秒/个）
	Act                int     // 攻击
	Hp                 int     // 血量
	BombLoad           int     // 载弹量
	Hurt               uint32  // buff伤害
	Duration           float32 // 持续时间
	TriggerInterval    float32 // 触发间隔
	SearchScope        float32 // 搜索范围
	AtkFrequency       float32 // 攻击间隔
	AtkRange           float32 // 攻击距离
	MovingSpeed        float32 // 移动速度
}

func (p *SoldierPropertyDefine) ParseFromRow(row []string) error {
	if len(row) < 24 {
		log.Panicf("SoldierPropertyDefine: row length out of index %d", len(row))
	}
	if row[0] != "" {
		p.Name = row[0]
	}
	if row[1] != "" {
		var value = MustParseTextValue("int", row[1], row)
		p.Level = value.(int)
	}
	if row[2] != "" {
		p.NameID = row[2]
	}
	if row[3] != "" {
		p.Description = row[3]
	}
	if row[4] != "" {
		p.BuildingName = row[4]
	}
	if row[5] != "" {
		var value = MustParseTextValue("uint32", row[5], row)
		p.BuildingLevel = value.(uint32)
	}
	if row[6] != "" {
		var value = MustParseTextValue("uint32", row[6], row)
		p.RequireSpace = value.(uint32)
	}
	if row[7] != "" {
		var value = MustParseTextValue("uint32", row[7], row)
		p.Volume = value.(uint32)
	}
	if row[8] != "" {
		var value = MustParseTextValue("uint32", row[8], row)
		p.UpgradeTime = value.(uint32)
	}
	if row[9] != "" {
		p.UpgradeMaterialID = row[9]
	}
	if row[10] != "" {
		var value = MustParseTextValue("int", row[10], row)
		p.UpgradeMaterialNum = value.(int)
	}
	if row[11] != "" {
		p.ConsumeMaterial = row[11]
	}
	if row[12] != "" {
		var value = MustParseTextValue("int", row[12], row)
		p.ConsumeMaterialNum = value.(int)
	}
	if row[13] != "" {
		var value = MustParseTextValue("int", row[13], row)
		p.ConsumeTime = value.(int)
	}
	if row[14] != "" {
		var value = MustParseTextValue("int", row[14], row)
		p.Act = value.(int)
	}
	if row[15] != "" {
		var value = MustParseTextValue("int", row[15], row)
		p.Hp = value.(int)
	}
	if row[16] != "" {
		var value = MustParseTextValue("int", row[16], row)
		p.BombLoad = value.(int)
	}
	if row[17] != "" {
		var value = MustParseTextValue("uint32", row[17], row)
		p.Hurt = value.(uint32)
	}
	if row[18] != "" {
		var value = MustParseTextValue("float32", row[18], row)
		p.Duration = value.(float32)
	}
	if row[19] != "" {
		var value = MustParseTextValue("float32", row[19], row)
		p.TriggerInterval = value.(float32)
	}
	if row[20] != "" {
		var value = MustParseTextValue("float32", row[20], row)
		p.SearchScope = value.(float32)
	}
	if row[21] != "" {
		var value = MustParseTextValue("float32", row[21], row)
		p.AtkFrequency = value.(float32)
	}
	if row[22] != "" {
		var value = MustParseTextValue("float32", row[22], row)
		p.AtkRange = value.(float32)
	}
	if row[23] != "" {
		var value = MustParseTextValue("float32", row[23], row)
		p.MovingSpeed = value.(float32)
	}
	return nil
}

func LoadSoldierPropertyDefineList(loader DataSourceLoader) ([]*SoldierPropertyDefine, error) {
	buf, err := loader.LoadDataByKey(KeySoldierPropertyDefineName)
	if err != nil {
		return nil, err
	}
	var list []*SoldierPropertyDefine
	var r = csv.NewReader(buf)
	for i := 0; ; i++ {
		row, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Errorf("SoldierPropertyDefine: read csv %v", err)
			return nil, err
		}
		var item SoldierPropertyDefine
		if err := item.ParseFromRow(row); err != nil {
			log.Errorf("SoldierPropertyDefine: parse row %d, %s, %v", i+1, row, err)
			return nil, err
		}
		list = append(list, &item)
	}
	return list, nil
}
