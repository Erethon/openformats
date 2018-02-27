from yaml import yaml

from openformats.formats.yaml import YamlHandler


class I18nYamlHandler(YamlHandler):
    name = "Yaml (Internationalization)"
    extension = ".yml"
    EXTRACTS_RAW = False

    lang_rules = []

    RULES = {
        0: 'zero',
        1: 'one',
        2: 'two',
        3: 'few',
        4: 'many',
        5: 'other'
    }

    def _compile_pluralized(self, string):
        plurals_dict = {
            self.RULES[rule]: self._wrap_in_quotes(translation).encode('utf-8')
            for rule, translation in string.string.items()
        }
        indentation_levels = string.key.count('.') + 1
        indent = " " * indentation_levels * 2
        yml_str = yaml.dump(plurals_dict, default_flow_style=False)
        return '\n'.join([
            "{indent}{line}".format(indent=indent, line=line)
            for line in yml_str.splitlines()
        ])

    def set_lang_rules(self, language_code, lang_rules):
        self.language = language_code
        self.lang_rules = [self.RULES[r] for r in lang_rules]

    def is_pluralized(self, val):
        if not isinstance(val, dict):
            return False
        if sorted(val.keys()) == sorted(self.lang_rules):
            return True
        return False

    def set_plural_rules(self, plural_rules):
        self.plural_rules = plural_rules

    def parse_pluralized_value(self, value):
        rules = {val: key for key, val in self.RULES.iteritems()}
        return {rules[key]: val[0] for key, val in value.iteritems()}

    def get_yaml_data_to_parse_and_root_key(self, yaml_data):
        try:
            keys = yaml_data.keys()
        except AttributeError:
            return yaml_data
        else:
            return yaml_data[keys[0]][0]
