预销售功能pos接口：
- 预销售规则列表接口
	1. 使用范围：预销售功能主页
    2. 入参：经营方式、设备号、商场编号、店铺号等
    3. 出参：名称、预售开始日期（yyyy-MM-dd）、预售结束日期
- 预售单保存接口
    1. 预售单下单页面
    2. 入参：会员信息（编号、电话等）、营业员信息、算选预售规则、预售金额、预购商品列表等
    3. 出参：预售单编号等
- 预售单支付接口
    1. 预售单收银页面
    2. 入参：支付方式列表（code、名称等）、支付金额、预售单编号等
    3. 出参：
- 预售单支付通知接口
    1. 预售单收银页面/小票打印页面
    2. 入参：银联支付信息、预售单编号等
    3. 出参：
- 预售单小票接口
    1. 预售单小票
    2. 入参：预售单编号
    3. 出参：单据类型名称、标题名称、商户名称、收营员、营业员、单号、完成日期、应收金额、实收金额、付款方式列表、备注、预购商品列表等
- 预售单取消接口（补充：预售填支付时退出或返回上一页是否需要取消已创建的预售单）
- 预购单详情查询接口
    1. 收银台“预购单提取”
    2. 入参：预售单编号
    3. 出参：当前可使用的预售单详情（编号、名称、时间范围、预售商品列表、所选会员、预付金额、营业员等）
- pos销售支付接口调整（联营、自营两个接口）
    1. 销售收银台
    2. 入参：原有参数基础上添加预售单列表参数
    3. 出参：不变
- pos销售小票接口调整（联营、自营两个接口）
    1. 小票打印
    2. 入参：不变
    3. 出参：添加“提取预售单金额”字段
- 预售单列可退列表接口
    1. 预售单退款列表页面
    2. 入参：经营方式、设备号、商场编号、店铺号等
    3. 出参：返回当前可退预售单列表（展示字段：编号、订单金额、支付方式列表、订单完成时间、单据状态）

- 预售单退款流程备注：
    1. 联营退款：主管密码验证-》获取退款详情-》输入退款金额（预售单不需要）退款单创建-》退款单退款支付-》支付通知-》小票打印
    2. 自营退款：退款单详情选择款商品（预售单不需要）-》创建退款单-》pos后台查询获取退款码-》退款码验证-》获取退款详情，输入退款金额（预售单不需要）-》退款单支付-》支付通知-》小票打印
    3. 补充：取消退款接口

- 退款流程接口调整
    1. 可退订单列表接口（联营和自营两个接口）：新增返回收款方式 “预收核销”
    2. 退款详情接口中（联营、自营）：新增收款方式“预付核销”名称及金额
    3. 小票接口（联营、自营）：添加“提取预售单金额”字段

- 接口列表：
    1. pay-b/self-operation/order/doOrderNew 创建订单（自营）
    2. pay-b/trade/doPay 订单支付（租赁、自营）
    3. pay-b/trade/notify 支付通知（租赁、自营）
    4. pay-b/order/refundList 可退列表（租赁、自营）
    5. pay-b/report/detail/{orderNo} 订单详情（租赁、自营）
    6. pay-b/order/refundDetail/{orderNo} 退单详情（租赁、自营）
    7. pay-b/trade/doRefund 退单提交（租赁、自营）
    8. pay-b/order/cancelOrder/{orderNo} 取消订单（租赁、自营）
    9. pay-b/order/printDetail/{orderNo} 销售小票（租赁、自营）
    10. pay-b/order/printRefundDetail/{orderNo}/{refundOrderNo} 退单小票（租赁、自营）
    11. pay-b/self-operation/order/previewNew 销售订单预览（自营）
    12. pay-b/self-operation/order/refund/preview 退单预览（自营）
    13. pay-b/self-operation/order/refund/create 退单创建（自营）
    14. pay-b/self-operation/order/refund/cancel/{orderNo} 取消退款单（自营）
    15. pay-b/self-operation/order/refund/code/verify/{orderNo}/{refundCode} 退款码验证（自营）
    16. pay-b/self-operation/order/refund/trade 退款支付（自营）
    17. pay-b/self-operation/order/refund/detail/{orderNo} 退款中订单详情（自营）
    18. pay-b/joint-operation/refundOrders 可退订单列表（联营）
    19. pay-b/joint-operation/order/jointRefund/detail/{orderNo} 退款单详情（联营）
    20. pay-b/joint-operation/order/jointRefund/detail/count 退款单商品明细（联营）
    21. pay-b/joint-operation/order/jointRefund/detail/refundCount/{orderNo}/{refundCode} 已发起退款详情（联营）
    22. pay-b/joint-operation/order/jointRefund/code/verify/{orderNo}/{refundOrderNo} 退款码校验（联营，该接口和描述功能有出入，具体查看后台接口代码）
    23. pay-b/joint-operation/order/jointRefund/cancel/{orderNo}/{refundNo} 取消退款（联营）
    24. pay-b/joint-trade/order/jointRefund/trade 退款支付（联营）
    25. pay-b/joint-operation/order/preview 销售预览（联营）
    26. pay-b/joint-operation/order/doOrder 创建销售单（联营）
    27. pay-b/joint-operation/order/jointRefund/create 创建退款单（联营）
    28. pay-b/joint-trade/doPay 销售单支付（联营）
    29. pay-b/joint-trade/notify 支付通知（联营）
    30. pay-b/joint-operation/order/cancelPayOrder 销售单取消（联营）
    31. /joint-trade/joint/notify 退款支付通知（联营）
    32. pay-b/joint-operation/supervisorValidate 主管密码验证（联营）