// This file is auto-generated by taxi v1.0.2, DO NOT EDIT!

package com.mycompany.csvconfig;

import java.util.*;


// 兵种属性配置, 兵种.xlsx
public class SoldierPropertyDefine
{
    public String  Name = "";                 // 士兵ID
    public int     Level = 0;                 // 士兵等级
    public String  NameID = "";               // 名字
    public String  Description = "";          // 描述
    public String  BuildingName = "";         // 所属建筑
    public int     BuildingLevel = 0;         // 建筑等级
    public int     RequireSpace = 0;          // 登陆艇占用空间
    public int     Volume = 0;                // 体积
    public int     UpgradeTime = 0;           // 升级消耗的时间(秒）
    public String  UpgradeMaterialID = "";    // 升级消耗的材料
    public int     UpgradeMaterialNum = 0;    // 升级消耗的数量
    public String  ConsumeMaterial = "";      // 生产消耗的材料
    public int     ConsumeMaterialNum = 0;    // 生产消耗的数量
    public int     ConsumeTime = 0;           // 生产消耗的时间（秒/个）
    public int     Act = 0;                   // 攻击
    public int     Hp = 0;                    // 血量
    public int     BombLoad = 0;              // 载弹量
    public int     Hurt = 0;                  // buff伤害
    public float   Duration = 0.0f;           // 持续时间
    public float   TriggerInterval = 0.0f;    // 触发间隔
    public float   SearchScope = 0.0f;        // 搜索范围
    public float   AtkFrequency = 0.0f;       // 攻击间隔
    public float   AtkRange = 0.0f;           // 攻击距离
    public float   MovingSpeed = 0.0f;        // 移动速度

    private static ArrayList<SoldierPropertyDefine> data_;
    public static ArrayList<SoldierPropertyDefine> getData() { return data_; } 

    // parse fields data from text row
    public void parseFromRow(String[] row)
    {
        if (row.length < 24) {
            throw new RuntimeException(String.format("SoldierPropertyDefine: row length out of index %d", row.length));
        }
        if (!row[0].isEmpty()) {
            this.Name = row[0].trim();
        }
        if (!row[1].isEmpty()) {
            this.Level = Integer.parseInt(row[1]);
        }
        if (!row[2].isEmpty()) {
            this.NameID = row[2].trim();
        }
        if (!row[3].isEmpty()) {
            this.Description = row[3].trim();
        }
        if (!row[4].isEmpty()) {
            this.BuildingName = row[4].trim();
        }
        if (!row[5].isEmpty()) {
            this.BuildingLevel = Integer.parseInt(row[5]);
        }
        if (!row[6].isEmpty()) {
            this.RequireSpace = Integer.parseInt(row[6]);
        }
        if (!row[7].isEmpty()) {
            this.Volume = Integer.parseInt(row[7]);
        }
        if (!row[8].isEmpty()) {
            this.UpgradeTime = Integer.parseInt(row[8]);
        }
        if (!row[9].isEmpty()) {
            this.UpgradeMaterialID = row[9].trim();
        }
        if (!row[10].isEmpty()) {
            this.UpgradeMaterialNum = Integer.parseInt(row[10]);
        }
        if (!row[11].isEmpty()) {
            this.ConsumeMaterial = row[11].trim();
        }
        if (!row[12].isEmpty()) {
            this.ConsumeMaterialNum = Integer.parseInt(row[12]);
        }
        if (!row[13].isEmpty()) {
            this.ConsumeTime = Integer.parseInt(row[13]);
        }
        if (!row[14].isEmpty()) {
            this.Act = Integer.parseInt(row[14]);
        }
        if (!row[15].isEmpty()) {
            this.Hp = Integer.parseInt(row[15]);
        }
        if (!row[16].isEmpty()) {
            this.BombLoad = Integer.parseInt(row[16]);
        }
        if (!row[17].isEmpty()) {
            this.Hurt = Integer.parseInt(row[17]);
        }
        if (!row[18].isEmpty()) {
            this.Duration = Float.parseFloat(row[18]);
        }
        if (!row[19].isEmpty()) {
            this.TriggerInterval = Float.parseFloat(row[19]);
        }
        if (!row[20].isEmpty()) {
            this.SearchScope = Float.parseFloat(row[20]);
        }
        if (!row[21].isEmpty()) {
            this.AtkFrequency = Float.parseFloat(row[21]);
        }
        if (!row[22].isEmpty()) {
            this.AtkRange = Float.parseFloat(row[22]);
        }
        if (!row[23].isEmpty()) {
            this.MovingSpeed = Float.parseFloat(row[23]);
        }
    }

    public static void loadFromFile(String filepath)
    {
        String[] lines = AutogenConfigManager.readFileToTextLines(filepath);
        data_ = new ArrayList<SoldierPropertyDefine>();
        for(String line : lines)
        {
            if (line.isEmpty())
                continue;
            String[] row = line.split("\\,", -1);
            SoldierPropertyDefine obj = new SoldierPropertyDefine();
            obj.parseFromRow(row);
            data_.add(obj);
         }
    }

    // get an item by key
    public static SoldierPropertyDefine getItemBy(String Name, int Level)
    {
        for (SoldierPropertyDefine item : data_)
        {
            if (item.Name.equals(Name) && item.Level == Level)
            {
                return item;
            }
        }
        return null;
    }

    // get a range of items by key
    public static ArrayList<SoldierPropertyDefine> getRange(String Name)
    {
        ArrayList<SoldierPropertyDefine> range = new ArrayList<SoldierPropertyDefine>();
        for (SoldierPropertyDefine item : data_)
        {
            if (item.Name.equals(Name))
            {
                range.add(item);
            }
        }
        return range;
    }

}
