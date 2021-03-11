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
<body>
<h1>添加用户</h1>
<form action="${pageContext.request.contextPath}/addUser.do" method="post">
    用户名：<input type="text" name="username"><br>
    密码：<input type="text" name="pwd"><br>
    <input type="submit" value="提交">
</form>
</body>
</html>