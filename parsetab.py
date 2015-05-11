
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '`\xb9Gq0J\xe9\xec"\x8b\xec\xcb\x7fU\xfee'
    
_lr_action_items = {'AND':([36,37,40,54,69,70,71,],[-21,-20,55,-22,-19,-23,-24,]),'COLON':([37,62,],[52,76,]),'LBRACE':([9,14,25,50,],[12,23,43,66,]),'NAME':([0,1,4,5,6,7,8,10,12,14,17,18,23,27,35,39,42,44,49,50,55,56,57,61,76,80,81,82,83,85,86,],[9,-4,-8,9,-7,-5,-9,-6,21,25,30,31,37,37,-12,37,-25,60,-13,25,37,37,72,75,84,-26,-14,-17,-18,-15,-16,]),'LCURLY':([9,14,29,],[17,27,46,]),'NUMBER':([43,],[59,]),'NEWLINE':([22,24,25,26,28,32,53,60,67,68,72,74,75,77,78,79,],[35,42,-27,-29,-28,49,-32,-31,80,81,82,-30,83,-35,85,86,]),'EQUALS':([9,33,34,47,48,],[14,50,51,64,65,]),'RBRACE':([20,21,36,37,38,40,41,54,59,69,70,71,73,],[33,34,-21,-20,53,57,-33,-22,74,-19,-23,-24,-34,]),'RARROW':([9,],[15,]),'BANG':([23,39,55,56,],[39,39,39,39,]),'LARROW':([9,],[16,]),'LT':([9,],[18,]),'GT':([31,],[48,]),'DICT':([14,50,],[29,29,]),'RCURLY':([30,37,45,63,69,84,88,],[47,-20,61,77,-19,-36,-37,]),'PLUS':([25,],[44,]),'STRING':([12,13,14,15,16,19,23,46,50,51,52,58,64,65,66,87,],[20,22,28,-11,-10,32,41,62,28,68,69,41,78,79,41,62,]),'COMMA':([41,84,],[58,87,]),'OR':([36,37,40,54,69,70,71,],[-21,-20,56,-22,-19,-23,-24,]),'$end':([1,2,3,4,5,6,7,8,10,11,35,42,49,80,81,82,83,85,86,],[-4,0,-1,-8,-3,-7,-5,-9,-6,-2,-12,-25,-13,-26,-14,-17,-18,-15,-16,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'paramline':([0,5,],[7,7,]),'filterexpression':([23,27,39,55,56,],[36,45,36,36,36,]),'requestline':([0,5,],[1,1,]),'outputright':([14,50,],[24,67,]),'outputdictitems':([46,87,],[63,88,]),'fetchcode':([0,],[2,]),'headerline':([0,5,],[10,10,]),'fetchlines':([0,5,],[3,11,]),'outputlistitems':([23,58,66,],[38,73,38,]),'fetchline':([0,5,],[5,5,]),'outputdict':([14,50,],[26,26,]),'get':([9,],[13,]),'coarsefilterexpression':([23,39,55,56,],[40,54,70,71,]),'filterline':([0,5,],[4,4,]),'outputline':([0,5,],[8,8,]),'post':([9,],[19,]),'cookieline':([0,5,],[6,6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> fetchcode","S'",1,None,None,None),
  ('fetchcode -> fetchlines','fetchcode',1,'p_fetchsection','D:\\githome\\projects\\fetch\\fetchparser.py',16),
  ('fetchlines -> fetchline fetchlines','fetchlines',2,'p_fetchlines','D:\\githome\\projects\\fetch\\fetchparser.py',20),
  ('fetchlines -> fetchline','fetchlines',1,'p_fetchlines','D:\\githome\\projects\\fetch\\fetchparser.py',21),
  ('fetchline -> requestline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',27),
  ('fetchline -> paramline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',28),
  ('fetchline -> headerline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',29),
  ('fetchline -> cookieline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',30),
  ('fetchline -> filterline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',31),
  ('fetchline -> outputline','fetchline',1,'p_fetchline_modify','D:\\githome\\projects\\fetch\\fetchparser.py',32),
  ('get -> LARROW','get',1,'p_get','D:\\githome\\projects\\fetch\\fetchparser.py',46),
  ('post -> RARROW','post',1,'p_post','D:\\githome\\projects\\fetch\\fetchparser.py',50),
  ('requestline -> NAME get STRING NEWLINE','requestline',4,'p_fetchline_fetch','D:\\githome\\projects\\fetch\\fetchparser.py',54),
  ('requestline -> NAME post STRING NEWLINE','requestline',4,'p_fetchline_fetch','D:\\githome\\projects\\fetch\\fetchparser.py',55),
  ('paramline -> NAME LBRACE NAME RBRACE EQUALS STRING NEWLINE','paramline',7,'p_paramline','D:\\githome\\projects\\fetch\\fetchparser.py',59),
  ('headerline -> NAME LCURLY NAME RCURLY EQUALS STRING NEWLINE','headerline',7,'p_headerline','D:\\githome\\projects\\fetch\\fetchparser.py',63),
  ('cookieline -> NAME LT NAME GT EQUALS STRING NEWLINE','cookieline',7,'p_cookieline','D:\\githome\\projects\\fetch\\fetchparser.py',67),
  ('filterline -> NAME EQUALS LBRACE coarsefilterexpression RBRACE NAME NEWLINE','filterline',7,'p_filterline_coarse','D:\\githome\\projects\\fetch\\fetchparser.py',76),
  ('filterline -> NAME EQUALS LCURLY filterexpression RCURLY NAME NEWLINE','filterline',7,'p_filterline_fine','D:\\githome\\projects\\fetch\\fetchparser.py',80),
  ('filterexpression -> NAME COLON STRING','filterexpression',3,'p_filterexpression','D:\\githome\\projects\\fetch\\fetchparser.py',84),
  ('filterexpression -> NAME','filterexpression',1,'p_filterexpression_noarg','D:\\githome\\projects\\fetch\\fetchparser.py',88),
  ('coarsefilterexpression -> filterexpression','coarsefilterexpression',1,'p_coarsefilterexpression','D:\\githome\\projects\\fetch\\fetchparser.py',92),
  ('coarsefilterexpression -> BANG coarsefilterexpression','coarsefilterexpression',2,'p_coarsefilterexpression_neg','D:\\githome\\projects\\fetch\\fetchparser.py',96),
  ('coarsefilterexpression -> coarsefilterexpression AND coarsefilterexpression','coarsefilterexpression',3,'p_coarsefilterexpression_combined','D:\\githome\\projects\\fetch\\fetchparser.py',100),
  ('coarsefilterexpression -> coarsefilterexpression OR coarsefilterexpression','coarsefilterexpression',3,'p_coarsefilterexpression_combined','D:\\githome\\projects\\fetch\\fetchparser.py',101),
  ('outputline -> NAME EQUALS outputright NEWLINE','outputline',4,'p_outputline','D:\\githome\\projects\\fetch\\fetchparser.py',110),
  ('outputline -> NAME LBRACE STRING RBRACE EQUALS outputright NEWLINE','outputline',7,'p_outputline_dict','D:\\githome\\projects\\fetch\\fetchparser.py',114),
  ('outputright -> NAME','outputright',1,'p_outputright','D:\\githome\\projects\\fetch\\fetchparser.py',118),
  ('outputright -> STRING','outputright',1,'p_outputright','D:\\githome\\projects\\fetch\\fetchparser.py',119),
  ('outputright -> outputdict','outputright',1,'p_outputright','D:\\githome\\projects\\fetch\\fetchparser.py',120),
  ('outputright -> NAME LBRACE NUMBER RBRACE','outputright',4,'p_outputright_arrayitem','D:\\githome\\projects\\fetch\\fetchparser.py',124),
  ('outputright -> NAME PLUS NAME','outputright',3,'p_outputright_expression','D:\\githome\\projects\\fetch\\fetchparser.py',128),
  ('outputright -> LBRACE outputlistitems RBRACE','outputright',3,'p_outputright_list','D:\\githome\\projects\\fetch\\fetchparser.py',132),
  ('outputlistitems -> STRING','outputlistitems',1,'p_outputlistitems_single','D:\\githome\\projects\\fetch\\fetchparser.py',136),
  ('outputlistitems -> STRING COMMA outputlistitems','outputlistitems',3,'p_outputlistitems_multiple','D:\\githome\\projects\\fetch\\fetchparser.py',140),
  ('outputdict -> DICT LCURLY outputdictitems RCURLY','outputdict',4,'p_outputdict','D:\\githome\\projects\\fetch\\fetchparser.py',144),
  ('outputdictitems -> STRING COLON NAME','outputdictitems',3,'p_outputdictitems_single','D:\\githome\\projects\\fetch\\fetchparser.py',148),
  ('outputdictitems -> STRING COLON NAME COMMA outputdictitems','outputdictitems',5,'p_outputdictitems_multiple','D:\\githome\\projects\\fetch\\fetchparser.py',152),
]