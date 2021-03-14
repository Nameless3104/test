<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/9
  Time: 16:32
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>

<script src="//apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<script>
    
    $(function () {
        // var Json = {键1:值1, 键2:值2};
        /*var userJson ={"name":"张三", "age":23, "sex":"男"};
        var name = userJson.name;
        var age = userJson["age"];
        alert(name);
        alert(age);*/

        /*var userJsons = [
            {"name":"张三", "age":23, "sex":"男"},
            {"name":"李四", "age":18, "sex":"男"},
            {"name":"王五", "age":20, "sex":"男"}
            ]
        for (var key in userJsons) {
            alert(userJsons[key].name);
        }*/

        var userJsons = {
            "users":[
                {"name":"张三", "age":23, "sex":"男"},
                {"name":"李四", "age":18, "sex":"男"},
                {"name":"王五", "age":20, "sex":"男"}
            ]
        }
        /*var name1 = userJsons.users[2].name;
        alert(name1);*/

        // JSON转为字符串
        var userJson ={"name":"张三", "age":23, "sex":"男"};
        var userJsonStr =JSON.stringify(userJson);
        alert(userJsonStr);

        // JSON数组转为字符串
        var userJsonsStr = JSON.stringify(userJsons);
        alert(userJsonsStr);

        // 字符串转为JSON
        var userJson2 = JSON.parse(userJsonStr);
        alert(typeof userJson2);

    })
    
</script>

<body>
cccc
</body>
</html>
