并发下载

使用threadPool

with futures.ThreadPoolExecutor(worker_num) as executor:
        res = executor.map(download_one, sorted(cc_list))
map出去

期物表示终将发生的事
情，而确定某件事会发生的唯一方式是执行的时间已经排定
结束后的回调
.add_done_callback()
用 as_completed 和 submit()重写
将map 函数改为for 循环 一个用来创建并产出期物，一个用来获取期物的结果


futures 
ThreadPoolExecutor  ProcessPoolExecutor()  processPool能够绕开GIL,
来执行CPU密集型任务。 默认的worker应该是系统cpu的个数，而ThreadPoolExecutor用来执行
iO密集型任务，所有可以多点worker，主要和内存有关


标准库中 使用c语言编写的I/O函数会释放GIL

python 灵活的多进程和多线程: multiprocessing 多进程，threading多线程
使用 yield from 链接的多个协程函数必须由非协程函数调用


# 并发的思路整理

- 多线程: threading
- 多进程: multiprocessing
- future包 concurrent ThreadPoolExecutor负责io密集型  ProcessPoolExecutor负责cpu密集型
- yield 异步处理
- asyncio包 事件循环驱动来处理并发，感觉和电脑的键盘鼠标有点像啊 

cpu 有多少核应该就是多少个并行，但并发量有可能是几千
并发是同时处理多个事情，并行是同时做多个事情


## 下载20个国旗不同版本的时间比较 (在本地架设服务器，请求延迟0.5秒的情况下)

- base_download :  spend time:10.607824087142944
- future_download_map : spend time:0.7470707893371582
- future_download_result+as_completed : spend time:3.759078025817871
- asyncio spend time:0.8281559944152832

