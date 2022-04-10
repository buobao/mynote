####什么是协程
>协程可以理解为是轻量级的线程，但是协程却不是线程，我们知道线程的实现有赖于操作系统对进程的实现。我们在创建线程的时候往往会调用操作系统的轻量级进程来实现线程的创建，线程的创建是一个比较消耗系统资源并且需要进入核心态才能创建的实体。一个进程可以包含多个线程，线程可以认为是操作系统的最小资源管理单元。而一个线程又可以包含多个协程。协程和线程的关系类似于线程和进程的关系，然而却又不完全一样。从编译语言角度讲，协程是通过语言特性实现的一种机制，或者称为语法糖，协程不被操作系统内核管理他可以在用户态被创建，并且创建的个数不受系统资源的限制，理论上我们可以创建无数个协程，所以创建协程的开销要远远小于创建线程。协程不以抢占的方式执行。协程可以被挂起，通过挂起的方式我们可以实现协程的切换。
> 协程通过kotlin编译器实现了回调，从代码角度讲，协程只是为开发者实现了回调的代码书写而已，协程本身不具备异步的能力。协程更多的是通过编译器的能力为开发者提供了自动书写回调的功能。对于开发者来说使用协程可以通过书写同步代码的方式来实现异步调用的能力。

``` java
      //协程的实现
    GlobalScope.launch(Dispatchers.Main) {
        val str1 = request1()
        val str2 = request2(str1)
        result.text = "$str1\n$str2"
    }

    private suspend fun request1():String {
        delay(2000)
        return "${System.currentTimeMillis()} request1 success.run on ${Thread.currentThread().name}"
    }

    private suspend fun request2(str:String):String {
        delay(2000)
        return "${System.currentTimeMillis()} request2 success.run on ${Thread.currentThread().name}"
    }


    //java代码实现
    //通过翻译成java代码实现可以看出，编译器为我们实现了回调的代码书写
    val callback = Continuation<String>(Dispatchers.Main){
        Log.e("CoroutineActivity",it.getOrNull()?:"")
    }
    request1(callback)

    public static final Object request1(Continuation preCallback) {
        ContinuationImpl request1Callback;
        if (!(preCallback instanceof ContinuationImpl) || (((ContinuationImpl) preCallback).label & Integer.MIN_VALUE) == 0) {
            request1Callback = new ContinuationImpl(preCallback) {
                @Override
                Object invokeSuspend(@NonNull Object resumeResult) {
                    this.result = resumeResult;
                    this.label |= Integer.MIN_VALUE;
                    Log.e("CoroutubeScene_complete","request1 resume.");
                    return request1(this); //挂起
                }
            };
        } else {
            request1Callback = (ContinuationImpl) preCallback;
        }

        switch (request1Callback.label) {
            case 0: {
  //                Object delay = DelayKt.delay(1000, request1Callback);
                Object delay = request2(request1Callback);
                if (delay == IntrinsicsKt.getCOROUTINE_SUSPENDED()) {
                    Log.e("CoroutubeScene_complete","request1 suspend.");
                    return IntrinsicsKt.getCOROUTINE_SUSPENDED();
                }
            }
        }
        Log.e("CoroutubeScene_complete", "request1 completed");
        return "result from request1 "+request1Callback.result;
    }

    public static final Object request2(Continuation preCallback) {
        ContinuationImpl request2Callback;
        if (!(preCallback instanceof ContinuationImpl) || (((ContinuationImpl) preCallback).label & Integer.MIN_VALUE) == 0) {
            request2Callback = new ContinuationImpl(preCallback) {
                @Override
                Object invokeSuspend(@NonNull Object resumeResult) {
                    this.result = resumeResult;
                    this.label |= Integer.MIN_VALUE;
                    Log.e("CoroutubeScene_complete","request2 resume.");
                    return request2(this); //挂起
                }
            };
        } else {
            request2Callback = (ContinuationImpl) preCallback;
        }

        switch (request2Callback.label) {
            case 0: {
                Object delay = DelayKt.delay(1000, request2Callback);
                if (delay == IntrinsicsKt.getCOROUTINE_SUSPENDED()) {
                    Log.e("CoroutubeScene_complete","request2 suspend.");
                    return IntrinsicsKt.getCOROUTINE_SUSPENDED();
                }
            }
        }
        Log.e("CoroutubeScene_complete", "request2 completed");
        return "result from request2";
    }

    static abstract class ContinuationImpl<T> implements Continuation<T> {
        private Continuation preCallback;
        int label;
        Object result;

        public ContinuationImpl(Continuation preCallback) {
            this.preCallback = preCallback;
        }

        @NonNull
        @Override
        public CoroutineContext getContext() {
            return preCallback.getContext();
        }

        @Override
        public void resumeWith(@NonNull Object resumeResult) {
            Object o = invokeSuspend(resumeResult);  //恢复
            if (o == IntrinsicsKt.getCOROUTINE_SUSPENDED()) {
                return;
            }

            preCallback.resumeWith(o);
        }

        abstract Object invokeSuspend(@NotNull Object resumeResult);
    }
```

#### GlobalScope、lifecycleScope、viewModelScope区别
``` java
//相对来说 GlobalScope不具备生命周期的感知能力，它创建的协程是process级别的，无法关联到宿主的什么周期。其余两个则可以

//        lifecycleScope.launch {  }
//        lifecycleScope.async {  }
        //指当宿主组件至少为onCreate的时候才去执行协程
        lifecycleScope.launchWhenCreated {
            whenCreated {
                //当宿主的生命周期为onCreate时执行 否则暂停
            }

            whenResumed {
                //当宿主的生命周期为onResume时执行，否则暂停
            }

            whenStarted {
                //当宿主的生命周去为onStart时执行，否则暂停
            }
        }

        lifecycleScope.launch {
            CoroutineScene1.getConfigContent()
        }

        //依次类推，还有以下两种:
//        lifecycleScope.launchWhenStarted {  }
//        lifecycleScope.launchWhenResumed {  }

//        viewModeScope 这个是在viewmodel中使用的
```

#### 从线程到协程的转变过程
``` java
//测试
fun getConfigContent() {
        //使用线程直接获取
        parseAssetsFile1("file1"){
            Log.i("parseAssetsFile",it)
        }

        //问题：globalscope创建的协程是precess级别的 当组建被回收以后协程依然会执行
//    GlobalScope.launch {  }
        //问题：lifecycleScope只能在activity和fragment中使用
//    lifecycleScope.launch

        //启用协程避免书写回调
        GlobalScope.launch {
            val fileContent = GlobalScope.async { parseAssetsFile2("file2") }.await()  
            //这里的书写不自然，还是存在lambda表达式的情况（类似回调）
            Log.i("parseAssetsFile",fileContent)
        }

        //这种协程调用更自然
        GlobalScope.launch {
            val fileContent = parseAssetsFile3("file3")
            Log.i("parseAssetsFile",fileContent)
        }

    }

    /**
     * 不使用协程
     */
    fun parseAssetsFile1(fileName:String,callback:(String)->Unit){
        Thread{
            Log.i("parseAssetsFile","loading file $fileName")
            Thread.sleep(2000)
            callback("assets file $fileName load success")
        }.start()
    }

    /**
     * 使用基本协程调用
     */
    suspend fun parseAssetsFile2(fileName:String):String {
        Log.i("parseAssetsFile","loading file $fileName")
        delay(2000)
        return "assets file $fileName load success"
    }

    /**
     * 通过这种方式使挂起函数调用更自然，不需要什么async和await
     */
    suspend fun parseAssetsFile3(fileName:String):String {
        return suspendCancellableCoroutine {
          //仍然是通过线程获取异步的能力
            Thread{
                Log.i("parseAssetsFile","loading file $fileName")
                Thread.sleep(2000)
                it.resumeWith(Result.success("assets file $fileName load success"))
            }.start()
        }
    }
```

#### 协程和线程的区别
- 协程和线程的创建区别
    - 线程的创建
    ```
    /**
    线程的创建很简单，我们创建线程的一般目的是需要线程帮我们执行
    一些比较耗时的任务以避免阻塞当前线程，如下示例所示：
    */
    val thread = Thread{
        Thread.sleep(1000)
        println("sleep end")
    }
    
    thread.start()
    thread.join()
    println("main end")
    ```
    - 协程的创建
    ```
    /*
    通过一个可挂起的lambda表达式就可以创建一个最简单的协程，这个协程中执行了一个延迟一秒输出的功能，类似上面线程执行的功能，在这个例子中我们得到的输出顺序是：
    main end
    sleep end
    resumeWith fun 100
    从这个例子中我们可以发现，协程执行的效果和我们通过线程实现的效果是一致的，当我们创建一个协程并执行的时候，当前线程会继续向下执行，
    协程体中等待一秒钟后会输出相应的内容，Continuation中的resumeWith方法会最后执行。
    和线程实现的唯一区别就是这个协程并没有异步的执行，在执行协程体中的delay方法时它阻塞了当前的线程，它是一个同步执行的过程。
    所以协程的异步能力需要我们自己去实现。
    通过这个简单的例子我们可以看到，协程体的返回值可以直接在resumewith中获取，而不需要通过回调的方式获取，这是协程的关键作用所在。
    */
    suspend {
      delay(1000)
      println("sleep end")
      100
    }.startCoroutine(object :Continuation<Int>{
      override val context: CoroutineContext
        get() = EmptyCoroutineContext

      override fun resumeWith(result: Result<Int>) {
        println("resumeWith fun ${result.getOrNull()}")
      }
    })
    println("main end")
    Thread.sleep(2000)
    ```
    那么，这个没有实现异步执行的协程有什么作用呢？
    ```
    /*
    上面这个例子可以改写成如下形式：
    */
    //创建一个continuation
    val continuation = suspend {
      delay(1000)
      println("sleep end")
      100
    }.createCoroutine(object:Continuation<Int>{
      override val context: CoroutineContext
        get() = EmptyCoroutineContext

      override fun resumeWith(result: Result<Int>) {
        println("resumeWith fun ${result.getOrNull()}")
      }
    })
    //调用continuation的resumeWith方法
    continuation.resumeWith(Result.success(Unit))  //执行协程
    println("main end")
    /*
    1.程序通过createCoroutine方法创建了一个continuation
    2.通过执行continuation的resumeWith来催动协程执行
    3.代码的输出结果是：
    main end
    sleep end
    resumeWith fun 100
    和上面的例子不同，这里是先将continuation创建出来然后通过调用resumeWiht来催动它执行。通过createCoroutine获取的continuation是SafeContinuation的一个实例，
    这个实例接收一个Continuation类型的delegate参数，也就是我们在createCoroutine中传入的匿名Continuation<Int>对象。所以调用continuation.resumeWith其实是
    调用createCoroutine参数中的这个Continuation<Int>的resumeWith。
    所以这段程序的执行逻辑就很明了了，当程序执行到continuation.resumeWith(Result.success(Unit))的时候会催动协程体中代码的执行（suspend中的代码），在执行到delay(1000)的时候又会挂起这个协程，
    进而会执行println(main end),当delay时间满后又会回到协程体继续向下执行，最后执行resumWith中的内容，如果这里将delay(1000)这句去掉，执行的结果为：
    sleep end
    resumeWith fun 100
    main end
    可以发现，协程给了我们一种机制，它可以将一个方法或者一段代码和我们的主流程隔离开来，当我们需要执行这段代码的时候可以通过continuation来
    催动它执行，它在执行的过程中也可以被挂起。虽然它和主流程是交替执行的（不是并发），它拥有自己独立的上下文，并且可以在执行过程中和
    主流程切换执行。
    */
    ```
- 协程中如何实现异步调用
    - 通过线程实现协程的异步执行
    ```
    /*
    上例中是用suspend lambda来创建协程是非常原始的一种方法，这里
    */
    ```


