r"""
Python library for interacting with scratch currencies.

Better documentation is available in https://pypi.org/project/eclipse-pay

Usage of LRC with password:
>>> from eclipse_pay import LRCOIN
>>> from scratchattach import WsCloudEvents 
>>> 
>>> lrc = LRCOIN(id2="<The id of your project>",username="griffpatch",password="SecurePassword123!")
>>> events = WsCloudEvents(*lrc.h_data)
>>> @events.event
>>> def on_set(event):
>>>     lrc.process(event)

Same can be done with any currency of eclipse_pay:
>>> from eclipse_pay import BLOCKBIT
>>> from scratchattach import WsCloudEvents 
>>> 
>>> bb = BLOCKBIT("<The id of your project>",password="SecurePassword123!")
>>> events = WsCloudEvents(*bb.h_data)
>>> @events.event
>>> def on_set(event):
>>>     bb.process(event)

In a scenario where alice sends bob 10 blockbits:
>>> from eclipse_pay import BLOCKBIT
>>> from scratchattach import WsCloudEvents 
>>> 
>>> bb = BLOCKBIT(id2="<The id of your project>",username="griffpatch",password="SecurePassword123!")
>>> events = WsCloudEvents(*bb.h_data)
>>> @events.event
>>> def on_set(event):
>>>     p = bb.process(event)
>>>     if type(p) == dict:
>>>         print(p)
{"sender":"alice","recipient":"bob","amount":"10"}

When someone requests a purchase using the scratch API, and the transaction is successfully done, it will return "1" in the scratch API, and json here.

`process()` of any currency return json about a transaction if there was one, otherwise returns False.

"""


import requests,random
from scratchattach import Session
from scratchattach import login
from scratchattach import Encoding as ecd
_LRC_ID = "881793781"
_BLOCKBIT_ID = "669020072"

            
class LRCOIN:
    def __init__(self,*,sessionid:str|None=None,username:str|None=None,password:str|None=None,id2:str|None=None):
        self._used = []
        if sessionid == None:
            self._acc = login(username,password)
        else:
            self._acc = Session(sessionid,username=username)
        self.connection = self._acc.connect_cloud(_LRC_ID)
        self._conn = self._acc.connect_cloud(id2)
        self.h_data = [id2,self._conn]
    def _timestamp(self):
        r_id = str(random.randint(1,9999999))
        self.connection.set_var("TO_HOST",r_id)
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={_LRC_ID}&limit=90&offset=0").json()
        self.stmp = 0
        for i in r:
            if i["value"] == r_id:
                self.stmp = i["timestamp"]
                return self.stmp
    def _check_transaction(self,sender,recipient,amount):
        trq = ecd.encode(f"give&{recipient}&{amount}")
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={_LRC_ID}&limit=90&offset=0").json()
        for i in r:
            if i["value"].split(".")[0] == trq and i["user"] == sender and self.stmp<i["timestamp"]:
                return True
        return False
    def process(self,event):
        e_id = event.value.split(".")[1]
        val = ecd.decode(event.value.split(".")[0]).split("&")
        
        if val[0] == "timestamp":
            self._timestamp()
            self._conn.set_var("[ECLIPSE-PAY]",ecd.encode("timestamp set")+f".{e_id}")
            return None
        elif val[0] == "purchase":
            self._conn.set_var("[ECLIPSE-PAY]",str(ecd.encode("1") if self._check_transaction(val[2],val[1],val[3]) else ecd.encode("0"))+f".{e_id}")
            return {"sender":val[2],"recipient":val[1],"amount":val[3]} if self._check_transaction(val[2],val[1],val[3]) else None
class BLOCKBIT:
    def __init__(self,*,sessionid:str|None=None,username:str|None=None,password:str|None=None,id2:None|str=None):
        self._used = []
        if sessionid == None:
            self._acc = login(username,password)
        else:
            self._acc = Session(sessionid,username=username)
        self.connection = self._acc.connect_cloud(_BLOCKBIT_ID)
        self.h_data = [id2,self._conn]
    def _timestamp(self):
        r_id = str(random.randint(1,9999999))+".01"
        self.connection.set_var("Cloud 1",r_id)
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={_BLOCKBIT_ID}&limit=90&offset=0").json()
        self.stmp = 0
        for i in r:
            if i["value"] == r_id:
                self.stmp = i["timestamp"]
                return self.stmp
    def _check_transaction(self,sender,recipient,amount):
        trq = ecd.encode(f"give&{recipient}&{amount}")
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={_BLOCKBIT_ID}&limit=90&offset=0").json()
        for i in r:
            if i["value"] == trq and i["user"] == sender and self.stmp<i["timestamp"]:
                return True
        return False
    def process(self,event):
        e_id = event.value.split(".")[1]
        val = ecd.decode(event.value.split(".")[0]).split("&")
        if val[0] == "timestamp":
            self._timestamp()
            self._conn.set_var("[ECLIPSE-PAY]",ecd.encode("timestamp set")+f".{e_id}")
            return None
        elif val[0] == "purchase":
            self._conn.set_var("[ECLIPSE-PAY]",str(ecd.encode("1") if self._check_transaction(val[2],val[1],val[3]) else ecd.encode("0"))+f".{e_id}")
            return {"sender":val[1],"recipient":val[2],"amount":val[3]} if self._check_transaction(val[2],val[1],val[3]) else None
class BaseCurrency:
    """Class for Implementing your currency
    \nOnly works if the system of the currency is same as LRCOIN."""
    def __init__(self,*,sessionid:str|None=None,username:str|None=None,password:str|None=None,id2:str|None=None):
        self._used = []
        if sessionid == None:
            self._acc = login(username,password)
        else:
            self._acc = Session(sessionid,username=username)
        self.connection = self._acc.connect_cloud(self.PROJECT_ID)
        self._conn = self._acc.connect_cloud(id2)
        self.h_data = [id2,self._conn]
    def _timestamp(self):
        r_id = str(random.randint(1,9999999))
        self.connection.set_var("FROM_HOST_1",r_id)
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.PROJECT_ID}&limit=90&offset=0").json()
        self.stmp = 0
        for i in r:
            if i["value"] == r_id:
                self.stmp = i["timestamp"]
                return self.stmp
    def _check_transaction(self,sender,recipient,amount):
        trq = ecd.encode(f"give&{recipient}&{amount}")
        r: list[dict] = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.PROJECT_ID}&limit=90&offset=0").json()
        for i in r:
            if i["value"].split(".")[0] == trq and i["user"] == sender and self.stmp<i["timestamp"]:
                return True
        return False
    def process(self,event):
        e_id = event.value.split(".")[1]
        val = ecd.decode(event.value.split(".")[0]).split("&")
        if val[0] == "timestamp":
            self._timestamp()
            self._conn.set_var("[ECLIPSE-PAY]",ecd.encode("timestamp set")+f".{e_id}")
            return None
        elif val[0] == "purchase":
            self._conn.set_var("[ECLIPSE-PAY]",str(ecd.encode("1") if self._check_transaction(val[2],val[1],val[3]) else ecd.encode("0"))+f".{e_id}")
            return {"sender":val[1],"recipient":val[2],"amount":val[3]} if self._check_transaction(val[2],val[1],val[3]) else None
    @property
    def PROJECT_ID():
        raise NotImplementedError("Please derive from BaseCurrency.")