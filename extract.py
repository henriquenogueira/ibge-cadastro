import os

from json import dumps

from data_spec import IBGE_ADDRESS_SPEC

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
JSON_DIR = os.path.join(BASE_DIR, 'json')


class LineFieldSpec:
    """
    Specifies how a line field should be parsed on a fixed-width
    file format.
    """
    def __init__(self, name, initial_position, length):

        if initial_position < 1:
            raise ValueError('Initial position must be equal or greater than 0')

        if length < 1:
            raise ValueError('Length must great than 0')

        self._initial_position = initial_position
        self._length = length
        self._name = name

    def __str__(self):
        return "<LineFieldSpec: '{}' [{}, {})>".format(self.name, self.start, self.end)

    @property
    def start(self):
        """
        Start of the slice for the current field
        """
        return self._initial_position - 1

    @property
    def end(self):
        """
        End of the slice for the current field
        """
        return self.start + self._length

    @property
    def name(self):
        """
        Returns the name of the field
        """
        return self._name

    def to_dic(self):
        """
        Extracts the field as a dictionary
        """
        return {self._name: (self.start, self.end)}


class LineSpec:
    """
    Keeps track of all fields expected for a line
    """
    def __init__(self, fields=[]):
        self._fields = fields

    def __len__(self):
        return len(self._fields)

    def __getitem__(self, item):
        return self._fields[item]

    def __iter__(self):
        return iter(self._fields)

    def append(self, e):
        """
        Adds a new field to the specification of the line
        """
        if type(e) is not LineFieldSpec:
            raise TypeError('A Line can only contain LineField values')
        self._fields.append(e.to_dict())

    def names(self):
        """
        Returns column names
        """
        return map(x.name for x in self._fields)

    def parse_line(self, line):
        """
        Parse a given line based on the fields specification
        for the current line
        """
        parsed_line = {}
        for idx, field in enumerate(self):
            parsed_line[field.name] = str.strip(line[field.start:field.end])
        return parsed_line

    def __str__(self):
        return '<Line: {} fields>'.format(len(self))


def main():

    # Settings line specification based on the IBGE format
    line = LineSpec(fields=[LineFieldSpec(*info) for info in IBGE_ADDRESS_SPEC])

    # Getting list of states
    states = [s for s in os.listdir(os.path.join(DATA_DIR)) if len(s) == 2 and s[0] != '.']

    # Triggering parsing process for each state
    for state in states:
        extract_state(line, state)


def extract_state(line, state):
    """
    Triggers parsing process for a given state
    """
    files = os.listdir(os.path.join(DATA_DIR, state))
    files = [f for f in files if '.json' not in f]
    for i, file in enumerate(files):
        print('State: {} - ({} / {})'.format(state, i + 1, len(files)), end=' ')
        extract_sector(file, line, state)


def extract_sector(file, line, state):
    """
    Browses all files for a given state
    """
    file_path = os.path.join(DATA_DIR, state, file)
    print('Processing file {}...'.format(file_path), end=' ')
    with open(file_path) as f:
        extract_file(f, file, line, state)
    print('Done!')


def extract_file(input_file, file, line, state):
    """
    For a given file, parses each line and create a
    JSON-formatted output file
    """
    sector_code = file.split('.')[0]
    json_filename = sector_code + '.json'
    o_file_path = os.path.join(JSON_DIR, json_filename)
    with open(o_file_path, 'w+') as o:
        process_line(input_file, line, o, sector_code, state)


def process_line(input_file, line, output_file, sector_code, state):
    try:
        for l in input_file:
            parsed = line.parse_line(l)
            json = {'line_data': parsed, 'state:': state, 'filename': sector_code}
            json_str = dumps(json)
            output_file.write(json_str + '\n')

    # Just keeping track of files that contain bizarre chars
    # (currently, there are three of them).
    except UnicodeError as e:
        with open(os.path.join(BASE_DIR, 'bad_files.txt'), 'a+') as m:
            m.write('-----------------------------------------------\n')
            m.write('{}/{}.TXT -- ({} - {}) {}:\n'.format(state, sector_code, e.start, e.end, e))
            m.write('{}\n'.format(l[e.start - 10:e.end + 10]))
    except Exception as e:
        with open(os.path.join(BASE_DIR, 'bad_files.txt'), 'a+') as m:
            m.write('-----------------------------------------------\n')
            m.write('{}/{}.TXT -- {}:\n'.format(state, sector_code, e))


if __name__ == '__main__':
    main()