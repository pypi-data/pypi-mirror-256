import base64 as _base64
import hashlib as _hashlib
import json as _json
import os as _os
import string as _string
import subprocess as _subprocess
import threading as _threading
import time as _time
from Crypto.Cipher import AES as _AES
from Crypto.Util.Padding import pad as _pad, unpad as _unpad
import psutil as _psutil
import requests as _requests
import platform as _platform
import sys as _sys
import inspect as _inspect

class base:
    def __init__(self, key: str=False, **kwargs):
        """初始化

        Args:
            host (str): CMS服务器地址
            port (int): 端口
            key (str): 密钥
            key_file (str): 密钥文件路径
            try_times (int): 尝试次数
        """
        self._lab_server_host="https://cms.yht.life" if 'host' not in kwargs else kwargs['host']
        self._lab_server_port=False if 'port' not in kwargs else int(kwargs['port'])
        if not self._lab_server_port:
            self._lab_server_port=443 if self._lab_server_host.startswith("https://") else 80
        self._lab_server = f'{self._lab_server_host}:{self._lab_server_port}'
        self.try_times=3 if 'try_times' not in kwargs else int(kwargs['try_times'])
        key=(False if 'key' not in kwargs else kwargs['key']) if not key else key 
        if not key:
            key=self._import_key_from_file(False if 'key_file' not in kwargs else kwargs['key_file'])
        self.key = key
        
        self._check_connection(True)
        self._check_key(True)
        self._map_func()
        
    def _check_connection(self,excp:bool=False):
        """检查连接函数
        """
        times=0
        while True:
            try:
                res = _requests.post(f'{self._lab_server}/',timeout=10).text
                break
            except Exception as e:
                times+=1
                if times==self.try_times:
                    if excp:
                        raise Exception('[Module] Connection Failure.') 
                    return False
                
        if 'TC Laboratory Central Management System' not in res:
            if excp:
                raise Exception('[Module] Server Invalid.')
            return False
        return True

    def _check_key(self,excp:bool=False):
        """检查密钥函数
        """
        if not self._encrypt_data(_json.dumps({}, ensure_ascii=False), self.key):
            if excp:
                raise Exception('[Module] Key Invalid.')
            return False
        return True
        
    def _import_key_from_file(self,path:str=False):
        """导入密钥函数

        Args:
            path (str): 密钥路径

        Returns:
            str: 密钥
        """
        # 如果没有密钥路径
        if not path:
            for part in _psutil.disk_partitions():
                p=f"{part.device}.lab/key"
                if _os.path.exists(p):
                    f=open(p,'r',encoding='utf-8')
                    d=f.read()
                    f.close()
                    return d
            raise Exception('[Module] Key File Not Found.')
        try:
            f=open(path,'r',encoding='utf-8')
            d=f.read()
            f.close()
        except:
            raise Exception('[Module] Cannot Read Key File.')
        return d
    
    def _encrypt_data(self,data: str, key: str):
        """加密函数

        Args:
            data (str): 待加密的数据
            key (str): 加密密钥

        Returns:
            str: base64格式的加密数据
        """
        try:
            key = key.encode()
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.encrypt(_pad(data.encode('utf-8'), _AES.block_size))
            return _base64.b64encode(text).decode()
        except:
            return False


    def _decrypt_data(self,data: str, key: str):
        """解密函数

        Args:
            data (str): 加密的数据
            key (str): 密钥

        Returns:
            str: 解密的数据
        """
        try:
            key = key.encode()
            data = _base64.b64decode(data)
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.decrypt(data)
            text = _unpad(text, _AES.block_size).decode()
            data=_json.loads(text)
            return data['data']
        except:
            return False
    
    def _request(self, data: dict={}):
        """向CMS发送数据

        Args:
            data (dict): 数据

        """
        data = {
            "key_md5": _hashlib.md5(self.key.encode(encoding='utf-8')).hexdigest(),
            "timestamp": _time.time(),
            "data": data
        }
        data = self._encrypt_data(_json.dumps(data, ensure_ascii=False), self.key)

        times=0
        while True:
            try:
                res = _requests.post(self._lab_server,json={'data': data},timeout=10).text
                break
            except Exception as e:
                times+=1
                if times==self.try_times:
                    raise Exception('[Module] Connection Failure.') 

        r = self._decrypt_data(res, self.key)
        res=r if r else _json.loads(res)
        if res and int(res['status_code']) == 1:
            return res['data']
        if res['status_code'] == 0:
            raise Exception(f"[CMS] {res['data']}")

    def _generate_execute(self,name):
        """生成执行函数
        """
        def execute(kw=False,**kwargs):
            data=self._deep_copy(self.func[name])
            if kw:
                kwargs=kw
            for i in kwargs:
                _in=False
                for j in data:
                    if i.upper()==j.upper():
                        data[j]=kwargs[i]
                        _in=True
                if not _in:
                    data[i]=kwargs[i]
                
            for i in data:
                if data[i]==None:
                    raise Exception(f'[CMS] Params Invalid.({i})')
            return self._request({'command': name, 'data': data})

        return execute
        
    def _deep_copy(self,data):
        """深拷贝函数
        """
        if type(data) in [int, float, str, bool, type(None)]:
            return data
        if type(data)==list:
            return [self._deep_copy(i) for i in data]
        if type(data)==dict:
            return {i:self._deep_copy(data[i]) for i in data}
        return data
    
    def _map_func(self):
        self.func={
            "create": {
                "NAME": None,
                "TYPE": None,
                "DESCRIPTION": "",
                "MINIMUM_LEVEL": 4,
                "PARENT_NODE":1,
                "PROPERTIES":{},
                "EXECUTABLE":True,
                "PARAMS":[],
                "CALLBACK_TYPE":"TEXT",
                "CHILDREN":[]
            },
            "delete": { 
                "ID": None,
                "only_child": False
            },
            "execute": {
                "ID":None,
                "params":[]
            },
            "heartbeat": {
                "ID":None
            },
            "query": {
                "ID":None,
                "task_id":None
            },
            "update": {
                "ID":None,
                "task_id":None
            },
            "get_obj_path": {
                "ID":None
            },
            "get_path_obj": {
                "path":None
            },
            "get": {
                "ID":None
            },
            "exist": {  
                "ID":None
            },
            "tree": {
                "ID":None
            },
        }
        for i in self.func:
            exec(f"self.{i}=self._generate_execute(i)")
    
    def _textualize(self,name,data):
        """文本对象化

        Args:
            name (str): 对象名称
            data: 任意对象

        Returns:
            dict: 对象
        """
        if type(data) in [int, float, str, bool, type(None)]:
            return {"name":name,"type":"VALUE","data":data}
        if type(data) in [list, dict]:
            return {"name":name,"type":"OBJECT","data":data}
        
    def _substantialize(self,p):
        """对象实体化

        Args:
            p (dict): 对象

        Returns:
            _type_: 对应对象
        """
        if p["type"] in ["VALUE","OBJECT"]:
            return p["data"]
            

# t.client(key='7320A03683C14A349B24E93C6BE08FB2',host="http://127.0.0.1",port=10000)       
class client:
    def __init__(self,**kwargs):
        # 初始化
        self._base=base(**kwargs)
        # 挂载对象
        self._mount_point_id=kwargs['mount_point'] if 'mount_point' in kwargs else '1'
        self._mount_point_id=self._trans2id(self._mount_point_id)
        self._mount(self,self._mount_point_id)
        # 刷新间隔
        self._refresh_interval=kwargs['refresh_interval'] if 'refresh_interval' in kwargs else 0.5
        # 挂载CMS操作
        self.CMS=self._base
    
    def _trans2id(self,p):
        """转换为id并检测是否合法

        Args:
            p (str): 路径或id
            
        Returns:
            str: id
        """
        if self._base.exist(id=p):
            return p
        return self._base.get_path_obj(path=p)
        
        
    def _mount(self,mount_point,mount_point_id):
        """挂载对象
        """
        for obj in self._base.tree(id=mount_point_id):
            exec(f"mount_point.{obj['NAME'].replace('-','_')}=self._generate_execute(obj)")
            # 挂载属性
            for attr in obj:
                exec(f"mount_point.{obj['NAME'].replace('-','_')}._{attr}=obj[attr]")
            self._mount(eval(f"mount_point.{obj['NAME'].replace('-','_')}"),obj['ID'])
            
    
    def _generate_execute(self,obj):
        """生成执行函数
        """
        def execute(**params):
            return self._execute(obj["ID"],params)
        return execute
    
    def _execute(self,id,params):
        """执行命令
        """
        # 解析参数
        # 回调
        _progress_callback=False
        if '_progress_callback' in params:
            _progress_callback=params['_progress_callback']
            del params['_progress_callback']
        # 对象化
        ps=[]
        for p in params:
            ps.append(self._base._textualize(p,params[p]))
        kwargs={"ID":id,"params":ps}
        # 创建任务
        task=self._base.execute(kwargs)
        # 查询任务
        res=self._base.query(task)
        while res["status"] in ["created","processing"]:
            res=self._base.query(task)
            # 回报进度
            if _progress_callback:
                _progress_callback(res["progress"],res["progress_text"])
            _time.sleep(self._refresh_interval)
        
        # 返回结果
        if res["status"]=="failed":# 如果失败
            raise Exception('[Task] '+ res["progress_text"])
        elif res["status"]=="finished":# 成功返回结果
            data=[]
            for r in res["result"]:
                data.append(self._base._substantialize(r))
            return tuple(data)
        else:
            raise Exception(f'[Task] Unknown Error.(res["status"]="{res["status"]}")')
    
    
class device:
    def __init__(self,device_id=False,**kwargs):
        # 初始化
        if not device_id and 'device_id' not in kwargs:
            raise Exception('[Module] Device ID Required.')
        self.device_id=device_id if device_id else kwargs['device_id']
        self._base=base(**kwargs)
        # 挂载函数
        self._mount_point_id=kwargs['mount_point'] if 'mount_point' in kwargs else device_id
        self._mount_point_id=self._trans2id(self._mount_point_id)
        self._mount_point_path=self._base.get_obj_path(id=self._mount_point_id)
        # 刷新间隔
        self._refresh_interval=kwargs['refresh_interval'] if 'refresh_interval' in kwargs else 0.5
        # 映射表
        self._map={}
        # 处理中的和已完成的任务
        self._tasks=[]
        
    def run(self,silent=False):
        """运行设备
        """
        _print=print
        if silent:
            _print=lambda x:x
        _print("[INFO] Checking...")
        try:
            e,m,t=self.statistics()
            _print(t)
        except Exception as e:
            _print(f"[WARNING] No Permission To Access Tree.")
        _print("[INFO] Started.")
        while True:
            try:
                self._check()
            except Exception as e:
                print(f"[WARNING] Could Not Refresh Tasks.({str(e)})")
            _time.sleep(self._refresh_interval)
    
    def _trans2id(self,p):
        """转换为id并检测是否合法

        Args:
            p (str): 路径或id
            
        Returns:
            str: id
        """
        if self._base.exist(id=p):
            return p
        return self._base.get_path_obj(path=p)
    
    def _trans2path(self,p):
        """转换为完整path

        Args:
            p (str): 路径或id
            
        Returns:
            str: path
        """
        if self._base.exist(id=p):
            return self._base.get_obj_path(id=p)
        p=self._mount_point_path+'.'+p if p else self._mount_point_path
        if not self._base.get_path_obj(path=p):
            raise Exception(f'[Module] Path Invalid.({p})')
        return p
    
    def mount(self,path,mode='direct'):
        """挂载函数到对象路径

        Args:
            path (str): 路径或id
            mode (str): 传参方式(direct/packed)
        """
        path=self._trans2path(path)
        id=self._trans2id(path)
        def outwrapper(func):
            self._map[id]={"func":func,"mode":mode}
            return func
        return outwrapper
    
    def _check(self):
        """检查并执行命令
        """
        res=self._base.heartbeat(id=self.device_id,status=["created","processing"])
        for r in res:
            if r['status']=='created':  
                self._tasks.append(r["task_id"])
                # 标记为进行中
                self._base.update(id=r["ID"],task_id=r['task_id'],status='processing')
                t=_threading.Thread(target=self._execute,args=(r,))
                t.daemon=True
                t.start()
            # 未完成的任务
            if r['status']=='processing' and r["task_id"] not in self._tasks:
                self._base.update(id=r["ID"],task_id=r['task_id'],status='created',progress_text='',progress=0)
            
    def _execute(self,task):
        """执行命令
        """
        # 如果未连接到此对象
        if not task["ID"] in self._map:
            self._tasks.remove(task["task_id"])
            return
        # 执行命令
        try:
            # 解析参数
            params={}
            for p in task["params"]:
                params[p['name']]=self._base._substantialize(p)
            if self._map[task["ID"]]["mode"]=='packed':
                # 注册进度函数
                params["_progress_callback"]=self.generate_progress_callback(task)
                self._finish(self._map[task["ID"]]["func"](params),task)
            elif self._map[task["ID"]]["mode"]=='direct':
                p_str=""
                for i in params:
                    p_str+=f"{i}=params['{i}'],"
                p_str=p_str[:-1]
                p_str=p_str+",_progress_callback=self.generate_progress_callback(task)" if '_progress_callback' in _inspect.getargspec(self._map[task["ID"]]["func"]).args else p_str
                p_str=p_str[1:] if p_str[0]==',' else p_str
                self._finish(eval(f'self._map[task["ID"]]["func"]({p_str})'),task)
            else:
                raise Exception('[Module] Mode Invalid.')
        except Exception as e:
            self._fail(str(e),task)
    
    def generate_progress_callback(self,task):
        """生成进度回调函数

        Args:
            task (dict): 任务
        """
        def progress_callback(progress=False,progress_text=False):
            """上传进度

            Args:
                progress (float): 进度(可选)
                progress_text (bool, optional): 进度信息(可选)
            """
            if progress_text:
                self._base.update(id=task["ID"],task_id=task['task_id'],progress=progress,progress_text=progress_text)
            else:
                self._base.update(id=task["ID"],task_id=task['task_id'],progress=progress)
        return progress_callback
        
    def _finish(self,res,task):
        params=[]
        if type(res) == tuple:
            for i in res:
                params.append(self._base._textualize('',i))
        else:
            params.append(self._base._textualize('',res))
        self._base.update(id=task["ID"],task_id=task['task_id'],status='finished',result=params,progress=100)
        
    def _fail(self,res,task):
        self._base.update(id=task["ID"],task_id=task['task_id'],status='failed',progress_text=res,progress=100)
        
    def statistics(self,id=None):
        """统计挂载情况
        """
        recursion=True
        if not id:
            id=self.device_id
            recursion=False
        executable=0
        mounted=0
        for i in self._base.tree(id=id):
            if i["EXECUTABLE"]:
                executable+=1
            if self._map.get(i["ID"]):
                mounted+=1
            exec,moun=self.statistics(i['ID'])
            executable+=exec
            moun+=moun
        if not recursion:
            mounted=len(self._map)
            if self._map.get(id):
                executable+=1
            t=f"[INFO] Mounted:{mounted} Executable:{executable}"
            if executable:
                t+=f" Percent:{round(mounted/executable*100,2)}%"
            return executable,mounted,t
        return executable,mounted