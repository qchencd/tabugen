// This file is auto-generated by TAKSi v1.3.0, DO NOT EDIT!

#pragma once

#include <stdint.h>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include "Utility/Range.h"


namespace config
{

class AutogenConfigManager
{
public:

    // Load all configurations
    static void LoadAll();

    // Clear all configurations
    static void ClearAll();

    // Read content from an asset file
    static std::string ReadFileContent(const char* filepath);

    // default loader
    static std::function<std::string(const char*)> reader;
};

// 新手引导配置
struct NewbieGuideDefine 
{
    std::string                      Name;                  // ID
    std::string                      Type;                  // 任务类型
    std::string                      Target;                // 目标
    std::vector<int16_t>             Accomplishment;        // 完成步骤
    std::map<std::string, uint32_t>  Goods;                 // 物品
    std::string                      Description;           // 描述

    static int Load(const char* filepath);
    static int ParseFromRow(const std::vector<StringPiece>& row, NewbieGuideDefine* ptr);
    static const std::vector<NewbieGuideDefine>* GetData(); 
};

} // namespace config
