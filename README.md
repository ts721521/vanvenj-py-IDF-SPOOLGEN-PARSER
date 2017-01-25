#什么是 IDF
IDF 是很多3D工具在模型转换成ISO图时生成的数据文件。
AVEVA 称它为 **Intermediate Data File**。
INTERGRAPH 称它为 **IsoGen Data File**。
这个文件中包含了很多管道元件的信息。
Intergraph 的 Spoolgen 软件可以利用IDF进行加工设计。

#什么是 pyIDF
客户通常会提供很多idf文件供我们加工设计，同时也会提供一份材料汇总清单供我们采购。
为了能够提前对客户的idf和材料清单进行对比，我们利用Python编写了一个IDF解析器，取名pyIdf，用于快速提取IDF中的数据。



[这里](http://www.bentleyuser.dk/sites/default/files/files/isogen_info.pdf) 是对IDF一些字段的定义。
