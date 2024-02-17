import pandas as pd
from ast import literal_eval

if __name__ == "__main__":
    from common import Entry, NaN
else:
    from .common import Entry, NaN


class Read():
    FIRST_CHAR2TYPES = {
        '[': list,
        '"': str,
        "'": str,
    }

    LIST_CAST_TYPES = {
        (int, float): float,
        (float, int): float
    }


    def __init__(self, is_onelist=False, tgt_parent=None):
        self.is_onelist = is_onelist
        self.tgt_parent = tgt_parent
        
        #init read
        self.out = None
        self.current_parent = None
        self.list_counter = 0
        self.yaml_obj = dict()
        self.yaml_obj_types = dict()
        self.all_types = dict()
        self.list_counter = 0
        self.block_seq_len = 0
        self.is_mini_data = False
        self.columns = {}
        self.is_data_1straw = False

        #line state
        self.key = None
        self.value = None
        self.is_parent = False
        self.is_child = False
        self.is_entry_minus = False
        self.is_double_minus = False
        self.is_multiline_obj_parsing_done = False
        self.is_parent_value = False
        self.is_obj_still_parsing = False
        self.is_2ndimen_parsing = False
    
    @classmethod
    def _ylist_type_cast(cls, old_types, new_types):
        def c(fromto):
            from_type, to_type = fromto
            if to_type is None or from_type is None:
                return from_type if from_type else to_type

            if from_type == to_type:
                return from_type
            else:
                new_type =  cls.LIST_CAST_TYPES.get(fromto, False)
                if not new_type:
                    raise Exception(f'List type error, tyring to cast {from_type} to {to_type}')
                return new_type
        
        return map(c, zip(old_types.values(), new_types.values()))

    @classmethod
    def infer_type(cls, value):
        ytype = cls.FIRST_CHAR2TYPES.get(value[0], False)
        if not ytype:
            if value == NaN:
                ytype = None
            else:
                ytype = float if '.' in value else int
        return ytype

    def _reset(self):
        #reset and skip
        if self.is_parent:
            if self.is_onelist and self.list_counter:
                raise Exception("You specified a one list('-') yaml2d file but a key was found after parsing the list")
            else:
                self.current_parent = self.key
            #TODO onelist is the default
            #self.list_counter = 0
            
        if self.is_multiline_obj_parsing_done:
            self.yaml_obj = dict()
            self.yaml_obj_types = dict()
            


    def process_line(self, line):
        striped_line = line.strip()
        if not striped_line:
            return True

        self.is_child = line[0].isspace()
        self.is_parent = not self.is_child
        line = striped_line

        keyvalue = line.strip().split(':', 1)
        if len(keyvalue) == 1:
            is_colon = False
            self.key, self.value =  keyvalue[0], None
        else:
            #note: relying on `len(':'.split(':')) == 2`
            is_colon = True
            self.key, self.value = keyvalue
            self.key, self.value = self.key.strip(), self.value.strip()
        
        
        self.is_parent_value = self.is_parent and self.value

        minus_counter = self.key[0] == '-'
        if minus_counter:
            self.key = self.key[1:].strip()
            minus_counter +=  self.key[0] == '-'
            if minus_counter > 1:
                self.key = self.key[1:].strip()

            
        if minus_counter > 1:
            self.is_mini_data = True
            
        self.is_double_minus = minus_counter == 2
        self.is_entry_minus = self.is_double_minus or \
                            (minus_counter == 1 and \
                             not self.is_mini_data)

        self.is_multiline_obj_parsing_done = (self.is_parent or self.is_entry_minus) and bool(self.yaml_obj)
        self.list_counter += self.is_entry_minus
        self.is_data_1straw = self.list_counter == 1

        if self.is_double_minus:
            self.block_seq_len = 0
        if self.block_seq_len or self.is_double_minus:
            self.block_seq_len += 1
            if self.is_data_1straw and is_colon:
                self.columns[self.block_seq_len - 1] = self.key
                return True
            else:
                self.value = self.key
                try:
                    self.key = self.columns[self.block_seq_len - 1]
                except KeyError as e:
                    raise Exception('Probably violated fixed set of features: ' + str(e)) from e

        
        #states
        if self.is_child:
            self.is_obj_still_parsing = True
        if self.is_parent:
            self.is_obj_still_parsing = False

        if self.is_obj_still_parsing:
            self.is_2ndimen_parsing = True
        if self.is_parent:
            self.is_2ndimen_parsing = False
        
        
    def parsing_obj(self):
        #record current line if not parent
        #if self.is_data_1straw and \
        #self.is_mini_data and \
        #self.columns:
        #    #was filling column names
        #    return False

        self.yaml_obj[self.key] = self.value
        ytype = self.infer_type(self.value)        
        self.yaml_obj_types[self.key] = ytype


    def read_obj(self):
        if self.list_counter and self.current_parent in self.all_types:
            new_obj_types = self.all_types[self.current_parent]
            new_obj_types = self._ylist_type_cast(self.all_types[self.current_parent], self.yaml_obj_types)
            self.yaml_obj_types = dict(zip(self.yaml_obj_types.keys(), new_obj_types))
        self.all_types[self.current_parent] = self.yaml_obj_types
        return True


    def read_generator(self, lines):
        for line in lines:
            if self.process_line(line):
                continue
            if self.is_multiline_obj_parsing_done:
                if self.read_obj():
                    yield Entry(
                        parent=self.current_parent,
                        obj=self.yaml_obj,
                        ytype=self.yaml_obj_types,
                        is_ylist= bool(self.list_counter),
                        is_parent_value= False,
                        is_last=False
                    )
            if self.is_parent_value:
                yield Entry(
                    parent= self.key,
                    obj=self.value,
                    ytype= self.infer_type(self.value),
                    is_parent_value= True,
                    is_ylist=False,
                    is_last=False
                )
            self._reset()
            if self.is_obj_still_parsing:
                self.parsing_obj()
        if self.is_obj_still_parsing:
            if self.read_obj():
                yield Entry(
                    obj=self.yaml_obj,
                    ytype=self.yaml_obj_types,
                    is_ylist= bool(self.list_counter),
                    is_parent_value= False,
                    is_last=False
                )
            yield Entry(is_last=True)
        

def _python_eval(value):
    if value == NaN:
        return None
    return literal_eval(value)


def read_onelist_meta(lines):
    read = Read(is_onelist=True, tgt_parent=None)
    out = {}
    for entry in read.read_generator(lines):
        if entry.is_ylist:
            return out
        if entry.is_parent_value:
            out[entry.parent] = _python_eval(entry.obj)
        else:
            out[entry.parent] = {k: _python_eval(v) for k, v in entry.obj.items()}
    return out
                 
def read_onelist_meta_from_file(path):
    with open(path, 'r') as f:
        return read_onelist_meta(f)

def read_onelist_generator(lines, transform=None):
    read = Read(is_onelist=True, tgt_parent=None)
    def gen():
        for entry in read.read_generator(lines):
            if not entry.is_ylist:
                continue
            tmp = {k: _python_eval(v) for k, v in entry.obj.items()}
            if transform:
                tmp = transform(tmp)
            yield tmp
    return gen

def read_onelist_generator_from_file(path):
    def gen():
        with open(path, 'r') as f:
            readgen =  read_onelist_generator(f)
            for item in readgen():
                yield item
    return gen

def read_onelist_dataframe(lines):
    read = Read(is_onelist=True, tgt_parent=None)
    data = {}
    gen = read_onelist_generator(lines)
    for entrydict in gen():
        if not data:
            data = {k:[v] for k,v in entrydict.items()}
        else:
            try:
                for k, v in entrydict.items():
                    data[k].append(v)
            except KeyError as e:
                raise Exception('Probably violated YAML (-)list must contain fixed features: ' + e.message) from e
    df = pd.DataFrame(data)
    return df

def read_onelist_dataframe_from_file(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        meta =  read_onelist_meta(f)
    with open(path, 'r', encoding=encoding) as f:
        df = read_onelist_dataframe(f)
    if hasattr(df, 'attrs'):
        df.attrs.update(meta)
    return df



if __name__ == "__main__":
    yamlf = """
config1:
  key1: 'value1'
  key2: 'value2'
  key3: 'value3'

config2:
  keyA: 'valueA'
  keyB: 'valueB'
  keyC: 'valueC'

data:
  - name: 'John Doe'
    age: 30
    city: 'New York'
  - name: 'Jane Smith'
    age: 25
    city: 'San Francisco'
  - name: 'Bob Johnson'
    age: 35
    city: 'Chicago'
  - name: 'Test'
    age: 35.0
    city: 'Chicago'
    """

    out = read_onelist_meta(yamlf.splitlines())
    print(out)
    gen = read_onelist_generator(yamlf.splitlines())

    for item in gen():
        print(item)
