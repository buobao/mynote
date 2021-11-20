- **handler、looper和messageQueue是如何工作的**
`looper是一个无限循环，我们要实现一个具有消息队列的线程，就需要先实现一个消息循环，looper实现了这样的功能。一般的，如果我们想通过线程实现一个功能，比如下载文件，我们会去创建一个线程并且在线程中执行下载的逻辑，当文件下载完成后我们的线程也就停止了。当我们再次需要下载文件的时候就需要重新创建一个线程来下载新的文件。那么有没有一个这样的功能，在我程序运行的过程中这个下载文件的线程是常在的，当有文件下载需求的时候我们只需要将下载文件的地址发送给它来实现文件的下载。要实现这样的功能我们就需要实现一个类似于无线循环的功能，也就是looper的功能。我们可以将需要下载的文件地址保存到一个队列queue中，looper通过循环读取queue中的文件地址来实现各个文件的下载，为了方便操作这个looper的queue,我们可以封装一个handler来操作这个queue。这个功能的实现非常类似于android中主线程消息队列的实现：
`
```
//1.ActivityThread中的main方法
public static void main(String[] args) {
        ...
        //创建一个MainLooper，查看Looper.prepareMainLooper的源码可知
        Looper.prepareMainLooper();

        ...

        //启动这个loop
        Looper.loop();

        throw new RuntimeException("Main thread loop unexpectedly exited");
    }

//2.Looper.loop中循环读取messageQueue中的消息并处理
public static void loop() {
        ...
        for (;;) {
            //读取队列中的msg，这里的next是一个阻塞方法，当没有消息时会阻塞，其中调用了MessageQueue的next方法，核心逻辑在那里面
            Message msg = queue.next(); // might block
            if (msg == null) {
                // No message indicates that the message queue is quitting.
                return;
            }

            ...
            //这里执行消息内容
            try {
                msg.target.dispatchMessage(msg); //是handler中的dispachMessage方法
                if (observer != null) {
                    observer.messageDispatched(token, msg);
                }
                dispatchEnd = needEndTime ? SystemClock.uptimeMillis() : 0;
            } catch (Exception exception) {
                if (observer != null) {
                    observer.dispatchingThrewException(token, msg, exception);
                }
                throw exception;
            } finally {
                ThreadLocalWorkSource.restore(origWorkSource);
                if (traceTag != 0) {
                    Trace.traceEnd(traceTag);
                }
            }
            
            ...

            //这里回收这个msg放入msgpool中，message.obtin创建message时会优先从msgpool中获取，避免频繁创建message
            msg.recycleUnchecked();
        }
    }

//3.通过handler向messagequeue中发送消息
    public Handler(@NonNull Looper looper, @Nullable Callback callback, boolean async) {
        mLooper = looper;
        mQueue = looper.mQueue; //这里的queue就是looper中的消息队列
        mCallback = callback;
        mAsynchronous = async;
    }

    //发送的每一个消息都带有相应的时间，如果需要发送的消息立即执行如sendMessageAtFrontOfQueue所示
    public boolean sendMessageAtTime(@NonNull Message msg, long uptimeMillis) {
        MessageQueue queue = mQueue;
        ...
        return enqueueMessage(queue, msg, uptimeMillis);
    }

    public final boolean sendMessageAtFrontOfQueue(@NonNull Message msg) {
        MessageQueue queue = mQueue;
        ...
        return enqueueMessage(queue, msg, 0);
    }

    private boolean enqueueMessage(@NonNull MessageQueue queue, @NonNull Message msg,
            long uptimeMillis) {
        msg.target = this;
        msg.workSourceUid = ThreadLocalWorkSource.getUid();

        if (mAsynchronous) {
            msg.setAsynchronous(true);
        }
        //插入消息队列
        return queue.enqueueMessage(msg, uptimeMillis);
    }

boolean enqueueMessage(Message msg, long when) {
        ...
            //将消息插入队列中合适的位置,可见messagequeue是一个优先级队列
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                msg.next = p;
                mMessages = msg;
                needWake = mBlocked;
            } else {
                // Inserted within the middle of the queue.  Usually we don't have to wake
                // up the event queue unless there is a barrier at the head of the queue
                // and the message is the earliest asynchronous message in the queue.
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                Message prev;
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }
            ...
        }
        return true;
    }

```
- **为什么handler会导致内存泄漏**
```
这个问题很简单，查看下Message的源码可知：
    public static Message obtain(Handler h, int what) {
        Message m = obtain();
        //这里每个message都会持有发送这个消息的handler实例，如果我们通过匿名对象的方式（通常都会复写handler的方法）来创建handler，
        //那么这个handler就会只有其外部类对象的引用，如果这个外部类对象恰好是一个activity那么这个message就间接持有了这个activity，
        //而消息队列中的message生命周期很可能超出了activity的生命周期，从而导致内存泄漏。
        m.target = h;
        m.what = what;

        return m;
    }
    一个可行的方法是可以通过单例模式创建一个全局的handler，以避免通过匿名内部类的方式实例化handler
```
- **关于ThreadLocal的问题** 
```
ThreadLocal可以看成是通过键值对的方式来存储数据的，我们在通过ThreadLocal.get方法获取值的时候实际上是以当前线程为key值查询数据的
    public void set(T value) {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null)
            map.set(this, value);
        else
            createMap(t, value);
    }

    public T get() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null) {
                @SuppressWarnings("unchecked")
                T result = (T)e.value;
                return result;
            }
        }
        return setInitialValue();
    }

    //所以我们在一个已经有了Looper的线程中都是可以直接创建handler的，这个handler默认会找到这个线程中的Looper
    public Handler() {
        this(null, false);
    }

    public Handler(@Nullable Callback callback, boolean async) {
        if (FIND_POTENTIAL_LEAKS) {
            final Class<? extends Handler> klass = getClass();
            if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
                    (klass.getModifiers() & Modifier.STATIC) == 0) {
                Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                    klass.getCanonicalName());
            }
        }
        //这里就获取了当前线程的Looper
        mLooper = Looper.myLooper();
        if (mLooper == null) {
            throw new RuntimeException(
                "Can't create handler inside thread " + Thread.currentThread()
                        + " that has not called Looper.prepare()");
        }
        mQueue = mLooper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }

    public static @Nullable Looper myLooper() {
        return sThreadLocal.get();
    }

    //在Looper的初始化中这个Looper就被添加到ThreadLocal中了
    private static void prepare(boolean quitAllowed) {
        if (sThreadLocal.get() != null) {
            throw new RuntimeException("Only one Looper may be created per thread");
        }
        sThreadLocal.set(new Looper(quitAllowed));
    }

```
- **一个常见的问题：主线程中的Looper死循环为什么不会导致线程卡死？**
```
首先，主线程中的looper不光会处理我们发送给它的消息，还需要处理其它消息，比如：屏幕的刷新消息，用户交互，广播消息等。我们的
主线程本生就是一个消息循环的工作模式。我们认为的应用或者线程卡死最直观的现象就是anr，什么时候会产生and呢？
当用户交互5秒内没有响应，当广播消息10秒内没有响应。那么什么情况下会导致没有响应呢？无非是主线程的looper在处理某个消息时卡住了，
它处理了太长时间而导致消息队列中和用户交互的消息，广播消息没能及时处理。
除此之外还有可能是整个主线程被阻塞了，比如在主线程中进行了网络请求。
所以，为什么主线程中的looper不会造成卡死呢？
```
