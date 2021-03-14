<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 16:09
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<html>
<head>
    <title>Title</title>
</head>

<script src="//apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>

<script>
    /*$(function(){
            alert("test");
        })*/
    /*function checkUserName() {
        const userName = $("#username").val();
        $.ajax({
            type: "POST",
            url: "${pageContext.request.contextPath}/findUserByName.do",
            data: "username="+userName,
            success: function(msg){
                if (parseInt(msg) === 1){
                    const nameErr = $("#nameErr");
                    nameErr.html("该用户名已存在");
                    nameErr.css("color", "red");
                } else {
                    $("#nameErr").html("");
                }
            }
        });
    }*/
    function checkUserName() {
        const userName = $("#username").val();
        $.ajax({
            type: "POST",
            url: "${pageContext.request.contextPath}/findUserByName.do",
            data: {
                "username":userName,
                "id":123
            },
            success: function(msg){
                if (parseInt(msg) === 1){
                    $("#aFlag").val("1");
                    const nameErr = $("#nameErr");
                    nameErr.html("该用户名已存在");
                    nameErr.css("color", "red");
                } else {
                    $("#aFlag").val("0");
                    $("#nameErr").html("");
                }
            }
        });
    }

    function checkAll() {
        var flag = $("#aFlag").val();
        if (flag == "1"){
            alert("输入有误，不能跳转");
            return false;
        } else {
            alert("输入正常");
            return false;
        }
    }
</script>

<body>
<h1>添加用户</h1>
<form action="${pageContext.request.contextPath}/addUser.do" method="post" onsubmit="return checkAll()">
    <input type="hidden" id="aFlag" value="1">
    <label>用户名：
    <input type="text" id="username" name="username" onchange="checkUserName()"> <span id="nameErr"></span>
</label><br>
   <label> 密码：
    <input type="text" name="pwd">
</label><br>
    <input type="submit" value="提交">
</form>
</body>
</html>