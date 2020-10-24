// This file is auto-generated by TAKSi v1.3.0, DO NOT EDIT!

#include "AutogenConfig.h"
#include <stddef.h>
#include <assert.h>
#include <memory>
#include <fstream>
#include "Utility/Conv.h"
#include "Utility/StringUtil.h"
#include "Utility/CSVReader.h"

using namespace std;

#ifndef ASSERT
#define ASSERT assert
#endif


static const char TAKSI_CSV_SEP = ',';
static const char TAKSI_CSV_QUOTE = '"';
static const char* TAKSI_ARRAY_DELIM = ",";
static const char* TAKSI_MAP_DELIM1 = ";";
static const char* TAKSI_MAP_DELIM2 = "=";

namespace config
{

std::function<std::string(const char*)> AutogenConfigManager::reader = AutogenConfigManager::ReadFileContent;

namespace 
{
    static GlobalPropertyDefine* _instance_globalpropertydefine = nullptr;
}

void AutogenConfigManager::LoadAll()
{
    ASSERT(reader);
    GlobalPropertyDefine::Load("global_property_define.csv");
}

void AutogenConfigManager::ClearAll()
{
    delete _instance_globalpropertydefine;
    _instance_globalpropertydefine = nullptr;
}


//Load content of an asset file'
std::string AutogenConfigManager::ReadFileContent(const char* filepath)
{
    ASSERT(filepath != nullptr);
    FILE* fp = std::fopen(filepath, "rb");
    if (fp == NULL) {
        return "";
    }
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (size == 0) {
        fclose(fp);
        return "";
    }
    std::string content;
    fread(&content[0], 1, size, fp);
    fclose(fp);
    return std::move(content);
}

const GlobalPropertyDefine* GlobalPropertyDefine::Instance()
{
    ASSERT(_instance_globalpropertydefine != nullptr);
    return _instance_globalpropertydefine;
}

// load GlobalPropertyDefine data from csv file
int GlobalPropertyDefine::Load(const char* filepath)
{
    std::string content = AutogenConfigManager::reader(filepath);
    CSVReader reader(TAKSI_CSV_SEP, TAKSI_CSV_QUOTE);
    reader.Parse(content);
    auto rows = reader.GetRows();
    ASSERT(!rows.empty());
    for (auto& row : rows)
    {
        if (!row.empty())
        {
            rows.push_back(row);
        }
    }
    GlobalPropertyDefine* dataptr = new GlobalPropertyDefine();
    GlobalPropertyDefine::ParseFromRows(rows, dataptr);
    delete _instance_globalpropertydefine;
    _instance_globalpropertydefine = dataptr;
    return 0;
}

// parse data object from csv rows
int GlobalPropertyDefine::ParseFromRows(const vector<vector<StringPiece>>& rows, GlobalPropertyDefine* ptr)
{
    ASSERT(rows.size() >= 12 && rows[0].size() >= 3);
    ASSERT(ptr != nullptr);
    ptr->GoldExchangeTimeFactor1 = ParseTextAs<double>(rows[0][3]);
    ptr->GoldExchangeTimeFactor2 = ParseTextAs<double>(rows[1][3]);
    ptr->GoldExchangeTimeFactor3 = ParseTextAs<double>(rows[2][3]);
    ptr->GoldExchangeResource1Price = ParseTextAs<uint16_t>(rows[3][3]);
    ptr->GoldExchangeResource2Price = ParseTextAs<uint16_t>(rows[4][3]);
    ptr->GoldExchangeResource3Price = ParseTextAs<uint16_t>(rows[5][3]);
    ptr->GoldExchangeResource4Price = ParseTextAs<uint16_t>(rows[6][3]);
    ptr->FreeCompleteSeconds = ParseTextAs<uint16_t>(rows[7][3]);
    ptr->CancelBuildReturnPercent = ParseTextAs<uint16_t>(rows[8][3]);
    ptr->EnableSearch = ParseTextAs<bool>(rows[9][3]);
    {
        const auto& array = Split(rows[10][3], TAKSI_ARRAY_DELIM, true);
        for (size_t i = 0; i < array.size(); i++)
        {
            ptr->SpawnLevelLimit.push_back(ParseTextAs<int>(array[i]));
        }
    }
    {
        const auto& dict = Split(rows[11][3], TAKSI_MAP_DELIM1, true);
        for (size_t i = 0; i < dict.size(); i++)
        {
            const auto& kv = Split(dict[i], TAKSI_MAP_DELIM2, true);
            ASSERT(kv.size() == 2);
            if(kv.size() == 2)
            {
                const auto& key = ParseTextAs<std::string>(kv[0]);
                ASSERT(ptr->FirstRechargeReward.count(key) == 0);
                ptr->FirstRechargeReward[key] = ParseTextAs<int>(kv[1]);
            }
        }
    }
    return 0;
}


} // namespace config 
