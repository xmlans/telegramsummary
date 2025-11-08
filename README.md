# Telegram Channel Summary 电报频道总结
Use Python and user agents to quickly collect statistics and summarize various key information about channels. <br>
使用Telegram 开发人员API拉取各种频道关键信息并制作总结 <br>
## How to start? 如何开始
首先请下载项目源代码，解压并打开目录，请确保你的设备已安装Python，执行<code>pip install telethon</code> 来安装Telethon <br>
然后打开Telegram 开发人员API页面 https://my.telegram.org/apps 获取App api_id和App api_hash 修改tg.py文件，将api id和api hash都换成你自己的 <br>
接下来在channel填写你要统计的频道用户名，配置BATCH_SIZE以设置限速（对于大型频道，消息超过1000+建议配置） <br>
执行<code>python tg.py</code> 然后输入你的账号绑定手机号，请附带国家代码，如美国手机+13333333333 然后你的Telegram会收到一个验证码，将其填入并稍等片刻即可输出总结 <br>
