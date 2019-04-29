# Markup Template Langage (MTL)
MTL provides a simple markup syntax for extracting data from semi-structured text data typically produces by various network vendors. mtl.py produces json data for network automation processing, and is particularly useful in Robotframework. This is not as powerful as other libraries such as textFSM, but grew from my frustration with regex. It is much easier, and templates are easy to share with others. It still needs work but has definate use cases right now.

## mtlRender.py
mtlRender is a pyQt5 based gui tool for testing your templates and cli output. Again, a little rough, but very userful. tfsmRender2.py is a similar tool for textFSM, and show's a beter way to get TextFSM to produce json instead of lists of lists for a data structure. util.py is a wrapper for many useful functions when interacting with network cli's and even some ncclient wrapped functionality for netconf, and a restconf client in its VERY early stages.

## Methods supported
* MID - searching for item with leading and trailing strings
* BOL - search for item with trailing, but no leading string
* EOL - search for item with leading, but no training string
> Key Concept – match the data around what you're looking for... What's in between is what you need.
## Sample output from mtl
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

## Example Usage
```python
from mtl import rendorValidator
data = renderValidator(template,sourceclioutput,"test1")
print(data)
```
## Sample Template
```python
[[fieldbegin='macaddress', method=MID, match=', address is ']]@[[fieldend='macaddress', match='(bia']]
[[fieldbegin='MTU', method=MID, match='MTU ']]@[[fieldend='MTU', match='bytes, BW']]
[[fieldbegin='inputerrors', method=BOL]]@[[fieldend='inputerrors', match=' input errors']]
[[fieldbegin='description', method=EOL, match='Description: ']]@[[fieldend='description', match=' \n']]
[[fieldbegin='internetaddress', method=EOL, match='Internet address is ']]@[[fieldend='internetaddress', match=' \n']]
[[fieldbegin='drops', method=BOL]]@[[fieldend='drops', match='drops for unrecognized']]
[[fieldbegin='totaloutputdrops', method=MID, match='bytes, ']]@[[fieldend='totaloutputdrops', match='total output drops']]
```

### Sample CLI Output
```cisco
RP/0/RSP0/CPU0:asr9k1#sh int TenGigE0/0/2/0
Sat Dec  8 13:37:02.464 MST
TenGigE0/0/2/0 is up, line protocol is up
  Interface state transitions: 1
  Hardware is TenGigE, address is d46d.503a.8920 (bia d46d.503a.8920)
  Layer 1 Transport Mode is LAN
  Description: SW1_Eth1/37
  Internet address is Unknown
  MTU 9202 bytes, BW 10000000 Kbit (Max: 10000000 Kbit)
     reliability 255/255, txload 0/255, rxload 2/255
  Encapsulation ARPA,
  Full-duplex, 10000Mb/s, LR, link type is force-up
  output flow control is on, input flow control is on
  Carrier delay (up) is 10 msec
  loopback not set,
  Last link flapped 12w0d
  Last input 00:00:00, output 00:00:00
  Last clearing of "show interface" counters never
  5 minute input rate 99801000 bits/sec, 9198 packets/sec
  5 minute output rate 8000 bits/sec, 3 packets/sec
     82764786634 packets input, 106449075723598 bytes, 7709064 total input drops
     3648686 drops for unrecognized upper-level protocol
     Received 18964502 broadcast packets, 82722699591 multicast packets
              0 runts, 0 giants, 0 throttles, 0 parity
     5279 input errors, 4836 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
     5792319893 packets output, 7864280346019 bytes, 0 total output drops
     Output 4479975 broadcast packets, 5772754062 multicast packets
     0 output errors, 0 underruns, 0 applique, 0 resets
     0 output buffer failures, 0 output buffers swapped out
     1 carrier transitions
```
