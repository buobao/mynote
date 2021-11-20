- **Binder是什么？**
> Binder是Android平台上提供的一种实现IPC的方式，它和Socket、共享内存、管道等这些技术一样，可以实现进程间的通信（跨进程通信）。
- **Binder是如何工作的？**
> Binder的通信模型包括四个部分，请求服务的client process, 提供服务的server process，ServiceManager和Binder驱动。
![name](./imgs/binder-model.png "图片来自：http://weishu.me/2016/01/12/binder-index-for-newer/")
> 首先，server process通过binder驱动向ServiceManger注册服务；client process通过Binder驱动向ServiceManager查询server并获取Binder实例（代理对象）；client process通过Binder驱动向server process发送请求（代理对象的方法调用）；server process通过Binder驱动将请求结果（方法调用的结果）返回给client process，结束。
- **Binder模型的工作原理**
> 在这个工作模型中Binder驱动和ServiceManager是系统提供的基础设施。整个binder机制的工作流程实际上是通过这两个基础设施完成的。我们通过Binder驱动将server注册到ServiceManager，这个ServiceManager中保存了注册过的所有server binder实例（代理对象），client process在通过Binder驱动向ServiceManager查询获取的binder对象其实是一个服务端binder的代理对象。client process在通过这个代理对象进行方法调用的时候并不是真正意义上对远程server process中的binder本地对象发起调用，client process中的调用会通过binder驱动转换成远程调用（这个调用的参数一般包括调用的方法名和方法的参数列表），由binder驱动向server process发起调用，server process在接收到请求时会调用本地的binder对象中的方法执行并将执行结果再通过binder驱动返回给client process。

- **AIDL是什么？**
> Android Interface Definition Language(安卓接口定义语言)，为了更方便的实现跨进程通信，android有了AIDL。而AIDL是通过Binder实现跨进程通信的。
- **AIDL的使用实例**
> server端创建aidl接口
```
package com.cetnaline.liaofang;
import com.cetnaline.liaofang.beans.UserInfo;
interface IMyAidlInterface {
    void basicTypes(int anInt, long aLong, boolean aBoolean, float aFloat,
            double aDouble, String aString);

    String getServiceName();
    //这里引用了一个自定义引用对象，需要创建一个对象引用的aidl文件
    UserInfo getUser(String name);
}

//文件UserInfo.aidl
//这个文件需要放在aidl包中和UserInfo实体类定义所在包路径相同的包路径下，具体参考项目结构图
package com.cetnaline.liaofang.beans;
parcelable UserInfo;

//创建好这两个文件后build项目已生成对应的java文件
```
> server端创建一个CustomService并注册
```
class CustomService : Service() {
    private val myAidlInterface = object:IMyAidlInterface.Stub(){
        override fun basicTypes(
            anInt: Int,
            aLong: Long,
            aBoolean: Boolean,
            aFloat: Float,
            aDouble: Double,
            aString: String?
        ) {

        }

        override fun getServiceName(): String {
            return "this is server"
        }

        override fun getUser(name: String?): UserInfo {
            return UserInfo("Tom",23)
        }
    }

    override fun onBind(intent: Intent?): IBinder? {
        //返回这个binder给client端
        return  myAidlInterface
    }

}
```
> server端的项目结构截图：
![name](./imgs/server-project-str.png "server项目结构图")
> 将上面定义的aidl文件完整的拷贝到client端项目中，包括包路径也需要相同。并且在client项目中相同的包路径下创建相同的UserInfo实体类。项目结构如下:
![name](./imgs/client-project-str.png "server项目结构图")
> 在client项目中创建一个activity并绑定服务端的service
```
class AidlActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityAidlBinding
    private lateinit var aidlInterface:IMyAidlInterface
    private lateinit var aidlServiceIntent:Intent
    private val conn = object:ServiceConnection{
        override fun onServiceConnected(name: ComponentName?, service: IBinder?) {
            aidlInterface = IMyAidlInterface.Stub.asInterface(service)
        }

        override fun onServiceDisconnected(name: ComponentName?){

        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityAidlBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        val navController = findNavController(R.id.nav_host_fragment_content_aidl)
        appBarConfiguration = AppBarConfiguration(navController.graph)
        setupActionBarWithNavController(navController, appBarConfiguration)


        aidlServiceIntent = Intent()
        aidlServiceIntent.action = "android.intent.action.custom_aidl"
        //在知道报名和service的类名时可以直接调用
        aidlServiceIntent.component = ComponentName("com.cetnaline.liaofang","com.cetnaline.liaofang.CustomService")
        //不知道包名和service的类名时可以通过intent action查询获取
//        val resolveInfo = packageManager.queryIntentServices(aidlServiceIntent,0)
//        if(resolveInfo.size!=1) {
//            return
//        }
//        val serviceInfo = resolveInfo[0]
//        val packageName = serviceInfo.serviceInfo.packageName
//        val className = serviceInfo.serviceInfo.name
//        val component = ComponentName(packageName,className)
//        aidlServiceIntent.component = component
        bindService(aidlServiceIntent,conn, Context.BIND_AUTO_CREATE)

        binding.fab.setOnClickListener { view ->
            if (this::aidlInterface.isInitialized) {
                //调用server中的方法
                val user = aidlInterface.getUser("Tom")
                Snackbar.make(view, "user name is "+user.name+" age is "+user.age, Snackbar.LENGTH_LONG)
                    .setAction("Action", null).show()
            }
        }
    }
}
```
-**Messenger是什么？**
> Messenger是基于AIDL实现的进程间通讯的一种简化方式，是一种轻量级的IPC方式。Messenger一次只能处理一个请求，服务端也不存在并发情形（Messenger服务端处理message是单线程处理，AIDL是通过binder线程池处理）。Messenger客户端获取返回值是同步的，而AIDL是异步的。在传递数据方面，AIDl是通过parcelable传输，Messenger通过Bundle传输。

> Messenger实现进程间通讯的一个实例：
```
//服务端
public class MessengerService extends Service {
    private static final String TAG = "MessengerService";
    private MessengerHandler mHandler=new MessengerHandler();
    private Messenger mMessenger=new Messenger(mHandler);
    private static class MessengerHandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            String clientMsg = bundle.getString("client");
            Log.i(TAG,"client:"+clientMsg);
            Message message = Message.obtain();
            Bundle bundle1 = new Bundle();
            bundle1.putString("service","message from server.");
            message.setData(bundle1);
            try {
                //replayto中存放的是client的messenger
                msg.replyTo.send(message);
            } catch (RemoteException e) {
                e.printStackTrace();
            }
        }
    }
    public MessengerService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        return mMessenger.getBinder();
    }
}

//客户端
public class MessengerActivity extends AppCompatActivity{
    private static final String TAG = "MessengerActivity";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_messenger);
    }

    public void onClick(View view) {
        switch (view.getId()){
            case R.id.bindService:
                Intent intent = new Intent(this,MessengerService.class);
                //绑定服务
                bindService(intent,mConnection,BIND_AUTO_CREATE);
                break;
            case R.id.unbindService:
                unbindService(mConnection);
                break;
        }
    }

    private ServiceConnection mConnection=new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            //获取服务端关联的Messenger对象,这一步和AIDL获取Binder对象类似
            Messenger mService=new Messenger(service);
            //创建Message对象
            Message message = Message.obtain();
            Bundle bundle = new Bundle();
            bundle.putString("client","message from client.");
            message.setData(bundle);
            message.replyTo=mRelyMessenger;
            try {
                mService.send(message);
            } catch (RemoteException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
    };

    private GetRelyHandler mGetRelyHandler=new GetRelyHandler();

    private Messenger mRelyMessenger=new Messenger(mGetRelyHandler);
    public static class  GetRelyHandler extends Handler{
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            Bundle bundle = msg.getData();
            String serviceMsg = bundle.getString("service");
            Log.i(TAG, "server："+serviceMsg);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

    }
}

```