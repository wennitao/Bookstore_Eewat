## 简介
姓名 | 学号 | 分工
--- | --- | ---
倪文韬 |  520030910139 | 60%里user和seller的接口实现，40%里订单状态、查询、取消订单的实现
叶瑶琦 | 520030910144 | 60%里buyer接口的实现，40%里发货到收货的实现
仇天元 |  | 

## 文档数据库设计



## 内部实现介绍

### 用户权限

#### 接口

见`doc/auth.md`.

#### 后端逻辑

`__init__`: 初始化数据库表

`check_token`: 检查`token`的时效性，是否小于`token_lifetime`.

`register`: 注册用户。

`check_password`: 检查密码是否正确。

`login`: 登录。

`logout`: 登出。

`unregister`: 注销。

`change_password`: 修改密码。

#### 数据库操作

`__init__`: 初始化数据库表

`register`: 在`user`表中插入新用户。

`check_password`: 在`user`表中查询`user_id`用户的密码。

`login`: 若密码验证成功， 在`user`表中更新`token`和`terminal`。

`logout`: 若为登录状态，在`user`表中更新`token`和`terminal`。

`unregister`: 在`user`表中删除`user_id`的用户。

`change_password`: 在`user`表中更新`user_id`用户的密码`password`。

#### 测试用例

`test_login.py`: 验证登录登出成功，和错误账号、密码的登出。

`test_password.py`: 验证修改密码后的登录，错误账号、密码。

`test_register.py`: 验证注册注销成功，错误账号密码，注册已注册账号。

### 买家用户

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

### 卖家用户

#### 接口

见`doc/seller.md`

#### 后端逻辑

`__init__`: 初始化数据库表。

`add_book`: 添加图书。

`add_stock_level`: 添加库存。

`create_store`: 创建店铺。

#### 数据库操作

`__init__`: 初始化数据库表。

`add_book`: 在`store`表中插入一条`(store_id, book_id)`的数据。

`add_stock_level`: 在`store`表中对`(store_id, book_id)`的库存`stock_level`增加。

`create_store`: 在`user_store`中插入一条`store_id`, `user_id`。

#### 测试用例

`test_add_book.py`: 验证添加图书成功，不存在的`store_id`，`store`中已存在`book_id`，不存在的`user_id`。

`test_add_stock_level.py`: 验证添加库存成功，不存在的`store_id`，`store`中不存在`book_id`，不存在的`user_id`。

`test_create_store.py`: 验证创建店铺成功，已存在的`store_id`。

### 发货收货 

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

### 搜索图书

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

### 订单状态、查询取消订单

#### 接口

见`doc/buyer.md`

#### 后端逻辑

`query_orders`: 查询`user_id`的所有订单，显示订单号，书店ID，下单时间，总金额，支付、取消状态，以及订单内书籍信息。

`cancel_order`: 取消`order_id`的订单，若已取消则会返回错误，若订单已支付则会退款。

设置了`paytimeLimit`的超时未付款取消订单时间，用lazy update的方式，在查询、取消、或支付订单时判断其是否超时，若超时则取消订单。

#### 数据库操作

`query_orders`: 在`new_order`表中查询`user_id`用户的所有订单的所有信息，并在`new_order_detail`表中，查询每个`order_id`购买书籍的详细信息。

`cancel_order`: 在`new_order`表中查询`order_id`的付款和取消状态。若已支付，则在`user`表中`buyer_id`和`seller_id`表项更新`balance`。若未支付，则在`new_order`表中更新`cancel`为`1`。

付款超时：在`new_order`表中查询该订单的付款时间。若超过`paytimeLimit`，则在`new_order`表中更新`cancel`为`1`。

#### 测试用例

`test_query_orders.py`: 验证查询订单成功，查询不存在的用户。

`test_cancel_order.py`: 验证取消订单成功，已支付的订单验证退款。验证重复取消，超时取消，验证超时后不可支付。

## 测试结果和覆盖率

## 亮点
1. 完全使用git管理整个仓库