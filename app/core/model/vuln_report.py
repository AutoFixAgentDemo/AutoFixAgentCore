from typing import List

from pydantic import BaseModel


class SingleVuln(BaseModel):
    """
    SingleVuln model

    Example:
    {
      "vul_type": "对限制目录的路径名限制不当（路径穿越）",
      "vul_sink_point": "entry.filename = pestrndup(hdr->name, i, myphar->is_persistent);",
      "vul_description": "在 PHP 5.3.0 到 5.4.41 版本中，ext/phar/phar.c 存在目录遍历漏洞，允许远程攻击者通过精心构造的 phar 文件中的 extract() 函数读取任意文件。",
      "vul_level": "高"
    }

    """
    vul_type: str
    vul_sink_point: str
    vul_description: str
    vul_level: str


class VulnReport(BaseModel):
    """
    VulnReport model

    Example:
    {
      "vulnerabilities": [
        {
          "vul_type": "对限制目录的路径名限制不当（路径穿越）",
          "vul_sink_point": "entry.filename = pestrndup(hdr->name, i, myphar->is_persistent);",
          "vul_description": "在 PHP 5.3.0 到 5.4.41 版本中，ext/phar/phar.c 存在目录遍历漏洞，允许远程攻击者通过精心构造的 phar 文件中的 extract() 函数读取任意文件。",
          "vul_level": "高"
        }
      ]
    }

    """
    vulnerabilities: List[SingleVuln]
