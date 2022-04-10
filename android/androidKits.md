### Android Kits
+ 在API21以下使用Vector Image
> 1. 在Module:app build.gradle的defaultConfig下添加配置:
`vectorDrawables.useSupportLibrary = true`
> 2. imageview使用app:srcCompat引用资源
> 3. 动态设置vector资源
```
VectorDrawableCompat vectorDrawableCompat = VectorDrawableCompat.create(context.getResources(),
            vectorRid, context.getTheme());
    //以下三种方式选一种
    //1.设置单一的颜色
    vectorDrawableCompat.setTint(context.getResources().getColor(colorRid)); 
    //2.设置状态性的，比如点击一个颜色，未点击一个颜色
    //vectorDrawableCompat.setTintList(ColorStateList.valueOf(colorRid));
    //3.用这个v4提供的也可，这个适用于任意的drawable着色
    //DrawableCompat.setTint(vectorDrawableCompat,.getResources().getColor(colorRid)); 
    imageView.setImageDrawable(vectorDrawableCompat);
```

+ 通知栏点击监听
>1. 创建一个NotificationClickReceiver,并注册到manifest
```
public class NotificationClickReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        String tag = intent.getStringExtra("tag");
        .....
    }
}
```
>2. 为通知栏消息setContentIntent一个PendingIntent
```
NotificationManager notificationManager = (NotificationManager) this.getSystemService(Context.NOTIFICATION_SERVICE);
        Notification.Builder builder = new Notification.Builder(MainActivity.this);
        builder.setSmallIcon(R.drawable.ic_launcher);
        builder.setTicker("title");
        builder.setContentTitle("notice");
        builder.setContentText("detail");
        builder.setWhen(System.currentTimeMillis());
        builder.setDefaults(Notification.DEFAULT_ALL);
        builder.setAutoCancel(true);
        Intent intent =new Intent (MainActivity.this,NotificationClickReceiver.class);
        //通过pending跳转到广播接收器，在广播接收器中添加逻辑
        //注意第二和第四个参数，不能设置成0，否则广播接收器接收到的intent会有缓存！
        PendingIntent pendingIntent =PendingIntent.getBroadcast(MainActivity.this, 1, intent, PendingIntent.FLAG_UPDATE_CURRENT);
        builder.setContentIntent(pendingIntent);
        Notification notification1 = builder.build();
        notificationManager.notify(124, notification1);
```

+ 取消listview点击水波纹
```
android:divider="@null"
android:listSelector="#00000000"
```

+ 显示listview分割线
```
android:divider="@drawable/news_item_div"
android:dividerHeight="10dp"
```

+ EditText和ScrollView滚动冲突（垂直滚动）
```
<EditText
        android:id="@+id/content"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:scrollbarStyle="insideInset"
        android:scrollbars="vertical"
        android:overScrollMode="always"/>

content.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View view, MotionEvent event) {
                view.getParent().requestDisallowInterceptTouchEvent(true);
                if (MotionEvent.ACTION_UP == event.getAction()) {
                    view.getParent().requestDisallowInterceptTouchEvent(false);
                }
                return false;
            }
        });
```

+ 设置elevation不显示阴影时考虑是不是没有设置背景色或者没有预留margin

+ ClickableSpan点击无效时，设置textview.setMovementMethod(LinkMovementMethod.getInstance())

+ 自定义gradle task 生成java文件
```java
task generateSources {
    File outputDir = file("$buildDir/../src/main/java/com/redstar/pospay")
    outputs.dir outputDir
    doFirst {
        outputDir.exists() || outputDir.mkdirs()
        String STG_URL = "public static final String STG_URL = \"" + rootProject.ext.stgUrl + "\";\n"
        String UAT_URL = "public static final String UAT_URL = \"" + rootProject.ext.uatUrl + "\";\n"
        String DEV_URL = "public static final String DEV_URL = \"" + rootProject.ext.devUrl + "\";\n"
        String RELEASE_URL = "public static final String RELEASE_URL = \"" + rootProject.ext.releaseUrl + "\";\n"

        String STG_APPID = "public static final String STG_APPID = \"" + rootProject.ext.debugAppId + "\";\n"
        String UAT_APPID = "public static final String UAT_APPID = \"" + rootProject.ext.debugAppId + "\";\n"
        String DEV_APPID = "public static final String DEV_APPID = \"" + rootProject.ext.debugAppId + "\";\n"
        String RELEASE_APPID = "public static final String RELEASE_APPID = \"" + rootProject.ext.releaseAppId + "\";\n"
        new File(outputDir, "EnvConstant.java").write("package com.redstar.pospay;\n\n" +
                "public class EnvConstant {\n"
                + " " + STG_URL + " " + UAT_URL + " " + DEV_URL +" " + RELEASE_URL +
                " " + STG_APPID +" " + UAT_APPID +" " + DEV_APPID +" " + RELEASE_APPID +"}")
    }
}
preBuild.dependsOn generateSources
```

+ adb拉起app
```shell
adb shell am start -n "com.redstar.pospay.sce/com.redstar.pospay.ui.login.LoginActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER
```

+ 命令行启动模拟器：
``` bat
D:\androidsdk\emulator>emulator -list-avds
Pixel_XL_API_28

D:\androidsdk\emulator>emulator -avd Pixel_XL_API_28
```