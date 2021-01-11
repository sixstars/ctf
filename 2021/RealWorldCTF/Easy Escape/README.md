QEMU逃逸题，在run.sh中看到有个设备叫fun。审计相关函数fun_mmio_read和fun_mmio_write，基本功能非常正常。

但其中put_result功能非常奇怪，result_addr我们可以随意设置，那么脑洞一下，如果就设置成mmio的物理地址呢？试了一下发现会在write的过程中再次触发write，那么我们可以在正常写入数据的过程中触发free，做写入的时候就是就是UAF了

流程如下：
1. 先分配一轮，再释放，填满tcache
2. 再分配一轮，从tcache里拿出来，由于是malloc，可以泄露堆指针，后面的tcache的分配释放我们基本可以预测了
3. 设置result_addr为物理地址+0x18的位置，触发UAF，使得能够分配req块两次，即可任意地址读写
4. 从堆内存搜索指向程序段的指针，计算GOT表位置，泄漏libc，覆盖free_hook即可
