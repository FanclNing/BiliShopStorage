# BiliShopStorage

### 说明
程序旨在完成哔哩哔哩会员购库存爬取

已完成功能：

- 二维码扫码登陆
- 指定商品库存查询
- 更多功能设置请参考配置文件

### 配置说明
- 列表yaml文件在后续b站更新时更改后可以继续使用

- cookie填入headers.yaml文件中 

- 在b站任意网页填入下列代码 或者直接执行monitor文件二维码登入

- ```javascript
    document
      .cookie
      .split(/\s*;\s*/)
      .map(it => it.split('='))
      .filter(it => ['DedeUserID','bili_jct', 'SESSDATA', 'buvid3'].indexOf(it[0]) > -1)
      .map(it => it.join('='))
      .join('; ')
      .split()
      .forEach(it => copy(it) || console.log(it))
    ```

- 只需含有 `DedeUserID=...;SESSDATA=...;bili_jct=...;buvid3=...` 即可