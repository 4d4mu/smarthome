
import common
import unittest
import lib.plugin
import lib.item
import lib.itembuilder
from lib.model.smartplugin import SmartPlugin
import threading

class TestConfig(unittest.TestCase):
    def props(self,cls):   
        return [i for i in cls.__dict__.keys() if i[:1] != '_']
        
    def test_item_relative(self):
        sh=MockSmartHome()
        
        #load items
        item_conf = None
        item_conf = lib.config.parse(common.BASE + "/tests/resources/item_items.conf", item_conf)
#        print(item_conf.items())
        sh.build_items(item_conf)
        if False: self.dump_items(sh)

        print()
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        self.assertIsNotNone(it)
        self.assertEqual(it._type, 'bool')
        it = sh.return_item("item_tree.grandparent.parent.my_item.child")
        self.assertIsNotNone(it)
        self.assertEqual(it._type, 'foo')

        print('== eval_trigger Tests:')
        # Attribute with relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        self.assertEqual(it.get_absolutepath('.', 'eval_trigger'), 'item_tree.grandparent.parent.my_item')
        self.assertEqual(it.get_absolutepath('.child', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child')
        self.assertEqual(it.get_absolutepath('.child.grandchild', 'eval_trigger'), 'item_tree.grandparent.parent.my_item.child.grandchild')
        self.assertEqual(it.get_absolutepath('..', 'eval_trigger'), 'item_tree.grandparent.parent')
        self.assertEqual(it.get_absolutepath('...', 'eval_trigger'), 'item_tree.grandparent')
        self.assertEqual(it.get_absolutepath('....', 'eval_trigger'), 'item_tree')
        self.assertEqual(it.get_absolutepath('.....', 'eval_trigger'), '')
        self.assertEqual(it.get_absolutepath('......', 'eval_trigger'), '')
        self.assertEqual(it.get_absolutepath('..sister', 'eval_trigger'), 'item_tree.grandparent.parent.sister')

        # Attribute w/o relative references
        print()
        self.assertEqual(it.get_absolutepath('item_tree.grandparent.parent.my_item', 'eval_trigger'), 'item_tree.grandparent.parent.my_item')
        self.assertEqual(it.get_absolutepath('abc', 'eval_trigger'), 'abc')

        print('== eval Tests:')
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        print(it.get_stringwithabsolutepathes('sh..child()', 'sh.', '(', 'eval'))
        self.assertEqual(it.get_stringwithabsolutepathes('sh..child()', 'sh.', '(', 'eval'), 'sh.item_tree.grandparent.parent.my_item.child()')
        self.assertEqual(it.get_stringwithabsolutepathes('5*sh..child()', 'sh.', '(', 'eval'), '5*sh.item_tree.grandparent.parent.my_item.child()')
        self.assertEqual(it.get_stringwithabsolutepathes('5 * sh..child() + 4', 'sh.', '(', 'eval'), '5 * sh.item_tree.grandparent.parent.my_item.child() + 4')
        print()

        print('== Plugin Tests:')
        # Attribute with relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item")
        it.expand_relativepathes('sv_widget', "'", "'")
        self.assertEqual(it.conf['sv_widget'], "{{ basic.switch('id_schreibtischleuchte', 'item_tree.grandparent.parent.my_item.onoff') }}")

        # Attribute w/o relative references
        it = sh.return_item("item_tree.grandparent.parent.my_item.child")
        orig = it.conf['sv_widget']
        it.expand_relativepathes('sv_widget', "'", "'")
        self.assertEqual(it.conf['sv_widget'], orig)
        self.assertEqual(it.conf['sv_widget'], "{{ basic.switch('id_schreibtischleuchte', 'item_tree.grandparent.parent.my_item.child.onoff') }}")
        print()

    def testItemCasts(self):
        pass
    def testItemJsonDump(self):
        import lib.itembuilder
        sh = MockSmartHome()

        # load items
        item_conf = None
        item_conf = lib.config.parse(common.BASE + "/tests/resources/item_dumps.yaml", item_conf)
        sh.build_items(item_conf)

      #  if 1: self.dump_items(sh)
        #print(item_conf)
        #print(sh.return_item("item1").to_json())
        #print(sh.return_item("item3.item3b.item3b1").to_json())
        #print(sh.return_item("item3").to_json())
        import json
        self.assertEqual(json.loads(sh.return_item("item3").to_json())['name'], sh.return_item("item3")._name)
        self.assertEqual(json.loads(sh.return_item("item3").to_json())['id'], sh.return_item("item3")._path)


class MockSmartHome():
    _sh = None
    __children = []
    def __init__(self):
        self._sh = self
    def build_items(self,item_conf):
        ib = lib.itembuilder.ItemBuilder(self)
        ib.build_itemtree(item_conf, self)
        _children, self.__item_dict, self.__items = ib.get_items()
        ib.run_items()
    class MockScheduler():
        def add(self, name, obj, prio=3, cron=None, cycle=None, value=None, offset=None, next=None): 
            print(name) 
            if isinstance(obj.__self__, SmartPlugin):
                name = name +'_'+ obj.__self__.get_instance_name()
            print(name)  
            print( obj) 
            print(obj.__self__.get_instance_name())
    __logs = {}
    __item_dict = {}
    __items = []
    __children = []
    _plugins = []


    scheduler = MockScheduler()
    def add_log(self, name, log):
        self.__logs[name] = log
    def now(self):
        import datetime
        return datetime.datetime.now()
    def add_item(self, path, item):
        if path not in self.__items:
            self.__items.append(path)
        self.__item_dict[path] = item
    def return_item(self, string):
        if string in self.__items:
            return self.__item_dict[string]
    def return_items(self):
        for item in self.__items:
            yield self.__item_dict[item]
    def return_plugins(self):
        for plugin in self._plugins:
            yield plugin
    def now(self):
        import datetime
        return datetime.datetime.now()
    def append_child(self, child,name):
        self.__children.append(child)
        # add top level itemst to SmartHome object.
        vars(self)[name] = child
if __name__ == '__main__':
    unittest.main(verbosity=2)

