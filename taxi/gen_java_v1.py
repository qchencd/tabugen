# Copyright (C) 2018-present ichenq@outlook.com. All rights reserved.
# Distributed under the terms and conditions of the Apache License.
# See accompanying files LICENSE.

import os
import codecs
import basegen
import predef
import descriptor
import lang
import util


JAVA_CLASS_TEMPLATE = """

import java.io.*;
import java.util.*;
import java.util.function.Function;

public class %s {

    // parse text to boolean value
    public static boolean parseBool(String text) {
        if (!text.isEmpty()) {
            return text.equals("1") ||
                    text.equalsIgnoreCase("on") ||
                    text.equalsIgnoreCase("yes")  ||
                    text.equalsIgnoreCase("true");
        }
        return false;
    }

    public static String readFileContent(String filepath) {
        StringBuilder sb = new StringBuilder();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filepath));
            String line = null;
            while ((line = reader.readLine()) != null) {
                sb.append(line);
                sb.append('\\n'); // line break
            }
            reader.close();
        } catch(IOException ex) {
            System.err.println(ex.getMessage());
        }
        return sb.toString();
    }
    
    // you can use your own file reader
    public static Function<String, String> reader;
    
    public static String[] readFileToTextLines(String filename) {
        if (reader == null) {
            reader = (filepath)-> readFileContent(filepath);
        }
        String content = reader.apply(filename);
        return content.split("\\n", -1);
    }    

"""

# java生成器
class JavaV1Generator(basegen.CodeGeneratorBase):
    TAB_SPACE = '    '

    def __init__(self):
        pass

    @staticmethod
    def name():
        return "java-v1"

    def get_instance_data_name(self, name):
        return '_instance_%s' % name.lower()

    #
    def gen_java_inner_class(self, struct, inner_fields):
        content = ''
        class_name = struct["options"][predef.PredefInnerTypeClass]
        content += '    public class %s \n' % class_name
        content += '    {\n'
        max_name_len = util.max_field_length(inner_fields, 'name', None)
        max_type_len = util.max_field_length(inner_fields, 'original_type_name', lang.map_java_type)
        for field in inner_fields:
            typename = lang.map_java_type(field['original_type_name'])
            assert typename != "", field['original_type_name']
            typename = util.pad_spaces(typename, max_type_len + 1)
            name = lang.name_with_default_java_value(field, typename)
            name = util.pad_spaces(name, max_name_len + 8)
            content += '        public %s %s // %s\n' % (typename.strip(), name, field['comment'])
        content += '    };\n\n'
        return content

    def gen_java_class(self, struct):
        content = ''

        fields = struct['fields']
        if struct['options'][predef.PredefParseKVMode]:
            fields = self.get_struct_kv_fields(struct)

        content += '// %s\n' % struct['comment']
        content += 'public class %s\n{\n' % struct['name']

        inner_class_done = False
        inner_typename = ''
        inner_var_name = ''
        inner_field_names, inner_fields = self.get_inner_class_fields(struct)
        if len(inner_fields) > 0:
            content += self.gen_java_inner_class(struct, inner_fields)
            inner_type_class = struct["options"][predef.PredefInnerTypeClass]
            inner_var_name = struct["options"][predef.PredefInnerTypeName]
            inner_typename = 'ArrayList<%s>' % inner_type_class

        vec_done = False
        vec_names, vec_name = self.get_vec_field_range(struct)

        max_name_len = util.max_field_length(fields, 'name', None)
        max_type_len = util.max_field_length(fields, 'original_type_name', lang.map_java_type)
        if len(inner_typename) > max_type_len:
            max_type_len = len(inner_typename)

        for field in fields:
            field_name = field['name']
            if field_name in inner_field_names:
                if not inner_class_done:
                    typename = util.pad_spaces(inner_typename, max_type_len)
                    content += '    public %s %s = new %s(); \n' % (typename, inner_var_name, typename)
                    inner_class_done = True
            else:
                typename = lang.map_java_type(field['original_type_name'])
                assert typename != "", field['original_type_name']
                typename = util.pad_spaces(typename, max_type_len + 1)
                if field['name'] not in vec_names:
                    name = lang.name_with_default_java_value(field, typename)
                    name = util.pad_spaces(name, max_name_len + 8)
                    content += '    public %s %s // %s\n' % (typename, name, field['comment'])
                elif not vec_done:
                    name = '%s = new %s[%d];' % (vec_name, typename.strip(), len(vec_names))
                    name = util.pad_spaces(name, max_name_len + 8)
                    content += '    public %s[] %s // %s\n' % (typename.strip(), name, field['comment'])
                    vec_done = True

        return content

    # 静态变量
    def gen_static_data(self, struct):
        content = '\n'
        if struct['options'][predef.PredefParseKVMode]:
            content += '    private static %s instance_;\n' % struct['name']
            content += '    public static %s getInstance() { return instance_; }\n\n' % struct['name']
        else:
            content += '    private static ArrayList<%s> data_;\n' % struct['name']
            content += '    public static ArrayList<%s> getData() { return data_; } \n\n' % struct['name']
        return content

    # 生成赋值方法
    def gen_field_assgin_stmt(self, name, typename, valuetext, tabs):
        content = ''
        space = self.TAB_SPACE * tabs
        if typename.lower() == 'string':
            content += '%s%s = %s.trim();\n' % (space, name, valuetext)
        elif typename.lower().find('bool') >= 0:
            content += '%s%s = Boolean.parseBoolean(%s);\n' % (space, name, valuetext)
        else:
            table = {
                'byte': 'Byte.parseByte(%s)',
                'short': 'Short.parseShort(%s)',
                'int': 'Integer.parseInt(%s)',
                'long': 'Long.parseLong(%s)',
                'float': 'Float.parseFloat(%s)',
                'double': 'Double.parseDouble(%s)'
            }
            line = table[typename] % valuetext
            content += '%s%s = %s;\n' % (space, name, line)
        return content

    # 生成array赋值
    def gen_field_array_assign_stmt(self, prefix, typename, name, row_name, array_delim, tabs):
        assert len(array_delim) == 1
        array_delim = array_delim.strip()
        if array_delim == '\\':
            array_delim = '\\\\'

        content = ''
        space = self.TAB_SPACE * tabs
        elem_type = descriptor.array_element_type(typename)
        elem_type = lang.map_java_type(elem_type)
        content += '%sString[] tokens = %s.split("\\\\%s");\n' % (space, row_name, array_delim)
        content += '%s%s[] list = new %s[tokens.length];\n' % (space, elem_type, elem_type)
        content += '%sfor (int i = 0; i < tokens.length; i++) {\n' % space
        content += '%s    if (!tokens[i].isEmpty()) {\n' % (self.TAB_SPACE * tabs)
        varname = '%s value' % elem_type
        content += self.gen_field_assgin_stmt(varname, elem_type, 'tokens[i]', tabs + 2)
        content += '%s        list[i] = value;\n' % (self.TAB_SPACE * tabs)
        content += '%s    }\n' % (self.TAB_SPACE * tabs)
        content += '%s}\n' % space
        content += '%s%s%s = list;\n' % (space, prefix, name)
        return content

        # 生成map赋值
    def gen_field_map_assign_stmt(self, prefix, typename, name, row_name, map_delims, tabs):
        assert len(map_delims) == 2, map_delims
        delim1 = map_delims[0].strip()
        if delim1 == '\\':
            delim1 = '\\\\'
        delim2 = map_delims[1].strip()
        if delim2 == '\\':
            delim2 = '\\\\'

        space = self.TAB_SPACE * tabs
        k, v = descriptor.map_key_value_types(typename)
        key_type = lang.map_java_type(k)
        val_type = lang.map_java_type(v)

        content = '%sString[] tokens = %s.split("\\\\%s");\n' % (space, row_name, delim1)
        content += '%sfor(int i = 0; i < tokens.length; i++) {\n' % space
        content += '%s    String text = tokens[i];\n' % space
        content += '%s    if (text.isEmpty()) {\n' % space
        content += '%s        continue;\n' % space
        content += '%s    }\n' % space
        content += '%s    String[] item = text.split("\\\\%s");\n' % (space, delim2)
        prefix1 = '%s key' % key_type
        prefix2 = '%s value' % val_type
        content += self.gen_field_assgin_stmt(prefix1, key_type, 'item[0]', tabs + 1)
        content += self.gen_field_assgin_stmt(prefix2, val_type, 'item[1]', tabs + 1)
        content += '%s    %s%s.put(key, value);\n' % (space, prefix, name)
        content += '%s}\n' % space
        return content

    # 生成内部类的parse
    def gen_java_inner_class_assign(self, struct, prefix, inner_fields):
        content = ''
        inner_class_type = struct["options"][predef.PredefInnerTypeClass]
        inner_var_name = struct["options"][predef.PredefInnerTypeName]
        start, end, step = self.get_inner_class_range(struct)
        assert start > 0 and end > 0 and step > 1
        content += '        for (int i = %s; i < %s; i += %s) \n' % (start, end, step)
        content += '        {\n'
        content += '            %s item = new %s();\n' % (inner_class_type, inner_class_type)
        for n in range(step):
            field = inner_fields[n]
            origin_type = field['original_type_name']
            typename = lang.map_java_type(origin_type)
            valuetext = 'row[i + %d]' % n
            content += '            if (!row[i + %d].isEmpty()) \n' % n
            content += '            {\n'
            content += self.gen_field_assgin_stmt("item." + field['name'], typename, valuetext, 4)
            content += '            }\n'
        content += '            %s%s.add(item);\n' % (prefix, inner_var_name)
        content += '        }\n'
        return content

    # 生成KV模式的Parse方法
    def gen_kv_parse_method(self, struct):
        rows = struct['data-rows']
        keycol = struct['options'][predef.PredefKeyColumn]
        valcol = struct['options'][predef.PredefValueColumn]
        typcol = int(struct['options'][predef.PredefValueTypeColumn])
        assert keycol > 0 and valcol > 0 and typcol > 0

        keyidx, keyfield = self.get_field_by_column_index(struct, keycol)
        validx, valfield = self.get_field_by_column_index(struct, valcol)
        typeidx, typefield = self.get_field_by_column_index(struct, typcol)

        array_delim = struct['options'].get(predef.OptionArrayDelimeter, predef.DefaultArrayDelimiter)
        map_delims = struct['options'].get(predef.OptionMapDelimeters, predef.DefaultMapDelimiters)

        content = ''
        content += '%s// parse fields data from text rows\n' % self.TAB_SPACE
        content += '%spublic void parseFromRows(String[][] rows)\n' % self.TAB_SPACE
        content += '%s{\n' % self.TAB_SPACE
        content += '%s    if (rows.length < %d) {\n' % (self.TAB_SPACE, len(rows))
        content += '%s        throw new RuntimeException(String.format("%s: row length out of index, %%d < %d", rows.length));\n' % (
            self.TAB_SPACE, struct['name'], len(rows))
        content += '%s}\n' % (self.TAB_SPACE * 2)

        idx = 0
        for row in rows:
            name = rows[idx][keyidx].strip()
            name = util.camel_case(name)
            origin_typename = rows[idx][typeidx].strip()
            typename = lang.map_java_type(origin_typename)
            valuetext = 'rows[%d][%d]' % (idx, validx)
            # print('kv', name, origin_typename, valuetext)
            if origin_typename.startswith('array'):
                content += '%s{\n' % (self.TAB_SPACE * 2)
                content += self.gen_field_array_assign_stmt('this.', origin_typename, name, valuetext, array_delim, 3)
                content += '%s}\n' % (self.TAB_SPACE * 2)
            elif origin_typename.startswith('map'):
                content += '%s{\n' % (self.TAB_SPACE * 2)
                content += self.gen_field_map_assign_stmt('this.', origin_typename, name, valuetext, map_delims, 3)
                content += '%s}\n' % (self.TAB_SPACE * 2)
            else:
                content += '%sif (!rows[%d][%d].isEmpty()) {\n' % (self.TAB_SPACE * 2, idx, validx)
                content += self.gen_field_assgin_stmt('this.' + name, typename, valuetext, 3)
                content += '%s}\n' % (self.TAB_SPACE * 2)
            idx += 1
        content += '%s}\n\n' % self.TAB_SPACE
        return content

    # 生成ParseFromRow方法
    def gen_parse_method(self, struct):
        content = ''
        if struct['options'][predef.PredefParseKVMode]:
            return self.gen_kv_parse_method(struct)

        array_delim = struct['options'].get(predef.OptionArrayDelimeter, predef.DefaultArrayDelimiter)
        map_delims = struct['options'].get(predef.OptionMapDelimeters, predef.DefaultMapDelimiters)

        vec_idx = 0
        vec_names, vec_name = self.get_vec_field_range(struct)

        inner_class_done = False
        inner_field_names, inner_fields = self.get_inner_class_fields(struct)

        content += '%s// parse fields data from text row\n' % self.TAB_SPACE
        content += '%spublic void parseFromRow(String[] row)\n' % self.TAB_SPACE
        content += '%s{\n' % self.TAB_SPACE
        content += '%sif (row.length < %d) {\n' % (self.TAB_SPACE * 2, len(struct['fields']))
        content += '%sthrow new RuntimeException(String.format("%s: row length out of index %%d", row.length));\n' % (
        self.TAB_SPACE * 3, struct['name'])
        content += '%s}\n' % (self.TAB_SPACE * 2)

        idx = 0
        prefix = 'this.'
        for field in struct['fields']:
            field_name = field['name']
            if field_name in inner_field_names:
                if not inner_class_done:
                    inner_class_done = True
                    content += self.gen_java_inner_class_assign(struct, prefix, inner_fields)
            else:
                origin_type_name = field['original_type_name']
                typename = lang.map_java_type(origin_type_name)
                valuetext = 'row[%d]' % idx
                if origin_type_name.startswith('array'):
                    content += '%s{\n' % (self.TAB_SPACE * 2)
                    content += self.gen_field_array_assign_stmt(prefix, origin_type_name, field_name, valuetext, array_delim, 3)
                    content += '%s}\n' % (self.TAB_SPACE * 2)
                elif origin_type_name.startswith('map'):
                    content += '%s{\n' % (self.TAB_SPACE * 2)
                    content += self.gen_field_map_assign_stmt(prefix, origin_type_name, field_name, valuetext, map_delims, 3)
                    content += '%s}\n' % (self.TAB_SPACE * 2)
                else:
                    content += '%sif (!row[%d].isEmpty()) {\n' % (self.TAB_SPACE * 2, idx)
                    if field_name in vec_names:
                        name = '%s[%d]' % (vec_name, vec_idx)
                        content += self.gen_field_assgin_stmt(prefix+name, typename, valuetext, 3)
                        vec_idx += 1
                    else:
                        content += self.gen_field_assgin_stmt(prefix+field_name, typename, valuetext, 3)
                    content += '%s}\n' % (self.TAB_SPACE*2)
            idx += 1
        content += '%s}\n\n' % self.TAB_SPACE
        return content

    # 生成内部类的parse
    def gen_inner_class_assign(self, struct, prefix, inner_fields):
        content = ''
        inner_class_type = struct["options"][predef.PredefInnerTypeClass]
        inner_var_name = struct["options"][predef.PredefInnerTypeName]
        start, end, step = self.get_inner_class_range(struct)
        assert start > 0 and end > 0 and step > 1
        content += '        for (int i = %s; i < %s; i += %s) \n' % (start, end, step)
        content += '        {\n'
        content += '            %s item = new %s();\n' % (inner_class_type, inner_class_type)
        for n in range(step):
            field = inner_fields[n]
            origin_type = field['original_type_name']
            typename = lang.map_java_type(origin_type)
            valuetext = 'row[i + %d]' % n
            content += '            if (!row[i + %d].isEmpty()) \n' % n
            content += '            {\n'
            content += self.gen_field_assgin_stmt("item." + field['name'], typename, valuetext, 4)
            content += '            }\n'
        content += '            %s%s.add(item);\n' % (prefix, inner_var_name)
        content += '        }\n'
        return content

    # KV模式的load
    def gen_kv_struct_load_method(self, struct):
        rows = struct['data-rows']
        keycol = struct['options'][predef.PredefKeyColumn]
        valcol = struct['options'][predef.PredefValueColumn]
        typcol = int(struct['options'][predef.PredefValueTypeColumn])
        assert keycol > 0 and valcol > 0 and typcol > 0

        content = '%spublic static void loadFromFile(String filepath)\n' % self.TAB_SPACE
        content += '%s{\n' % self.TAB_SPACE
        content += '%s    String[] lines = %s.readFileToTextLines(filepath);\n' % (self.TAB_SPACE, util.config_manager_name)
        content += '%s    String[][] rows = new String[lines.length][];\n' % self.TAB_SPACE
        content += '%s    for(int i = 0; i < lines.length; i++)\n' % self.TAB_SPACE
        content += '%s    {\n' % self.TAB_SPACE
        content += '%s        String line = lines[i];\n' % self.TAB_SPACE
        content += '%s        rows[i] = line.split("\\\\,", -1);\n' % self.TAB_SPACE
        content += '%s    }\n' % self.TAB_SPACE
        content += '%s    instance_ = new %s();\n' % (self.TAB_SPACE, struct['name'])
        content += '%s    instance_.parseFromRows(rows);\n' % self.TAB_SPACE
        content += '%s}\n\n' % self.TAB_SPACE
        return content

    # 生成Load方法
    def gen_load_method(self, struct):
        if struct['options'][predef.PredefParseKVMode]:
            return self.gen_kv_struct_load_method(struct)

        content = ''
        content = '%spublic static void loadFromFile(String filepath)\n' % self.TAB_SPACE
        content += '%s{\n' % self.TAB_SPACE
        content += '%s    String[] lines = %s.readFileToTextLines(filepath);\n' % (self.TAB_SPACE, util.config_manager_name)
        content += '%s    data_ = new ArrayList<%s>();\n' % (self.TAB_SPACE, struct['name'])
        content += '%s    for(String line : lines)\n' % self.TAB_SPACE
        content += '%s    {\n' % self.TAB_SPACE
        content += '%s        if (line.isEmpty())\n' % self.TAB_SPACE
        content += '%s            continue;\n' % self.TAB_SPACE
        content += '%s        String[] row = line.split("\\\\,", -1);\n' % self.TAB_SPACE
        content += '%s        %s obj = new %s();\n' % (self.TAB_SPACE, struct['name'], struct['name'])
        content += "%s        obj.parseFromRow(row);\n" % self.TAB_SPACE
        content += "%s        data_.add(obj);\n" % self.TAB_SPACE
        content += '%s     }\n' % self.TAB_SPACE
        content += '%s}\n\n' % self.TAB_SPACE
        return content

    # 字段比较
    def gen_equal_stmt(self, prefix, struct, key):
        keys = self.get_struct_keys(struct, key, lang.map_java_type)
        args = []
        for tpl in keys:
            if lang.is_java_primitive_type(tpl[0]):
                args.append('%s%s == %s' % (prefix, tpl[1], tpl[1]))
            else:
                args.append('%s%s.equals(%s)' % (prefix, tpl[1], tpl[1]))
        return ' && '.join(args)

    # 生成getItemBy()方法
    def gen_get_method(self, struct):
        if struct['options'][predef.PredefParseKVMode]:
            return ''

        keys = self.get_struct_keys(struct, predef.PredefGetMethodKeys, lang.map_java_type)
        if len(keys) == 0:
            return ''

        formal_param = []
        arg_names = []
        for tpl in keys:
            typename = tpl[0]
            formal_param.append('%s %s' % (typename, tpl[1]))
            arg_names.append(tpl[1])

        content = ''
        content += '    // get an item by key\n'
        content += '    public static %s getItemBy(%s)\n' % (struct['name'], ', '.join(formal_param))
        content += '    {\n'
        content += '        for (%s item : data_)\n' % struct['name']
        content += '        {\n'
        content += '            if (%s)\n' % self.gen_equal_stmt('item.', struct, 'get-keys')
        content += '            {\n'
        content += '                return item;\n'
        content += '            }\n'
        content += '        }\n'
        content += '        return null;\n'
        content += '    }\n\n'
        return content

        # 生成getRange()方法
    def gen_range_method(self, struct):
        if struct['options'][predef.PredefParseKVMode]:
            return ''

        if predef.PredefRangeMethodKeys not in struct['options']:
            return ''

        keys = self.get_struct_keys(struct, predef.PredefRangeMethodKeys, lang.map_java_type)
        assert len(keys) > 0

        formal_param = []
        arg_names = []
        for tpl in keys:
            typename = tpl[0]
            formal_param.append('%s %s' % (typename, tpl[1]))
            arg_names.append(tpl[1])

        content = ''
        content += '    // get a range of items by key\n'
        content += '    public static ArrayList<%s> getRange(%s)\n' % (struct['name'], ', '.join(formal_param))
        content += '    {\n'
        content += '        ArrayList<%s> range = new ArrayList<%s>();\n' % (struct['name'], struct['name'])
        content += '        for (%s item : data_)\n' % struct['name']
        content += '        {\n'
        content += '            if (%s)\n' % self.gen_equal_stmt('item.', struct, 'range-keys')
        content += '            {\n'
        content += '                range.add(item);\n'
        content += '            }\n'
        content += '        }\n'
        content += '        return range;\n'
        content += '    }\n\n'
        return content

    # 生成对象及方法
    def generate_class(self, struct, params):
        content = '\n'
        content += self.gen_java_class(struct)
        content += self.gen_static_data(struct)
        content += self.gen_parse_method(struct)
        content += self.gen_load_method(struct)
        content += self.gen_get_method(struct)
        content += self.gen_range_method(struct)
        content += '}\n'
        return content

    def run(self, descriptors, args):
        params = util.parse_args(args)

        mgr_content = ''
        mgr_filename = '%s.java' % util.config_manager_name

        basedir = params.get(predef.OptionOutSourceFile, '.')
        print(basedir)
        if 'pkg' in params:
            package = params['pkg']
            names = [basedir] + package.split('.')
            basedir = '/'.join(names)
            mgr_content = 'package %s;' % package
            mgr_filename = '%s/%s' % (basedir, mgr_filename)
            try:
                print('make dir', basedir)
                os.makedirs(basedir)
            except Exception as e:
                # print(e)
                pass

        class_dict = {}
        mgr_content += JAVA_CLASS_TEMPLATE % util.config_manager_name
        load_func_content = '    public static void loadAllConfig() {\n'

        data_only = params.get(predef.OptionDataOnly, False)
        no_data = params.get(predef.OptionNoData, False)

        for struct in descriptors:
            print(util.current_time(), 'start generate', struct['source'])
            self.setup_comment(struct)
            self.setup_key_value_mode(struct)
            if not data_only:
                content = ''
                filename = '%s.java' % struct['camel_case_name']
                # print(filename)
                if 'pkg' in params:
                    filename = '%s/%s' % (basedir, filename)
                    content += 'package %s;\n\n' % params['pkg']
                content += 'import java.util.*;\n'
                content += '\n'
                content += self.generate_class(struct, params)
                class_dict[filename] = content

                load_func_content += '        %s.loadFromFile("%s.csv");\n' % (struct['name'], struct['name'].lower())

        load_func_content += '    }\n'
        mgr_content += load_func_content
        mgr_content += '}\n'
        class_dict[mgr_filename] = mgr_content

        if not data_only:
            for filename in class_dict:
                content = class_dict[filename]
                f = codecs.open(filename, 'w', 'utf-8')
                f.writelines(content)
                f.close()
                print('wrote source file to', filename)

        if not no_data or data_only:
            for struct in descriptors:
                self.write_data_rows(struct, params)
