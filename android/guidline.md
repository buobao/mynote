1. Launcher启动流程与ActivityThread分析
![name](../imgs/launcher-activitythread.png "图片")
![name](../imgs/loading-flow.png "图片")


- ZygoteInit工作内容：
``` java
public static void main(String argv[]) {
    //预加载frameworks/base/preloaded-classes和framework_res.apk资源,这些系统资源加载可以避免在启动app时加载缓慢
    preloadClasses();
    preloadResouces();
    preloadSharedLibraries();

    //启动system_server进程，该进程是framework的核心进程
    if (argv[1].equals("start-system-server")) {
        startSystemServer();
    }

    //创建socket服务
    registerZygoteSocket();

    //进入阻塞状态，等待连接，用以处理来自AMS申请进程创建的请求
    runSelectLoopMode();

    //Zygote进程创建完成
}
```
- SystemServer工作内容：
``` java
public static void main(String argv[]) {
    //创建系统的服务的管理者
    SystemServiceManager mSystemServiceManager = new SystemServiceManager(mSystemContext);
    //启动引导服务
    startBootstrapServices();
    //启动核心服务
    startCoreServices();
    //启动其它一般服务
    startOtherServices();
}
```

2. Launcher的启动流程
![name](../imgs/launcher-start.png "图片")
- 涉及到的不同类的作用：
    - ActivityManagerService: activity生命周期调度的服务类
    - ActivityTaskManagerService: 是将ActivityManagerService中对activity管理的功能转移到该类中处理，专门负责activity相关的工作
    - RootActivityContainer: 调用了packageservice查询系统中已安装的所有应用哪一个是复符合launcher标准并活动一个Intent对象，让后将Intent对象交由ActivityStarter对象处理
    - ActivityStarter: 启动Launcher前的各种检查如权限等，然后启动Launcher。
    - ActivityRecord: 是在server端对antivity的的映射，因为在server端是无法拿到activity的实例的，所以使用activityrecord记录存储了activity的所有信息。
    - TaskRecord: 就是任务栈，记录的一个或多个activityrecord的实例。
    - ActivityStack: 它不是任务栈！它是任务栈的管理者，应用运行时会有一个或多个TaskRecord，这些任务栈就交给activityStack管理。
    - ActivityStackSupervisor: 手机运行中会启动一个或多个应用，当启动多个应用时就会有多个ActivityStack，这时候就需要它来对ActivityStack进行管理。
    - ProcessList: Android10中引入，将原ActivityServiceManager中启动进程的工作交由该类完成
    - ZygoteProcess: 由它来和Zygote进程建立起socket连接把创建进程需要的参数发送过去。

- 任务栈结构：
![name](../imgs/stack-stract.png "图片")

- Launcher启动的流程图:
![name](../imgs/launcher-flow.png "图片")
