from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[    
        "settings.toml",    
        ".secrets.toml",    
    ],
    merge_enabled=True,    
    lowercase_read=True,   
)

# 使用 dict() 转换来查看配置
print("\nLLM config:", dict(settings.LLM))

# 打印单个配置项
print("\n个别配置项:")
try:
    print("Type:", settings.LLM.type)
except AttributeError:
    print("Type not found")
    
try:
    print("Model:", settings.LLM.model)
except AttributeError:
    print("Model not found")
    
try:
    print("Host:", settings.LLM.host)
except AttributeError:
    print("Host:", settings.LLM.get('host'))

# 打印文件内容
print("\n配置文件内容:")
try:
    with open("settings.toml", "r") as f:
        print("settings.toml:", f.read())
except Exception as e:
    print("Error reading settings.toml:", e)

try:
    with open(".secrets.toml", "r") as f:
        print("\n.secrets.toml:", f.read())
except Exception as e:
    print("Error reading .secrets.toml:", e)