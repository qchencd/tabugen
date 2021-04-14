// This file is auto-generated by Tabugen v0.5.0, DO NOT EDIT!

using System;
using System.Collections.Generic;

namespace Config
{

// 全局数值配置, 全局变量表.xlsx
public class GlobalPropertyDefine
{
    public double                   GoldExchangeTimeFactor1 = 0.0f;    // 金币兑换时间参数1
    public double                   GoldExchangeTimeFactor2 = 0.0f;    // 金币兑换时间参数2
    public double                   GoldExchangeTimeFactor3 = 0.0f;    // 金币兑换时间参数3
    public ushort                   GoldExchangeResource1Price = 0;    // 金币兑换资源1价格
    public ushort                   GoldExchangeResource2Price = 0;    // 金币兑换资源2价格
    public ushort                   GoldExchangeResource3Price = 0;    // 金币兑换资源3价格
    public ushort                   GoldExchangeResource4Price = 0;    // 金币兑换资源4价格
    public ushort                   FreeCompleteSeconds = 0;           // 免费立即完成时间
    public ushort                   CancelBuildReturnPercent = 0;      // 取消建造后返还资源比例
    public bool                     EnableSearch = false;              // 开启搜索
    public int[]                    SpawnLevelLimit = null;            // 最大刷新个数显示
    public Dictionary<string, int>  FirstRechargeReward = null;        // 首充奖励

    // parse object fields from text rows
    public void ParseFromRows(List<List<string>> rows)
    {
        if (rows.Count < 12) {
            throw new ArgumentException(string.Format("GlobalPropertyDefine: row length out of index, {0} < 12", rows.Count));
        }
        if (rows[0][2].Length > 0) {
            this.GoldExchangeTimeFactor1 = double.Parse(rows[0][2]);
        }
        if (rows[1][2].Length > 0) {
            this.GoldExchangeTimeFactor2 = double.Parse(rows[1][2]);
        }
        if (rows[2][2].Length > 0) {
            this.GoldExchangeTimeFactor3 = double.Parse(rows[2][2]);
        }
        if (rows[3][2].Length > 0) {
            this.GoldExchangeResource1Price = ushort.Parse(rows[3][2]);
        }
        if (rows[4][2].Length > 0) {
            this.GoldExchangeResource2Price = ushort.Parse(rows[4][2]);
        }
        if (rows[5][2].Length > 0) {
            this.GoldExchangeResource3Price = ushort.Parse(rows[5][2]);
        }
        if (rows[6][2].Length > 0) {
            this.GoldExchangeResource4Price = ushort.Parse(rows[6][2]);
        }
        if (rows[7][2].Length > 0) {
            this.FreeCompleteSeconds = ushort.Parse(rows[7][2]);
        }
        if (rows[8][2].Length > 0) {
            this.CancelBuildReturnPercent = ushort.Parse(rows[8][2]);
        }
        if (rows[9][2].Length > 0) {
            this.EnableSearch = AutogenConfigManager.ParseBool(rows[9][2]);
        }
        {
            var items = rows[10][2].Split(AutogenConfigManager.TABUGEN_ARRAY_DELIM, StringSplitOptions.RemoveEmptyEntries);
            this.SpawnLevelLimit = new int[items.Length];
            for(int i = 0; i < items.Length; i++) 
            {
                var value = int.Parse(items[i]);
                this.SpawnLevelLimit[i] = value;
            }
        }
        {
            var items = rows[11][2].Split(AutogenConfigManager.TABUGEN_MAP_DELIM1, StringSplitOptions.RemoveEmptyEntries);
            this.FirstRechargeReward = new Dictionary<string,int>();
            for(int i = 0; i < items.Length; i++) 
            {
                string text = items[i];
                if (text.Length == 0) {
                    continue;
                }
                var item = text.Split(AutogenConfigManager.TABUGEN_MAP_DELIM2, StringSplitOptions.RemoveEmptyEntries);
                if (items.Length == 2) {
                var key = item[0].Trim();
                var value = int.Parse(item[1]);
                    this.FirstRechargeReward[key] = value;
                }
            }
        }
    }
}


public class AutogenConfigManager 
{    
    public const char TABUGEN_CSV_SEP = ',';           // CSV field delimiter
    public const char TABUGEN_CSV_QUOTE = '"';          // CSV field quote
    public const char TABUGEN_ARRAY_DELIM = ',';       // array item delimiter
    public const char TABUGEN_MAP_DELIM1 = ';';        // map item delimiter
    public const char TABUGEN_MAP_DELIM2 = '=';        // map key-value delimiter
    
    // self-defined boolean value parse
    public static bool ParseBool(string text)
    {
        if (text == null || text.Length == 0) {
            return false;
        }
        return string.Equals(text, "1") ||
            string.Equals(text, "Y") || 
            string.Equals(text, "ON");
    }
}


}
