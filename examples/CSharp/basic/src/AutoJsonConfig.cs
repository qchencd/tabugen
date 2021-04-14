// This file is auto-generated by Tabugen v0.5.0, DO NOT EDIT!

using System;
using System.Collections.Generic;

namespace Config2
{

// 兵种属性配置, 兵种.xlsx
public class SoldierPropertyDefine
{
    public string  Name = "";                 // 士兵ID
    public int     Level = 0;                 // 士兵等级
    public string  NameID = "";               // 名字
    public string  Description = "";          // 描述
    public string  BuildingName = "";         // 所属建筑
    public uint    BuildingLevel = 0;         // 建筑等级
    public uint    RequireSpace = 0;          // 登陆艇占用空间
    public uint    UpgradeTime = 0;           // 升级消耗的时间(秒）
    public string  UpgradeMaterialID = "";    // 升级消耗的材料
    public long    UpgradeMaterialNum = 0;    // 升级消耗的数量
    public string  ConsumeMaterial = "";      // 生产消耗的材料
    public int     ConsumeMaterialNum = 0;    // 生产消耗的数量
    public int     ConsumeTime = 0;           // 生产消耗的时间（秒/个）
    public int     Act = 0;                   // 攻击
    public int     Hp = 0;                    // 血量
    public short   BombLoad = 0;              // 载弹量
    public float   Duration = 0.0f;           // 持续时间
    public float   TriggerInterval = 0.0f;    // 触发间隔
    public short   SearchScope = 0;           // 搜索范围
    public float   AtkFrequency = 0.0f;       // 攻击间隔
    public double  AtkRange = 0.0f;           // 攻击距离
    public double  MovingSpeed = 0.0f;        // 移动速度
    public bool    EnableBurn = false;        // 燃烧特效
}


}
