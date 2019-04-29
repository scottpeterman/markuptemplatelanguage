# Markup Template Langage (MTL)
MTL is a simple markup syntax for extracting data from semi-structured text data typically produces by various network vendors. mtl.py produces json data for network automation processing

## Methods supported
* MID - searching for item with leading and trailing strings
* BOL - search for item with trailing, but no leading string
* EOL - search for item with leading, but no training string
> Key Concept – match the data around what you're looking for... What's in between is what you need.
###Sample output from mtl
```javascript
{
  "test1": {
    "totaloutputdrops": "0",
    "macaddress": "d46d.503b.6913",
    "internetaddress": "Unknown",
    "description": "SW1_Eth1/37",
    "MTU": "9202",
    "drops": "3648686",
    "inputerrors": "5279"
  }
}
```
###Sample Template
```python
[[fieldbegin='macaddress', method=MID, match=', address is ']]@[[fieldend='macaddress', match='(bia']]
[[fieldbegin='MTU', method=MID, match='MTU ']]@[[fieldend='MTU', match='bytes, BW']]
[[fieldbegin='inputerrors', method=BOL]]@[[fieldend='inputerrors', match=' input errors']]
[[fieldbegin='description', method=EOL, match='Description: ']]@[[fieldend='description', match=' \n']]
[[fieldbegin='internetaddress', method=EOL, match='Internet address is ']]@[[fieldend='internetaddress', match=' \n']]
[[fieldbegin='drops', method=BOL]]@[[fieldend='drops', match='drops for unrecognized']]
[[fieldbegin='totaloutputdrops', method=MID, match='bytes, ']]@[[fieldend='totaloutputdrops', match='total output drops']]
```

