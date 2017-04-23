## 需求分析 ##

 1. 查找拉勾网(https://www.lagou.com)上面有关大数据相关的招聘信息
 2. 将招聘信息存储在本地mongodb中
 3. 使用数据分析架构来分析招聘信息中职位描述的一些关键字


## 概要设计 ##

 1. 使用scrapy来抓取拉勾网
 2. 本地架设mongodb
 3. 使用python相关的数据分析module


## 详细设计 ##

 1. 经过对拉勾网数据的分析，职位与职位详情是分两处爬到内容
    - 职位
        https://www.lagou.com/jobs/positionAjax.json?pn=\{\\$PAGE\}&kd=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=%E6%88%90%E9%83%BD&needAddtionalResult=false, 其中\{\\$PAGE\}需要自行替换成整形数据的page页码
    - 职位详情
        https://www.lagou.com/jobs/\{\\$positionId\}.html
 
 2. 由于是要写入mongodb中，所以pipelines.py中需要写入相关的pipeline

 3. 
 

## 问题 ##

 1. mongodb的update，会将整个document中data **replace** 成设定的值
 e.g. db.mycollection.update({"_id": 1234}, {"aaa": "bbb"})，它会将_id为1234的document的其它field删掉，将其全部内容替换成{"aaa": "bbb"}
原因在于：

    > **Update Specific Fields**

    > If the <update> document contains update operator modifiers, such as those using the $set modifier, then:

    > The <update> document must contain only update operator expressions.
The update() method updates only the corresponding fields in the document.
To update an embedded document or an array as a whole, specify the replacement value for the field. To update particular fields in an embedded document or in an array, use dot notation to specify the field.

    > **Replace a Document Entirely**

    > If the <update> document contains only field:value expressions, then:

    > The update() method replaces the matching document with the <update> document. The update() method does not replace the _id value. For an example, see Replace All Fields.
update() cannot update multiple documents.

 2. scrapy的内容，分两个parts，part I的结果会决定part II的结果，如何讲两个parts的内容一并写入到一条mongodb的document中？
    - part I的内容先用一个parse方法yield一条item，再将item中的内容取出来，yield另一个request丢给另一个parse方法中，再负责yield一条item。
    - 两个parts的pipeline用同一个，part I的item过来调用insert方法，part II的item过来调用update方法
    - 使用part I / part II 中不同的一些key来区分二者，以区别对待

 3. 拉勾网API会在不使用cookie的情况下禁用ip，咋办
 request中带上cookies的参数，cookie在browser中自己找
