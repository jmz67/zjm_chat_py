# 允许函数和类的注解使用尚未定义或将来将定义的类型，这在 3.7 中是必须的，但在 3.10 中已经默认启动
from __future__ import annotations
# 装饰器，用于将一个方法转换为只读属性，首次调用时计算其值返回结果，后续直接访问缓存
from functools import cached_property

from io import StringIO

import os 

from pathlib import Path

import typing as t 

from memoization import cached, CachingAlgorithmFlag

from pydantic import BaseModel, Field, ConfigDict, computed_field

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, YamlConfigSettingsSource, SettingsConfigDict

import ruamel.yaml
from ruamel.yaml.comments import CommentedBase, TaggedScalar 

def import_yaml() -> ruamel.yaml.YAML:
    def text_block_representer(dumper, data):
        style = None
        if len(data.splitlines()) > 1:
            style = "|"
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)

    yaml = ruamel.yaml.YAML()
    yaml.block_seq_indent = 2
    yaml.map_indent = 2
    yaml.sequence_dash_offset = 2
    yaml.sequence_indent = 4

    # this representer makes all OrderedDict to TaggedScalar
    # yaml.representer.add_representer(str, text_block_representer)
    return yaml

class SubModelComment(t.TypedDict):
    """
    parameter defines how to create template for sub model
    """
    model_obj: BaseModel
    dump_kwds: t.Dict
    is_entire_comment: bool = False
    sub_comment: t.Dict[str, "SubModelComment"]

class YamlTemplate:
    ...


class BaseFileSettings(BaseSettings):

    model_config = SettingsConfigDict(
        use_attribute_docstrings=True,
        extra="ignore",
        yaml_file_encoding="utf-8",
        env_file_encoding="utf-8",
    )

    def model_post_init(self, __context: os.Any) -> None:
        """
        该方法用于初始化类，同时设置私有属性 _auto_reload
        """
        self._auto_reload = True
        # 调用了父类的 model_post_init 方法以确保任何基类中的初始化后处理也能被执行
        return super().model_post_init(__context)

    @property
    def auto_reload(self) -> bool:
        """
        该装饰器定义了一个只读方法，使得可以通过 settings.auto_reload 来获取私有属性 _auto_reload，而不需要显式地调用方法
        """
        return self._auto_reload

    @auto_reload.setter
    def auto_reload(self, val: bool):
        """
        该装饰器定义了一个 setter 方法，允许通过 settings.auto_reload = value 来修改 _auto_reload 的值。这里的 val 是新的布尔值
        """
        self._auto_reload = val


    # 这个类方法，允许我们自定义 BaseSettings 类在实例化的时候从哪些来源加载数据，以及这些来源的优化级
    # 通过重写这些方法，我们可以控制应用程序如何获取配置信息，从而更加灵活地管理设置

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings, YamlConfigSettingsSource(settings_cls)

    def create_template_file(
            self,
            model_obj: BaseFileSettings = None,
            dump_kwds: t.Dict = {},
            sub_comments: t.Dict[str, SubModelComment] = {},
            write_file: bool | str | Path = False,
            file_format: t.Literal["yaml", "json"] = "yaml",
    ) -> str:
        if model_obj is None:
            model_obj = self
        if file_format == "yaml":
            template = YamlTemplate(model_obj=model_obj, dump_kwds=dump_kwds, sub_comments=sub_comments)
            return template.create_yaml_template(write_to=write_file)
        else:
            dump_kwds.setdefault("indent", 4)
            data = model_obj.model_dump_json(**dump_kwds)
            if write_file:
                write_file = self.model_config.get("json_file")
                with open(write_file, "w", encoding="utf-8") as fp:
                    fp.write(data)
            return data





if __name__ == "__main__":
    # def text_block_representer(dumper, data):
    #     style = None
    #     if len(data.splitlines()) > 1:
    #         style = "|"
    #     return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)
    #
    # # 创建一个新的 YAML 对象
    # yaml = ruamel.yaml.YAML()
    # yaml.indent(mapping=2, sequence=4, offset=2) # 设置缩进格式
    #
    # # 添加自定义的序列化器
    # yaml.representer.add_representer(str, text_block_representer)
    #
    # # 测试数据
    # data = {
    #     'single_line': 'This is a single line string.',
    #     'multi_line': '''This is a multi-line string.
    # It spans across multiple lines.
    # Each line will be preserved as it is.'''
    # }
    #
    # # 使用 StringIO 来捕获输出
    # output = StringIO()
    # yaml.dump(data, output)
    # output.seek(0)
    # print(output.getvalue())

    # output = StringIO()
    # output.write('Hello, world!')
    # print("Initial content:", output.getvalue())
    # # 这个时候读取不到任何字符，因为指针已经在末尾了
    # print("Trying to read without seeking:", output.read())
    # output.seek(0)
    # print("Reading without seeking:", output.read())

    ...