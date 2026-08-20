import importlib, pathlib, time, json
from memory import remember
def spawn(name, skills:list):
    remember("agent_spawn",{"name":name,"skills":skills,"ts":time.time()})
    for s in skills:
        try: importlib.import_module(f"plugins.{s}")
        except Exception as e: remember("agent_error",{"agent":name,"skill":s,"err":str(e)})
    return {"agent":name,"skills":skills}
def replicate(template:str,new_name:str,overrides:dict=None):
    src=pathlib.Path("plugins")/f"{template}.py"; dst=pathlib.Path("plugins")/f"{new_name}.py"
    code=src.read_text(); 
    if overrides:
        for k,v in overrides.items(): code=code.replace(k,v)
    dst.write_text(code); remember("agent_clone",{"from":template,"to":new_name})
    return str(dst)