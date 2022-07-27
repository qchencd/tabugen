// This file is auto-generated by Tabular v0.9.1, DO NOT EDIT!
package config

import (
	"bytes"
	"encoding/csv"
	"io"
	"log"
	"math"
	"strconv"
)

func parseBool(s string) bool {
	switch len(s) {
	case 0:
		return false
	case 1:
		return s[0] == '1' || s[0] == 'y' || s[0] == 'Y'
	case 2:
		return s == "on" || s == "ON"
	case 3:
		return s == "yes" || s == "YES"
	default:
		b, err := strconv.ParseBool(s)
		if err != nil {
			log.Panicf("parseBool: cannot pasre %s to boolean: %v", s, err)
		}
		return b
	}
}

func parseI8(s string) int8 {
	var n = parseI32(s)
	if n > math.MaxInt8 || n < math.MinInt8 {
		log.Panicf("parseI8: value %s out of range", s)
	}
	return int8(n)
}

func parseU8(s string) uint8 {
	var n = parseU32(s)
	if n > math.MaxUint8 || n < 0 {
		log.Panicf("parseU8: value %s out of range", s)
	}
	return uint8(n)
}

func parseI16(s string) int16 {
	var n = parseI32(s)
	if n > math.MaxInt16 || n < math.MinInt16 {
		log.Panicf("parseI16: value %s out of range", s)
	}
	return int16(n)
}

func parseU16(s string) uint16 {
	var n = parseU32(s)
	if n > math.MaxUint16 || n < 0 {
		log.Panicf("parseU16: value %s out of range", s)
	}
	return uint16(n)
}

func parseI32(s string) int32 {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseInt(s, 10, 32)
	if err != nil {
		log.Panicf("parseI32: cannot parse [%s] to int32: %v", s, err)
	}
	return int32(n)
}

func parseU32(s string) uint32 {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseUint(s, 10, 32)
	if err != nil {
		log.Panicf("parseU32: cannot parse [%s] to uint32: %v", s, err)
	}
	return uint32(n)
}

func parseInt(s string) int {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		log.Panicf("parseU32: cannot parse [%s] to int: %v", s, err)
	}
	return int(n)
}

func parseUint(s string) uint {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseUint(s, 10, 64)
	if err != nil {
		log.Panicf("parseU32: cannot parse [%s] to int: %v", s, err)
	}
	return uint(n)
}

func parseI64(s string) int64 {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil {
		log.Panicf("parseI64: cannot parse [%s] to int64: %v", s, err)
	}
	return n
}

func parseU64(s string) uint64 {
	if s == "" {
		return 0
	}
	n, err := strconv.ParseUint(s, 10, 64)
	if err != nil {
		log.Panicf("parseU64: cannot parse [%s] to uint64: %v", s, err)
	}
	return n
}

func parseF32(s string) float32 {
	if s == "" {
		return 0
	}
	f, err := strconv.ParseFloat(s, 32)
	if err != nil {
		log.Panicf("parseF32: cannot parse [%s] to double: %v", s, err)
	}
	return float32(f)
}

func parseF64(s string) float64 {
	if s == "" {
		return 0
	}
	f, err := strconv.ParseFloat(s, 64)
	if err != nil {
		log.Panicf("parseF64: cannot parse [%s] to double: %v", s, err)
	}
	return f
}

type StructuredConfig interface {
	ParseFromRow(row []string) error
}

// ReadCSVRecords read CSV data to key-value record list
func ReadCSVRecords(data []byte) ([]map[string]string, error) {
	var records []map[string]string
	var header []string
	var r = csv.NewReader(bytes.NewReader(data))
	for i := 0; ; i++ {
		row, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Printf("ReadCSVRecords: read csv %v", err)
			return nil, err
		}
		if i == 0 {
			header = row
			continue
		}
		var record = make(map[string]string)
		for j, s := range row {
			record[header[j]] = s
		}
		records = append(records, record)
	}
	return records, nil
}

// RecordsToKVMap parse records to key-value string map
func RecordsToKVMap(records []map[string]string) map[string]string {
	var fields = make(map[string]string)
	for _, rec := range records {
		fields[rec["Key"]] = rec["Value"]
	}
	return fields
}



const (
	TABUGEN_SEP_DELIM1  = `|` // map item delimiter
	TABUGEN_SEP_DELIM2  = `=` // map key-value delimiter
)

