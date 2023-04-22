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
见`doc/buyer.md`

#### 后端逻辑
`__init__`: 初始化数据库表

`new_order`: 生成一个新的订单，包括其具体的信息（书籍以及数量）.

`payment`: 支付`order_id`订单。

`add_funds`: 增加存款。

`query_orders`: 查询订单。

`cancel_order`: 取消订单。

#### 数据库操作
`__init__`: 初始化数据库表

`new_order`: 在插入前检查该用户是否拥有足够的存款来支付这笔订单所需要的花费，若满足，则在`neworder`表中插入该订单简要信息，即`store_id`, `user_id`等，并在`neworderdetail`表中插入订单具体信息。

`payment`: 若用户足够支付这笔订单的花费，并且满足其他前置条件，则在`order`表中将`paid`属性改为`True`，并将用户的存款`balance`属性减去对应价格。

`add_funds`: 若`user`的`token`满足条件，则将`user`的`balance`属性增加对应数值。

`query_orders`: 在`neworder`表以及`neworderdetail`表中查询对应信息，并将其放入`orders`的`list`中返回。

`cancel_order`: 在`neworder`表以及`neworderdetail`表中查询对应信息，若可以取消该订单，根据`paid`的对应属性来判断是否需要退款，如果需要退款，则在`user`的数据库中将对应`buyer_id`的存款退回，并将`seller_id`的金额减去相应数值，最后将`order`表中对应属性`cancelled`设置为`True`。

#### 测试用例
`test_add_funds.py`: 验证用户存取款是否成功，以及错误账号密码是否返回错误。

`test_cancel_order.py`: 验证用户取消订单是否成功，以及重复取消，过期取消和过期取消后继续支付等问题。

`test_new_order.py`: 验证是否成功发起新订单，以及书籍和商店和用户信息是否存在，以及是否拥有足够的库存量等问题。

`test_payment.py`: 验证订单支付是否成功，以及存款不足、用户认证失败、重复付款、取消后付款等问题。

`test_query_orders.py`: 验证订单是否查询成功，以及用户认证失败等问题。
### 卖家用户

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

### 发货收货 

#### 接口
`be/model/seller.py`：deliver_order函数。
具体可见`doc/seller.md`。

#### 后端逻辑
在收到一个`order_id`的对应`order`的发货请求后，首先是判断该`order`是不是存在，以及检查该`order`的前置条件是否均被满足（即是否已经付款，并且没有被取消等）。若该`order`满足发货要求，则在`orderDetail`中找出该`order`所购买的书籍以及数量，并判断书店中的库存是否满足要求，若满足要求，则进行发货，同时减少商店中对应书籍的库存量。最后将该`order`的`delivered`属性设置为`True`，表示该订单已经发货。

#### 数据库操作
在`neworder`数据库中查询对应`order_id`的所有信息，并在`neworderdetail`数据库中查询对应订单的具体信息，随后在store数据库中对对应`store_id`和`book_id`的对应数据将`stock_level`减去对应数值，最后在`order`数据库中将`delivered`属性设置为`True`。

#### 测试用例
`fe/test/test_deliver_order.py`: 一共进行了四种不同的测试：正常发货、未付款要求发货、重复发货、取消订单后要求发货，测试用例均正常通过。

### 搜索图书

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

### 订单状态、查询取消订单

#### 接口

#### 后端逻辑

#### 数据库操作

#### 测试用例

## 测试结果和覆盖率

## 亮点
1. 完全使用git管理整个仓库